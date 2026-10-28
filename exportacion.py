import json
import os
from datetime import datetime

# Nombre de los archivos que se utilizarán para exportar los contactos
ARCHIVO_JSON = "contactos_exportados.json"
ARCHIVO_PDF = "reporte_contactos.pdf"

# Exporta la lista de contactos a un archivo JSON
def exportar_json(contactos, ruta=ARCHIVO_JSON):

    try:
        # Abre el archivo en modo escritura con codificación UTF-8
        with open(ruta, "w", encoding="utf-8") as archivo:
            # Guarda los contactos en formato JSON con una indentación de 4 espacios
            json.dump(contactos, archivo, ensure_ascii=False, indent=4)
        # Devuelve la ruta absoluta del archivo guardado
        return os.path.abspath(ruta)
    # Maneja errores relacionados con la escritura del archivo
    except OSError as error:
        # Genera un mensaje indicando que no se pudo guardar el JSON
        raise OSError(f"No se pudo guardar el JSON: {error}") from error

# Genera un reporte PDF utilizando los contactos guardados en un archivo JSON
def generar_pdf_desde_json(ruta_json=ARCHIVO_JSON, ruta_pdf=ARCHIVO_PDF):
    try:
        # Abre el archivo JSON en modo lectura
        with open(ruta_json, "r", encoding="utf-8") as archivo:
            # Carga los contactos almacenados en el archivo JSON
            contactos = json.load(archivo)
    # Maneja el error cuando el archivo JSON no existe
    except FileNotFoundError as error:
        # Indica que primero se deben exportar los contactos
        raise FileNotFoundError(
            "Primero exporte los contactos a JSON."
        ) from error
    # Maneja errores cuando el contenido JSON tiene un formato incorrecto
    except json.JSONDecodeError as error:
        # Muestra un mensaje indicando que el archivo está dañado o es inválido
        raise ValueError("El archivo JSON está dañado o tiene formato inválido.") from error

    # Verifica que los contactos estén almacenados en una lista
    if not isinstance(contactos, list):
        raise ValueError("El JSON debe contener una lista de contactos.")

    try:
        # Importa la clase FPDF para crear documentos PDF
        from fpdf import FPDF
    # Maneja el error si la biblioteca FPDF no está instalada
    except ImportError as error:
        # Indica el comando necesario para instalar la biblioteca
        raise ImportError(
            "Falta instalar fpdf2. Ejecute: python -m pip install fpdf2"
        ) from error

    # Crea un documento PDF en orientación horizontal y tamaño A4
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    # Configura los saltos de página automáticos y el margen inferior
    pdf.set_auto_page_break(auto=True, margin=15)
    # Agrega una página al documento
    pdf.add_page()

    # Configura la fuente Helvetica en negrita y tamaño 16
    pdf.set_font("Helvetica", "B", 16)
    # Escribe el título del reporte centrado
    pdf.cell(0, 10, "Agenda de Contactos", new_x="LMARGIN", new_y="NEXT", align="C")

    # Configura la fuente Helvetica con tamaño 10
    pdf.set_font("Helvetica", size=10)
    # Obtiene la fecha y hora actuales con el formato indicado
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # Escribe la fecha y hora de generación del reporte
    pdf.cell(0, 8, f"Fecha de generacion: {fecha}", new_x="LMARGIN", new_y="NEXT")
    # Agrega un pequeño espacio antes de la tabla
    pdf.ln(3)

    # Define los títulos de las columnas y sus respectivos anchos
    columnas = [
        ("ID", 15),
        ("Nombre", 55),
        ("Telefono", 35),
        ("Correo", 75),
        ("Ciudad", 55),
    ]

    # Configura la fuente en negrita y tamaño 9 para los encabezados
    pdf.set_font("Helvetica", "B", 9)
    # Recorre las columnas para dibujar los encabezados de la tabla
    for titulo, ancho in columnas:
        # Escribe cada título con bordes y alineación centrada
        pdf.cell(ancho, 9, titulo, border=1, align="C")
    # Pasa a la siguiente línea después de los encabezados
    pdf.ln()

    # Configura la fuente con tamaño 8 para los datos de los contactos
    pdf.set_font("Helvetica", size=8)
    # Recorre la lista de contactos
    for contacto in contactos:
        # Obtiene los datos del contacto y los convierte a texto
        # Si algún campo no existe, utiliza una cadena vacía
        valores = [
            str(contacto.get("id", "")),
            str(contacto.get("nombre", "")),
            str(contacto.get("telefono", "")),
            str(contacto.get("correo", "")),
            str(contacto.get("ciudad", "")),
        ]
        # Recorre los valores junto con los anchos de las columnas
        for valor, (_, ancho) in zip(valores, columnas):
            # Sustituye caracteres que la fuente básica de FPDF no representa
            valor = valor.encode("latin-1", "replace").decode("latin-1")
            # Escribe el dato en una celda con bordes y limita el texto a 45 caracteres
            pdf.cell(ancho, 8, valor[:45], border=1)
        # Pasa a la siguiente línea para mostrar el próximo contacto
        pdf.ln()

    # Guarda el documento PDF en la ruta indicada
    pdf.output(ruta_pdf)
    # Devuelve la ruta absoluta del archivo PDF generado
    return os.path.abspath(ruta_pdf)

# Exporta los contactos a JSON y genera el PDF utilizando ese mismo archivo
def exportar_json_y_pdf(contactos):
    """Exporta a JSON y genera el PDF a partir de ese mismo JSON."""
    # Guarda los contactos en el archivo JSON y obtiene su ruta
    ruta_json = exportar_json(contactos)
    # Genera el PDF a partir del archivo JSON creado
    ruta_pdf = generar_pdf_desde_json(ruta_json)
    # Devuelve las rutas de los dos archivos generados
    return ruta_json, ruta_pdf