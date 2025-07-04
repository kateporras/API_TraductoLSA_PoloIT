from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.traductor_audioOtexto_videoLSA import traductor_audioOtexto_videoLSA_controller
#from app.traductor_videoLSA_textoOAudio import traductor_videoLSA_textoOAudio_controller



app= FastAPI()

# permisos para el front React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://3.149.133.67:8080"],#"http://localhost:<num>" va el dominio del front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(traductor_audioOtexto_videoLSA_controller.router, 
                   tags=["Traductor Audio A Video LSA"])
#app.include_router(traductor_videoLSA_textoOAudio_controller.router, 
#                  tags=["Traductor Video LSA A Texto"])