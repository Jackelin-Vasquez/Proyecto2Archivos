import json
import os
from datetime import datetime

ARCHIVO_JSON = "contactos_exportados.json"
ARCHIVO_PDF = "reporte_contactos.pdf"

def exportar_json(contactos, ruta=ARCHIVO_JSON):
   
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(contactos, archivo, ensure_ascii=False, indent=4)
        return os.path.abspath(ruta)
    except OSError as error:
        raise OSError(f"No se pudo guardar el JSON: {error}") from error

def generar_pdf_desde_json(ruta_json=ARCHIVO_JSON, ruta_pdf=ARCHIVO_PDF):
    try:
        with open(ruta_json, "r", encoding="utf-8") as archivo:
            contactos = json.load(archivo)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            "Primero exporte los contactos a JSON."
        ) from error
    except json.JSONDecodeError as error:
        raise ValueError("El archivo JSON está dañado o tiene formato inválido.") from error

    if not isinstance(contactos, list):
        raise ValueError("El JSON debe contener una lista de contactos.")

    try:
        from fpdf import FPDF
    except ImportError as error:
        raise ImportError(
            "Falta instalar fpdf2. Ejecute: python -m pip install fpdf2"
        ) from error

    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Agenda de Contactos", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", size=10)
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pdf.cell(0, 8, f"Fecha de generacion: {fecha}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    columnas = [
        ("ID", 15),
        ("Nombre", 55),
        ("Telefono", 35),
        ("Correo", 75),
        ("Ciudad", 55),
    ]
    pdf.set_font("Helvetica", "B", 9)
    for titulo, ancho in columnas:
        pdf.cell(ancho, 9, titulo, border=1, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", size=8)
    for contacto in contactos:
        valores = [
            str(contacto.get("id", "")),
            str(contacto.get("nombre", "")),
            str(contacto.get("telefono", "")),
            str(contacto.get("correo", "")),
            str(contacto.get("ciudad", "")),
        ]
        for valor, (_, ancho) in zip(valores, columnas):
            # Sustituye caracteres que la fuente básica de FPDF no representa.
            valor = valor.encode("latin-1", "replace").decode("latin-1")
            pdf.cell(ancho, 8, valor[:45], border=1)
        pdf.ln()

    pdf.output(ruta_pdf)
    return os.path.abspath(ruta_pdf)

def exportar_json_y_pdf(contactos):
    """Exporta a JSON y genera el PDF a partir de ese mismo JSON."""
    ruta_json = exportar_json(contactos)
    ruta_pdf = generar_pdf_desde_json(ruta_json)
    return ruta_json, ruta_pdf