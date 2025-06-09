# API_TraductoLSA_PoloIT
# Traductor de Lengua de Señas en Video

Es una API que recibe un mensaje de texto o un archivo de audio(.mp3), procesa el contenido, y devuelve un video `.mp4` que muestra el mensaje traducido a **lenguaje de señas**. Ideal para aplicaciones de accesibilidad, integración con sitios web y herramientas de comunicación inclusiva.
---

## Funcionalidades

- 📥 Recibe un texto o un audio( .mp3 )
- 🎥 Generación de video `.mp4` con el traductor en señas
- 📤 Devuelve el video generado como respuesta
---
## Tecnologías utilizadas

- **FastAPI** (backend de la API)
- **Python** (procesamiento de audio y texto)
- **Docker** (para contenerización)
- **FFmpeg / MoviePy** (para generar el video)
- **Postman** (para pruebas de la API)
---

## Ejecucion con Docker

### Construir la imagen de Docker

```bash
docker build -t traductor .
```

### Ejecutar el contenedor
 
```bash
docker run --name traductor-back -p 8000:8000 traductor
```
---
## Pruebas con Postman

### Endpoint 1: Traduccion de Texto a Video

**POST** `http://localhost:8000/traducirTexto`
#### Request (body `raw-JSON`)
```bash
{
	"texto":"Hola como estas"
}
```
#### Response:

- ***Codigo:** `200 OK`
- **Body:** archivo `.mp4` (video con la traduccion en LSA)



### Endpoint 2: Traduccion de Audio a Video

**POST** `http://localhost:8000/traducirAudio`
#### Request (body `form-data`)

| Key   |Type    | Value                            | 
|-------|--------|----------------------------------|
| file  |**File**| (subir archivo `.mp3`)           |
#### Response:

- ***Codigo:** `200 OK`
- **Body:** archivo `.mp4` (video con la traduccion en LSA)
---



