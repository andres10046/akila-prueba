"""Deduplicación de correos por hash de remitente+asunto+cuerpo."""

import hashlib


def _hash_correo(correo: dict) -> str:
    clave = (
        correo.get("remitente", "").strip().lower()
        + "|" + correo.get("asunto", "").strip().lower()
        + "|" + correo.get("cuerpo", "").strip().lower()
    )
    return hashlib.sha256(clave.encode("utf-8")).hexdigest()


def deduplicar(correos: list[dict]) -> tuple[list[dict], list[dict]]:
    """Devuelve (únicos, duplicados). Mantiene el primero visto."""
    vistos = set()
    unicos, duplicados = [], []
    for c in correos:
        h = _hash_correo(c)
        if h in vistos:
            duplicados.append(c)
        else:
            vistos.add(h)
            unicos.append(c)
    return unicos, duplicados