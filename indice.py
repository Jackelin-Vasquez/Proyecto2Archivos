import json
import os

ARCHIVO_INDICE = "indice.json"

def cargar_indice():
    if not os.path.exists(ARCHIVO_INDICE):
        guardar_indice({})
        return {}

    try:
        with open(ARCHIVO_INDICE, "r", encoding="utf-8") as archivo:
            indice = json.load(archivo)

        if not isinstance(indice, dict):
            raise ValueError("El índice debe contener un objeto JSON.")

        # Normalizar las claves a texto y los números de registro a enteros.
        indice_limpio = {}
        for identificador, registro in indice.items():
            indice_limpio[str(identificador)] = int(registro)
        return indice_limpio

    except (json.JSONDecodeError, ValueError, TypeError, OSError) as error:
        raise ValueError(
            "No se pudo leer indice.json. El archivo puede estar dañado o no tener permisos."
        ) from error

def guardar_indice(indice):
    """Guarda el índice en UTF-8."""
    archivo_temporal = ARCHIVO_INDICE + ".tmp"
    with open(archivo_temporal, "w", encoding="utf-8") as archivo:
        json.dump(indice, archivo, ensure_ascii=False, indent=4)
    os.replace(archivo_temporal, ARCHIVO_INDICE)

def agregar_al_indice(identificador, numero_registro):
    """Agrega un ID al índice. No permite duplicados."""
    indice = cargar_indice()
    clave = str(identificador)

    if clave in indice:
        raise ValueError("Ya existe un contacto con ese ID.")

    indice[clave] = int(numero_registro)
    guardar_indice(indice)

def buscar_en_indice(identificador):
    indice = cargar_indice()
    return indice.get(str(identificador))


def reconstruir_indice(contactos):

    indice = {}
    for contacto in contactos:
        clave = str(contacto["id"])
        if clave in indice:
            raise ValueError("Hay IDs duplicados; no se puede reconstruir el índice.")
        indice[clave] = int(contacto["registro"])
    guardar_indice(indice)
    return indice
