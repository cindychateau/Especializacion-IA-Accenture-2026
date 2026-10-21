import json
import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()


def armar_peticion(pregunta, system_instruction=None, response_schema=None):
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía")

    api_key = os.getenv("GEMINI_API_KEY")
    modelo = "gemini-3.6-flash"
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{modelo}:generateContent?key={api_key}"
    )

    body = {"contents": [{"parts": [{"text": pregunta}]}]}

    if system_instruction is not None:
        body["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }

    if response_schema is not None:
        body["generationConfig"] = {
            "responseMimeType": "application/json",
            "responseSchema": response_schema,
        }

    return url, body


def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body, timeout=30)
    except requests.exceptions.Timeout:
        raise RuntimeError("El servicio no respondió dentro de 30 segundos.") from None
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se pudo conectar con el servicio.") from None
    except requests.exceptions.RequestException:
        raise RuntimeError("No se pudo completar la petición HTTP.") from None

    if not respuesta.ok:
        raise RuntimeError(f"La API respondió con error HTTP {respuesta.status_code}.")

    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta HTTP no contiene JSON válido.") from None


def extraer_texto(datos):
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("La respuesta no trae el texto generado esperado.") from None


def parsear_respuesta_json(texto, categorias_permitidas=None):
    """Valida el contrato compartido por los tres prompts de este banco."""
    limpio = texto.strip()
    limpio = re.sub(r"^```(?:json)?\s*", "", limpio)
    limpio = re.sub(r"\s*```$", "", limpio)

    try:
        datos = json.loads(limpio)
    except json.JSONDecodeError:
        raise ValueError("El texto del modelo no es JSON válido.") from None

    if not isinstance(datos, dict):
        raise ValueError("Se esperaba un objeto JSON.")

    if set(datos) != {"categoria", "confianza"}:
        raise ValueError("El JSON debe tener solo categoria y confianza.")

    if not isinstance(datos["categoria"], str):
        raise ValueError("categoria debe ser texto.")

    if categorias_permitidas is not None:
        if datos["categoria"] not in categorias_permitidas:
            raise ValueError("La categoría no está permitida para este prompt.")

    confianza = datos["confianza"]
    if type(confianza) not in (int, float) or not 0 <= confianza <= 1:
        raise ValueError("confianza debe ser un número entre 0 y 1.")

    return datos


def calcular_costo(datos, precio_entrada, precio_salida):
    uso = datos["usageMetadata"]
    tokens_entrada = uso["promptTokenCount"]
    tokens_salida = uso["candidatesTokenCount"]
    tokens_razonamiento = uso.get("thoughtsTokenCount", 0)

    return (
        tokens_entrada * precio_entrada
        + (tokens_salida + tokens_razonamiento) * precio_salida
    )


def obtener_dato_de_prueba(pregunta):
    url, body = armar_peticion(pregunta)
    datos = enviar_peticion(url, body)
    # Valores heredados del proyecto: verificar contra las tarifas del modelo.
    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"Costo estimado de la operación: ${costo:.6f} USD")
    return extraer_texto(datos)


if __name__ == "__main__":
    try:
        print(obtener_dato_de_prueba("Cuenta un chiste chileno"))
    except (ValueError, RuntimeError, KeyError) as error:
        print("No se pudo completar la operación:", error)
