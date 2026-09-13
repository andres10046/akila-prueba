# Prueba técnica Akila

Solución a los dos ejercicios.

| # | Ejercicio | Carpeta |
|---|---|---|
| 1 | Triaje de correos y volcado a seguimiento | [`ejercicio_1_triaje_correos/`](./ejercicio_1_triaje_correos/) |
| 2 | Panel de ventas de apartamentos (Streamlit) | [`ejercicio_2_panel_ventas/`](./ejercicio_2_panel_ventas/) |

Cada carpeta tiene su propio README con instrucciones exactas.

## Ejercicio 2 — Panel de ventas (arranque rápido)

```bash
cd ejercicio_2_panel_ventas
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

> La primera vez, Streamlit pide un email. Déjalo en blanco y pulsa Enter.

## Ejercicio 1 — Triaje de correos (arranque rápido)

```bash
cd ejercicio_1_triaje_correos
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py --input data/correos_clientes.csv
```

Genera `output/seguimiento.xlsx`.

## Uso de IA

Se usó ChatGPT/Claude como asistente durante el desarrollo (esqueletos, propuesta de reglas, redacción de READMEs, depuración). **Ningún ejercicio usa IA en tiempo de ejecución.** Todo el código se validó manualmente contra los datos reales.

## Supuestos y limitaciones

- Probado en Linux con Python 3.12.
- El modo IMAP del Ejercicio 1 no se ejecutó por falta de credenciales.
- Los CSV se asumen estáticos y locales.
- Ver el README de cada ejercicio para limitaciones específicas.
