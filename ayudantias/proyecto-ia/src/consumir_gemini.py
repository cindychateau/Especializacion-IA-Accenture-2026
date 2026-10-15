import os
import requests
from dotenv import load_dotenv
  
load_dotenv()
  
def obtener_dato_de_prueba(pregunta):
    api_key = os.getenv("GEMINI_API_KEY")
    modelo = "gemini-flash-latest"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
    
    body = {
     	"contents": [
         	{"parts": [{"text": pregunta}]}
     	]
     }
    
    respuesta = requests.post(url, json=body)
    print(respuesta)
    datos = respuesta.json()
    return datos["candidates"][0]["content"]["parts"][0]["text"]

print(obtener_dato_de_prueba("Cuéntame un chiste"))