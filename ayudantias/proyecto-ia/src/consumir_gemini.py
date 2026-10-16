import os
import requests
from dotenv import load_dotenv
  
load_dotenv()
  
def armar_peticion(pregunta):
     api_key = os.getenv("GEMINI_API_KEY")
     modelo = "gemini-flash-latest"
     url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
     body = {
         "contents": 
             [{"parts": [{"text": pregunta}]}
              ]
            }
     return url, body
  
def enviar_peticion(url, body):
     respuesta = requests.post(url, json=body)
     return respuesta.json()
  
def extraer_texto(datos):
     return datos["candidates"][0]["content"]["parts"][0]["text"]
  
def obtener_dato_de_prueba(pregunta):
     url, body = armar_peticion(pregunta)
     datos = enviar_peticion(url, body)
     return extraer_texto(datos)

print(obtener_dato_de_prueba("Qué día es hoy?"))