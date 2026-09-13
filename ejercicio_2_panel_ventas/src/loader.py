"""Lectura y normalización del CSV."""

from pathlib import Path
import pandas as pd

CSV_DEFECTO = Path(__file__).resolve().parent.parent / "data" / "apartamentos_akila.csv"

COLUMNAS_FECHA = ("fecha_venta", "fecha_entrega")
COLUMNAS_NUMERICAS = (
    "precio_cop", "area_m2", "porcentaje_credito",
    "monto_credito_cop", "monto_contado_cop",
)


def _normalizar_columnas(df):
    df.columns = (
        df.columns.str.strip().str.lower()
        .str.replace("á", "a", regex=False).str.replace("é", "e", regex=False)
        .str.replace("í", "i", regex=False).str.replace("ó", "o", regex=False)
        .str.replace("ú", "u", regex=False).str.replace(" ", "_", regex=False)
    )
    return df


def _parsear_fechas(df):
    """Parsea fechas del CSV (ISO YYYY-MM-DD). Vacíos → NaT."""
    for c in COLUMNAS_FECHA:
        if c in df.columns:
            serie = df[c].astype(str).str.strip().str.strip('"').str.strip("'")
            serie = serie.replace({"": None, "nan": None, "None": None, "NaT": None})
            df[c] = pd.to_datetime(serie, errors="coerce")
    return df


def _parsear_numericos(df):
    for c in COLUMNAS_NUMERICAS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def _normalizar_categoricos(df):
    for c in ("estado", "forma_pago"):
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip().str.lower()
    return df


def cargar_apartamentos(ruta=CSV_DEFECTO):
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el CSV en: {ruta}")

    df = pd.read_csv(ruta, encoding="utf-8-sig")  # utf-8-sig quita el BOM
    df = _normalizar_columnas(df)
    df = _parsear_fechas(df)
    df = _parsear_numericos(df)
    df = _normalizar_categoricos(df)
    return df