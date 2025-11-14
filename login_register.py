import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import json
import os
import subprocess

USUARIOS_FILE = "usuarios.json"


def cargar_usuarios():
    if not os.path.exists(USUARIOS_FILE):
        return {}
    with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)


class LoginRegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spain Corporation - Login")
        self.root.geometry("500x520")
        self.root.resizable(False, False)

        # ---- Fondo ----
        self.bg_image = Image.open("assets/fondo_menu2.jpg")
        self.bg_image = self.bg_image.resize((500, 520), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.background_label = tk.Label(root, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ---- Banner ----
        banner = tk.Frame(root, bg="#0A0F24")
        banner.place(relx=0, rely=0, relwidth=1, height=120)

        tk.Label(
            banner, 
            text="SPAIN CORPORATION", 
            font=("Poppins", 22, "bold"), 
            bg="#0A0F24", 
            fg="#D4AF37"
        ).pack(pady=35)

        # ---- Panel con animación ----
        self.panel_y_start = 1.5     # FUERA DE LA VENTANA
        self.panel_scale = 0.70      # empieza chico
        self.panel_target = 0.58     # posición final Y
        self.panel = tk.Frame(root, bg="#F2F2F2")

        # colocamos el panel inicialmente abajo
        self.panel.place(relx=0.5, rely=self.panel_y_start, anchor="center", width=380, height=330)

        # iniciar animación después de cargar UI
        self.root.after(200, self.animar_panel)

        # crear formulario
        self.modo = "login"
        self.crear_login()

    # -------------------------------------------------------------------
    # 🔥 ANIMACIÓN: panel sube desde abajo + efecto escala (suave)
    # -------------------------------------------------------------------
    def animar_panel(self, paso=0):
        if paso > 20:
            return

        # interpolación suave
        t = paso / 20

        # slide vertical
        new_y = self.panel_y_start + (self.panel_target - self.panel_y_start) * t
        self.panel.place_configure(rely=new_y)

        # escala (crece suavemente)
        escala = self.panel_scale + (1 - self.panel_scale) * t
        new_width = int(380 * escala)
        new_height = int(330 * escala)
        self.panel.place_configure(width=new_width, height=new_height)

        self.root.after(20, lambda: self.animar_panel(paso + 1))

    # ------------------- UI -------------------
    def limpiar_panel(self):
        for widget in self.panel.winfo_children():
            widget.destroy()

    def crear_login(self):
        self.limpiar_panel()
        self.modo = "login"

        tk.Label(self.panel, text="Iniciar Sesión", font=("Poppins", 18, "bold"),
                 bg="#F2F2F2", fg="#0A0F24").pack(pady=10)

        tk.Label(self.panel, text="Usuario:", bg="#F2F2F2").pack()
        self.usuario = tk.Entry(self.panel, font=("Poppins", 12))
        self.usuario.pack(pady=5)

        tk.Label(self.panel, text="Contraseña:", bg="#F2F2F2").pack()
        self.password = tk.Entry(self.panel, show="*", font=("Poppins", 12))
        self.password.pack(pady=5)

        tk.Button(self.panel, text="Entrar", font=("Poppins", 12, "bold"),
                  bg="#D4AF37", fg="black", width=20, command=self.login).pack(pady=10)

        tk.Button(self.panel, text="Registrar nuevo usuario",
                  font=("Poppins", 10, "bold"),
                  bg="#0A0F24", fg="white", width=20,
                  command=self.crear_registro).pack()

    def crear_registro(self):
        self.limpiar_panel()
        self.modo = "registro"

        tk.Label(self.panel, text="Registrar Usuario", font=("Poppins", 18, "bold"),
                 bg="#F2F2F2", fg="#0A0F24").pack(pady=10)

        tk.Label(self.panel, text="Nuevo usuario:", bg="#F2F2F2").pack()
        self.usuario = tk.Entry(self.panel, font=("Poppins", 12))
        self.usuario.pack(pady=5)

        tk.Label(self.panel, text="Contraseña:", bg="#F2F2F2").pack()
        self.password = tk.Entry(self.panel, show="*", font=("Poppins", 12))
        self.password.pack(pady=5)

        tk.Label(self.panel, text="Confirmar contraseña:", bg="#F2F2F2").pack()
        self.password_conf = tk.Entry(self.panel, show="*", font=("Poppins", 12))
        self.password_conf.pack(pady=5)

        tk.Button(self.panel, text="Registrar", font=("Poppins", 12, "bold"),
                  bg="#D4AF37", fg="black", width=20,
                  command=self.registrar_usuario).pack(pady=10)

        tk.Button(self.panel, text="Volver al login",
                  font=("Poppins", 10, "bold"),
                  bg="#0A0F24", fg="white", width=20,
                  command=self.crear_login).pack()

    # ------------------- LÓGICA -------------------
    def registrar_usuario(self):
        usuario = self.usuario.get().strip()
        password = self.password.get()
        password_conf = self.password_conf.get()

        if not usuario or not password:
            messagebox.showwarning("Error", "Complete todos los campos.")
            return
        if password != password_conf:
            messagebox.showwarning("Error", "Las contraseñas no coinciden.")
            return

        usuarios = cargar_usuarios()
        if usuario in usuarios:
            messagebox.showwarning("Error", "El usuario ya existe.")
            return

        usuarios[usuario] = password
        guardar_usuarios(usuarios)
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        self.crear_login()

    def login(self):
        usuario = self.usuario.get().strip()
        password = self.password.get()

        usuarios = cargar_usuarios()
        if usuario in usuarios and usuarios[usuario] == password:
            messagebox.showinfo("Bienvenido", f"Hola, {usuario}!")
            self.root.destroy()
            subprocess.Popen(["python", "main.py", "from_login"])
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginRegisterApp(root)
    root.mainloop()
