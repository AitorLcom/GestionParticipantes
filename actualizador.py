# actualizador.py
import requests
import subprocess
import sys
import os
from config import VERSION as VERSION_LOCAL

URL_JSON = "https://raw.githubusercontent.com/AitorLcom/GestorParticipantes/main/version.json"

def verificar_actualizacion():
    try:
        r = requests.get(URL_JSON)
        data = r.json()
        ultima = data["version"]
        enlace = data["url"]

        if ultima != VERSION_LOCAL:
            print("¡Nueva versión disponible!")
            archivo = "actualizacion.exe"
            with open(archivo, "wb") as f:
                f.write(requests.get(enlace).content)
            subprocess.Popen(archivo)
            sys.exit()
        else:
            print("Aplicación actualizada.")
    except Exception as e:
        print("Error al comprobar actualizaciones:", e)
