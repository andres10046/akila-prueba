"""Cálculos puros: KPIs y agregaciones. Sin Streamlit, sin Plotly."""

import pandas as pd


def _vendidos(df):
    return df[df["estado"] == "vendido"].copy()


def _disponibles(df):
    return df[df["estado"] == "disponible"].copy()


def kpis_globales(df):
    v, d, t = _vendidos(df), _disponibles(df), len(df)
    return {
        "total_apartamentos": t,
        "total_vendidos": len(v),
        "total_disponibles": len(d),
        "variedad_producto": df["tipo_apartamento"].nunique(),
        "valor_vendido_cop": float(v["precio_cop"].sum()),
        "precio_promedio_cop": float(v["precio_cop"].mean()) if len(v) else 0.0,
        "pct_vendido": round(len(v) / t * 100, 2) if t else 0.0,
        "pct_por_vender": round(len(d) / t * 100, 2) if t else 0.0,
    }


def ventas_por_semana(df):
    v = _vendidos(df).dropna(subset=["fecha_venta"])
    if v.empty:
        return pd.DataFrame(columns=["periodo", "num_ventas", "valor_cop"])
    v = v.assign(periodo=v["fecha_venta"].dt.to_period("W").dt.start_time)
    return (
        v.groupby("periodo")
        .agg(num_ventas=("apartamento", "count"), valor_cop=("precio_cop", "sum"))
        .reset_index()
        .sort_values("periodo")
    )


def ventas_por_mes(df):
    v = _vendidos(df).dropna(subset=["fecha_venta"])
    if v.empty:
        return pd.DataFrame(columns=["periodo", "num_ventas", "valor_cop"])
    v = v.assign(periodo=v["fecha_venta"].dt.to_period("M").dt.start_time)
    return (
        v.groupby("periodo")
        .agg(num_ventas=("apartamento", "count"), valor_cop=("precio_cop", "sum"))
        .reset_index()
        .sort_values("periodo")
    )


def ventas_por_tipo(df):
    v = _vendidos(df)
    if v.empty:
        return pd.DataFrame(columns=["tipo_apartamento", "vendidos", "pct_sobre_total"])
    t = (
        v.groupby("tipo_apartamento")
        .size()
        .reset_index(name="vendidos")
        .sort_values("vendidos", ascending=False)
    )
    t["pct_sobre_total"] = (t["vendidos"] / t["vendidos"].sum() * 100).round(2)
    return t


def disponibles_por_tipo(df):
    d = _disponibles(df)
    if d.empty:
        return pd.DataFrame(columns=["tipo_apartamento", "disponibles"])
    return (
        d.groupby("tipo_apartamento")
        .size()
        .reset_index(name="disponibles")
        .sort_values("disponibles", ascending=False)
    )