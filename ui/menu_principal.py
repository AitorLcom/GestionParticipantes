import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

from ui.vista_participantes import VistaParticipantes
from ui.vista_configuracion import VistaConfiguracion
from ui.vista_participaciones import VistaParticipaciones
from ui.vista_historial import VistaHistorial
from ui.vista_asignador import VistaAsignador

# Ruta de recursos compatible con PyInstaller
def ruta_recurso(relativa):
    """Devuelve la ruta absoluta al recurso, compatible con PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
    else:
        base = os.path.abspath(".")

    return os.path.join(base, relativa)

class MenuPrincipal:
    def __init__(self, master):
        """Inicializa la ventana principal con menú lateral y contenido dinámico."""
        self.master = master
        self.master.title("Gestor de Participaciones")
        self.master.geometry("1100x650")
        self.master.configure(bg="#000000")

        # Establecer icono de la ventana desde recurso compatible
        try:
            self.master.iconbitmap(ruta_recurso("recursos/logo.ico"))
        except Exception as e:
            print(f"No se pudo cargar el icono de la ventana: {e}")

        self.vista_actual = None

        self.crear_menu_lateral()
        self.crear_area_contenido()
        self.mostrar_inicio()

    def crear_menu_lateral(self):
        """Crea el menú lateral con botones de navegación."""
        self.frame_menu = ttk.Frame(self.master, width=200, style="TFrame")
        self.frame_menu.pack(side=tk.LEFT, fill=tk.Y)

        opciones = [
            ("Inicio", self.mostrar_inicio),
            ("Participantes", self.mostrar_participantes),
            ("Participaciones", self.mostrar_participaciones),
            ("Asignador", self.mostrar_asignador),
            ("Historial", self.mostrar_historial),
            ("Configuración", self.mostrar_configuracion),
        ]

        for texto, comando in opciones:
            btn = ttk.Button(self.frame_menu, text=texto, command=comando, style="TButton")
            btn.pack(fill=tk.X, padx=10, pady=5)

    def crear_area_contenido(self):
        """Crea el área central donde se mostrarán las diferentes vistas."""
        self.frame_contenido = ttk.Frame(self.master, padding=20, style="TFrame")
        self.frame_contenido.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def limpiar_contenido(self):
        """Limpia la vista actual si permite salir."""
        if self.vista_actual and hasattr(self.vista_actual, 'confirmar_salida'):
            if not self.vista_actual.confirmar_salida():
                return False
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        self.vista_actual = None
        return True

    def mostrar_inicio(self):
        """Muestra una vista de bienvenida con logotipo."""
        if not self.limpiar_contenido():
            return

        marco = ttk.Frame(self.frame_contenido, style="TFrame", padding=30)
        marco.pack(expand=True)

        # Mostrar el logotipo desde ruta compatible con PyInstaller
        try:
            imagen = Image.open(ruta_recurso("recursos/logo.png")).resize((100, 100))
            self.logo_img = ImageTk.PhotoImage(imagen)
            ttk.Label(marco, image=self.logo_img, background="#000000").pack(pady=(0, 20))
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")

        # Mensaje de bienvenida
        mensaje = (
            "Gestor de participantes V 0.4\n\n"
        )
        ttk.Label(
            marco,
            text=mensaje,
            font=("Segoe UI", 14),
            wraplength=800,
            justify="center",
            foreground="#e3e3e3",
            background="#000000"
        ).pack(expand=True, fill=tk.BOTH)

    def mostrar_participantes(self):
        if not self.limpiar_contenido():
            return
        self.vista_actual = VistaParticipantes(self.frame_contenido)

    def mostrar_participaciones(self):
        if not self.limpiar_contenido():
            return
        self.vista_actual = VistaParticipaciones(self.frame_contenido)

    def mostrar_asignador(self):
        if not self.limpiar_contenido():
            return
        self.vista_actual = VistaAsignador(self.frame_contenido)

    def mostrar_configuracion(self):
        if not self.limpiar_contenido():
            return
        self.vista_actual = VistaConfiguracion(self.frame_contenido)

    def mostrar_historial(self):
        if not self.limpiar_contenido():
            return
        self.vista_actual = VistaHistorial(self.frame_contenido)

def lanzar_menu(root):
    MenuPrincipal(root)

if __name__ == "__main__":
    root = tk.Tk()
    from estilos import aplicar_estilos
    aplicar_estilos(root)
    lanzar_menu(root)
    root.mainloop()
