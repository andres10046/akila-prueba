"""Descarta correos que no son de clientes (bancos, spam, partners)."""

from src import reglas


def es_cliente(correo: dict) -> tuple[bool, str]:
    """Devuelve (es_cliente, motivo)."""
    remitente = correo.get("remitente", "").strip().lower()

    if remitente in reglas.REMITENTES_NO_CLIENTE:
        return False, f"Remitente en lista negra: {remitente}"

    for d in reglas.DOMINIOS_NO_CLIENTE:
        if d in remitente:
            return False, f"Dominio no-cliente: {d}"

    return True, ""


def filtrar_no_clientes(correos: list[dict]) -> tuple[list[dict], list[dict]]:
    """Devuelve (clientes, no_clientes)."""
    clientes, no_clientes = [], []
    for c in correos:
        ok, motivo = es_cliente(c)
        if ok:
            clientes.append(c)
        else:
            c["_motivo_descarte"] = motivo
            no_clientes.append(c)
    return clientes, no_clientes