"""Clasificador de correos. Reglas primero. IA como extensión futura."""

from dataclasses import dataclass
from src import reglas


@dataclass
class Clasificacion:
    tipo: str           # consulta | incidencia | pedido | reclamacion | ambiguo
    urgencia: str       # Alta | Media | Baja
    accion: str
    responsable: str
    confianza: str      # Alta | Media | Baja
    motivo: str


def _limpiar_asunto(asunto: str) -> str:
    """Quita prefijos tipo 'RE:', 'FWD:', 'RV:' al inicio (pueden venir en cadena)."""
    a = asunto.strip().lower()
    cambio = True
    while cambio:
        cambio = False
        for pref in reglas.PREFIJOS_IGNORADOS_ASUNTO:
            if a.startswith(pref):
                a = a[len(pref):].strip()
                cambio = True
    return a


def _contar_hits(texto: str, palabras: list[str]) -> list[str]:
    return [p for p in palabras if p in texto]


def _es_cuerpo_trivial(cuerpo: str) -> bool:
    """Cuerpo vacío o de cortesía ('ok gracias', 'buenos días')."""
    c = cuerpo.strip()
    if len(c) < 30:
        return True
    if len(c.split()) < 5:
        return True
    return False


def _detectar_tipo(asunto: str, cuerpo: str) -> tuple[str, float, list[str]]:
    """Devuelve (tipo, puntuación, palabras que matchearon).

    Reglas de puntuación:
      - Cuerpo no trivial: asunto vale 1, cuerpo vale 2 por cada hit.
      - Cuerpo trivial:    asunto vale 0.5, cuerpo vale 1 por cada hit.
      - Umbral mínimo:     1.0 punto para clasificar.
      - Empate:            se resuelve por PRIORIDAD_TIPOS.
    """
    a = _limpiar_asunto(asunto)
    c = cuerpo.lower()
    trivial = _es_cuerpo_trivial(cuerpo)

    puntuaciones = {}
    detalle = {}
    for tipo, palabras in reglas.PALABRAS_TIPO.items():
        hits_asunto = _contar_hits(a, palabras)
        hits_cuerpo = _contar_hits(c, palabras)

        if trivial:
            puntuacion = 0.5 * len(hits_asunto) + 1.0 * len(hits_cuerpo)
        else:
            puntuacion = 1.0 * len(hits_asunto) + 2.0 * len(hits_cuerpo)

        if puntuacion > 0:
            puntuaciones[tipo] = puntuacion
            detalle[tipo] = list(set(hits_asunto + hits_cuerpo))

    # Umbral mínimo
    if not puntuaciones or max(puntuaciones.values()) < 1.0:
        return "ambiguo", 0.0, []

    max_p = max(puntuaciones.values())
    candidatos = [t for t, p in puntuaciones.items() if p == max_p]

    for tipo in reglas.PRIORIDAD_TIPOS:
        if tipo in candidatos:
            return tipo, max_p, detalle[tipo]

    return candidatos[0], max_p, detalle[candidatos[0]]


def _detectar_urgencia(texto: str) -> str:
    t = texto.lower()
    if any(p in t for p in reglas.PALABRAS_URGENCIA_ALTA):
        return "Alta"
    if any(p in t for p in reglas.PALABRAS_URGENCIA_MEDIA):
        return "Media"
    return "Baja"


def clasificar(correo: dict) -> Clasificacion:
    asunto = correo.get("asunto", "") or ""
    cuerpo = correo.get("cuerpo", "") or ""

    tipo, puntuacion, palabras = _detectar_tipo(asunto, cuerpo)
    urgencia = _detectar_urgencia(f"{asunto} {cuerpo}")

    if tipo == "ambiguo":
        confianza = "Baja"
        motivo = "Sin coincidencias suficientes"
    elif puntuacion >= 3:
        confianza = "Alta"
        motivo = f"{puntuacion:.1f} pts · {palabras}"
    else:
        confianza = "Media"
        motivo = f"{puntuacion:.1f} pts · {palabras}"

    return Clasificacion(
        tipo=tipo,
        urgencia=urgencia,
        accion=reglas.ACCIONES.get(tipo, "Revisión manual"),
        responsable=reglas.RESPONSABLES.get(tipo, "Revisión manual"),
        confianza=confianza,
        motivo=motivo,
    )