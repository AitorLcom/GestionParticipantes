import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import pandas as pd

from core.datos_cache import obtener, actualizar, guardar_todos

class VistaParticipaciones:
    def __init__(self, master):
        """Inicializa la vista de participaciones."""
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.participaciones_df = obtener("participaciones")
        self.fecha_seleccionada = None
        self.tipos_validos = obtener("opciones_tipos")["Tipos"].dropna().tolist()

        self._crear_widgets()

    def _crear_widgets(self):
        """Crea el calendario y contenedor de tabla."""
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Label(top_frame, text="Selecciona una fecha de reunión:").pack(anchor="w")

        self.calendario = Calendar(top_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendario.pack(pady=5)

        ttk.Button(top_frame, text="Ver Participaciones", command=self._mostrar_participaciones).pack()

        self.tabla_frame = ttk.Frame(self.frame)
        self.tabla_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _mostrar_participaciones(self):
        """Muestra las participaciones existentes para la fecha seleccionada."""
        for widget in self.tabla_frame.winfo_children():
            widget.destroy()

        self.fecha_seleccionada = self.calendario.get_date()

        ttk.Label(
            self.tabla_frame,
            text=f"Participaciones para {self.fecha_seleccionada}",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=5)

        # Botones de acción
        btns = ttk.Frame(self.tabla_frame)
        btns.pack()
        ttk.Button(btns, text="Añadir", command=self._añadir_participacion).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Eliminar", command=self._eliminar_participacion).pack(side=tk.LEFT, padx=5)

        # Tabla
        cols = ["Número", "Fecha", "Sala", "Tipo"]
        self.tree = ttk.Treeview(self.tabla_frame, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Rellenar con datos filtrados por fecha
        filtradas = self.participaciones_df[self.participaciones_df["Fecha"] == self.fecha_seleccionada]
        for _, row in filtradas.iterrows():
            self.tree.insert("", tk.END, values=[row["Número"], row["Fecha"], row["Sala"], row["Tipo"]])

    def _añadir_participacion(self):
        """Abre un formulario con estilo oscuro para agregar una nueva participación."""
        vent = tk.Toplevel(self.master)
        vent.title("Nueva participación")
        vent.configure(bg="#000000")
        vent.resizable(False, False)
        vent.grab_set()

        marco = ttk.Frame(vent, padding=20, style="TFrame")
        marco.pack(fill=tk.BOTH, expand=True)

        campos = {
            "Número": tk.StringVar(),
            "Sala": tk.StringVar(value="A"),
            "Tipo": tk.StringVar()
        }
        duplicar = tk.BooleanVar()

        # Campo fijo de fecha
        ttk.Label(marco, text=f"Fecha: {self.fecha_seleccionada}").grid(row=0, column=0, columnspan=2, pady=5)

        # Campo número
        ttk.Label(marco, text="Número:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(marco, textvariable=campos["Número"]).grid(row=1, column=1, padx=5)

        # Campo sala
        ttk.Label(marco, text="Sala:").grid(row=2, column=0, sticky="e", padx=5)
        ttk.Combobox(marco, textvariable=campos["Sala"], values=["A", "B"], state="readonly").grid(row=2, column=1, padx=5)

        # Campo tipo
        ttk.Label(marco, text="Tipo:").grid(row=3, column=0, sticky="e", padx=5)
        ttk.Combobox(marco, textvariable=campos["Tipo"], values=self.tipos_validos, state="readonly").grid(row=3, column=1, padx=5)

        # Checkbox duplicar
        ttk.Checkbutton(marco, text="Duplicar para ambas salas", variable=duplicar).grid(row=4, column=0, columnspan=2, pady=5)

        # Función guardar
        def guardar():
            try:
                numero = int(campos["Número"].get())
            except ValueError:
                messagebox.showerror("Error", "El número debe ser un entero.")
                return

            base = {
                "Número": numero,
                "Fecha": self.fecha_seleccionada,
                "Tipo": campos["Tipo"].get(),
                "Género": "",
                "Asignado": ""
            }

            nuevas = []
            if duplicar.get():
                for sala in ["A", "B"]:
                    nuevas.append({**base, "Sala": sala})
            else:
                nuevas.append({**base, "Sala": campos["Sala"].get()})

            self.participaciones_df = pd.concat([self.participaciones_df, pd.DataFrame(nuevas)], ignore_index=True)
            actualizar("participaciones", self.participaciones_df)
            guardar_todos()
            self._mostrar_participaciones()
            vent.destroy()

        ttk.Button(marco, text="Guardar", command=guardar).grid(row=5, column=0, columnspan=2, pady=10)

    def _eliminar_participacion(self):
        """Elimina la participación seleccionada en la tabla."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Eliminar", "Selecciona una participación")
            return

        item = self.tree.item(sel[0], "values")
        numero = int(item[0])
        fecha = item[1]

        confirm = messagebox.askyesno("Eliminar", f"¿Eliminar participación {numero} de {fecha}?")
        if confirm:
            self.participaciones_df = self.participaciones_df[
                ~((self.participaciones_df["Número"] == numero) & (self.participaciones_df["Fecha"] == fecha))
            ]
            actualizar("participaciones", self.participaciones_df)
            guardar_todos()
            self._mostrar_participaciones()
