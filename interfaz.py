"""
Agenda de Contactos con Acceso Aleatorio
Interfaz adaptada del proyecto anterior. Solo interfaz y datos de demostración.
Requiere: pip install PyQt6
Ejecución: python interfaz_agenda.py
"""

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QLabel, QPushButton,
    QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFormLayout,
    QDialog, QDialogButtonBox, QMenu
)

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

STYLE = f"""
* {{ font-family: "Segoe UI"; font-size: 10pt; }}
QMainWindow, QWidget {{ background: {BG}; color: {INK}; }}
QMenuBar {{ background: {PANEL}; color: {WHITE}; border-bottom: 1px solid {LINE}; padding: 5px; }}
QMenuBar::item {{ padding: 7px 10px; border-radius: 5px; }}
QMenuBar::item:selected {{ background: {PURPLE}; color: white; }}
QMenu {{ background: {PANEL}; color: {WHITE}; border: 1px solid {LINE}; }}
QMenu::item:selected {{ background: {PURPLE}; color: white; }}
QFrame#panel {{ background: {PANEL}; border: 1px solid {LINE}; border-radius: 10px; }}
QLabel#appTitle {{ color: {WHITE}; font-size: 25pt; font-weight: 750; }}
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


def label(text, object_name=None, muted=False):
    widget = QLabel(text)
    if object_name:
        widget.setObjectName(object_name)
    if muted:
        widget.setObjectName("muted")
    return widget


def panel():
    frame = QFrame()
    frame.setObjectName("panel")
    return frame


def button(text, color=None, callback=None):
    b = QPushButton(text)
    if color:
        b.setObjectName(color)
    if callback:
        b.clicked.connect(callback)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    return b


class ContactDialog(QDialog):
    def __init__(self, title="Agregar contacto", contact=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(400)
        self.setStyleSheet(STYLE)
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

    def values(self):
        return {k: field.text().strip() for k, field in self.fields.items()}


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agenda de Contactos")
        self.resize(1180, 760)
        self.setMinimumSize(980, 650)
        self.contactos = [
            {"id": "1", "nombre": "Juan Pérez", "telefono": "5555-1111", "correo": "juan@correo.com", "ciudad": "Quetzaltenango"},
            {"id": "2", "nombre": "María Gómez", "telefono": "5555-2222", "correo": "maria@correo.com", "ciudad": "Guatemala"},
            {"id": "3", "nombre": "Carlos Ruiz", "telefono": "5555-3333", "correo": "carlos@correo.com", "ciudad": "Cobán"},
            {"id": "4", "nombre": "Lucía Torres", "telefono": "5555-4444", "correo": "lucia@correo.com", "ciudad": "Antigua"},
        ]
        self.crear_menu()
        self.crear_interfaz()
        self.setStyleSheet(STYLE)
        self.ir_a(0)

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
        action(menu_exportar, "Exportar a JSON", lambda: self.demo("Exportar a JSON"))
        action(menu_exportar, "Generar reporte PDF", lambda: self.demo("Generar reporte PDF"))
        action(menu_herramientas, "Verificar integridad SHA-256", lambda: self.demo("Verificar integridad SHA-256"))
        action(menu_herramientas, "Crear respaldo ZIP", lambda: self.demo("Crear respaldo ZIP"))
        action(menu_herramientas, "Información del archivo", lambda: self.demo("Información del archivo"))
        action(menu_ayuda, "Acerca del proyecto", lambda: self.ir_a(4))
        action(menu_archivo, "Salir", self.close)

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

    def encabezado(self, titulo, descripcion):
        box = QVBoxLayout()
        box.setSpacing(4)
        box.addWidget(label(titulo, "pageTitle"))
        box.addWidget(label(descripcion, muted=True))
        return box

    def pagina_inicio(self):
        page = QWidget()
        root = QVBoxLayout(page)
        root.setContentsMargins(20, 20, 20, 18)
        root.setSpacing(18)
        hero = panel()
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(28, 22, 28, 22)
        hero_layout.setSpacing(25)
        icon = label("♟", "heroIcon")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setFixedSize(165, 150)
        hero_layout.addWidget(icon)
        copy = QVBoxLayout()
        copy.addStretch()
        copy.addWidget(label("Agenda de Contactos", "appTitle"))
        subtitle = label("con Acceso Aleatorio")
        subtitle.setStyleSheet(f"font-size:17pt;font-weight:700;color:{NAVY};")
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
            ("♙", "Contactos", "Agregar, buscar y\nmodificar", PURPLE, 1),
            ("⇧", "Exportar", "JSON y PDF", PURPLE_HOVER, 2),
            ("⚒", "Herramientas", "Integridad, respaldo\ne información", LILAC, 3),
            ("?", "Ayuda", "Información del\nproyecto", "#45404F", 4),
        ]
        for i, (symbol, title, desc, color, target) in enumerate(options):
            card = panel()
            box = QVBoxLayout(card)
            box.setContentsMargins(14, 14, 14, 14)
            box.setSpacing(7)
            icon_label = label(symbol)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet(f"font-size:28pt;color:white;background:{color};border-radius:10px;")
            icon_label.setFixedHeight(58)
            box.addWidget(icon_label)
            title_label = label(title, "sectionTitle")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            box.addWidget(title_label)
            desc_label = label(desc, muted=True)
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            box.addWidget(desc_label)
            box.addStretch()
            box.addWidget(button("Abrir sección  →", "primary" if target == 1 else None,
                                 lambda checked=False, idx=target: self.ir_a(idx)))
            cards.addWidget(card, 0, i)
        root.addLayout(cards, 2)
        return page

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
        form_layout.addWidget(label("♙  Agregar contacto", "sectionTitle"))
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
        form_layout.addWidget(button("▣  Guardar contacto", "primary", self.guardar_contacto))
        form_layout.addWidget(button("↻  Limpiar campos", None, self.limpiar_formulario))
        form_layout.addStretch()
        columns.addWidget(form_panel, 1)

        table_panel = panel()
        table_layout = QVBoxLayout(table_panel)
        table_layout.setContentsMargins(14, 14, 14, 14)
        table_layout.setSpacing(10)
        top = QHBoxLayout()
        top.addWidget(label("♣  Contactos registrados", "sectionTitle"))
        top.addStretch()
        self.buscar_input = QLineEdit()
        self.buscar_input.setPlaceholderText("Buscar por ID...")
        self.buscar_input.setMaximumWidth(190)
        self.buscar_input.returnPressed.connect(self.buscar_contacto)
        top.addWidget(self.buscar_input)
        top.addWidget(button("⌕", "primary", self.buscar_contacto))
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
        bottom.addWidget(button("Mostrar todos", None, self.actualizar_tabla))
        bottom.addWidget(button("✎  Modificar seleccionado", "purple", self.modificar_contacto))
        table_layout.addLayout(bottom)
        columns.addWidget(table_panel, 2)
        root.addLayout(columns, 1)
        self.actualizar_tabla()
        return page

    def actualizar_tabla(self, contactos=None):
        data = self.contactos if contactos is None else contactos
        self.tabla.setRowCount(0)
        for contacto in data:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            for col, key in enumerate(("id", "nombre", "telefono", "correo", "ciudad")):
                self.tabla.setItem(row, col, QTableWidgetItem(contacto[key]))
        self.lbl_conteo.setText(f"{len(data)} contacto(s) · datos de demostración")

    def limpiar_formulario(self):
        for field in self.contact_fields.values():
            field.clear()

    def guardar_contacto(self):
        data = {key: field.text().strip() for key, field in self.contact_fields.items()}
        if not all(data.values()):
            QMessageBox.warning(self, "Campos incompletos", "Completa todos los campos.")
            return
        if not data["id"].isdigit():
            QMessageBox.warning(self, "ID inválido", "El ID debe ser un número entero.")
            return
        if any(c["id"] == data["id"] for c in self.contactos):
            QMessageBox.warning(self, "ID repetido", "Ya existe un contacto con ese ID.")
            return
        self.contactos.append(data)
        self.actualizar_tabla()
        self.limpiar_formulario()
        QMessageBox.information(self, "Contacto agregado",
                                "Se agregó a la lista temporal. Aún no se guarda en archivos.")

    def agregar_contacto_dialogo(self):
        dialog = ContactDialog("Agregar contacto", parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.values()
            if not all(data.values()) or not data["id"].isdigit():
                QMessageBox.warning(self, "Datos inválidos", "Completa los campos y utiliza un ID numérico.")
                return
            if any(c["id"] == data["id"] for c in self.contactos):
                QMessageBox.warning(self, "ID repetido", "Ya existe un contacto con ese ID.")
                return
            self.contactos.append(data)
            self.actualizar_tabla()
            self.ir_a(1)

    def buscar_contacto(self):
        query = self.buscar_input.text().strip()
        if not query:
            self.actualizar_tabla()
            return
        resultados = [c for c in self.contactos if c["id"] == query]
        self.actualizar_tabla(resultados)
        if not resultados:
            QMessageBox.information(self, "Sin resultados",
                                    f"No se encontró un contacto con ID {query} en los datos de ejemplo.")

    def modificar_contacto(self):
        row = self.tabla.currentRow()
        if row < 0:
            QMessageBox.information(self, "Selecciona un contacto", "Selecciona una fila de la tabla.")
            return
        cid = self.tabla.item(row, 0).text()
        contacto = next((c for c in self.contactos if c["id"] == cid), None)
        if not contacto:
            return
        dialog = ContactDialog("Modificar contacto", contacto, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.values()
            if not all(values.values()):
                QMessageBox.warning(self, "Campos incompletos", "Completa todos los campos.")
                return
            contacto.update({k: v for k, v in values.items() if k != "id"})
            self.actualizar_tabla()

    def pagina_exportar(self):
        page = QWidget()
        root = QVBoxLayout(page)
        root.setContentsMargins(20, 22, 20, 20)
        root.setSpacing(18)
        root.addLayout(self.encabezado("Exportar contactos", "Guarda y comparte la información de tu agenda."))
        cards = QHBoxLayout()
        cards.setSpacing(16)
        for symbol, title, desc, color, action in [
            ("▧", "Exportar a JSON", "Guarda todos los contactos en un archivo JSON.", PURPLE, "Exportar a JSON"),
            ("▤", "Generar reporte PDF", "Crea un reporte PDF con los contactos y la fecha de generación.", PURPLE_HOVER, "Generar reporte PDF"),
        ]:
            card = panel()
            box = QVBoxLayout(card)
            box.setContentsMargins(22, 22, 22, 22)
            icon = label(symbol)
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon.setFixedSize(64, 64)
            icon.setStyleSheet(f"background:{color};color:white;font-size:28pt;border-radius:12px;")
            box.addWidget(icon)
            box.addWidget(label(title, "sectionTitle"))
            detail = label(desc, muted=True)
            detail.setWordWrap(True)
            box.addWidget(detail)
            box.addStretch()
            box.addWidget(button("Exportar" if "JSON" in action else "Generar PDF",
                                 "green" if color == GREEN else "danger",
                                 lambda checked=False, a=action: self.demo(a)))
            cards.addWidget(card)
        root.addLayout(cards)
        preview = panel()
        pv = QVBoxLayout(preview)
        pv.addWidget(label("Vista previa", "sectionTitle"))
        pv.addWidget(label("• contactos_exportados.json", muted=True))
        pv.addWidget(label("• reporte_contactos.pdf", muted=True))
        pv.addWidget(label("Los archivos se generarán al conectar la lógica del laboratorio.", muted=True))
        root.addWidget(preview)
        root.addStretch()
        return page

    def pagina_herramientas(self):
        page = QWidget()
        root = QVBoxLayout(page)
        root.setContentsMargins(20, 22, 20, 20)
        root.setSpacing(18)
        root.addLayout(self.encabezado("Herramientas", "Integridad, copias de seguridad e información del archivo."))
        grid = QGridLayout()
        grid.setSpacing(14)
        items = [
            ("⬡", "Verificar integridad", "Calcula y compara el hash SHA-256 del archivo de contactos.", PURPLE, "Verificar integridad"),
            ("▤", "Crear respaldo ZIP", "Comprime el archivo de contactos y el índice.", PURPLE, "Crear respaldo ZIP"),
            ("ⓘ", "Información del archivo", "Muestra tamaño, fecha de modificación y permisos.", LILAC, "Información del archivo"),
            ("▣", "Ver metadatos", "Consulta detalles técnicos de los archivos.", "#45404F", "Ver metadatos"),
        ]
        for i, (symbol, title, desc, color, action) in enumerate(items):
            card = panel()
            row = QHBoxLayout(card)
            row.setContentsMargins(16, 16, 16, 16)
            icon = label(symbol)
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon.setFixedSize(58, 58)
            icon.setStyleSheet(f"background:{color};color:white;border-radius:12px;font-size:24pt;")
            row.addWidget(icon)
            body = QVBoxLayout()
            body.addWidget(label(title, "sectionTitle"))
            detail = label(desc, muted=True)
            detail.setWordWrap(True)
            body.addWidget(detail)
            body.addStretch()
            body.addWidget(button(action, "primary", lambda checked=False, a=action: self.demo(a)))
            row.addLayout(body, 1)
            grid.addWidget(card, i // 2, i % 2)
        root.addLayout(grid)
        root.addStretch()
        return page

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

    def demo(self, accion):
        QMessageBox.information(
            self, accion,
            f"«{accion}» ya tiene su botón en la interfaz.\n\n"
            "La operación real se conectará después con el manejo de archivos."
        )

    def ir_a(self, index):
        # La navegación se realiza desde el menú superior y las tarjetas de inicio.
        self.stack.setCurrentIndex(index)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(STYLE)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
