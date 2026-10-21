import json
import time
from datetime import datetime
from pathlib import Path

from prompts.banco import BANCO_DE_PROMPTS
from src.consumir_gemini import (
    armar_peticion,
    enviar_peticion,
    extraer_texto,
    parsear_respuesta_json,
)


def main():
    # Cada ejecución conserva su propio registro para comparar antes y después.
    registro = {
        "fecha_hora_local": datetime.now().astimezone().isoformat(),
        "validacion": "JSON tras limpieza de Markdown, claves, tipos y categorías",
        "banco_probado": BANCO_DE_PROMPTS,
        "resultados": {},
    }

    for prompt in BANCO_DE_PROMPTS:
        resumen = {
            "intentos": 3,
            "exitos": 0,
            "fallos_formato": 0,
            "errores_api": 0,
            "detalle": [],
        }
        registro["resultados"][prompt["nombre"]] = resumen

        for intento in range(1, 4):
            detalle = {"intento": intento}

            try:
                url, body = armar_peticion(
                    prompt["ejemplo_usuario"],
                    prompt["system_instruction"],
                    prompt.get("response_schema"),
                )
                respuesta = enviar_peticion(url, body)
                texto = extraer_texto(respuesta)

            except RuntimeError as error:
                resumen["errores_api"] += 1
                detalle.update(estado="error_api", error=str(error))

            else:
                detalle["modelo_reportado"] = respuesta.get("modelVersion")
                detalle["respuesta_original"] = texto

                try:
                    datos = parsear_respuesta_json(
                        texto, prompt["categorias_permitidas"]
                    )
                    if not all(k in datos for k in prompt["claves_esperadas"]):
                        raise ValueError("Faltan claves esperadas.")

                except ValueError as error:
                    resumen["fallos_formato"] += 1
                    detalle.update(estado="fallo_formato", error=str(error))

                else:
                    resumen["exitos"] += 1
                    detalle.update(estado="valida", datos=datos)

            resumen["detalle"].append(detalle)
            print(f"{prompt['nombre']} - intento {intento}: {detalle['estado']}")
            time.sleep(1)

        print(
            f"{prompt['nombre']}: {resumen['exitos']}/3 válidas; "
            f"{resumen['fallos_formato']} fallos de formato; "
            f"{resumen['errores_api']} errores de API.\n"
        )

    carpeta = Path(__file__).resolve().parent
    ruta = carpeta / "registro_resultados.json"
    sello = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    historico = carpeta / f"registro_{sello}.json"
    contenido = json.dumps(registro, indent=2, ensure_ascii=False)
    ruta.write_text(contenido, encoding="utf-8")
    historico.write_text(contenido, encoding="utf-8")
    print("Registro más reciente:", ruta)
    print("Copia de esta ejecución:", historico)


if __name__ == "__main__":
    main()
