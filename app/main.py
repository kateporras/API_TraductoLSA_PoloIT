from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.traductor_audio_videoLSA import audio_videoLSA_controller



app= FastAPI()

# permisos para el front React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],#"http://localhost:<num>" va el dominio del front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(audio_videoLSA_controller.router, 
                   tags=["Traductor Audio A Video LSA"])

