"""Carga correos desde CSV (modo demo)."""

from pathlib import Path
import pandas as pd

CSV_DEFECTO = Path(__file__).resolve().parent.parent.parent / "data" / "correos_clientes.csv"


def cargar_correos(ruta: str | Path = CSV_DEFECTO) -> list[dict]:
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el CSV en: {ruta}")

    df = pd.read_csv(ruta, encoding="utf-8-sig")
    df.columns = df.columns.str.strip().str.lower()

    # Fecha: puede venir ISO o latina
    df["fecha_recepcion"] = pd.to_datetime(df["fecha_recepcion"], errors="coerce")

    return df.to_dict(orient="records")