import pandas as pd
import spacy
import whisper  

#Cargamos el modelo Whisper para el audio
#modeloWhisper = whisper.load_model("base")
#Cargamos el modelo de spacy
modeloSpacy=spacy.load("es_core_news_sm")
# si quieron verlo iterativo colocar #%%
#Cargamos el dataset de videos
dataf_Videos=pd.read_csv("./data/LSA_V1.csv")

#pasamos de audio a texto
def convertir_audioAtexto(ruta_audio:str):
    modeloWhisper = whisper.load_model("base")
    result = modeloWhisper.transcribe(ruta_audio)
    return result["text"]       

#pasamos el texto a glosas
def procesar_texto_glosas(texto:str):
    doc = modeloSpacy(texto)
    resultGlosas=[]

    for token in doc:
        if not token.is_space and not token.is_punct:
            resultGlosas.append(token.lemma_.upper())

    return resultGlosas     

#con las glosas creamos las rutas de video que corresponde
def procesar_texto_videoLSA(glosas):
    rutasVideo=[]
    glosasRegex="|".join(glosas)
    dataf_VideosFiltrados=dataf_Videos[dataf_Videos["descripcion"].str.contains(glosasRegex, case=False, na=False)]

    for itemVideo in dataf_VideosFiltrados['videoURL']:
        rutasVideo.append(itemVideo)

    return rutasVideo   