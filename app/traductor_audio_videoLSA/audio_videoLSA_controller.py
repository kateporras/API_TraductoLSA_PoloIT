from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.traductor_audio_videoLSA.audio_videoLSA_service import procesar_audio_a_videoLSA, procesar_texto_a_videoLSA

router = APIRouter()

@router.post("/traducirAudio")
async def traducir_audio_a_videoLSA(file: UploadFile = File(...)):
    print(file.filename)
    if not file.filename.endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Formato de archivo no soportado. Use .mp3 ")
    
    return await procesar_audio_a_videoLSA(file)

class textInput(BaseModel):
    texto: str

@router.post("/traducirTexto")
async def traducir_texto_a_videoLSA(texto: textInput):

    texto = texto.texto.strip()

    return await procesar_texto_a_videoLSA(texto)       

