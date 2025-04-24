import os
from datetime import datetime
import atexit
import tkinter as tk
from core import gestor_datos
from core import datos_cache
from ui.menu_principal import lanzar_menu
from estilos import aplicar_estilos

# Rutas base
DATA_DIR = "data"
LOGS_DIR = os.path.join(DATA_DIR, "logs")
LOG_FILE = os.path.join(LOGS_DIR, "log.txt")

# Archivos y columnas requeridas
TABLAS_REQUERIDAS = {
    "participantes.csv": ["Nombre", "Género", "Tipos", "Última participación", "Último tipo", "Última sala"],
    "participaciones.csv": ["Fecha", "Número", "Tipo", "Género", "Sala", "Asignado"],
    "opciones_tipos.csv": ["Tipos"]
}

def registrar_log(mensaje):
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {mensaje}\n")

def al_cerrar():
    registrar_log("Programa finalizado.")

def preparar_tablas():
    registrar_log("Comprobando existencia de archivos CSV requeridos...")
    for archivo, columnas in TABLAS_REQUERIDAS.items():
        ruta = os.path.join(DATA_DIR, archivo)
        if not os.path.exists(ruta):
            gestor_datos.asegurarse_archivo(archivo, columnas)
            registrar_log(f"Archivo creado: {archivo} con columnas {columnas}")
        else:
            registrar_log(f"Archivo ya existe: {archivo}")

def main():
    atexit.register(al_cerrar)

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        registrar_log("Directorio 'data' creado.")

    preparar_tablas()

    bases = gestor_datos.listar_csv()
    if bases:
        registrar_log(f"Bases de datos encontradas: {bases}")
    else:
        registrar_log("No se encontraron bases de datos CSV.")

    datos_cache.cargar_datos_en_memoria()

    root = tk.Tk()
    aplicar_estilos(root)
    lanzar_menu(root)
    root.mainloop()

if __name__ == "__main__":
    main()