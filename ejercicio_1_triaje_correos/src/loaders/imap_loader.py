"""Carga correos desde un buzón IMAP (modo producción).

Requiere credenciales en .env. No se ejecuta en la demo por falta de acceso
a un buzón real. El código está listo para producción.
"""

import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

IMAP_HOST = os.getenv("IMAP_HOST", "")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
IMAP_USER = os.getenv("IMAP_USER", "")
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD", "")
IMAP_FOLDER = os.getenv("IMAP_FOLDER", "INBOX")


def _decodificar(valor) -> str:
    if valor is None:
        return ""
    partes = decode_header(valor)
    out = []
    for texto, enc in partes:
        if isinstance(texto, bytes):
            out.append(texto.decode(enc or "utf-8", errors="replace"))
        else:
            out.append(texto)
    return " ".join(out)


def _extraer_cuerpo(msg) -> str:
    if msg.is_multipart():
        for parte in msg.walk():
            if parte.get_content_type() == "text/plain":
                return parte.get_payload(decode=True).decode(
                    parte.get_content_charset() or "utf-8", errors="replace"
                )
        return ""
    return msg.get_payload(decode=True).decode(
        msg.get_content_charset() or "utf-8", errors="replace"
    )


def cargar_correos_no_leidos() -> list[dict]:
    """Conecta al buzón y devuelve los correos no leídos como dicts."""
    if not all([IMAP_HOST, IMAP_USER, IMAP_PASSWORD]):
        raise EnvironmentError(
            "Faltan credenciales IMAP. Copia .env.example a .env y complétalo."
        )

    correos = []
    with imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT) as mail:
        mail.login(IMAP_USER, IMAP_PASSWORD)
        mail.select(IMAP_FOLDER)

        _, data = mail.search(None, "(UNSEEN)")
        for uid in data[0].split():
            _, msg_data = mail.fetch(uid, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            correos.append({
                "uid": uid.decode(),
                "fecha_recepcion": parsedate_to_datetime(msg.get("Date")),
                "remitente": _decodificar(msg.get("From", "")),
                "asunto": _decodificar(msg.get("Subject", "")),
                "cuerpo": _extraer_cuerpo(msg).strip(),
            })

    return correos


def marcar_como_leido(uids: list[str]) -> None:
    """Marca una lista de UIDs como leídos."""
    if not uids:
        return
    with imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT) as mail:
        mail.login(IMAP_USER, IMAP_PASSWORD)
        mail.select(IMAP_FOLDER)
        for uid in uids:
            mail.store(uid, "+FLAGS", "\\Seen")