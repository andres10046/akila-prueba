"""Capa de presentación: render de KPIs y gráficos en Streamlit."""

import streamlit as st
import plotly.express as px


def render_kpis(k: dict, anio: str = "Todos") -> None:
    sufijo = f" ({anio})" if anio != "Todos" else ""

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric(f"Vendidos{sufijo}", f"{k['total_vendidos']}")
    c2.metric(
        "Disponibles (proyecto)",
        f"{k['total_disponibles']}",
        f"{k['pct_por_vender']}% por vender",
    )
    c3.metric("Tipos de producto", f"{k['variedad_producto']}")
    c4.metric(f"Valor vendido{sufijo} (COP)", f"${k['valor_vendido_cop']:,.0f}")
    c5.metric(f"Precio promedio{sufijo} (COP)", f"${k['precio_promedio_cop']:,.0f}")


def render_ventas_tiempo(datos, granularidad: str = "Semanal", anio: str = "Todos") -> None:
    titulo = f"Ventas por {granularidad.lower()}"
    if anio != "Todos":
        titulo += f" — {anio}"
    st.subheader(f"📅 {titulo}")

    if datos.empty:
        st.info(f"No hay ventas con fecha válida en {anio}.")
        return

    fig = px.bar(
        datos, x="periodo", y="num_ventas", text="num_ventas",
        labels={"periodo": granularidad, "num_ventas": "Nº ventas"},
    )
    fig.update_layout(
        xaxis_tickformat="%b %Y" if granularidad == "Mensual" else "%d %b %Y"
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander(f"Ver tabla de ventas por {granularidad.lower()}"):
        st.dataframe(
            datos.rename(columns={
                "periodo": granularidad,
                "num_ventas": "Nº ventas",
                "valor_cop": "Valor (COP)",
            }),
            use_container_width=True, hide_index=True,
        )


def render_ventas_tipo(t) -> None:
    st.subheader("🏷️ Tipos de apartamento vendidos")
    if t.empty:
        st.info("Sin ventas registradas.")
        return
    st.dataframe(t, use_container_width=True, hide_index=True)
    st.plotly_chart(
        px.pie(t, names="tipo_apartamento", values="vendidos", hole=0.4),
        use_container_width=True,
    )


def render_disponibles(d) -> None:
    st.subheader("🟢 Disponibles por tipo (proyecto)")
    if d.empty:
        st.info("Sin disponibles.")
        return
    st.dataframe(d, use_container_width=True, hide_index=True)
    st.plotly_chart(
        px.bar(d, x="tipo_apartamento", y="disponibles", text="disponibles"),
        use_container_width=True,
    )