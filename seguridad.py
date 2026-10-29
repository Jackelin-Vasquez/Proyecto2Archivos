# Cálculo SHA-256, respaldos ZIP y metadatos (os.stat)
"""Parte 3 - Seguridad: SHA-256, respaldo ZIP y metadatos (os.stat / os.access).

Todas las funciones reciben rutas como parámetros y NO lanzan excepciones
hacia la interfaz: devuelven (ok, datos/mensaje) para que la GUI muestre
un messagebox en lugar de caerse.
"""
import hashlib
import os
import zipfile
from datetime import datetime

ARCHIVO_DATOS = "contactos.dat"
ARCHIVO_INDICE = "indice.json"
ARCHIVO_HASH = "contactos.sha256"


# ---------------------------------------------------------------- SHA-256
def calcular_hash(ruta=ARCHIVO_DATOS):
    """SHA-256 del archivo leído en bloques (no carga todo en memoria)."""
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(8192), b""):
            h.update(bloque)
    return h.hexdigest()


def guardar_hash(ruta=ARCHIVO_DATOS, ruta_hash=ARCHIVO_HASH):
    """Llamar después de CADA escritura en contactos.dat (agregar/modificar)."""
    try:
        with open(ruta_hash, "w", encoding="utf-8") as f:
            f.write(calcular_hash(ruta))
        return True, "Hash actualizado."
    except FileNotFoundError:
        return False, f"No existe el archivo '{ruta}'."
    except PermissionError:
        return False, "Sin permisos para escribir el hash."
    except OSError as e:
        return False, f"Error al guardar el hash: {e}"


def verificar_integridad(ruta=ARCHIVO_DATOS, ruta_hash=ARCHIVO_HASH):
    """Compara el hash actual con el guardado. Llamar al iniciar la app.

    Devuelve (estado, mensaje) con estado en:
    'ok' | 'alterado' | 'sin_hash' | 'sin_datos' | 'error'
    """
    if not os.path.exists(ruta):
        return "sin_datos", "El archivo de contactos aún no existe."
    try:
        actual = calcular_hash(ruta)
    except PermissionError:
        return "error", "Sin permisos para leer el archivo de contactos."
    except OSError as e:
        return "error", f"No se pudo leer el archivo: {e}"
    try:
        with open(ruta_hash, "r", encoding="utf-8") as f:
            guardado = f.read().strip()
    except FileNotFoundError:
        return "sin_hash", "No hay hash previo; se generará uno nuevo."
    except (PermissionError, OSError) as e:
        return "error", f"No se pudo leer el hash guardado: {e}"
    if actual == guardado:
        return "ok", "Integridad verificada: el archivo no ha sido modificado."
    return "alterado", ("¡ADVERTENCIA! El archivo fue modificado fuera de la "
                        "aplicación.\n\nGuardado: %s\nActual:   %s" % (guardado, actual))


# ------------------------------------------------------------- Respaldo ZIP
def crear_respaldo(archivos=(ARCHIVO_DATOS, ARCHIVO_INDICE), carpeta="."):
    """Crea respaldo_AAAAMMDD_HHMMSS.zip y devuelve estadísticas de tamaño.

    Devuelve (ok, dict | mensaje). dict: ruta_zip, original, comprimido, ahorro_pct
    """
    # El dict también incluye "omitidos" y "detalle" (lista de (nombre, original, comprimido)
    # por archivo). "original" es la suma de los archivos y "comprimido" el tamaño real del .zip.
    existentes = [a for a in archivos if os.path.exists(a)]
    if not existentes:
        return False, "No hay archivos para respaldar."
    nombre = datetime.now().strftime("respaldo_%Y%m%d_%H%M%S.zip")
    ruta_zip = os.path.join(carpeta, nombre)
    try:
        with zipfile.ZipFile(ruta_zip, "w", zipfile.ZIP_DEFLATED) as z:
            for a in existentes:
                z.write(a, arcname=os.path.basename(a))
        # Verifica que el ZIP recién creado no esté dañado
        with zipfile.ZipFile(ruta_zip, "r") as z:
            if z.testzip() is not None:
                return False, "El respaldo se creó pero falló su verificación."
            detalle = [(i.filename, i.file_size, i.compress_size) for i in z.infolist()]
        original = sum(os.path.getsize(a) for a in existentes)
        comprimido = os.path.getsize(ruta_zip)
    except PermissionError:
        return False, "Sin permisos para crear el respaldo."
    except (OSError, zipfile.BadZipFile) as e:
        return False, f"Error al crear el respaldo: {e}"
    ahorro = (1 - comprimido / original) * 100 if original else 0.0
    return True, {"ruta_zip": ruta_zip, "original": original,
                  "comprimido": comprimido, "ahorro_pct": round(ahorro, 1),
                  "omitidos": [a for a in archivos if a not in existentes],
                  "detalle": detalle}


# ---------------------------------------------------- Metadatos y permisos
def info_archivo(ruta=ARCHIVO_DATOS):
    """Tamaño, última modificación y permisos con os.stat y os.access."""
    try:
        st = os.stat(ruta)
    except FileNotFoundError:
        return False, f"El archivo '{ruta}' no existe."
    except PermissionError:
        return False, "Sin permisos para consultar el archivo."
    except OSError as e:
        return False, f"Error al consultar el archivo: {e}"
    return True, {
        "ruta": os.path.abspath(ruta),
        "tamano_bytes": st.st_size,
        "modificado": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        "lectura": os.access(ruta, os.R_OK),
        "escritura": os.access(ruta, os.W_OK),
    }