import json
import os

# Nombre del archivo donde se almacena el índice
ARCHIVO_INDICE = "indice.json"

# Carga el índice desde el archivo JSON
def cargar_indice():
    # Verifica si el archivo no existe
    if not os.path.exists(ARCHIVO_INDICE):
        # Crea un índice vacío y lo guarda
        guardar_indice({})
        return {}

    try:
        # Abre el archivo en modo lectura con codificación UTF-8
        with open(ARCHIVO_INDICE, "r", encoding="utf-8") as archivo:
            # Lee los datos del archivo JSON
            indice = json.load(archivo)

        # Verifica que los datos sean un diccionario
        if not isinstance(indice, dict):
            raise ValueError("El índice debe contener un objeto JSON.")

        # Crea un diccionario para guardar los datos normalizados
        indice_limpio = {}
        # Recorre cada identificador y su número de registro
        for identificador, registro in indice.items():
            # Convierte el identificador a texto y el registro a entero
            indice_limpio[str(identificador)] = int(registro)
        # Devuelve el índice con los datos normalizados
        return indice_limpio

    # Maneja errores al leer o convertir los datos del archivo
    except (json.JSONDecodeError, ValueError, TypeError, OSError) as error:
        # Muestra un mensaje indicando que no se pudo leer el archivo
        raise ValueError(
            "No se pudo leer indice.json. El archivo puede estar dañado o no tener permisos."
        ) from error

# Guarda el índice en el archivo JSON
def guardar_indice(indice):
    """Guarda el índice en UTF-8."""
    # Define el nombre del archivo temporal
    archivo_temporal = ARCHIVO_INDICE + ".tmp"
    # Abre el archivo temporal en modo escritura
    with open(archivo_temporal, "w", encoding="utf-8") as archivo:
        # Guarda el índice en formato JSON, conservando los caracteres especiales
        json.dump(indice, archivo, ensure_ascii=False, indent=4)
    # Reemplaza el archivo original por el archivo temporal
    os.replace(archivo_temporal, ARCHIVO_INDICE)

# Agrega un identificador y su número de registro al índice
def agregar_al_indice(identificador, numero_registro):
    """Agrega un ID al índice. No permite duplicados."""
    # Carga el índice existente
    indice = cargar_indice()
    # Convierte el identificador a texto
    clave = str(identificador)

    # Verifica si el identificador ya existe
    if clave in indice:
        # Genera un error si el identificador está duplicado
        raise ValueError("Ya existe un contacto con ese ID.")

    # Agrega el identificador y convierte el registro a entero
    indice[clave] = int(numero_registro)
    # Guarda los cambios en el archivo JSON
    guardar_indice(indice)

# Busca un identificador dentro del índice
def buscar_en_indice(identificador):
    # Carga el índice almacenado
    indice = cargar_indice()
    # Devuelve el número de registro o None si no existe
    return indice.get(str(identificador))


# Reconstruye el índice utilizando la lista de contactos
def reconstruir_indice(contactos):

    # Crea un diccionario vacío para el nuevo índice
    indice = {}
    # Recorre todos los contactos recibidos
    for contacto in contactos:
        # Obtiene el ID del contacto y lo convierte a texto
        clave = str(contacto["id"])
        # Comprueba si el ID ya fue agregado
        if clave in indice:
            # Genera un error si existen identificadores duplicados
            raise ValueError("Hay IDs duplicados; no se puede reconstruir el índice.")
        # Guarda el ID y su número de registro convertido a entero
        indice[clave] = int(contacto["registro"])
    # Guarda el índice reconstruido en el archivo JSON
    guardar_indice(indice)
    # Devuelve el índice reconstruido
    return indice