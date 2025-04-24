from core import gestor_datos

# Diccionario para mantener los datos cargados en memoria
datos = {}

# Archivos requeridos y sus claves internas
TABLAS = {
    "participantes": "participantes.csv",
    "participaciones": "participaciones.csv",
    "historial": "historial.csv",
    "opciones_tipos": "opciones_tipos.csv"
}

def cargar_datos_en_memoria():
    """Carga todos los CSV definidos en TABLAS y los guarda en el diccionario 'datos'."""
    for clave, archivo in TABLAS.items():
        datos[clave] = gestor_datos.cargar_csv(archivo)


def guardar_todos():
    """Guarda todos los DataFrames en memoria de nuevo en sus respectivos archivos CSV."""
    for clave, archivo in TABLAS.items():
        df = datos.get(clave)
        if df is not None:
            gestor_datos.guardar_csv(archivo, df)


def obtener(nombre):
    """Devuelve el DataFrame correspondiente al nombre dado."""
    return datos.get(nombre)


def actualizar(nombre, nuevo_df):
    """Actualiza el DataFrame en memoria para una clave específica."""
    datos[nombre] = nuevo_df