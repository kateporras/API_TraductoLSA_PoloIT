import tempfile
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from app.traductor_videoLSA_textoOAudio.traductor_videoLSA_textoOAudio_service import predecir_palabra_desde_video


router = APIRouter()

@router.post("/traducir_video_lsa_texto")
async def traducir_video_lsa_texto(file: UploadFile = File(...)):
    """
    Endpoint para traducir un video de lenguaje de señas a texto.
    
    Args:
        file (UploadFile): Archivo de video en formato mp4.
        
    Returns:
        dict: Diccionario con la palabra traducida.
    """
    try:
        #Guardar temporalmente el archivo
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        palabra = predecir_palabra_desde_video(temp_file_path)

        return {"palabra": palabra}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )  
    