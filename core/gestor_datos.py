import os
import sys
import pandas as pd

# Función para ruta válida de archivos de datos
def ruta_datos_local(relativa=""):
    """Devuelve una ruta válida de escritura para datos, incluso empaquetado con PyInstaller."""
    if getattr(sys, 'frozen', False):
        base = os.path.join(os.path.expanduser("~"), "GestorParticipantesData")
    else:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

    ruta = os.path.join(base, relativa)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    return ruta

def ruta_archivo(nombre_archivo):
    """Construye la ruta completa a un archivo dentro de la carpeta de datos."""
    return ruta_datos_local(nombre_archivo)

def cargar_csv(nombre_archivo):
    """Carga un archivo CSV como DataFrame. Devuelve DataFrame vacío si no existe o está malformado."""
    ruta = ruta_archivo(nombre_archivo)
    if not os.path.exists(ruta):
        return pd.DataFrame()
    try:
        return pd.read_csv(ruta)
    except pd.errors.EmptyDataError:
        print(f"[AVISO] Archivo CSV vacío: {nombre_archivo}. Se devolverá DataFrame vacío.")
        return pd.DataFrame()

def guardar_csv(nombre_archivo, dataframe):
    """Guarda un DataFrame en un archivo CSV."""
    ruta = ruta_archivo(nombre_archivo)
    dataframe.to_csv(ruta, index=False, encoding="utf-8")

def asegurarse_archivo(nombre_archivo, columnas):
    """Crea un archivo CSV vacío con columnas dadas si no existe."""
    ruta = ruta_archivo(nombre_archivo)
    if not os.path.exists(ruta):
        df = pd.DataFrame(columns=columnas)
        df.to_csv(ruta, index=False, encoding="utf-8")

def listar_csv():
    """Devuelve una lista de archivos CSV en el directorio de datos."""
    base = os.path.dirname(ruta_datos_local())  # asegura consistencia
    if not os.path.exists(base):
        os.makedirs(base)
    return [f for f in os.listdir(base) if f.endswith(".csv")]
