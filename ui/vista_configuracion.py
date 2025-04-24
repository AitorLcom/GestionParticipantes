import tkinter as tk
from tkinter import ttk, messagebox
from core import datos_cache
import pandas as pd

class VistaConfiguracion:
    def __init__(self, master):
        """Inicializa la vista de configuración de tipos."""
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.tipos_df = datos_cache.obtener("opciones_tipos")

        self.crear_widgets()

    def crear_widgets(self):
        """Crea la interfaz de edición de tipos de participación."""
        ttk.Label(self.frame, text="Tipos de Participación", font=("Segoe UI", 12, "bold")).pack(pady=(10, 0))

        # Lista de tipos
        self.lista_tipos = tk.Listbox(self.frame, height=5)
        self.lista_tipos.pack(fill=tk.X, padx=10)
        self.actualizar_lista(self.lista_tipos, self.tipos_df["Tipos"].dropna().tolist())

        # Controles para añadir y eliminar
        frame_tipos = ttk.Frame(self.frame)
        frame_tipos.pack(pady=5)

        self.entrada_tipo = ttk.Entry(frame_tipos)
        self.entrada_tipo.pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_tipos, text="Añadir", command=self.agregar_tipo).pack(side=tk.LEFT)
        ttk.Button(frame_tipos, text="Eliminar", command=self.eliminar_tipo).pack(side=tk.LEFT)

        # Botón para guardar
        ttk.Button(self.frame, text="Guardar Cambios", command=self.guardar_cambios).pack(pady=10)

    def actualizar_lista(self, listbox, valores):
        """Rellena una lista con los valores dados."""
        listbox.delete(0, tk.END)
        for val in valores:
            listbox.insert(tk.END, val)

    def agregar_tipo(self):
        """Agrega un nuevo tipo si no existe ya."""
        nuevo = self.entrada_tipo.get().strip()
        if nuevo and nuevo not in self.lista_tipos.get(0, tk.END):
            self.lista_tipos.insert(tk.END, nuevo)
            self.entrada_tipo.delete(0, tk.END)

    def eliminar_tipo(self):
        """Elimina los tipos seleccionados de la lista."""
        seleccion = self.lista_tipos.curselection()
        for idx in reversed(seleccion):  # eliminar en orden inverso para evitar errores de índice
            self.lista_tipos.delete(idx)

    def guardar_cambios(self):
        """Guarda los tipos modificados en la caché y en disco."""
        nuevos_tipos = list(self.lista_tipos.get(0, tk.END))
        datos_cache.actualizar("opciones_tipos", pd.DataFrame({"Tipos": nuevos_tipos}))
        datos_cache.guardar_todos()
        messagebox.showinfo("Guardado", "Cambios guardados correctamente.")
