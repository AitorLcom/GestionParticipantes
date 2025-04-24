import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pandas as pd

from core.datos_cache import obtener, actualizar, guardar_todos

class VistaHistorial:
    def __init__(self, master):
        """Inicializa la vista del historial de participaciones."""
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.participaciones_df = obtener("participaciones")
        self.participantes_df = obtener("participantes")
        self.nombres_participantes = sorted(self.participantes_df["Nombre"].dropna().unique().tolist())

        self._crear_widgets()
        self._cargar_tabla()

    def _crear_widgets(self):
        """Crea los elementos de filtrado y tabla."""
        filtro_frame = ttk.LabelFrame(self.frame, text="Filtros")
        filtro_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(filtro_frame, text="Participante:").grid(row=0, column=0, padx=5, pady=5)
        self.filtro_participante = ttk.Entry(filtro_frame)
        self.filtro_participante.grid(row=0, column=1, padx=5, pady=5)
        self.filtro_participante.bind("<KeyRelease>", self._actualizar_sugerencias)

        self.lista_sugerencias = tk.Listbox(filtro_frame, height=3)
        self.lista_sugerencias.grid(row=1, column=1, padx=5, pady=(0, 5), sticky="ew")
        self.lista_sugerencias.bind("<<ListboxSelect>>", self._seleccionar_sugerencia)

        ttk.Label(filtro_frame, text="Fecha:").grid(row=0, column=2, padx=5, pady=5)
        self.filtro_fecha = DateEntry(filtro_frame, date_pattern="yyyy-MM-dd")
        self.filtro_fecha.grid(row=0, column=3, padx=5, pady=5)
        self.usar_fecha = tk.BooleanVar()
        ttk.Checkbutton(filtro_frame, text="Usar fecha", variable=self.usar_fecha).grid(row=0, column=4, padx=5, pady=5)

        ttk.Button(filtro_frame, text="Aplicar filtros", command=self._filtrar).grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(filtro_frame, text="Quitar filtros", command=self._quitar_filtros).grid(row=0, column=6, padx=5, pady=5)

        self.tree = ttk.Treeview(
            self.frame,
            columns=["Fecha", "Tipo", "Sala", "Participante", "Notas"],
            show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.checkbox_frame = ttk.Frame(self.frame)
        self.checkbox_frame.pack(pady=5)
        ttk.Button(self.checkbox_frame, text="Marcar como no realizada", command=self._marcar_no_realizada).pack()

    def _actualizar_sugerencias(self, event=None):
        texto = self.filtro_participante.get().lower()
        coincidencias = [n for n in self.nombres_participantes if texto in n.lower()]
        self.lista_sugerencias.delete(0, tk.END)
        for nombre in coincidencias[:5]:
            self.lista_sugerencias.insert(tk.END, nombre)

    def _seleccionar_sugerencia(self, event):
        seleccion = self.lista_sugerencias.curselection()
        if seleccion:
            nombre = self.lista_sugerencias.get(seleccion[0])
            self.filtro_participante.delete(0, tk.END)
            self.filtro_participante.insert(0, nombre)
            self.lista_sugerencias.delete(0, tk.END)

    def _cargar_tabla(self, datos=None):
        """Carga datos en la tabla (todos o filtrados). Limpia 'nan' en Notas."""
        self.tree.delete(*self.tree.get_children())
        df = datos if datos is not None else self.participaciones_df

        for _, row in df.iterrows():
            nota = row.get("Notas", "")
            nota = "" if pd.isna(nota) or str(nota).strip().lower() == "nan" else str(nota)
            self.tree.insert(
                "", tk.END,
                values=[
                    row["Fecha"],
                    row["Tipo"],
                    row["Sala"],
                    row["Asignado"],
                    nota
                ]
            )

    def _filtrar(self):
        df = self.participaciones_df.copy()
        participante = self.filtro_participante.get().strip()
        usar_fecha = self.usar_fecha.get()

        if usar_fecha:
            fecha = self.filtro_fecha.get_date().strftime("%Y-%m-%d")
            df["Fecha"] = pd.to_datetime(df["Fecha"], errors='coerce').dt.strftime("%Y-%m-%d")
            df = df[df["Fecha"] == fecha]

        if participante:
            df = df[df["Asignado"] == participante]

        self._cargar_tabla(df)

    def _quitar_filtros(self):
        self.filtro_participante.delete(0, tk.END)
        self.lista_sugerencias.delete(0, tk.END)
        self.usar_fecha.set(False)
        self._cargar_tabla()

    def _marcar_no_realizada(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Seleccionar", "Selecciona una fila")
            return

        item = self.tree.item(sel[0], "values")
        fecha, tipo, sala, asignado = item[:4]

        idx = self.participaciones_df[
            (self.participaciones_df["Fecha"] == fecha) &
            (self.participaciones_df["Tipo"] == tipo) &
            (self.participaciones_df["Sala"] == sala) &
            (self.participaciones_df["Asignado"] == asignado)
        ].index

        if not idx.empty:
            # Forzamos que la nota sea exactamente "No realizada"
            self.participaciones_df.at[idx[0], "Notas"] = "No realizada"
            actualizar("participaciones", self.participaciones_df)
            guardar_todos()
            self._cargar_tabla()
            messagebox.showinfo("Actualizado", "La participación ha sido marcada como no realizada.")
