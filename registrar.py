import tkinter as tk
from tkinter import ttk, messagebox
import json, os

USERS_FILE = "usuarios.json"

def guardar_usuario():
    usuario = entry_usuario.get()
    password = entry_password.get()

    if not usuario or not password:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    usuarios = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            usuarios = json.load(f)

    if usuario in usuarios:
        messagebox.showerror("Error", "El usuario ya existe")
    else:
        usuarios[usuario] = password
        with open(USERS_FILE, "w") as f:
            json.dump(usuarios, f, indent=4)
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        root.destroy()

root = tk.Tk()
root.title("Registrar - SPAIN CORPORATION")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="REGISTRAR", font=("Arial", 22, "bold")).pack(pady=20)
tk.Label(root, text="Usuario:").pack()
entry_usuario = tk.Entry(root, width=30)
entry_usuario.pack()

tk.Label(root, text="Contraseña:").pack()
entry_password = tk.Entry(root, width=30, show="*")
entry_password.pack()

ttk.Button(root, text="Registrar", command=guardar_usuario).pack(pady=20)
ttk.Button(root, text="Volver", command=root.destroy).pack()

root.mainloop()
