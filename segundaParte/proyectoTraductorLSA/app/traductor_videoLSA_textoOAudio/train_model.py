#------Rutas------
import json
import os
import pickle
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Masking, EarlyStopping
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder 
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorlow.keras.callbacks import EarlyStopping

from app.traductor_videoLSA_textoOAudio.traductor_videoLSA_textoOAudio_util import extraer_frames_modelo, extraer_keypoints_de_frames


dataset_videos="data/videos"
dataset_npy="data/npy"
modelo_output="modelo/modelo_lenguaje_senias.h5"
encoder_output="modelo/encoder_lenguaje_senias.pkl"
max_frames_output="modelo/max_frames.json"

os.makedirs(dataset_npy, exist_ok=True)

#----------ProcesamosVideos----------

videos_dict, max_frames = extraer_frames_modelo(dataset_videos) 

x=[]
y=[]

for palabra, frames in videos_dict.items():
    keypoints = extraer_keypoints_de_frames(frames, max_frames)
    np.save(os.path.join(dataset_npy, f"{palabra}.npy"), keypoints[0])
    x.append(keypoints[0])
    y.append(palabra)

x = np.array(x)

#codificamos las etiquetas
le= LabelEncoder()
y_encoded = le.fit_transform(y)
#convertimos a formato one-hot
y_one_hot = to_categorical(y_encoded)

#--------------Keras Model----------------
model=Sequential()
model.add(Masking(mask_value=0.0, input_shape=(x.shape[1],x.shape[2])))
model.add(LSTM(128, return_sequences=False))
model.add(Dense(64, activation='relu'))
model.add(Dense(y_one_hot.shape[1], activation='softmax'))

#Compilamos el modelo con:
#-'adam' como optimizador
#-loss para clasificacion multi-clase
#-'accuracy' para ver que tan bien predice
model.compile(optimizer="adam",
              loss="categorical_crossentropy",
              metrics=["accuracy"])

#Sila validacion no mejora en 5 epochs detiene el entrenamiento
early_stop=EarlyStopping(monitor="val_loss",patience=5,restore_best_weights=True)

#Entrenamos el modelo
print("Iniciando entrenamiento del modelo...")
history = model.fit(x, y_one_hot,
                    epochs=50, 
                    batch_size=1, 
                    callbacks=[early_stop])

#-------------Guardamos el modelo y el encoder-------
model.save(modelo_output)
with open(encoder_output, 'wb') as f:
    pickle.dump(le, f)
    
with open(max_frames_output, 'w') as f:
    json.dump({"max_frames": max_frames}, f)

print("Modelo y encoder guardados correctamente.")
print("Entrenamiento completado.")