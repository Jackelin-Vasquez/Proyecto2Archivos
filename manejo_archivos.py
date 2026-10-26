# Lógica de acceso aleatorio, seek(), tell() y UTF-8
import os

ARCHIVO_DAT = "contactos.dat"
TAM_REGISTRO = 100  # Tamaño fijo en caracteres

# Definición de longitudes de campos (Suman exactamente 100 caracteres) :]
L_ID = 5
L_NOMBRE = 30
L_TEL = 15
L_CORREO = 30
L_CIUDAD = 20


def empaquetar_registro(id_val, nombre, telefono, correo, ciudad):
    """Aqui se rellenacada campo con espacios para asegurar el tamaño fijo."""
    s_id = str(id_val).ljust(L_ID)[:L_ID]
    s_nombre = str(nombre).ljust(L_NOMBRE)[:L_NOMBRE]
    s_tel = str(telefono).ljust(L_TEL)[:L_TEL]
    s_correo = str(correo).ljust(L_CORREO)[:L_CORREO]
    s_ciudad = str(ciudad).ljust(L_CIUDAD)[:L_CIUDAD]

    registro = s_id + s_nombre + s_tel + s_correo + s_ciudad
    if len(registro) != TAM_REGISTRO:
        raise ValueError(f"El registro debe medir {TAM_REGISTRO} caracteres.")
    return registro


def agregar_contacto(id_val, nombre, telefono, correo, ciudad):
    """Agrega un contacto al final del archivo""" #aqui se usa telle y seek
    registro = empaquetar_registro(id_val, nombre, telefono, correo, ciudad)

    # Si no existe el archivo, se crea. Usamos UTF-8.
    modo = "a+" if os.path.exists(ARCHIVO_DAT) else "w+"
    with open(ARCHIVO_DAT, modo, encoding="utf-8") as f:
        f.seek(0, os.SEEK_END)
        pos_actual = f.tell()  # Muestra la posición actual en bytes/caracteres
        f.write(registro)
        num_registro = pos_actual // TAM_REGISTRO
        print(f"[DEBUG] Contacto guardado en tell(): {pos_actual} (Registro #{num_registro})")
        return num_registro


def modificar_contacto_en_lugar(num_registro, id_val, nombre, telefono, correo, ciudad):
    #Modifica un registro existente en su posición exacta sin reescribir todo el archivo.
    if not os.path.exists(ARCHIVO_DAT):
        raise FileNotFoundError("El archivo de contactos no existe.")

    registro = empaquetar_registro(id_val, nombre, telefono, correo, ciudad)
    posicion = num_registro * TAM_REGISTRO

    with open(ARCHIVO_DAT, "r+", encoding="utf-8") as f:
        f.seek(posicion, os.SEEK_SET)
        print(f"[DEBUG] Posicionándonos para modificar en tell(): {f.tell()}")
        f.write(registro)