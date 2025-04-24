import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from tkcalendar import DateEntry

from core.datos_cache import obtener, actualizar, guardar_todos

class VistaParticipantes:
    def __init__(self, master):
        """Inicializa la vista de participantes y su interfaz."""
        self.master = master
        self.frame = ttk.Frame(master, padding=10, style="TFrame")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Datos principales
        self.participantes_df = obtener("participantes")
        tipos_df = obtener("opciones_tipos")
        self.opciones_tipos = tipos_df if tipos_df is not None and not tipos_df.empty else pd.DataFrame(columns=["Tipos"])
        self.tipos_lista = self.opciones_tipos["Tipos"].dropna().tolist()
        self.generos_lista = ["Hombre", "Mujer"]
        self.cambios_guardados = True

        self._crear_widgets()
        self._cargar_tabla()

    def _crear_widgets(self):
        """Crea los botones y la tabla de participantes."""
        btn_frame = ttk.Frame(self.frame, style="TFrame")
        btn_frame.pack(fill=tk.X, pady=5)

        estilo = {"padding": 5}
        # Botones principales
        ttk.Button(btn_frame, text="Añadir", command=self._on_add, **estilo).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Editar", command=self._on_edit, **estilo).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self._on_delete, **estilo).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Guardar", command=self._on_save, **estilo).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cargar desde archivo", command=self._on_load, **estilo).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exportar", command=self._on_export, **estilo).pack(side=tk.LEFT, padx=5)

        # Tabla
        tabla_frame = ttk.Frame(self.frame, style="TFrame")
        tabla_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        cols = ["Nombre", "Género", "Tipos", "Última participación", "Último tipo", "Última sala"]
        self.tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", style="Treeview")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="center")

        vsb = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def _cargar_tabla(self):
        """Carga los datos del DataFrame en la tabla visual."""
        self.tree.delete(*self.tree.get_children())
        for _, row in self.participantes_df.iterrows():
            vals = [row.get(col, "") for col in self.tree["columns"]]
            self.tree.insert("", tk.END, values=vals)
        self.cambios_guardados = True

    def _abrir_formulario(self, data=None):
        """Abre una ventana para añadir o editar un participante."""
        top = tk.Toplevel(self.master)
        top.title("Editar Participante" if data else "Nuevo Participante")
        top.configure(bg="#000000")
        top.resizable(False, False)
        top.grab_set()

        marco = ttk.Frame(top, padding=20, style="TFrame")
        marco.pack(fill=tk.BOTH, expand=True)

        campos = ["Nombre", "Género", "Tipos", "Última participación"]
        entradas = {}

        for i, campo in enumerate(campos):
            ttk.Label(marco, text=campo + ":").grid(row=i, column=0, sticky="e", pady=5, padx=10)
            if campo == "Género":
                combo = ttk.Combobox(marco, values=self.generos_lista, state="readonly")
                combo.grid(row=i, column=1, sticky="ew", pady=5)
                entradas[campo] = combo
            elif campo == "Tipos":
                listbox = tk.Listbox(marco, selectmode=tk.MULTIPLE, height=5, exportselection=False)
                for tipo in self.tipos_lista:
                    listbox.insert(tk.END, tipo)
                listbox.grid(row=i, column=1, sticky="ew", pady=5)
                entradas[campo] = listbox
            elif campo == "Última participación":
                fecha = DateEntry(marco, date_pattern="yyyy-mm-dd", background="#5b3c88", foreground="#e3e3e3")
                fecha.grid(row=i, column=1, sticky="ew", pady=5)
                entradas[campo] = fecha
            else:
                entry = ttk.Entry(marco)
                entry.grid(row=i, column=1, sticky="ew", pady=5)
                entradas[campo] = entry

        # Cargar datos si es edición
        for campo, widget in entradas.items():
            if data and campo in data:
                valor = data[campo]
                if isinstance(widget, DateEntry):
                    try:
                        widget.set_date(valor)
                    except:
                        pass
                elif isinstance(widget, tk.Listbox):
                    tipos_existentes = [t.strip() for t in valor.split(",")]
                    for i, tipo in enumerate(self.tipos_lista):
                        if tipo in tipos_existentes:
                            widget.selection_set(i)
                else:
                    widget.insert(0, valor)

        marco.columnconfigure(1, weight=1)

        def guardar():
            nuevo = {}
            for campo in campos:
                widget = entradas[campo]
                if campo == "Tipos":
                    seleccionados = [widget.get(i) for i in widget.curselection()]
                    nuevo[campo] = ", ".join(seleccionados)
                else:
                    nuevo[campo] = widget.get()

            if not nuevo["Nombre"]:
                messagebox.showerror("Error", "El campo 'Nombre' es obligatorio.")
                return

            if data:
                self.participantes_df.loc[self.participantes_df["Nombre"] == data["Nombre"], nuevo.keys()] = nuevo.values()
            else:
                if nuevo["Nombre"] in self.participantes_df["Nombre"].values:
                    messagebox.showerror("Error", "Ese nombre ya existe.")
                    return
                nuevo.update({"Último tipo": "", "Última sala": ""})
                self.participantes_df = pd.concat([self.participantes_df, pd.DataFrame([nuevo])], ignore_index=True)

            self._cargar_tabla()
            self.cambios_guardados = False
            top.destroy()

        ttk.Button(marco, text="Guardar", command=guardar).grid(row=len(campos), column=0, columnspan=2, pady=10)

    # === Acciones del menú ===
    def _on_add(self):
        self._abrir_formulario()

    def _on_edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Editar", "Selecciona un participante")
            return
        vals = self.tree.item(sel[0], "values")
        datos = dict(zip(self.tree["columns"], vals))
        self._abrir_formulario(datos)

    def _on_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Eliminar", "Selecciona un participante")
            return
        if not messagebox.askyesno("Eliminar", "¿Seguro que deseas eliminar este participante?"):
            return
        for item in sel:
            nombre = self.tree.item(item, "values")[0]
            self.participantes_df = self.participantes_df[self.participantes_df["Nombre"] != nombre]
        self._cargar_tabla()
        self.cambios_guardados = False

    def _on_save(self):
        """Guarda los cambios en caché y en disco."""
        actualizar("participantes", self.participantes_df)
        guardar_todos()
        self.cambios_guardados = True
        messagebox.showinfo("Guardado", "Cambios guardados correctamente.")

    def _on_load(self):
        """Carga datos desde un archivo CSV/Excel/ODS."""
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv"), ("Excel", "*.xlsx"), ("ODS", "*.ods")])
        if not path:
            return
        ext = os.path.splitext(path)[1].lower()
        try:
            if ext == ".csv":
                df = pd.read_csv(path)
            elif ext == ".xlsx":
                df = pd.read_excel(path)
            elif ext == ".ods":
                df = pd.read_excel(path, engine="odf")
            else:
                raise ValueError("Formato no soportado")
        except ImportError as e:
            messagebox.showerror("Cargar", f"Falta el módulo requerido para ODS: {e}")
            return
        except Exception as e:
            messagebox.showerror("Cargar", f"No se pudo cargar el archivo:\n{e}")
            return

        req = ["Nombre", "Género", "Tipos", "Última participación", "Último tipo", "Última sala"]
        if not all(col in df.columns for col in req):
            messagebox.showerror("Cargar", "El archivo no contiene las columnas requeridas")
            return
        if not messagebox.askyesno("Cargar", "¿Reemplazar datos actuales?"):
            return

        self.participantes_df = df[req].astype(str).copy()
        self._cargar_tabla()
        self.cambios_guardados = False

    def _on_export(self):
        """Exporta los datos actuales a un archivo CSV/Excel/ODS."""
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv"), ("Excel", "*.xlsx"), ("ODS", "*.ods")])
        if not path:
            return
        ext = os.path.splitext(path)[1].lower()
        try:
            if ext == ".csv":
                self.participantes_df.to_csv(path, index=False)
            elif ext == ".xlsx":
                self.participantes_df.to_excel(path, index=False)
            elif ext == ".ods":
                self.participantes_df.to_excel(path, index=False, engine="odf")
            else:
                raise ValueError("Formato no soportado")
            messagebox.showinfo("Exportar", f"Exportado correctamente:\n{path}")
        except ImportError as e:
            messagebox.showerror("Exportar", f"Falta el módulo requerido para ODS: {e}")
        except Exception as e:
            messagebox.showerror("Exportar", f"No se pudo exportar:\n{e}")
