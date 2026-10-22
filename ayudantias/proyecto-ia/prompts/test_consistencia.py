import json
import time

from prompts.banco import BANCO_DE_PROMPTS
from src.consumir_gemini import (
    armar_peticion,
    enviar_peticion,
    extraer_texto,
    parsear_respuesta_json,
)

INTENTOS = 3
registro = {}

for prompt in BANCO_DE_PROMPTS:
    print(f"Probando {prompt['nombre']}...")

    exitos = 0
    fallos_formato = 0
    errores_api = 0

    for intento in range(1, INTENTOS + 1):
        try:
            url, body = armar_peticion(
                prompt["ejemplo_usuario"],
                prompt["system_instruction"],
                prompt.get("response_schema"),
            )
            respuesta = enviar_peticion(url, body)
            texto = extraer_texto(respuesta)
            datos = parsear_respuesta_json(texto, prompt["categorias_permitidas"])

            if all(clave in datos for clave in prompt["claves_esperadas"]):
                exitos += 1
                print(f"  intento {intento}: válido {datos}")
            else:
                fallos_formato += 1
                print(f"  intento {intento} falló: faltan claves esperadas")

        except RuntimeError as error:
            # Falló la API o la red: no es culpa del prompt
            errores_api += 1
            print(f"  intento {intento} error de API: {error}")

        except ValueError as error:
            # El modelo respondió, pero no con el JSON que esperábamos
            fallos_formato += 1
            print(f"  intento {intento} falló: {error}")

        time.sleep(1)

    print(f"{prompt['nombre']}: {exitos}/{INTENTOS} respuestas válidas\n")

    registro[prompt["nombre"]] = {
        "intentos": INTENTOS,
        "exitos": exitos,
        "fallos_formato": fallos_formato,
        "errores_api": errores_api,
    }

with open("prompts/registro_resultados.json", "w", encoding="utf-8") as archivo:
    json.dump(registro, archivo, indent=2, ensure_ascii=False)

print("Registro guardado en prompts/registro_resultados.json")
