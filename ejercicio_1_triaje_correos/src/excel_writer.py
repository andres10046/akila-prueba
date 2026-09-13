"""Escribe el Excel de seguimiento con las columnas que pide el enunciado."""

from pathlib import Path
import pandas as pd

COLUMNAS = ["Fecha", "Cliente", "Tipo", "Urgencia", "Acción", "Responsable",
            "Confianza", "Requiere_Revision"]


def escribir_excel(filas: list[dict], ruta: str | Path) -> Path:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(filas, columns=COLUMNAS)
    df.to_excel(ruta, index=False, sheet_name="Seguimiento")
    return ruta