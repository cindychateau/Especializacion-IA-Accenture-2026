FORMATO = (
    "Devuelve únicamente un objeto JSON válido, sin texto adicional ni Markdown. "
    "Debe tener exactamente dos claves: 'categoria' (string) "
    "y 'confianza' (número entre 0 y 1). "
)

MENSAJE = (
    "No puedo acceder al portal desde ayer. "
    "Ya cambié mi contraseña y sigo bloqueado. "
    "Hoy vence la entrega de mi informe y estoy muy molesto."
)

ESQUEMA = {
    "type": "OBJECT",
    "properties": {
        "categoria": {"type": "STRING"},
        "confianza": {"type": "NUMBER"},
    },
    "required": ["categoria", "confianza"],
}

BANCO_DE_PROMPTS = [
    {
        "nombre": "clasificar_tema",
        "system_instruction": FORMATO + (
            "Clasifica el tema principal del ticket. "
            "Usa 'acceso' para problemas de ingreso o contraseña, "
            "'facturacion' para cobros y pagos, y 'otro' en los demás casos."
        ),
        "ejemplo_usuario": MENSAJE,
        "claves_esperadas": ["categoria", "confianza"],
        "categorias_permitidas": ["acceso", "facturacion", "otro"],
        "response_schema": ESQUEMA,
    },
    {
        "nombre": "clasificar_prioridad",
        "system_instruction": FORMATO + (
            "Clasifica la prioridad del ticket. "
            "Usa 'alta' si un bloqueo impide cumplir un plazo de hoy, "
            "'media' si hay un bloqueo sin ese plazo, "
            "y 'baja' si es una consulta sin bloqueo. "
            "Usa solo la información del mensaje."
        ),
        "ejemplo_usuario": MENSAJE,
        "claves_esperadas": ["categoria", "confianza"],
        "categorias_permitidas": ["alta", "media", "baja"],
        "response_schema": ESQUEMA,
    },
    {
        "nombre": "clasificar_sentimiento",
        "system_instruction": FORMATO + (
            "Clasifica el sentimiento expresado en el ticket. "
            "Usa 'positivo' para satisfacción, 'negativo' para molestia "
            "o frustración, y 'neutro' si no expresa ninguno de los anteriores."
        ),
        "ejemplo_usuario": MENSAJE,
        "claves_esperadas": ["categoria", "confianza"],
        "categorias_permitidas": ["positivo", "negativo", "neutro"],
        "response_schema": ESQUEMA,
    },
]
