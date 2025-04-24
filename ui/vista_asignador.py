import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import pandas as pd

from core.datos_cache import obtener, actualizar, guardar_todos
from core.asignador import asignar_participantes

class VistaAsignador:
    def __init__(self, master):
        """Inicializa la vista de asignador automático."""
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.participaciones_df = obtener("participaciones")
        self.participantes_df = obtener("participantes")

        self._crear_widgets()

    def _crear_widgets(self):
        """Crea los controles para filtrado, asignación y edición."""
        filtro_frame = ttk.LabelFrame(self.frame, text="Rango de fechas")
        filtro_frame.pack(fill=tk.X, padx=10, pady=10)

        # Entradas de fechas
        ttk.Label(filtro_frame, text="Desde:").grid(row=0, column=0, padx=5, pady=5)
        self.fecha_inicio = DateEntry(filtro_frame, date_pattern="yyyy-MM-dd")
        self.fecha_inicio.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filtro_frame, text="Hasta:").grid(row=0, column=2, padx=5, pady=5)
        self.fecha_fin = DateEntry(filtro_frame, date_pattern="yyyy-MM-dd")
        self.fecha_fin.grid(row=0, column=3, padx=5, pady=5)

        # Botones de acción
        ttk.Button(filtro_frame, text="Mostrar participaciones", command=self._mostrar_participaciones).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(filtro_frame, text="Asignar participantes", command=self._asignar_participantes).grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(filtro_frame, text="Guardar cambios", command=self._guardar_cambios).grid(row=0, column=6, padx=5, pady=5)

        # Tabla de participaciones
        self.tree = ttk.Treeview(self.frame, columns=["Fecha", "Número", "Sala", "Tipo", "Asignado"], show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree.bind("<Double-1>", self._editar_celda)

    def _mostrar_participaciones(self):
        """Filtra y muestra participaciones dentro del rango de fechas."""
        self.tree.delete(*self.tree.get_children())

        inicio = self.fecha_inicio.get_date()
        fin = self.fecha_fin.get_date()

        fecha_dt = pd.to_datetime(self.participaciones_df["Fecha"], errors='coerce')
        self.filtradas = self.participaciones_df[
            (fecha_dt >= pd.to_datetime(inicio)) & (fecha_dt <= pd.to_datetime(fin))
        ].copy()

        for _, row in self.filtradas.iterrows():
            self.tree.insert("", tk.END, values=[row["Fecha"], row["Número"], row["Sala"], row["Tipo"], row["Asignado"]])

    def _asignar_participantes(self):
        """Llama al algoritmo de asignación y actualiza los datos mostrados."""
        inicio = self.fecha_inicio.get_date()
        fin = self.fecha_fin.get_date()

        filtradas = self.participaciones_df.copy()
        filtradas["Fecha_dt"] = pd.to_datetime(filtradas["Fecha"])
        rango_df = filtradas[
            (filtradas["Fecha_dt"] >= pd.to_datetime(inicio)) & 
            (filtradas["Fecha_dt"] <= pd.to_datetime(fin))
        ].copy()

        if rango_df.empty:
            messagebox.showinfo("Sin datos", "No hay participaciones en el rango seleccionado.")
            return

        # Asignación automática
        df_actualizado, participantes_actualizados = asignar_participantes(
            rango_df, self.participantes_df.copy(), master=self.master
        )

        # Actualiza la base de datos con los asignados
        for idx, row in df_actualizado.iterrows():
            original_idx = self.participaciones_df[
                (self.participaciones_df["Fecha"] == row["Fecha"]) &
                (self.participaciones_df["Número"] == row["Número"]) &
                (self.participaciones_df["Sala"] == row["Sala"])
            ].index
            if not original_idx.empty:
                self.participaciones_df.at[original_idx[0], "Asignado"] = row["Asignado"]

        self.participaciones_df = df_actualizado  # datos actualizados
        self._mostrar_participaciones()           # refresca vista con fechas ya seleccionadas


        messagebox.showinfo("Asignación completa", "Participantes asignados correctamente. Puedes hacer cambios manuales antes de guardar.")

    def _editar_celda(self, event):
        """Permite editar manualmente el nombre del participante asignado."""
        item = self.tree.selection()[0]
        columna = self.tree.identify_column(event.x)

        # Solo editable la columna de "Asignado"
        if columna == "#5":
            nombre_actual = self.tree.item(item, "values")[4]

            ventana = tk.Toplevel(self.master)
            ventana.title("Editar participante")
            ventana.geometry("300x100")

            ttk.Label(ventana, text="Nuevo participante:").pack(pady=5)

            combo = ttk.Combobox(ventana, values=sorted(self.participantes_df["Nombre"].dropna().tolist()))
            combo.set(nombre_actual)
            combo.pack(pady=5)

            def guardar():
                nuevo_nombre = combo.get()
                valores = list(self.tree.item(item, "values"))
                valores[4] = nuevo_nombre
                self.tree.item(item, values=valores)
                ventana.destroy()

            ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=5)

    def _guardar_cambios(self):
        """Guarda en el DataFrame y disco los cambios hechos en la tabla."""
        for item in self.tree.get_children():
            valores = self.tree.item(item, "values")
            idx = self.participaciones_df[
                (self.participaciones_df["Fecha"] == valores[0]) &
                (self.participaciones_df["Número"] == int(valores[1])) &
                (self.participaciones_df["Sala"] == valores[2])
            ].index
            if not idx.empty:
                self.participaciones_df.at[idx[0], "Asignado"] = valores[4]

        actualizar("participaciones", self.participaciones_df)
        guardar_todos()
        messagebox.showinfo("Guardado", "Cambios guardados en la base de datos.")
