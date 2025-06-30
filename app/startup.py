import os
import subprocess

MODELO_PATH = "modelo/modelo_lenguaje_senias.h5"

# Verificar si ya existe el modelo entrenado
if not os.path.exists(MODELO_PATH):
    print("Modelo no encontrado. Iniciando entrenamiento...")
    subprocess.run(["python", "app/traductor_videoLSA_textoOAudio/train_model.py"], check=True)
else:
    print("Modelo ya entrenado. Saltando entrenamiento.")

# Iniciar FastAPI con Uvicorn
subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"])
