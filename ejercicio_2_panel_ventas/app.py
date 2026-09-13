"""Entry point del tablero. Solo orquesta."""

from pathlib import Path
import streamlit as st

from src.loader import cargar_apartamentos, CSV_DEFECTO
from src.metricas import (
    kpis_globales, ventas_por_semana, ventas_por_mes,
    ventas_por_tipo, disponibles_por_tipo,
)
from src.charts import (
    render_kpis, render_ventas_tiempo, render_ventas_tipo, render_disponibles,
)

st.set_page_config(page_title="Panel Ventas — Akila", layout="wide")


@st.cache_data(ttl=60, show_spinner="Leyendo datos...")
def _cargar(ruta: str):
    return cargar_apartamentos(ruta)


# ---------- Sidebar: datos ----------
st.sidebar.title("🏢 Akila")
st.sidebar.header("⚙️ Datos")
ruta = st.sidebar.text_input("Ruta del CSV", value=str(CSV_DEFECTO))
if st.sidebar.button("🔄 Recargar datos"):
    st.cache_data.clear()

try:
    df = _cargar(ruta)
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()


# ---------- Sidebar: filtros ----------
st.sidebar.divider()

st.sidebar.header("📅 Año de venta")
anios_venta = sorted(df["fecha_venta"].dropna().dt.year.unique().tolist())
anio_sel = st.sidebar.radio(
    "Selecciona el año",
    ["Todos"] + [str(a) for a in anios_venta],
    index=0,
)

st.sidebar.header("📊 Vista")
granularidad = st.sidebar.radio(
    "Ver ventas por",
    ["Semanal", "Mensual"],   # Semanal por defecto (lo pide el enunciado)
    horizontal=True,
)

df_v = df if anio_sel == "Todos" else df[df["fecha_venta"].dt.year == int(anio_sel)]


# ---------- Cabecera ----------
st.title("🏢 Panel de ventas — Proyecto Akila")
st.caption(f"{Path(ruta).name} · {len(df)} apartamentos · Año de venta: {anio_sel}")


# ---------- KPIs ----------
# Ventas: del año seleccionado. Inventario: del proyecto completo.
k_ventas = kpis_globales(df_v)
k_proyecto = kpis_globales(df)

k = {
    "total_vendidos":     k_ventas["total_vendidos"],
    "valor_vendido_cop":  k_ventas["valor_vendido_cop"],
    "precio_promedio_cop": k_ventas["precio_promedio_cop"],
    "total_disponibles":  k_proyecto["total_disponibles"],
    "variedad_producto":  k_proyecto["variedad_producto"],
    "pct_por_vender":     k_proyecto["pct_por_vender"],
}
render_kpis(k, anio_sel)


# ---------- Ventas por periodo ----------
datos_tiempo = ventas_por_semana(df_v) if granularidad == "Semanal" else ventas_por_mes(df_v)
render_ventas_tiempo(datos_tiempo, granularidad, anio_sel)


# ---------- Tipos vendidos (año) y disponibles (proyecto) ----------
col_a, col_b = st.columns(2)
with col_a:
    render_ventas_tipo(ventas_por_tipo(df_v))
with col_b:
    render_disponibles(disponibles_por_tipo(df))


# ---------- Detalle ----------
with st.expander("🔍 Ver datos crudos (filtrados por año)"):
    st.dataframe(df_v, use_container_width=True)