"""Reglas de negocio: clasificación, urgencia, acción y responsable.

Estas tablas las define Akila. La IA NO las modifica.
"""

# Palabras clave por tipo. El clasificador puntúa cada tipo y gana el de más hits.

PALABRAS_TIPO = {
    "reclamacion": [
        "reclamo", "reclamación", "queja", "indignado", "devolución",
        "desistir", "no quedó", "no funciona", "nadie me contesta",
        "nadie me dice", "no me han", "tres semanas", "nadie me llama",
        "sin respuesta",
    ],
    "incidencia": [
        "incidencia", "falla", "fallo", "problema", "error",
        "inundado", "roto", "dañado", "no carga",
        "se atrasa", "retraso", "retrasado",
    ],
    "pedido": [
        "solicito", "requiero",
        "documentos", "escrituración", "consignar",
        "cuota inicial", "desembolso",
    ],
        "consulta": [
        "consulta", "información",
        "precios", "disponible", "cotización", "quisiera saber",
        "me gustaría", "cuánto", "cuándo", "para cuándo",
        "forma de pago", "formas de pago",
        "cambiar", "cambio",
    ],
}

PALABRAS_URGENCIA_ALTA = [
    "urgente", "hoy", "esta semana", "inmediato", "ya pagué",
    "desembolso", "vence", "plazo",
]

PALABRAS_URGENCIA_MEDIA = [
    "pronto", "cuanto antes", "necesito que",
]

ACCIONES = {
    "consulta":    "Responder con información",
    "incidencia":  "Registrar incidencia y asignar técnico",
    "pedido":      "Gestionar pedido con administración",
    "reclamacion": "Escalar a atención al cliente",
    "ambiguo":     "Revisión manual",
    "no_cliente":  "Descartar",
}

RESPONSABLES = {
    "consulta":    "Equipo comercial",
    "incidencia":  "Equipo técnico",
    "pedido":      "Administración",
    "reclamacion": "Atención al cliente",
    "ambiguo":     "Revisión manual",
    "no_cliente":  "N/A",
}

# Prioridad en caso de empate
PRIORIDAD_TIPOS = ["reclamacion", "incidencia", "pedido", "consulta"]

# Dominios y remitentes que no son clientes
DOMINIOS_NO_CLIENTE = [
    "bancolombia.com.co",
    "notificaciones@",
    "noreply@",
]

REMITENTES_NO_CLIENTE = [
    "gerencia@inmobiliariasur.co",
]

# Prefijos de asunto que se ignoran
PREFIJOS_IGNORADOS_ASUNTO = ["re:", "rv:", "fwd:", "fw:"]