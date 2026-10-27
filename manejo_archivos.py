# Lógica de acceso aleatorio, seek(), tell() y UTF-8
import os

ARCHIVO_DAT = "contactos.dat"
TAM_REGISTRO = 100  # Tamaño fijo en bytes

# Definición de longitudes de campos (Suman exactamente 100 caracteres) :]
L_ID = 5
L_NOMBRE = 30
L_TEL = 15
L_CORREO = 30
L_CIUDAD = 20

# Último acceso con seek()/tell(); esto depsues lo mostrara la interfaz :].
ultimo_acceso = {}


def _registrar_acceso(operacion, num_registro, posicion):
    ultimo_acceso.clear()
    ultimo_acceso.update(operacion=operacion, registro=num_registro, posicion=posicion)


def descripcion_acceso():
    """Texto legible del último acceso (vacío si aún no hubo ninguno)."""
    if not ultimo_acceso:
        return ""
    return (f"{ultimo_acceso['operacion']}: registro #{ultimo_acceso['registro']} · "
            f"tell() = {ultimo_acceso['posicion']} (seek({ultimo_acceso['registro']} × {TAM_REGISTRO}))")


CAMPOS = (
    ("id", L_ID),
    ("nombre", L_NOMBRE),
    ("telefono", L_TEL),
    ("correo", L_CORREO),
    ("ciudad", L_CIUDAD),
)


def _campo(valor, longitud):
    """Codifica en UTF-8, recorta a -longitud- bytes sin partir un carácter y rellena con espacios."""
    datos = str(valor).encode("utf-8")[:longitud]
    datos = datos.decode("utf-8", errors="ignore").encode("utf-8")
    return datos.ljust(longitud, b" ")


def empaquetar_registro(id_val, nombre, telefono, correo, ciudad):
    """Aqui se rellenacada campo con espacios para asegurar el tamaño fijo."""
    registro = b"".join(
        _campo(valor, longitud)
        for valor, (_, longitud) in zip((id_val, nombre, telefono, correo, ciudad), CAMPOS)
    )
    if len(registro) != TAM_REGISTRO:
        raise ValueError(f"El registro debe medir {TAM_REGISTRO} bytes.")
    return registro


def desempaquetar_registro(datos, num_registro):
    #Convierte 100 bytes en un diccionario de contacto (con su número de registro).
    contacto = {}
    pos = 0
    for clave, longitud in CAMPOS:
        contacto[clave] = datos[pos:pos + longitud].decode("utf-8", errors="replace").strip()
        pos += longitud
    contacto["registro"] = num_registro
    return contacto


def agregar_contacto(id_val, nombre, telefono, correo, ciudad):
    """Agrega un contacto al final del archivo""" #aqui se usa telle y seek
    registro = empaquetar_registro(id_val, nombre, telefono, correo, ciudad)

    with open(ARCHIVO_DAT, "ab") as f:  # "ab" crea el archivo si no existe
        f.seek(0, os.SEEK_END)
        pos_actual = f.tell()  # Muestra la posición actual en bytes/caracteres
        f.write(registro)
    num_registro = pos_actual // TAM_REGISTRO
    _registrar_acceso("Agregar (al final)", num_registro, pos_actual)
    print(f"[DEBUG] Contacto guardado en tell(): {pos_actual} (Registro #{num_registro})")
    return num_registro


def tamano_valido():
    #True si el archivo no existe o su tamaño es múltiplo exacto del registro.
    if not os.path.exists(ARCHIVO_DAT):
        return True
    return os.path.getsize(ARCHIVO_DAT) % TAM_REGISTRO == 0


def total_registros():
    #Cantidad de registros completos que contiene el archivo.
    if not os.path.exists(ARCHIVO_DAT):
        return 0
    return os.path.getsize(ARCHIVO_DAT) // TAM_REGISTRO


def leer_contacto(num_registro):
    #Lee un registro por acceso aleatorio. Devuelve dict o None si no existe.
    if num_registro is None or num_registro < 0 or not os.path.exists(ARCHIVO_DAT):
        return None
    with open(ARCHIVO_DAT, "rb") as f:
        f.seek(num_registro * TAM_REGISTRO, os.SEEK_SET)
        posicion = f.tell()
        datos = f.read(TAM_REGISTRO)
    if len(datos) != TAM_REGISTRO:
        return None
    _registrar_acceso("Lectura por seek()", num_registro, posicion)
    print(f"[DEBUG] Lectura directa con seek(): tell() = {posicion} (Registro #{num_registro})")
    return desempaquetar_registro(datos, num_registro)


def leer_todos():
    #Lee todos los registros en orden. Devuelve una lista de dicts.
    contactos = []
    if not os.path.exists(ARCHIVO_DAT):
        return contactos
    with open(ARCHIVO_DAT, "rb") as f:
        num = 0
        while True:
            datos = f.read(TAM_REGISTRO)
            if len(datos) != TAM_REGISTRO:
                break
            contactos.append(desempaquetar_registro(datos, num))
            num += 1
    return contactos


def modificar_contacto_en_lugar(num_registro, id_val, nombre, telefono, correo, ciudad):
    #Modifica un registro existente en su posición exacta sin reescribir todo el archivo.
    if not os.path.exists(ARCHIVO_DAT):
        raise FileNotFoundError("El archivo de contactos no existe.")
    if num_registro < 0 or num_registro >= total_registros():
        raise IndexError("El registro a modificar no existe.")

    registro = empaquetar_registro(id_val, nombre, telefono, correo, ciudad)
    posicion = num_registro * TAM_REGISTRO

    with open(ARCHIVO_DAT, "r+b") as f:
        f.seek(posicion, os.SEEK_SET)
        posicion = f.tell()
        print(f"[DEBUG] Posicionándonos para modificar en tell(): {posicion}")
        f.write(registro)
    _registrar_acceso("Modificación en el lugar", num_registro, posicion)
