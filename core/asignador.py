import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk

from core.datos_cache import actualizar, guardar_todos

# === Barra de progreso visual para el proceso de asignación ===
def mostrar_barra_carga(master, pasos):
    """Muestra una ventana emergente con barra de progreso centrada en pantalla."""
    ventana = tk.Toplevel(master)
    ventana.title("Asignando participantes")
    ventana.geometry("420x150")
    ventana.resizable(False, False)
    ventana.configure(bg="#f0f2f5")
    ventana.transient(master)
    ventana.grab_set()

    # Centrar ventana en pantalla
    ventana.update_idletasks()
    ancho = 420
    alto = 150
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    contenedor = tk.Frame(ventana, bg="#f0f2f5", padx=15, pady=15)
    contenedor.pack(fill=tk.BOTH, expand=True)

    label = tk.Label(contenedor, text="Inicializando...", font=("Segoe UI", 11), bg="#f0f2f5")
    label.pack(pady=(10, 5))

    progress = ttk.Progressbar(contenedor, orient=tk.HORIZONTAL, length=350, mode="determinate")
    progress.pack(fill=tk.X, expand=True, pady=(5, 15))
    progress["maximum"] = len(pasos)

    def avanzar(etapa, i):
        label.config(text=etapa)
        label.update_idletasks()
        progress["value"] = i + 1
        progress.update_idletasks()
        ventana.update()
        ventana.after(1000)

    return ventana, avanzar

# === Algoritmo de asignación automática ===
def asignar_participantes(participaciones_df, participantes_df, master=None):
    """Asigna automáticamente participantes a las participaciones según criterios definidos."""
    pasos = [
        "Comprobando requisitos",
        "Leyendo participantes",
        "Comprobando últimas participaciones",
        "Comprobando última sala",
        "Comprobando participaciones no realizadas",
        "Asignando"
    ]

    ventana, avanzar = (None, lambda *_: None)
    if master:
        ventana, avanzar = mostrar_barra_carga(master, pasos)

    # Asegurar que las columnas requeridas existen
    if "Asignado" not in participaciones_df.columns:
        participaciones_df["Asignado"] = ""
    else:
        participaciones_df["Asignado"] = participaciones_df["Asignado"].fillna("").astype(str)

    if "Notas" not in participaciones_df.columns:
        participaciones_df["Notas"] = ""

    avanzar(pasos[0], 0)

    # Conversión de fechas
    participantes_df["Última participación"] = pd.to_datetime(participantes_df["Última participación"], errors="coerce")
    participaciones_df["Fecha"] = pd.to_datetime(participaciones_df["Fecha"], errors="coerce")

    avanzar(pasos[1], 1)

    # Ordenar participaciones por fecha
    participaciones_df = participaciones_df.sort_values(by="Fecha").copy()

    avanzar(pasos[2], 2)
    avanzar(pasos[3], 3)

    # Detectar penalizados por no asistir
    historial_fallos = participaciones_df[participaciones_df["Notas"].astype(str).str.contains("No realizada", na=False)]
    penalizados = historial_fallos["Asignado"].dropna().unique().tolist()

    avanzar(pasos[4], 4)

    asignadas = []

    for i, participacion in participaciones_df.iterrows():
        tipo_req = participacion["Tipo"]
        sala_objetivo = participacion["Sala"]
        fecha_participacion = participacion["Fecha"]

        candidatos = []

        for _, p in participantes_df.iterrows():
            tipos = [t.strip() for t in str(p["Tipos"]).split(",") if t.strip()]
            if tipo_req not in tipos:
                continue

            ya_asignado_ese_dia = any(
                (asignado["Fecha"].date() == fecha_participacion.date() and
                 asignado["Participante"] == p["Nombre"])
                for asignado in asignadas
            )
            if ya_asignado_ese_dia:
                continue

            if p["Última sala"] == sala_objetivo:
                continue

            candidatos.append(p)

        if not candidatos:
            continue

        def prioridad(p):
            nombre = p["Nombre"]
            ultima_fecha = p["Última participación"]
            dias = (fecha_participacion - ultima_fecha).days if pd.notna(ultima_fecha) else 9999
            if nombre in penalizados:
                dias /= 2
            return -dias

        candidatos.sort(key=prioridad)
        seleccionado = candidatos[0]
        nombre = seleccionado["Nombre"]
        participaciones_df.loc[i, "Asignado"] = nombre

        participantes_df.loc[participantes_df["Nombre"] == nombre, "Última participación"] = fecha_participacion.strftime("%Y-%m-%d")
        participantes_df.loc[participantes_df["Nombre"] == nombre, "Último tipo"] = tipo_req
        participantes_df.loc[participantes_df["Nombre"] == nombre, "Última sala"] = sala_objetivo

        asignadas.append({
            "Fecha": fecha_participacion,
            "Participante": nombre
        })

    avanzar(pasos[5], 5)

    if master and ventana:
        ventana.destroy()

    actualizar("participaciones", participaciones_df)
    actualizar("participantes", participantes_df)
    guardar_todos()

    return participaciones_df.copy(), participantes_df.copy()
