import os
import requests
from dotenv import load_dotenv

load_dotenv()


def armar_peticion(pregunta):
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía")
    api_key = os.getenv("GEMINI_API_KEY")
    modelo = "gemini-3.6-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
    body = {"contents": [{"parts": [{"text": pregunta}]}]}
    return url, body


def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se pudo conectar con el servicio. Intenta de nuevo en unos segundos.")
    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no llegó en el formato esperado.")


def extraer_texto(datos):
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError("La respuesta no trae el texto generado en el lugar esperado.")


def obtener_dato_de_prueba(pregunta):
    url, body = armar_peticion(pregunta)
    datos = enviar_peticion(url, body)
    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"Costo estimado de la operación: ${costo:.6f} USD")
    return extraer_texto(datos)

def calcular_costo(datos, precio_entrada, precio_salida):
    uso = datos["usageMetadata"]

    tokens_entrada = uso["promptTokenCount"]
    tokens_salida = uso["candidatesTokenCount"]
    tokens_razonamiento = uso.get("thoughtsTokenCount", 0)

    costo = (
        tokens_entrada * precio_entrada
        + (tokens_salida + tokens_razonamiento) * precio_salida
    )

    return costo


try:
    print(obtener_dato_de_prueba("Cuenta un chiste chileno"))
except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operación:", error)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

"""
=========================================================================================
| Código HTTP | Excepción / caso         | Qué significa                | Dónde se maneja       |
|-------------|--------------------------|------------------------------|-----------------------|
| (ninguno)   | ValueError               | Pregunta vacía o muy larga.  | armar_peticion        |
|             |                          | Se detecta ANTES de llamar   |                       |
|             |                          | a Google (validación).       |                       |
| (ninguno)   | requests Timeout         | Google tardó demasiado en    | enviar_peticion       |
|             |                          | responder.                   |                       |
| (ninguno)   | requests ConnectionError | No hay internet o la URL     | enviar_peticion       |
|             |                          | está mal escrita. Nunca se   |                       |
|             |                          | llegó al servidor.           |                       |
| 429         | Too Many Requests        | Se superó el límite de       | enviar_peticion       |
|             |                          | peticiones del plan gratis.  |                       |
| 503         | Service Unavailable      | El modelo está saturado.     | enviar_peticion       |
|             |                          | Es problema de Google, no    |                       |
|             |                          | nuestro: hay que reintentar. |                       |
| 405 y otros | JSONDecodeError          | Llegó una respuesta que no   | enviar_peticion       |
|             |                          | es JSON (por ejemplo HTML).  |                       |
| 400 / 403 / | KeyError / IndexError    | Google respondió, pero con   | extraer_texto         |
| 404         |                          | un JSON de error y sin       |                       |
|             |                          | "candidates": llave inválida |                       |
|             |                          | (400), API no habilitada     |                       |
|             |                          | (403) o modelo inexistente   |                       |
|             |                          | (404).                       |                       |
| 200         | (éxito)                  | Todo funcionó: llega el      | -                     |
|             |                          | texto generado.              |                       |
=========================================================================================

REGLA RÁPIDA
- Sin código HTTP -> el problema ocurrió antes de llegar a Google (internet, URL, validación).
- 4xx             -> el problema está en lo que ENVIAMOS (llave, modelo, cuerpo, límite).
- 5xx             -> el problema está del lado de GOOGLE: nuestro código está bien, reintentar.
- 200             -> Google respondió bien.
"""