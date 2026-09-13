# Ejercicio 1 — Triaje de correos y volcado a seguimiento

Automatización del proceso de lectura, clasificación y volcado a Excel de los correos entrantes de clientes de Akila. Hoy lo hace una persona a mano (~2 h/día). Este sistema lo reduce a **minutos de revisión humana** sobre los correos ambiguos.

## Qué hace

Dado un buzón de correo (o un CSV exportado, para la demo):

1. **Carga** los correos entrantes.
2. **Deduplica** por hash de remitente + asunto + cuerpo.
3. **Filtra** los correos que no son de clientes (bancos, spam, partners).
4. **Clasifica** cada correo: tipo (`consulta`, `incidencia`, `pedido`, `reclamacion`), urgencia (`Alta`, `Media`, `Baja`) y confianza (`Alta`, `Media`, `Baja`).
5. **Aplica** la tabla de negocio tipo → acción → responsable.
6. **Escribe** un Excel de seguimiento con las columnas `Fecha | Cliente | Tipo | Urgencia | Acción | Responsable`.
7. **Marca** los correos como leídos (solo en modo producción con IMAP).

Los correos con **confianza Baja** van a una cola de revisión humana. Sustituye el "los dejo para el final o pregunto a un compañero" del proceso actual, acotándolo a los casos que de verdad lo necesitan.

## Requisitos

- Python 3.10 o superior
- pip

## Cómo ejecutarlo

### Modo demo (con el CSV incluido)

```bash
cd ejercicio_1_triaje_correos

# 1. Entorno virtual
python3 -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\Activate.ps1     # Windows PowerShell

# 2. Dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 3. Procesar el CSV de muestra
python main.py --input data/correos_clientes.csv
```

Salida esperada:

```
[info] Modo demo: leyendo data/correos_clientes.csv
[info] Correos leídos:          15
[info] Duplicados descartados:  1
[info] No-clientes descartados: 2
[info] Procesados:              12
[info] Revisión Sí:             2
[info] Revisión Quizá:          3
[ok]   Excel generado en: output/seguimiento.xlsx
```

El Excel queda en `output/seguimiento.xlsx`.

### Modo producción (IMAP real)

⚠️ **No ejecutado en esta demo por falta de credenciales**, pero el código está listo para producción (`src/loaders/imap_loader.py`).

```bash
# 1. Copia la plantilla de variables de entorno
cp .env.example .env

# 2. Edita .env con las credenciales del buzón
#    (en Gmail: App Password, NO la contraseña real)

# 3. Ejecutar
python main.py --imap
```

En este modo, además de generar el Excel, se **marcan los correos como leídos** en el buzón.

## Estructura

```
ejercicio_1_triaje_correos/
├── README.md
├── requirements.txt
├── .env.example                     # plantilla de credenciales (sin secretos)
├── data/
│   └── correos_clientes.csv         # muestra de 15 correos
├── src/
│   ├── __init__.py
│   ├── reglas.py                    # tablas de negocio (tipo→acción→responsable)
│   ├── clasificador.py              # clasificación por reglas + puntuación
│   ├── dedupe.py                    # deduplicación por hash
│   ├── filtros.py                   # descarta no-clientes
│   ├── excel_writer.py              # escribe el .xlsx
│   └── loaders/
│       ├── __init__.py
│       ├── csv_loader.py            # modo demo
│       └── imap_loader.py           # modo producción
├── output/
│   └── seguimiento.xlsx             # generado al ejecutar
└── main.py                          # entry point
```

**Separación de capas:**

- `loaders/` → entrada. CSV para demo, IMAP para producción. **Mismo formato de salida** (`list[dict]`), así el resto del pipeline es idéntico.
- `reglas.py` → tablas de negocio. **Esto no lo decide la IA.** Lo define Akila.
- `clasificador.py` → lógica de clasificación. Reglas con puntuación.
- `dedupe.py`, `filtros.py` → preproceso.
- `excel_writer.py` → salida.
- `main.py` → orquesta el pipeline.

Cambiar el origen (CSV → IMAP) toca solo `loaders/`. Cambiar la tabla tipo→acción toca solo `reglas.py`. Cambiar el formato de salida (Excel → CSV o BD) toca solo `excel_writer.py`.



## Decisiones de diseño

- **Reglas antes que IA.** Las reglas cubren el 80% de los casos con precisión alta y son auditables. La IA se reserva para los casos ambiguos (extensión futura, ver `docs/que_automatizar.md`).
- **La IA no decide acción ni responsable.** Son política de negocio, van en `reglas.py`. La IA no debe inventarse "escalar a jurídica" o "asignar a Juan".
- **Tres niveles de confianza (Alta/Media/Baja).** No todo va a revisión humana, solo lo que de verdad lo necesita.
- **Cuerpo pesa más que asunto.** Evita falsos positivos por asuntos heredados (`RE: cuota inicial` con cuerpo `ok gracias`).
- **Umbral mínimo de 1.0 pt.** Por debajo, ambiguo → revisión humana. Es lo que reemplaza el "lo dejo para el final" actual.
- **Dedupe por hash de remitente+asunto+cuerpo.** Elimina el problema de "a veces se le duplica una entrada".
- **Fecha y campos de cabecera se rellenan solos.** Elimina el "se le olvida rellenar la fecha".

## Verificación manual de coherencia

```bash
python -c "
from src.loaders.csv_loader import cargar_correos
from src.dedupe import deduplicar
from src.filtros import filtrar_no_clientes

correos = cargar_correos('data/correos_clientes.csv')
unicos, dupes = deduplicar(correos)
clientes, no_clientes = filtrar_no_clientes(unicos)

print(f'Leídos:          {len(correos)}')
print(f'Duplicados:      {len(dupes)}')
print(f'No-clientes:     {len(no_clientes)}')
print(f'Procesados:      {len(clientes)}')
print()
print('Comprobación: 15 - 1 - 2 = 12 ->', 15 - 1 - 2 == len(clientes))
"
```

**Esperado:**

```
Leídos:          15
Duplicados:      1
No-clientes:     2
Procesados:      12

Comprobación: 15 - 1 - 2 = 12 -> True
```

## Solución de problemas

| Error | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | Venv no activado o deps no instaladas | `source .venv/bin/activate && pip install -r requirements.txt` |
| `FileNotFoundError: data/correos_clientes.csv` | Estás fuera de la carpeta del ejercicio | `cd ejercicio_1_triaje_correos` |
| `EnvironmentError: Faltan credenciales IMAP` | Modo `--imap` sin `.env` | Copia `.env.example` a `.env` y complétalo |
| La clasificación asigna `ambiguo` a demasiados correos | Umbral de puntuación muy alto | Ajusta `PALABRAS_TIPO` o el umbral mínimo en `clasificador.py` |

## Uso de IA

**En producción: no se usa IA/LLM.** El clasificador es 100% reglas, auditable y determinista.

**En desarrollo:** se usó IA (ChatGPT/Claude) como asistente para escribir el esqueleto del código, proponer palabras clave iniciales y detectar bugs. Todo se validó manualmente contra el CSV real, iterando sobre las reglas hasta que la clasificación de los 15 correos fue razonable.

Detalle completo en `../docs/uso_ia.md`.

## Supuestos y limitaciones

- **Modo IMAP no ejecutado.** No se dispone de credenciales de un buzón real. El código sigue la API estándar de `imaplib` y está listo para producción, pero no se ha validado contra un servidor real.
- **Clasificación por reglas.** No hay ML ni LLM en producción. Funciona con las palabras clave definidas en `reglas.py`. Ajustarlas es tarea de negocio, no de código.
- **Número de apartamento no extraído.** El CSV trae correos con números de apartamento en el cuerpo (p. ej. "apartamento 803"), pero no se extraen a una columna. Sería una extensión natural con regex.
- **Multi-intención.** Los correos que mezclan temas (p. ej. cotización + incidencia) se clasifican por la intención principal. La secundaria no se registra.
- **Sin autenticación ni persistencia.** Es una demo. En producción se integraría con el Excel existente o con una base de datos.