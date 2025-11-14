import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
from PIL import Image, ImageTk, ImageFilter


class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal - Spain CORPORATION")
        self.root.geometry("700x500")

        # --------------------------------------------------------
        #              CARGAR Y AJUSTAR IMAGEN DE FONDO
        # --------------------------------------------------------
        self.fondo_original = None
        self.fondo_tk = None

        try:
            ruta_fondo = os.path.join(os.path.dirname(__file__), "assets", "fondo_menu2.jpg")
            self.fondo_original = Image.open(ruta_fondo)
        except Exception as e:
            print("Error cargando fondo:", e)
            self.root.config(bg="#ececec")

        self.fondo_label = tk.Label(self.root)
        self.fondo_label.place(relwidth=1, relheight=1)
        self.root.bind("<Configure>", self.ajustar_fondo)

        # --------------------------------------------------------
        #              PANEL (inicia abajo y oculto)
        # --------------------------------------------------------
        self.panel_y_pos = 1.30      # empieza fuera de pantalla
        self.panel_opacidad = 0       # fade-in
        self.boton_opacidad = 0       # fade-in botones

        self.panel = tk.Frame(
            root,
            bg="#0a1a2f",
            bd=0,
            highlightthickness=0
        )
        self.panel.place(relx=0.5, rely=self.panel_y_pos, anchor="center", width=420, height=420)

        # --------------------------------------------------------
        #                       TÍTULO
        # --------------------------------------------------------
        self.titulo = tk.Label(
            self.panel,
            text="𝑺𝑷𝑨𝑰𝑵 𝑪𝑶𝑹𝑷 𝐌𝐄𝐍𝐔",
            font=("Segoe UI", 28, "bold"),
            fg="#D4AF37",
            bg="#0a1a2f"
        )
        self.titulo.pack(pady=25)

        # --------------------------------------------------------
        #                BOTONES GUARDADOS PARA ANIMARLOS
        # --------------------------------------------------------
        self.botones = []

        self.crear_boton_moderno("Ver Productos", self.ver_productos, "#fff6a3", "#ffe870")
        self.crear_boton_moderno("ABM de Productos", self.abrir_abm_productos, "#fff6a3", "#ffe870")
        self.crear_boton_moderno("Cerrar Sesión", self.cerrar_sesion, "#ffb3b3", "#ff8a8a")

        for b in self.botones:
            b.place_forget()

        # dejar ver el fondo 3 segundos
        self.root.after(3000, self.iniciar_animacion)

    # --------------------------------------------------------
    #      BOTÓN MODERNO — ESTILO Y BINDINGS (hover / click)
    # --------------------------------------------------------
    def crear_boton_moderno(self, texto, comando, hover_color, click_color):
        btn = tk.Label(
            self.panel,
            text=texto,
            font=("Segoe UI", 15),
            bg="#ffffff",
            fg="#111111",
            padx=18,
            pady=10,
            cursor="hand2",
            bd=0,
            relief="flat",
            highlightthickness=2,
            highlightbackground="#DDDDDD",
            highlightcolor="#DDDDDD"
        )

        btn.original_bg = "#ffffff"
        btn.hover_color = hover_color
        btn.click_color = click_color
        btn.comando = comando
        btn.opacity = 0

        btn.bind("<Enter>", lambda e, b=btn: self._on_enter(b))
        btn.bind("<Leave>", lambda e, b=btn: self._on_leave(b))
        btn.bind("<Button-1>", lambda e, b=btn: self._on_click(b))

        self.botones.append(btn)
        return btn

    def _on_enter(self, btn):
        btn.config(bg=btn.hover_color)

    def _on_leave(self, btn):
        btn.config(bg=btn.original_bg)

    def _on_click(self, btn):
        btn.config(bg=btn.click_color)

        def shrink(step=0):
            if step < 4:
                btn.config(pady=10 - step)
                self.root.after(18, lambda: shrink(step + 1))
            else:
                expand()

        def expand(step=0):
            if step < 4:
                btn.config(pady=6 + step)
                self.root.after(18, lambda: expand(step + 1))
            else:
                btn.config(bg=btn.original_bg)
                try:
                    btn.comando()
                except Exception as e:
                    messagebox.showerror("Error", f"Ocurrió un error al ejecutar: {e}")

        shrink()

    # --------------------------------------------------------
    #           APARICIÓN DE LOS BOTONES (fade)
    # --------------------------------------------------------
    def animar_botones(self, index=0):
        if index >= len(self.botones):
            return

        btn = self.botones[index]
        y_rel = 0.32 + index * 0.18

        btn.place(relx=0.5, rely=y_rel, anchor="n", width=320)

        def fade(step=0):
            if step <= 10:
                alpha = step / 10
                gray = int(255 * alpha)
                btn.config(bg=f"#{gray:02x}{gray:02x}{gray:02x}")
                self.root.after(22, lambda: fade(step + 1))

        fade()
        self.root.after(220, lambda: self.animar_botones(index + 1))

    # --------------------------------------------------------
    #            AJUSTE AUTOMÁTICO DEL FONDO
    # --------------------------------------------------------
    def ajustar_fondo(self, event):
        if self.fondo_original is None:
            return

        w, h = self.root.winfo_width(), self.root.winfo_height()
        if w < 2 or h < 2:
            return

        fondo = self.fondo_original.resize((w, h), Image.Resampling.LANCZOS)
        fondo = fondo.filter(ImageFilter.GaussianBlur(2))

        self.fondo_tk = ImageTk.PhotoImage(fondo)
        self.fondo_label.config(image=self.fondo_tk)

    # --------------------------------------------------------
    #        ANIMACIÓN MUY SUAVE: EASE OUT + MÁS FPS
    # --------------------------------------------------------
    def iniciar_animacion(self):
        self.animar_panel()
        self.root.after(900, lambda: self.animar_botones(0))

    def animar_panel(self):
        objetivo = 0.50
        actual = self.panel_y_pos

        # distancia a recorrer
        delta = actual - objetivo

        if abs(delta) > 0.001:
            # interpolación suave (ease out)
            self.panel_y_pos -= delta * 0.12  # velocidad reducida progresivamente

            # actualizar posición
            self.panel.place(relx=0.5, rely=self.panel_y_pos, anchor="center")

            # fade
            if self.panel_opacidad < 1:
                self.panel_opacidad += 0.02
                a = min(1.0, self.panel_opacidad)
                azul = (10 * a, 26 * a, 47 * a)
                color = f"#{int(azul[0]):02x}{int(azul[1]):02x}{int(azul[2]):02x}"
                self.panel.config(bg=color)
                self.titulo.config(bg=color)

            # más FPS → más fluido
            self.root.after(10, self.animar_panel)

    # --------------------------------------------------------
    #                    FUNCIONES
    # --------------------------------------------------------
    def ver_productos(self):
        subprocess.Popen(["python", "ver_productos.py"])

    def abrir_abm_productos(self):
        subprocess.Popen(["python", "productos_abm.py"])

    def cerrar_sesion(self):
        self.root.destroy()
        subprocess.Popen(["python", "login_register.py"])


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] != "from_login":
        subprocess.Popen(["python", "login_register.py"])
        sys.exit()

    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()
