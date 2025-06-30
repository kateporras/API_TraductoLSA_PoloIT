
import tensorflow as tf
import numpy as np
import pickle
from app.traductor_videoLSA_textoOAudio.traductor_videoLSA_textoOAudio_util import cargar_max_frames, extraer_frames, extraer_keypoints_de_frames


#rutas del modelo y encoder
MODEL_PATH = "modelo/modelo_lenguaje_senias.h5"
ENCODER_PATH = "modelo/encoder_palabras.pkl"

MAX_FRAMES = cargar_max_frames()

#cargamos el modelo y el encoder una sola vez al iniciar

model=tf.keras.models.load_model(MODEL_PATH)

with open(ENCODER_PATH, "rb") as f:
    encoder = pickle.load(f)

def predecir_palabra_desde_video(video_path:str) -> str:
    """
    Predice la palabra en lenguaje de señas a partir de un video.
    
    Args:
        video_path (str): Ruta al video que contiene la secuencia de señas.
        
    Returns:
        str: Palabra predicha en lenguaje de señas.
    """
    # Extraer frames del video
    frames = extraer_frames(video_path)
    
    # Extraer keypoints de los frames
    keypoints = extraer_keypoints_de_frames(frames, MAX_FRAMES)
    
    # Realizar la predicción
    prediccion = model.predict(keypoints)
    
    # Obtener la palabra con mayor probabilidad
    palabra_predicha = encoder.inverse_transform([np.argmax(prediccion)])
    
    return palabra_predicha[0]