# actualizador.py
import requests
import subprocess
import sys
import os
from config import VERSION as VERSION_LOCAL
from tkinter import messagebox, Toplevel

URL_JSON = "https://raw.githubusercontent.com/AitorLcom/GestionParticipantes/refs/heads/main/version.json"

def verificar_actualizacion(root):
    try:
        print("Buscando actualizaciones...")
        r = requests.get(URL_JSON)
        data = r.json()
        ultima = data["version"]
        enlace = data["url"]

        print(f"Versión actual: {VERSION_LOCAL}")
        print(f"Última versión disponible: {ultima}")

        # Crear ventana emergente con Toplevel
        ventana = Toplevel(root)
        ventana.withdraw()

        if ultima != VERSION_LOCAL:
            mensaje = (f"¡Nueva versión disponible!\n\n"
                       f"Versión actual: {VERSION_LOCAL}\n"
                       f"Nueva versión: {ultima}\n\n"
                       f"Descargando nueva versión...")
            messagebox.showinfo("Actualización disponible", mensaje, parent=ventana)

            archivo = "actualizacion.exe"
            print(f"Descargando nueva versión desde: {enlace}")
            with open(archivo, "wb") as f:
                contenido = requests.get(enlace).content
                f.write(contenido)
                print(f"Descarga completada. Tamaño del archivo: {len(contenido)} bytes.")
            print("Iniciando instalación de la nueva versión...")
            messagebox.showinfo("Instalación", "La nueva versión se instalará ahora.", parent=ventana)
            subprocess.Popen(archivo)
            return False  # Indica que la aplicación no debe continuar
        else:
            mensaje = (f"No se encontraron actualizaciones.\n\n"
                       f"Versión actual: {VERSION_LOCAL}\n"
                       f"Última versión disponible: {ultima}")
            messagebox.showinfo("Sin actualizaciones", mensaje, parent=ventana)
            print("No se encontraron actualizaciones. La aplicación ya está actualizada.")
    except Exception as e:
        print("Error al comprobar actualizaciones:", e)
        messagebox.showerror("Error", f"Error al comprobar actualizaciones:\n{e}", parent=ventana)
    finally:
        ventana.destroy()
    return True  # Indica que la aplicación debe continuar
