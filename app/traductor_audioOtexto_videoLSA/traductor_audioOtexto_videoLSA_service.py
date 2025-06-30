import os
import uuid

from fastapi.responses import FileResponse
from moviepy.editor import VideoFileClip, concatenate_videoclips # type: ignore
from app.traductor_audioOtexto_videoLSA.traductor_audioOtexto_videoLSA_util import convertir_audioAtexto, procesar_texto_glosas, procesar_texto_videoLSA
from fastapi import HTTPException
import shutil



async def procesar_texto_a_videoLSA(texto):
    if not texto:
        raise HTTPException(status_code=400, detail="Texto Vacio")  
    # Procesamos el texto a glosas
    glosas = procesar_texto_glosas(texto)
    rutas_videos_glosas = procesar_texto_videoLSA(glosas)

    # Validamos si no se encontro glosas
    if not rutas_videos_glosas:
        raise HTTPException(status_code=404, detail="No se encontraron la traduccion")
    
    # Armamos los clips para unirlos
    clips = []  
    for path in rutas_videos_glosas:
        print(f"Procesando video: {path}")
        if os.path.exists(path):
            clips.append(VideoFileClip(path))
        else:
            raise HTTPException(status_code=404, detail=f"Video no encontrado: {path}")
    if not clips:   
        raise HTTPException(status_code=500, detail="No se encontraron videos para unir")
    # Unimos los clips
    video_final = concatenate_videoclips(clips, method="compose")
    
    # Creamos un nombre unico para el video final
    video_final_path = os.path.join("output", f"{uuid.uuid4()}.mp4")
    video_final.write_videofile(video_final_path, codec="libx264", audio_codec="aac")   
    
    # liberar memoria de los clips  
    for clip in clips:
        clip.close()
    video_final.close()
    
    # Eliminar el video final si existe
    #if os.path.exists(video_final_path):
    #    os.remove(video_final_path)
    
    # Devolver el video al front
    if not os.path.exists(video_final_path):
        raise HTTPException(status_code=500, detail="Error al generar el video final")  
    return FileResponse(video_final_path, media_type="video/mp4", filename=os.path.basename(video_final_path))
        
        
        



async def procesar_audio_a_videoLSA(file):
    #creamos una carpeta donde guardaremos los archivos mp3
    os.makedirs("temp", exist_ok=True)
    # creamos un nombre unico para el archivo mp3
    audio_path = os.path.join("temp", f"{uuid.uuid4()}.mp3")
    # abre el archivo en modo escritura binaria
    with open(audio_path, "wb") as audio_file:
        # copia el objeto binario que subio el usuario file.file(viene desde  FastAPI)
        # el contenido se copia al archivo audio_file
        shutil.copyfileobj(file.file, audio_file)

    try:
        # Convertimos audio a texto
        texto = convertir_audioAtexto(audio_path).strip()  # elimina espacios al final y al inicio del texto

        return await procesar_texto_a_videoLSA(texto)
    finally:
        # Eliminar el archivo de audio temporal
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        