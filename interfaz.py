import os
import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QLabel, QPushButton,
    QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFormLayout,
    QDialog, QDialogButtonBox, QMenu
)

import exportacion
import indice
import manejo_archivos
import seguridad

# Paleta de colores
BG = "#15171C"
PANEL = "#20232A"
PANEL_HOVER = "#343740"
PURPLE = "#7048A8"
PURPLE_HOVER = "#8359BB"
LILAC = "#A978E0"
WHITE = "#EDEDED"
MUTED = "#A5A5A5"
LINE = "#3A3D46"
INPUT_LINE = "#444750"
INK = "#EDEDED"
NAVY = "#EDEDED"
BLUE = PURPLE
BLUE_HOVER = PURPLE_HOVER
GREEN = PURPLE
ORANGE = LILAC
RED = PURPLE_HOVER
TEAL = LILAC
PALE_BLUE = "#343740"

# Hoja de estilos del tema oscuro. Los QLabel ahora usan fondo transparente para evitar
# rectángulos de color detrás de los textos.
DARK_STYLE = f"""
* {{ font-family: "Segoe UI"; font-size: 10pt; }}
QMainWindow, QWidget {{ background: {BG}; color: {INK}; }}
QLabel {{ background: transparent; }}
QMenuBar {{ background: {PANEL}; color: {WHITE}; border-bottom: 1px solid {LINE}; padding: 5px; }}
QMenuBar::item {{ padding: 7px 10px; border-radius: 5px; }}
QMenuBar::item:selected {{ background: {PURPLE}; color: white; }}
QMenu {{ background: {PANEL}; color: {WHITE}; border: 1px solid {LINE}; }}
QMenu::item:selected {{ background: {PURPLE}; color: white; }}
QFrame#panel {{ background: {PANEL}; border: 1px solid {LINE}; border-radius: 10px; }}
QLabel#appTitle {{ color: {WHITE}; font-size: 25pt; font-weight: 750; }}
QLabel#subtitle {{ color: {WHITE}; font-size: 17pt; font-weight: 700; background: transparent; }}
QLabel#pageTitle {{ color: {WHITE}; font-size: 20pt; font-weight: 750; }}
QLabel#sectionTitle {{ color: {LILAC}; font-size: 12pt; font-weight: 700; }}
QLabel#muted {{ color: {MUTED}; }}
QLabel#heroIcon {{ background: {PURPLE}; color: white; border-radius: 22px; font-size: 62pt; font-weight: 700; }}
QLineEdit {{ background: {BG}; border: 1px solid {INPUT_LINE}; border-radius: 6px; padding: 9px 10px; color: {WHITE}; selection-background-color: {PURPLE}; }}
QLineEdit:focus {{ border: 1px solid {LILAC}; }}
QPushButton {{ background: {PANEL}; color: {WHITE}; border: 1px solid {LINE}; border-radius: 7px; padding: 9px 13px; font-weight: 650; }}
QPushButton:hover {{ background: {PANEL_HOVER}; }}
QPushButton#primary {{ background: {PURPLE}; color: white; border: none; }}
QPushButton#primary:hover {{ background: {PURPLE_HOVER}; }}
QPushButton#green, QPushButton#orange, QPushButton#purple {{ background: {PURPLE}; color: white; border: none; }}
QPushButton#green:hover, QPushButton#orange:hover, QPushButton#purple:hover {{ background: {PURPLE_HOVER}; }}
QPushButton#danger {{ background: #8E3E69; color: white; border: none; }}
QTableWidget {{ background: {PANEL}; alternate-background-color: #252830; color: {WHITE}; gridline-color: {LINE}; border: 1px solid {LINE}; border-radius: 7px; selection-background-color: {PURPLE}; selection-color: white; }}
QHeaderView::section {{ background: #292C34; color: {LILAC}; border: none; border-bottom: 1px solid {LINE}; padding: 9px 7px; font-weight: 700; }}
QTableWidget::item {{ padding: 6px; }}
QDialog {{ background: {BG}; }}
QComboBox, QSpinBox {{ background: {PANEL}; color: {WHITE}; border: 1px solid {INPUT_LINE}; border-radius: 6px; padding: 8px; }}
QToolTip {{ background: {PANEL}; color: {WHITE}; border: 1px solid {LINE}; }}
"""

# Hoja de estilos del tema claro
LIGHT_STYLE = f"""
* {{ font-family: "Segoe UI"; font-size: 10pt; }}
QMainWindow, QWidget {{ background: #F5F3F9; color: #282333; }}
QLabel {{ background: transparent; }}
QMenuBar {{ background: #FFFFFF; color: #282333; border-bottom: 1px solid #DDD5E8; padding: 5px; }}
QMenuBar::item {{ padding: 7px 10px; border-radius: 5px; }}
QMenuBar::item:selected {{ background: {PURPLE}; color: white; }}
QMenu {{ background: #FFFFFF; color: #282333; border: 1px solid #DDD5E8; }}
QMenu::item:selected {{ background: {PURPLE}; color: white; }}
QFrame#panel {{ background: #FFFFFF; border: 1px solid #E1DAEA; border-radius: 10px; }}
QLabel#appTitle, QLabel#pageTitle {{ color: #282333; font-weight: 750; }}
QLabel#appTitle {{ font-size: 25pt; }}
QLabel#subtitle {{ color: #282333; font-size: 17pt; font-weight: 700; background: transparent; }}
QLabel#pageTitle {{ font-size: 20pt; }}
QLabel#sectionTitle {{ color: {PURPLE}; font-size: 12pt; font-weight: 700; }}
QLabel#muted {{ color: #746C80; }}
QLabel#heroIcon {{ background: {PURPLE}; color: white; border-radius: 22px; font-size: 62pt; font-weight: 700; }}
QLineEdit {{ background: #FFFFFF; border: 1px solid #D6CDDF; border-radius: 6px; padding: 9px 10px; color: #282333; selection-background-color: {PURPLE}; }}
QLineEdit:focus {{ border: 1px solid {LILAC}; }}
QPushButton {{ background: #F0ECF6; color: #342A43; border: 1px solid #DDD5E8; border-radius: 7px; padding: 9px 13px; font-weight: 650; }}
QPushButton:hover {{ background: #E7DFF1; }}
QPushButton#primary, QPushButton#green, QPushButton#orange, QPushButton#purple {{ background: {PURPLE}; color: white; border: none; }}
QPushButton#primary:hover, QPushButton#green:hover, QPushButton#orange:hover, QPushButton#purple:hover {{ background: {PURPLE_HOVER}; }}
QPushButton#danger {{ background: #8E3E69; color: white; border: none; }}
QTableWidget {{ background: #FFFFFF; alternate-background-color: #F7F4FA; color: #282333; gridline-color: #E1DAEA; border: 1px solid #E1DAEA; border-radius: 7px; selection-background-color: {PURPLE}; selection-color: white; }}
QHeaderView::section {{ background: #EEE8F5; color: {PURPLE}; border: none; border-bottom: 1px solid #DDD5E8; padding: 9px 7px; font-weight: 700; }}
QTableWidget::item {{ padding: 6px; }}
QDialog {{ background: #F5F3F9; }}
QComboBox, QSpinBox {{ background: #FFFFFF; color: #282333; border: 1px solid #D6CDDF; border-radius: 6px; padding: 8px; }}
QToolTip {{ background: #FFFFFF; color: #282333; border: 1px solid #DDD5E8; }}
"""

# STYLE se mantiene como alias del tema oscuro para compatibilidad con los diálogos.
STYLE = DARK_STYLE


# Función auxiliar para crear etiquetas con los estilos compartidos de la aplicación.
def label(text, object_name=None, muted=False):
    widget = QLabel(text)
    if object_name:
        widget.setObjectName(object_name)
    if muted:
        widget.setObjectName("muted")
    return widget


# Crea un panel reutilizable con bordes redondeados y el color definido por el tema.
def panel():
    frame = QFrame()
    frame.setObjectName("panel")
    return frame


# Crea botones uniformes y conecta su señal al método indicado, si se proporciona.
def button(text, color=None, callback=None):
    b = QPushButton(text)
    if color:
        b.setObjectName(color)
    if callback:
        b.clicked.connect(callback)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    return b


# Diálogo reutilizable para capturar o modificar los datos de un contacto.
class ContactDialog(QDialog):
    def __init__(self, title="Agregar contacto", contact=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(400)
        self.setStyleSheet(parent.styleSheet() if parent else DARK_STYLE)
        contact = contact or {}
        root = QVBoxLayout(self)
        root.setContentsMargins(22, 20, 22, 20)
        root.setSpacing(13)
        root.addWidget(label(title, "sectionTitle"))
        form = QFormLayout()
        form.setSpacing(11)
        self.fields = {}
        for key, caption in [
            ("id", "ID"), ("nombre", "Nombre"), ("telefono", "Teléfono"),
            ("correo", "Correo"), ("ciudad", "Ciudad")
        ]:
            field = QLineEdit(str(contact.get(key, "")))
            field.setPlaceholderText(f"Escribe {caption.lower()}")
            if key == "id" and contact:
                field.setReadOnly(True)
            self.fields[key] = field
            form.addRow(caption + ":", field)
        root.addLayout(form)
        buttons = QDialogButtonBox()
        save = buttons.addButton("Guardar", QDialogButtonBox.ButtonRole.AcceptRole)
        save.setObjectName("primary")
        cancel = buttons.addButton("Cancelar", QDialogButtonBox.ButtonRole.RejectRole)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        save.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)
        root.addWidget(buttons)

    # Devuelve los valores escritos en el formulario, sin espacios sobrantes.
    def values(self):
        return {k: field.text().strip() for k, field in self.fields.items()}


# Ventana principal: contiene el menú, las páginas y los datos temporales de ejemplo.
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agenda de Contactos")
        self.resize(1180, 760)
        self.setMinimumSize(980, 650)
        # Indica cuál tema está activo para poder alternarlo desde Herramientas.
        self.tema_claro = False
        # Contactos leídos de contactos.dat (estose llena en recargar_contactos).
        self.contactos = []
        self.crear_menu()
        self.crear_interfaz()
        self.setStyleSheet(DARK_STYLE)
        self.ir_a(0)
        # La verificación de integridad y del índice se haria al abrir la ventana.
        QTimer.singleShot(0, self.verificar_al_iniciar)

    # Construye una única barra superior para evitar opciones de navegación duplicadas.
    def crear_menu(self):
        barra = self.menuBar()
        menu_contactos = barra.addMenu("Contactos")
        menu_exportar = barra.addMenu("Exportar")
        menu_herramientas = barra.addMenu("Herramientas")
        menu_ayuda = barra.addMenu("Ayuda")
        menu_archivo = barra.addMenu("Archivo")

        def action(menu, texto, callback):
            item = QAction(texto, self)
            item.triggered.connect(callback)
            menu.addAction(item)

        action(menu_contactos, "Ver contactos", lambda: self.ir_a(1))
        action(menu_contactos, "Agregar contacto", self.agregar_contacto_dialogo)
        action(menu_contactos, "Buscar por ID", lambda: self.ir_a(1))
        action(menu_exportar, "Exportar a JSON", self.exportar_json_ui)
        action(menu_exportar, "Generar reporte PDF", self.exportar_pdf_ui)
        action(menu_herramientas, "Verificar integridad SHA-256", lambda: self.verificar_integridad_ui())
        action(menu_herramientas, "Crear respaldo ZIP", self.crear_respaldo_ui)
        action(menu_herramientas, "Información del archivo", self.info_archivo_ui)
        self.accion_tema = QAction("Cambiar a tema claro", self)
        self.accion_tema.triggered.connect(self.alternar_tema)
        menu_herramientas.addSeparator()
        menu_herramientas.addAction(self.accion_tema)
        action(menu_ayuda, "Acerca del proyecto", lambda: self.ir_a(4))
        action(menu_archivo, "Salir", self.close)

    # Crea el contenedor central y registra todas las páginas en un QStackedWidget.
    def crear_interfaz(self):
        central = QWidget()
        outer = QVBoxLayout(central)
        outer.setContentsMargins(12, 10, 12, 12)
        outer.setSpacing(0)

        # Una sola navegación: el menú superior de Qt. No duplicar categorías.
        self.stack = QStackedWidget()
        self.stack.addWidget(self.pagina_inicio())
        self.stack.addWidget(self.pagina_contactos())
        self.stack.addWidget(self.pagina_exportar())
        self.stack.addWidget(self.pagina_herramientas())
        self.stack.addWidget(self.pagina_ayuda())

        outer.addWidget(self.stack, 1)
        self.setCentralWidget(central)

    # Encabezado estándar reutilizado en las páginas secundarias.
    def encabezado(self, titulo, descripcion):
        box = QVBoxLayout()
        box.setSpacing(4)
        box.addWidget(label(titulo, "pageTitle"))
        box.addWidget(label(descripcion, muted=True))
        return box

    # Página inicial con una presentación y accesos directos a cada sección.
    def pagina_inicio(self):
        page = QWidget()
        root = QVBoxLayout(page)
        root.setContentsMargins(20, 20, 20, 18)
        root.setSpacing(18)
        hero = panel()
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(28, 22, 28, 22)
        hero_layout.setSpacing(25)
        icon = label("ID", "heroIcon")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setFixedSize(165, 150)
        hero_layout.addWidget(icon)
        copy = QVBoxLayout()
        copy.addStretch()
        copy.addWidget(label("Agenda de Contactos", "appTitle"))
        subtitle = label("con Acceso Aleatorio", "subtitle")
        copy.addWidget(subtitle)
        copy.addSpacing(8)
        copy.addWidget(label("Administra tus contactos de forma rápida y segura.", muted=True))
        copy.addSpacing(12)
        copy.addWidget(label("Acceso por ID   •   Índice JSON   •   Respaldo seguro", muted=True))
        copy.addStretch()
        hero_layout.addLayout(copy, 1)
        root.addWidget(hero, 2)

        cards = QGridLayout()
        cards.setSpacing(14)
        options = [
            ("01", "Contactos", "Agregar, buscar y\nmodificar", PURPLE, 1),
            ("02", "Exportar", "JSON y PDF", PURPLE_HOVER, 2),
            ("03", "Herramientas", "Integridad, respaldo\ne información", LILAC, 3),
            ("04", "Ayuda", "Información del\nproyecto", "#45404F", 4),
        ]
        for i, (symbol, title, desc, color, target) in enumerate(options):
            card = panel()
            box = QVBoxLayout(card)
            box.setContentsMargins(14, 14, 14, 14)
            box.setSpacing(7)
            icon_label = label(symbol)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Los identificadores numerados sustituyen los emojis por una señal visual sobria.
            icon_label.setStyleSheet(f"font-size:22pt;font-weight:700;color:white;background:{color};border-radius:10px;")
            icon_label.setFixedHeight(58)
            box.addWidget(icon_label)
            title_label = label(title, "sectionTitle")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            box.addWidget(title_label)
            desc_label = label(desc, muted=True)
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            box.addWidget(desc_label)
            box.addStretch()
            box.addWidget(button("Abrir sección", "primary" if target == 1 else None,
                                 lambda checked=False, idx=target: self.ir_a(idx)))
            cards.addWidget(card, 0, i)
        root.addLayout(cards, 2)
        return page

    # Página de contactos: formulario de alta y tabla para consultar/modificar.
    def pagina_contactos(self):
        page = QWidget()
        root = QVBoxLayout(page)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)
        root.addLayout(self.encabezado("Contactos", "Agrega, busca y modifica los datos de tu agenda."))
        columns = QHBoxLayout()
        columns.setSpacing(12)

        form_panel = panel()
        form_layout = QVBoxLayout(form_panel)
        form_layout.setContentsMargins(18, 18, 18, 18)
        form_layout.addWidget(label("Nuevo contacto", "sectionTitle"))
        self.contact_fields = {}
        form = QFormLayout()
        form.setSpacing(10)
        for key, caption in [("id", "ID"), ("nombre", "Nombre"), ("telefono", "Teléfono"),
                             ("correo", "Correo"), ("ciudad", "Ciudad")]:
            field = QLineEdit()
            field.setPlaceholderText(f"Ingresa {caption.lower()}")
            self.contact_fields[key] = field
            form.addRow(caption + ":", field)
        form_layout.addLayout(form)
        form_layout.addSpacing(6)
        form_layout.addWidget(button("Guardar contacto", "primary", self.guardar_contacto))
        form_layout.addWidget(button("Limpiar campos", None, self.limpiar_formulario))
        form_layout.addStretch()
        columns.addWidget(form_panel, 1)

        table_panel = panel()
        table_layout = QVBoxLayout(table_panel)
        table_layout.setContentsMargins(14, 14, 14, 14)
        table_layout.setSpacing(10)
        top = QHBoxLayout()
        top.addWidget(label("Contactos registrados", "sectionTitle"))
        top.addStretch()
        self.buscar_input = QLineEdit()
        self.buscar_input.setPlaceholderText("Buscar por ID...")
        self.buscar_input.setMaximumWidth(190)
        self.buscar_input.returnPressed.connect(self.buscar_contacto)
        top.addWidget(self.buscar_input)
        top.addWidget(button("Buscar", "primary", self.buscar_contacto))
        table_layout.addLayout(top)

        self.tabla = QTableWidget(0, 5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Teléfono", "Correo", "Ciudad"])
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_layout.addWidget(self.tabla, 1)
        bottom = QHBoxLayout()
        self.lbl_conteo = label("", muted=True)
        bottom.addWidget(self.lbl_conteo)
        bottom.addStretch()
        bottom.addWidget(button("Mostrar todos", None, self.mostrar_todos))
        bottom.addWidget(button("Modificar seleccionado", "purple", self.modificar_contacto))
        table_layout.addLayout(bottom)
        self.lbl_acceso = label("Acceso aleatorio: aún sin operaciones.", muted=True)
        table_layout.addWidget(self.lbl_acceso)
        columns.addWidget(table_panel, 2)
        root.addLayout(columns, 1)
        return page

    # datos
    # Lee contactos.dat y refresca la tabla.
    def recargar_contactos(self):
        try:
            self.contactos = manejo_archivos.leer_todos()
        except OSError as error:
            QMessageBox.critical(self, "Error de lectura", f"No se pudo leer contactos.dat:\n{error}")
            self.contactos = []
        self.actualizar_tabla()

    # Comprueba que indice.json coincida con contactos.dat; si no, lo reconstruye.
    def sincronizar_indice(self):
        esperado = {c["id"]: c["registro"] for c in self.contactos}
        try:
            if len(esperado) != len(self.contactos):
                raise ValueError("contactos.dat contiene IDs duplicados.")
            try:
                actual = indice.cargar_indice()
            except ValueError:
                actual = None
            if actual != esperado:
                indice.reconstruir_indice(self.contactos)
                QMessageBox.information(
                    self, "Índice reconstruido",
                    "indice.json no coincidía con contactos.dat y fue reconstruido.")
        except (ValueError, OSError) as error:
            QMessageBox.warning(self, "Problema con el índice", str(error))

    # Se ejecuta una vez al abrir la aplicación.
    def verificar_al_iniciar(self):
        self.recargar_contactos()
        if not manejo_archivos.tamano_valido():
            QMessageBox.warning(
                self, "Archivo de contactos dañado",
                "El tamaño de contactos.dat no es múltiplo de "
                f"{manejo_archivos.TAM_REGISTRO} bytes; el último registro está incompleto "
                "y se ignorará.")
        self.sincronizar_indice()
        self.verificar_integridad_ui(silencioso=True)

    # Actualiza la tabla, si se pasa una lista, muestra solo esos resultados.
    def actualizar_tabla(self, contactos=None):
        data = self.contactos if contactos is None else contactos
        self.tabla.setRowCount(0)
        for contacto in data:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            for col, key in enumerate(("id", "nombre", "telefono", "correo", "ciudad")):
                self.tabla.setItem(row, col, QTableWidgetItem(contacto[key]))
        if contactos is None:
            self.lbl_conteo.setText(f"{len(data)} contacto(s)")
        else:
            self.lbl_conteo.setText(f"{len(data)} de {len(self.contactos)} contacto(s)")

    # Muestra en pantalla el último uso de seek()/tell()
    def mostrar_acceso(self):
        texto = manejo_archivos.descripcion_acceso()
        if texto:
            self.lbl_acceso.setText("Acceso aleatorio → " + texto)

    # Quita el filtro de búsqueda y muestra todos los contactos
    def mostrar_todos(self):
        self.buscar_input.clear()
        self.actualizar_tabla()

    # Vacía todos los campos del formulario de alta.
    def limpiar_formulario(self):
        for field in self.contact_fields.values():
            field.clear()

    # Devuelve un mensaje de error si los datos no son válidos, o None si están bien.
    def validar_contacto(self, data):
        if not all(data.values()):
            return "Completa todos los campos."
        if not (data["id"].isascii() and data["id"].isdigit()):
            return "El ID debe ser un número entero."
        for clave, longitud in manejo_archivos.CAMPOS:
            if len(data[clave].encode("utf-8")) > longitud:
                return (f"El campo «{clave}» admite como máximo {longitud} caracteres "
                        "(las letras con acento ocupan más espacio).")
        return None

    # Guarda un contacto nuev, valida, escribe en .dat, actualiza índice y hash.
    def registrar_contacto(self, data):
        data = dict(data)
        error = self.validar_contacto(data)
        if error:
            QMessageBox.warning(self, "Datos inválidos", error)
            return False
        data["id"] = str(int(data["id"]))  # "007" y "7" son el mismo ID
        try:
            if indice.buscar_en_indice(data["id"]) is not None:
                QMessageBox.warning(self, "ID repetido", "Ya existe un contacto con ese ID.")
                return False
            num = manejo_archivos.agregar_contacto(
                data["id"], data["nombre"], data["telefono"], data["correo"], data["ciudad"])
            indice.agregar_al_indice(data["id"], num)
        except (OSError, ValueError) as error:
            QMessageBox.critical(self, "No se pudo guardar", str(error))
            self.recargar_contactos()
            return False
        ok, mensaje = seguridad.guardar_hash()
        if not ok:
            QMessageBox.warning(self, "Hash no actualizado", mensaje)
        self.recargar_contactos()
        self.mostrar_acceso()
        return True

    # Botón "Guardar contacto" del formulario.
    def guardar_contacto(self):
        data = {key: field.text().strip() for key, field in self.contact_fields.items()}
        if self.registrar_contacto(data):
            self.limpiar_formulario()
            QMessageBox.information(self, "Contacto agregado",
                                    "El contacto se guardó correctamente.\n\n"
                                    + manejo_archivos.descripcion_acceso())

    # Permite agregar un contacto desde la opción correspondiente del menú superior.
    def agregar_contacto_dialogo(self):
        dialog = ContactDialog("Agregar contacto", parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if self.registrar_contacto(dialog.values()):
                self.ir_a(1)

    # Búsqueda por ID usando el índice (indice.json) y acceso aleatorio al registro.
    def buscar_contacto(self):
        query = self.buscar_input.text().strip()
        if not query:
            self.actualizar_tabla()
            return
        if query.isascii() and query.isdigit():
            query = str(int(query))
        contacto = None
        try:
            numero = indice.buscar_en_indice(query)
            if numero is not None:
                contacto = manejo_archivos.leer_contacto(numero)
        except (OSError, ValueError) as error:
            QMessageBox.critical(self, "Error en la búsqueda", str(error))
            return
        if contacto is not None and contacto["id"] != query:
            contacto = None  # el índice no coincide con el archivo
        self.actualizar_tabla([contacto] if contacto else [])
        if contacto is not None:
            self.mostrar_acceso()
        if contacto is None:
            QMessageBox.information(self, "Sin resultados",
                                    f"No se encontró un contacto con ID {query}.")

    # Abre el diálogo con los datos seleccionados y modifica el registro en su lugar.
    def modificar_contacto(self):
        row = self.tabla.currentRow()
        if row < 0:
            QMessageBox.information(self, "Selecciona un contacto", "Selecciona una fila de la tabla.")
            return
        cid = self.tabla.item(row, 0).text()
        try:
            numero = indice.buscar_en_indice(cid)
            contacto = manejo_archivos.leer_contacto(numero)
        except (OSError, ValueError) as error:
            QMessageBox.critical(self, "Error de lectura", str(error))
            return
        if not contacto:
            QMessageBox.warning(self, "No encontrado", "El contacto ya no existe en el archivo.")
            self.recargar_contactos()
            return
        dialog = ContactDialog("Modificar contacto", contacto, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.values()
            values["id"] = contacto["id"]  # el ID no se puede cambiar
            error = self.validar_contacto(values)
            if error:
                QMessageBox.warning(self, "Datos inválidos", error)
                return
            try:
                manejo_archivos.modificar_contacto_en_lugar(
                    numero, values["id"], values["nombre"], values["telefono"],
                    values["correo"], values["ciudad"])
            except (OSError, IndexError) as error:
                QMessageBox.critical(self, "No se pudo modificar", str(error))
                return
            ok, mensaje = seguridad.guardar_hash()
            if not ok:
                QMessageBox.warning(self, "Hash no actualizado", mensaje)
            self.mostrar_todos()
            self.recargar_contactos()
            self.mostrar_acceso()
            QMessageBox.information(self, "Contacto modificado",
                                    "Solo se sobrescribió ese registro.\n\n"
                                    + manejo_archivos.descripcion_acceso())

    # Página de exportación: JSON y PDF generados con el módulo exportacion.
    def pagina_exportar(self):
        page = QWidget()
        root = QVBoxLayout(page)
        root.setContentsMargins(20, 22, 20, 20)
        root.setSpacing(18)
        root.addLayout(self.encabezado("Exportar contactos", "Guarda y comparte la información de tu agenda."))
        cards = QHBoxLayout()
        cards.setSpacing(16)
        for symbol, title, desc, color, action in [
            ("JSON", "Exportar a JSON", "Guarda todos los contactos en un archivo JSON.", PURPLE, "Exportar a JSON"),
            ("PDF", "Generar reporte PDF", "Crea un reporte PDF con los contactos y la fecha de generación.", PURPLE_HOVER, "Generar reporte PDF"),
        ]:
            card = panel()
            box = QVBoxLayout(card)
            box.setContentsMargins(22, 22, 22, 22)
            icon = label(symbol)
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon.setFixedSize(64, 64)
            # JSON y PDF se muestran como etiquetas breves, legibles en ambos temas.
            icon.setStyleSheet(f"background:{color};color:white;font-size:13pt;font-weight:700;border-radius:12px;")
            box.addWidget(icon)
            box.addWidget(label(title, "sectionTitle"))
            detail = label(desc, muted=True)
            detail.setWordWrap(True)
            box.addWidget(detail)
            box.addStretch()
            callback = self.exportar_json_ui if "JSON" in action else self.exportar_pdf_ui
            box.addWidget(button("Exportar" if "JSON" in action else "Generar PDF",
                                 "green" if color == GREEN else "danger", callback))
            cards.addWidget(card)
        root.addLayout(cards)
        preview = panel()
        pv = QVBoxLayout(preview)
        pv.addWidget(label("Vista previa", "sectionTitle"))
        pv.addWidget(label("• contactos_exportados.json", muted=True))
        pv.addWidget(label("• reporte_contactos.pdf", muted=True))
        pv.addWidget(label("Los archivos se guardan en la misma carpeta que la aplicación.", muted=True))
        root.addWidget(preview)
        root.addStretch()
        return page

    # Herramientas de integridad (SHA-256), respaldo ZIP y metadatos.
    def pagina_herramientas(self):
        page = QWidget()
        root = QVBoxLayout(page)
        root.setContentsMargins(20, 22, 20, 20)
        root.setSpacing(18)
        root.addLayout(self.encabezado("Herramientas", "Integridad, copias de seguridad e información del archivo."))
        grid = QGridLayout()
        grid.setSpacing(14)
        items = [
            ("SHA", "Verificar integridad", "Calcula y compara el hash SHA-256 del archivo de contactos.", PURPLE, "Verificar integridad", lambda: self.verificar_integridad_ui()),
            ("ZIP", "Crear respaldo ZIP", "Comprime el archivo de contactos y el índice.", PURPLE, "Crear respaldo ZIP", self.crear_respaldo_ui),
            ("INFO", "Información del archivo", "Muestra tamaño, fecha de modificación y permisos.", LILAC, "Información del archivo", self.info_archivo_ui),
            ("META", "Ver metadatos", "Consulta detalles técnicos de los archivos.", "#45404F", "Ver metadatos", self.metadatos_ui),
        ]
        for i, (symbol, title, desc, color, action, callback) in enumerate(items):
            card = panel()
            row = QHBoxLayout(card)
            row.setContentsMargins(16, 16, 16, 16)
            icon = label(symbol)
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon.setFixedSize(58, 58)
            # Siglas cortas identifican cada herramienta sin depender de emojis del sistema.
            icon.setStyleSheet(f"background:{color};color:white;border-radius:12px;font-size:10pt;font-weight:700;")
            row.addWidget(icon)
            body = QVBoxLayout()
            body.addWidget(label(title, "sectionTitle"))
            detail = label(desc, muted=True)
            detail.setWordWrap(True)
            body.addWidget(detail)
            body.addStretch()
            body.addWidget(button(action, "primary", callback))
            row.addLayout(body, 1)
            grid.addWidget(card, i // 2, i % 2)
        root.addLayout(grid)
        root.addStretch()
        return page

    # Resume el objetivo del proyecto y las funciones que debe incluir el laboratorio.
    def pagina_ayuda(self):
        page = QWidget()
        root = QVBoxLayout(page)
        root.setContentsMargins(20, 22, 20, 20)
        root.setSpacing(16)
        root.addLayout(self.encabezado("Ayuda", "Información general de la aplicación."))
        card = panel()
        box = QVBoxLayout(card)
        box.setContentsMargins(24, 24, 24, 24)
        box.setSpacing(12)
        box.addWidget(label("Agenda de Contactos con Acceso Aleatorio", "sectionTitle"))
        box.addWidget(label("Aplicación de escritorio para administrar contactos usando registros de tamaño fijo y acceso aleatorio.", muted=True))
        box.addWidget(label("Funciones del laboratorio", "sectionTitle"))
        for line in [
            "• Agregar, buscar por ID y modificar contactos.",
            "• Mantener un índice primario en indice.json.",
            "• Usar seek() y tell() para acceder a los registros.",
            "• Exportar a JSON y generar un reporte PDF.",
            "• Verificar integridad con SHA-256 y crear respaldos ZIP.",
            "• Consultar metadatos y permisos de los archivos.",
        ]:
            box.addWidget(label(line))
        box.addStretch()
        root.addWidget(card)
        root.addStretch()
        return page

    # Cambia entre la hoja de estilos oscura y la clara sin reiniciar la aplicación.
    def alternar_tema(self):
        """Alterna entre el tema oscuro morado y el tema claro."""
        self.tema_claro = not self.tema_claro
        self.setStyleSheet(LIGHT_STYLE if self.tema_claro else DARK_STYLE)
        self.accion_tema.setText(
            "Cambiar a tema oscuro" if self.tema_claro else "Cambiar a tema claro"
        )

    # ------------------------------------------------------------ exportación
    # Contactos sin el campo interno "registro", tal como se exportan.
    def contactos_para_exportar(self):
        claves = ("id", "nombre", "telefono", "correo", "ciudad")
        return [{k: c[k] for k in claves} for c in self.contactos]

    def exportar_json_ui(self):
        if not self.contactos:
            QMessageBox.information(self, "Sin contactos", "No hay contactos para exportar.")
            return
        try:
            ruta = exportacion.exportar_json(self.contactos_para_exportar())
        except OSError as error:
            QMessageBox.critical(self, "Error al exportar", str(error))
            return
        QMessageBox.information(self, "Exportación exitosa", f"JSON guardado en:\n{ruta}")

    # El PDF se genera a partir del JSON, así que primero se actualiza el JSON.
    def exportar_pdf_ui(self):
        if not self.contactos:
            QMessageBox.information(self, "Sin contactos", "No hay contactos para exportar.")
            return
        try:
            ruta_json, ruta_pdf = exportacion.exportar_json_y_pdf(self.contactos_para_exportar())
        except Exception as error:  # la app no debe caerse por un fallo del PDF
            QMessageBox.critical(self, "Error al generar el PDF", str(error))
            return
        QMessageBox.information(self, "Reporte generado",
                                f"JSON: {ruta_json}\nPDF: {ruta_pdf}")

    # ------------------------------------------------------------- seguridad
    # Compara el hash SHA-256 de contactos.dat con el guardado.
    # silencioso=True (al iniciar): solo avisa si hay algo anormal.
    def verificar_integridad_ui(self, silencioso=False):
        estado, mensaje = seguridad.verificar_integridad()
        if estado == "ok":
            if not silencioso:
                QMessageBox.information(self, "Integridad verificada", mensaje)
        elif estado == "sin_datos":
            if not silencioso:
                QMessageBox.information(self, "Integridad", mensaje)
        elif estado == "sin_hash":
            ok, resultado = seguridad.guardar_hash()
            if not silencioso or not ok:
                QMessageBox.information(self, "Integridad",
                                        f"{mensaje}\n{resultado}" if ok else resultado)
        elif estado == "alterado":
            respuesta = QMessageBox.question(
                self, "Archivo alterado",
                mensaje + "\n\n¿Aceptar el estado actual y regenerar el hash?")
            if respuesta == QMessageBox.StandardButton.Yes:
                ok, resultado = seguridad.guardar_hash()
                QMessageBox.information(self, "Integridad", resultado)
        else:
            QMessageBox.warning(self, "Error de integridad", mensaje)

    def crear_respaldo_ui(self):
        ok, datos = seguridad.crear_respaldo()
        if not ok:
            QMessageBox.warning(self, "Respaldo", datos)
            return
        texto = (f"Respaldo creado:\n{os.path.abspath(datos['ruta_zip'])}\n\n"
                 f"Tamaño original: {datos['original']} bytes\n"
                 f"Tamaño comprimido: {datos['comprimido']} bytes\n"
                 f"Ahorro: {datos['ahorro_pct']} %")
        if datos["omitidos"]:
            texto += "\n\nNo se incluyeron (no existen): " + ", ".join(datos["omitidos"])
        QMessageBox.information(self, "Respaldo creado", texto)

    # Texto con tamaño, fecha y permisos de un archivo.
    def _descripcion_archivo(self, ruta):
        ok, datos = seguridad.info_archivo(ruta)
        if not ok:
            return f"{ruta}\n  {datos}"
        permisos = ("lectura " if datos["lectura"] else "") + ("escritura" if datos["escritura"] else "")
        return (f"{datos['ruta']}\n  Tamaño: {datos['tamano_bytes']} bytes\n"
                f"  Modificado: {datos['modificado']}\n"
                f"  Permisos: {permisos.strip() or 'ninguno'}")

    def info_archivo_ui(self):
        QMessageBox.information(self, "Información del archivo",
                                self._descripcion_archivo(seguridad.ARCHIVO_DATOS))

    def metadatos_ui(self):
        texto = "\n\n".join(self._descripcion_archivo(r) for r in (
            seguridad.ARCHIVO_DATOS, seguridad.ARCHIVO_INDICE, seguridad.ARCHIVO_HASH))
        texto += f"\n\nRegistros en contactos.dat: {manejo_archivos.total_registros()}"
        QMessageBox.information(self, "Metadatos de los archivos", texto)

    # Cambia la página visible dentro del QStackedWidget.
    def ir_a(self, index):
        # La navegación se realiza desde el menú superior y las tarjetas de inicio.
        self.stack.setCurrentIndex(index)


def main():
    # Los archivos de datos viven junto al programa, sin importar desde dónde se ejecute.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(DARK_STYLE)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
