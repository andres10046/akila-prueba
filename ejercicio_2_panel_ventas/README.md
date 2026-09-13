# Prueba técnica Akila

Repositorio con la solución a ejercicios de la prueba técnica.

## Contenido


- **Ejercicio 2 — Panel de ventas de apartamentos**: tablero interactivo en Python + Streamlit sobre `apartamentos_akila.csv` (carpeta `ejercicio_2_panel_ventas/`).

Cada carpeta tiene su propio README con detalle. Este documento cubre los requisitos comunes y cómo ejecutar todo.

---

## Requisitos previos

- **Python 3.10 o superior**
- **pip** (viene con Python)
- **git**
- Sistema operativo: Linux, macOS o Windows con WSL

Verifica tu versión:

```bash
python3 --version
```

Debe imprimir `Python 3.10.x` o superior.

---

## Cómo ejecutar el Ejercicio 2 (panel de ventas)

### 1. Clonar el repositorio

```bash
git clone https://github.com/<tu-usuario>/akila-prueba.git
cd akila-prueba
```

### 2. Crear y activar un entorno virtual

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Sabrás que el entorno está activo porque el prompt cambia a `(.venv)`.

> **¿Por qué entorno virtual?** Para no instalar las dependencias del proyecto en el Python del sistema. Cada proyecto puede necesitar versiones distintas de las mismas librerías, y el venv las aísla.

### 3. Instalar dependencias

Con el entorno virtual activo:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

El `requirements.txt` de la raíz incluye todo lo necesario para ambos ejercicios.

### 4. Ejecutar el panel

```bash
cd ejercicio_2_panel_ventas
streamlit run app.py
```

>  **Importante:** usa `streamlit run app.py`, **no** `python app.py`. Streamlit necesita su propio runner para levantar el servidor web. Si lo ejecutas con `python` verás warnings como `missing ScriptRunContext` y la app no arrancará bien.

Se abrirá automáticamente el navegador en `http://localhost:8501`.

### 5. Primera ejecución: Streamlit pide email

La primera vez que ejecutes Streamlit en tu máquina, verás:

```
👋 Welcome to Streamlit!

If you'd like to receive helpful onboarding emails, news, offers, promotions,
and the occasional swag, please enter your email address below. Otherwise,
leave this field blank.

Email:
```

**Deja el campo en blanco y pulsa `Enter`.** No es obligatorio, no es un error, y no vuelve a aparecer en las siguientes ejecuciones.



---

## Qué verás en el panel

Al abrir el Ejercicio 2 encontrarás:

- **Cabecera:** nombre del archivo cargado, total de apartamentos y año de venta seleccionado.
- **KPIs (5):**
  - Vendidos (con año si aplica)
  - Disponibles del proyecto + % por vender
  - Tipos de producto distintos
  - Valor vendido en COP (con año si aplica)
  - Precio promedio en COP (con año si aplica)
- **Ventas por semana / mes:** gráfico de barras filtrable por año y conmutable entre vista semanal y mensual.
- **Tipos de apartamento vendidos:** tabla con nº y % sobre el total.
- **Disponibles por tipo:** tabla y gráfico del stock actual del proyecto.
- **Datos crudos:** expander con el dataframe filtrado.

### Cómo usar los filtros

En la barra lateral:

- **Año de venta:** `Todos / 2025 / 2026`. Filtra las secciones de ventas (KPIs de ventas, gráfico semanal/mensual, tipos vendidos). Los KPIs de inventario (Disponibles, Tipos, % por vender) **no** se filtran por año, porque los apartamentos disponibles no tienen fecha de venta.
- **Vista:** `Semanal` (por defecto) o `Mensual`.
- **Recargar datos:** relee el CSV si lo has modificado.

---

## Estructura del proyecto (Ejercicio 2)

```
ejercicio_2_panel_ventas/
├── data/
│   └── apartamentos_akila.csv   # dataset de entrada
├── src/
│   ├── loader.py                # lectura y normalización del CSV
│   ├── metricas.py              # cálculos puros (KPIs, agregaciones)
│   └── charts.py                # render de KPIs y gráficos en Streamlit
└── app.py                       # entry point: orquesta todo
```

**Separación de capas:**

- `loader.py` → solo IO. Lee el CSV, normaliza columnas, parsea fechas y tipos.
- `metricas.py` → lógica de negocio. Funciones puras, sin Streamlit ni Plotly. Testeables con pytest sin levantar UI.
- `charts.py` → presentación. Recibe datos y los pinta en Streamlit.
- `app.py` → orquesta.

Esto permite cambiar Streamlit por Dash, o el CSV por una API, tocando solo una capa.

---

## Solución de problemas

### `ModuleNotFoundError: No module named 'streamlit'`

El entorno virtual no está activado o no instalaste las dependencias.

```bash
source .venv/bin/activate     # Linux/macOS
pip install -r requirements.txt
```

### `streamlit: command not found`

Estás fuera del venv. Actívalo antes de ejecutar.

### `Warning: to view this Streamlit app on a browser, run it with...`

Estás corriendo con `python app.py`. Usa `streamlit run app.py`.

### `FileNotFoundError: No se encontró el CSV`

Verifica que exista `ejercicio_2_panel_ventas/data/apartamentos_akila.csv`. Si lo moviste, ajusta la ruta en el sidebar.

### `KeyError: 'fecha_venta'` o similar

El CSV no tiene las columnas esperadas. Ejecuta:

```bash
head -1 ejercicio_2_panel_ventas/data/apartamentos_akila.csv
```

y comprueba los nombres.

---

## Herramientas de IA utilizadas

Este proyecto se desarrolló con apoyo de asistentes de IA (Claude) para:

- Generación del esqueleto inicial de `loader.py`, `metricas.py` y `charts.py`.
- Propuesta de estructura de capas (IO / dominio / presentación).
- Redacción de este README.

**Validación humana:**

- Todos los scripts se ejecutaron contra el CSV real (`apartamentos_akila.csv`, 457 filas).
- Se verificó coherencia numérica: `271 vendidos + 186 disponibles = 457`; `% vendido + % por vender = 100%`.
- Se corrigió manualmente el parseo de fechas (el CSV trae ISO `YYYY-MM-DD`, no `DD/MM/YYYY`) tras detectar que los 457 registros quedaban como `NaT`.
- Se ajustó la arquitectura tras iteraciones: se descartó una separación `io/domain/presentation` en subcarpetas por ser sobre-ingeniería para este alcance.



---

## Supuestos y limitaciones

- El CSV de entrada se asume **estático** y en la ruta `data/apartamentos_akila.csv`. En producción, apuntaría a una base de datos o endpoint.
- El filtro por año aplica a las **ventas**, no a los disponibles (estos no tienen fecha de venta).
- No hay autenticación ni control de acceso; es una demo.
- El panel **no** persiste cambios. Es de solo lectura.
- La app se ha probado en **Python 3.12 / Linux (Ubuntu)** y macOS. En Windows debería funcionar, pero no se ha verificado exhaustivamente.

---


