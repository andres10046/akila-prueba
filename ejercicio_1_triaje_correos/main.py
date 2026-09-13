"""Entry point del triaje de correos.

Modos:
  --input <csv>     lee correos desde CSV (modo demo)
  --imap            lee correos de un buzón IMAP (modo producción)
"""

import argparse
from pathlib import Path

from src.loaders.csv_loader import cargar_correos as cargar_csv
from src.loaders.imap_loader import cargar_correos_no_leidos, marcar_como_leido
from src.dedupe import deduplicar
from src.filtros import filtrar_no_clientes
from src.clasificador import clasificar
from src.excel_writer import escribir_excel


def procesar(correos: list[dict]) -> list[dict]:
    unicos, duplicados = deduplicar(correos)
    clientes, no_clientes = filtrar_no_clientes(unicos)

    filas = []
    for c in clientes:
        cl = clasificar(c)

        # Regla de revisión: Baja confianza → Sí; Media → Quizá; Alta → No
        if cl.confianza == "Baja":
            revision = "Sí"
        elif cl.confianza == "Media":
            revision = "Quizá"
        else:
            revision = "No"

        filas.append({
            "Fecha": c.get("fecha_recepcion"),
            "Cliente": c.get("remitente", "").split("@")[0],
            "Tipo": cl.tipo,
            "Urgencia": cl.urgencia,
            "Acción": cl.accion,
            "Responsable": cl.responsable,
            "Confianza": cl.confianza,
            "Requiere_Revision": revision,
        })

    print(f"[info] Correos leídos:          {len(correos)}")
    print(f"[info] Duplicados descartados:  {len(duplicados)}")
    print(f"[info] No-clientes descartados: {len(no_clientes)}")
    print(f"[info] Procesados:              {len(filas)}")
    print(f"[info] Revisión Sí:             {sum(1 for f in filas if f['Requiere_Revision'] == 'Sí')}")
    print(f"[info] Revisión Quizá:          {sum(1 for f in filas if f['Requiere_Revision'] == 'Quizá')}")

    return filas


def main():
    parser = argparse.ArgumentParser(description="Triaje de correos Akila")
    parser.add_argument("--input", help="Ruta al CSV de correos (modo demo)")
    parser.add_argument("--output", default="output/seguimiento.xlsx",
                        help="Ruta del Excel de salida")
    parser.add_argument("--imap", action="store_true",
                        help="Leer correos desde buzón IMAP (modo producción)")
    args = parser.parse_args()

    if args.imap:
        print("[info] Modo producción: leyendo buzón IMAP...")
        correos = cargar_correos_no_leidos()
    elif args.input:
        print(f"[info] Modo demo: leyendo {args.input}")
        correos = cargar_csv(args.input)
    else:
        parser.error("Debes indicar --input <csv> o --imap")

    filas = procesar(correos)
    ruta = escribir_excel(filas, args.output)
    print(f"[ok]   Excel generado en: {ruta}")

    if args.imap:
        uids = [c["uid"] for c in correos if "uid" in c]
        marcar_como_leido(uids)
        print(f"[ok]   {len(uids)} correos marcados como leídos")


if __name__ == "__main__":
    main()