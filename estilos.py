from tkinter import ttk

def aplicar_estilos(root):
    """Aplica un tema oscuro personalizado a los widgets de la interfaz."""
    style = ttk.Style()
    style.theme_use("clam")  # Usa el tema base 'clam' como punto de partida

    # === Paleta de colores personalizada ===
    fondo = "#000000"       # Fondo principal (negro)
    gris = "#292929"        # Recuadros y contenedores
    texto = "#e3e3e3"       # Color principal del texto
    lila = "#5b3c88"        # Color de acento
    encabezado = "#1c1c1c"  # Fondo para encabezados de tabla

    # === Estilo para botones ===
    style.configure("TButton",
                    background=gris,
                    foreground=texto,
                    font=("Segoe UI", 11),
                    borderwidth=0,
                    focusthickness=0,
                    padding=(10, 6))
    style.map("TButton",
              background=[("active", lila), ("pressed", lila)],
              foreground=[("disabled", "#888888")])

    # === Estilo para etiquetas (Label) ===
    style.configure("TLabel",
                    background=fondo,
                    foreground=texto,
                    font=("Segoe UI", 11))

    # === Estilo para contenedores ===
    style.configure("TFrame", background=fondo)
    style.configure("TLabelframe",
                    background=fondo,
                    foreground=texto,
                    font=("Segoe UI", 11, "bold"))
    style.configure("TLabelframe.Label",
                    background=fondo,
                    foreground=texto)

    # === Estilo para barras de progreso ===
    style.configure("TProgressbar",
                    troughcolor=gris,
                    background=lila,
                    bordercolor=gris,
                    lightcolor=lila,
                    darkcolor=lila)

    # === Scrollbar vertical personalizada ===
    style.configure("Vertical.TScrollbar",
                    gripcount=0,
                    background=lila,
                    troughcolor=gris,
                    bordercolor=gris,
                    lightcolor=lila,
                    darkcolor=lila,
                    arrowcolor=texto)

    # === Estilo para tablas (Treeview) ===
    style.configure("Treeview",
                    background=gris,
                    fieldbackground=gris,
                    foreground=texto,
                    rowheight=28,
                    font=("Segoe UI", 10),
                    borderwidth=0,
                    relief="flat")
    style.map("Treeview",
              background=[("selected", lila)],
              foreground=[("selected", texto)])

    # Layout personalizado para Treeview (estructura interna)
    style.layout("Treeview", [
        ("Treeview.field", {'sticky': 'nswe', 'children': [
            ("Treeview.padding", {'sticky': 'nswe', 'children': [
                ("Treeview.treearea", {'sticky': 'nswe'})
            ]})
        ]})
    ])

    # === Estilo para encabezados de tablas ===
    style.configure("Treeview.Heading",
                    background=encabezado,
                    foreground=texto,
                    font=("Segoe UI", 10, "bold"))
    style.map("Treeview.Heading",
              background=[("active", lila)])

    # === Estilos globales para menús (tk.Menu) ===
    root.option_add("*Menu.background", gris)
    root.option_add("*Menu.foreground", texto)
    root.option_add("*Menu.activeBackground", lila)
    root.option_add("*Menu.activeForeground", texto)
    root.option_add("*Menu.relief", "flat")
    root.option_add("*Menu.borderWidth", 0)
