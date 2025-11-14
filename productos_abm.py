import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ===============================
#      PALETA DE COLORES 🇪🇸
# ===============================
ROJO = "#AA151B"
AMARILLO = "#F1BF00"
ROJO_OSCURO = "#7A1015"
BLANCO = "#FFFFFF"
GRIS = "#EEEEEE"

# -------------------------------
# FUNCIONES DE MANEJO DE PRODUCTOS
# -------------------------------

def cargar_productos():
    if os.path.exists("productos.json"):
        with open("productos.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_productos():
    with open("productos.json", "w", encoding="utf-8") as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)

def actualizar_tabla():
    tabla.delete(*tabla.get_children())
    for p in productos:
        tabla.insert("", tk.END, values=(
            p["codigo"],
            p["nombre"],
            p["descripcion"],
            p["precio"],
            p["stock"],
            p["categoria"]
        ))

def limpiar_campos():
    entry_codigo.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_descripcion.delete("1.0", tk.END)
    entry_precio.delete(0, tk.END)
    combo_stock.set("")
    combo_categoria.set("")

def alta_producto():
    codigo = entry_codigo.get().strip()
    nombre = entry_nombre.get().strip()
    descripcion = entry_descripcion.get("1.0", tk.END).strip()
    precio = entry_precio.get().strip()
    stock = combo_stock.get()
    categoria = combo_categoria.get()

    if not codigo or not nombre or not precio:
        messagebox.showwarning("Campos obligatorios", "Código, nombre y precio son obligatorios.")
        return

    for p in productos:
        if p["codigo"] == codigo:
            messagebox.showerror("Error", "Ya existe un producto con ese código.")
            return

    nuevo = {
        "codigo": codigo,
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "stock": stock,
        "categoria": categoria
    }

    productos.append(nuevo)
    guardar_productos()
    actualizar_tabla()
    limpiar_campos()
    messagebox.showinfo("Éxito", "Producto agregado correctamente.")

def seleccionar_producto(event):
    seleccion = tabla.focus()
    if not seleccion:
        return
    valores = tabla.item(seleccion, "values")
    limpiar_campos()

    entry_codigo.insert(0, valores[0])
    entry_nombre.insert(0, valores[1])
    entry_descripcion.insert("1.0", valores[2])
    entry_precio.insert(0, valores[3])
    combo_stock.set(valores[4])
    combo_categoria.set(valores[5])

def modificar_producto():
    seleccion = tabla.focus()
    if not seleccion:
        messagebox.showwarning("Sin selección", "Seleccione un producto para modificar.")
        return

    codigo = entry_codigo.get().strip()
    for p in productos:
        if p["codigo"] == codigo:
            p["nombre"] = entry_nombre.get().strip()
            p["descripcion"] = entry_descripcion.get("1.0", tk.END).strip()
            p["precio"] = entry_precio.get().strip()
            p["stock"] = combo_stock.get()
            p["categoria"] = combo_categoria.get()

            guardar_productos()
            actualizar_tabla()
            limpiar_campos()
            messagebox.showinfo("Éxito", "Producto modificado correctamente.")
            return

def baja_producto():
    seleccion = tabla.focus()
    if not seleccion:
        messagebox.showwarning("Sin selección", "Seleccione un producto para eliminar.")
        return

    valores = tabla.item(seleccion, "values")
    codigo = valores[0]

    confirmar = messagebox.askyesno("Confirmar baja", f"¿Desea eliminar el producto '{valores[1]}'?")
    if not confirmar:
        return

    global productos
    productos = [p for p in productos if p["codigo"] != codigo]
    guardar_productos()
    actualizar_tabla()
    limpiar_campos()
    messagebox.showinfo("Éxito", "Producto eliminado correctamente.")


# -------------------------------
#      INTERFAZ GRÁFICA GUI 🇪🇸
# -------------------------------

root = tk.Tk()
root.title("Gestión de Productos — Spain CORP")
root.geometry("1000x700")
root.configure(bg=ROJO)

# Marco exterior amarillo
marco_principal = tk.Frame(root, bg=AMARILLO, bd=5)
marco_principal.pack(expand=True, fill="both", padx=20, pady=20)

# Contenedor interior blanco
contenedor = tk.Frame(marco_principal, bg=BLANCO)
contenedor.pack(expand=True, fill="both", padx=15, pady=15)

# Título
titulo = tk.Label(
    contenedor,
    text="🛠️ Gestión de Productos (ABM)",
    font=("Arial", 26, "bold"),
    bg=BLANCO,
    fg=ROJO_OSCURO
)
titulo.pack(pady=10)

# -------------------------------
#   FORMULARIO
# -------------------------------
frame_form = tk.Frame(contenedor, bg=BLANCO)
frame_form.pack(fill="x", pady=10)

def etiqueta(texto, fila):
    tk.Label(frame_form, text=texto, font=("Arial", 12, "bold"),
             bg=BLANCO, fg=ROJO_OSCURO).grid(row=fila, column=0, sticky="w", pady=5)

etiqueta("Código:", 0)
entry_codigo = tk.Entry(frame_form, font=("Arial", 12), width=25)
entry_codigo.grid(row=0, column=1, padx=10)

etiqueta("Nombre:", 1)
entry_nombre = tk.Entry(frame_form, font=("Arial", 12), width=25)
entry_nombre.grid(row=1, column=1, padx=10)

etiqueta("Descripción:", 2)
entry_descripcion = tk.Text(frame_form, font=("Arial", 12), width=40, height=3)
entry_descripcion.grid(row=2, column=1, padx=10, pady=5)

etiqueta("Precio:", 3)
entry_precio = tk.Entry(frame_form, font=("Arial", 12), width=25)
entry_precio.grid(row=3, column=1, padx=10)

etiqueta("Stock:", 4)
combo_stock = ttk.Combobox(frame_form, values=["Sin Stock", "Bajo", "Medio", "Alto"], font=("Arial", 12), width=23)
combo_stock.grid(row=4, column=1, padx=10)

etiqueta("Categoría:", 5)
combo_categoria = ttk.Combobox(frame_form, values=["Ropa", "Juguetes", "Accesorios", "Electrónica", "Otros"], font=("Arial", 12), width=23)
combo_categoria.grid(row=5, column=1, padx=10)

# -------------------------------
#   BOTONES CRUD
# -------------------------------
frame_botones = tk.Frame(contenedor, bg=BLANCO)
frame_botones.pack(fill="x", pady=10)

tk.Button(frame_botones, text="💾 Guardar", command=alta_producto,
          bg=ROJO, fg=BLANCO, font=("Arial", 12, "bold"),
          padx=15, pady=5).pack(side="left", padx=15)

tk.Button(frame_botones, text="✏️ Modificar", command=modificar_producto,
          bg=AMARILLO, fg=ROJO_OSCURO, font=("Arial", 12, "bold"),
          padx=15, pady=5).pack(side="left", padx=15)

tk.Button(frame_botones, text="🗑️ Eliminar", command=baja_producto,
          bg=ROJO_OSCURO, fg=BLANCO, font=("Arial", 12, "bold"),
          padx=15, pady=5).pack(side="left", padx=15)

tk.Button(frame_botones, text="🧹 Limpiar", command=limpiar_campos,
          bg=GRIS, fg="black", font=("Arial", 12, "bold"),
          padx=15, pady=5).pack(side="left", padx=15)

# -------------------------------
#   TABLA DE PRODUCTOS
# -------------------------------
style = ttk.Style()
style.theme_use("default")

style.configure(
    "Treeview.Heading",
    background=ROJO,
    foreground=BLANCO,
    font=("Arial", 12, "bold")
)

style.configure(
    "Treeview",
    font=("Arial", 11),
    rowheight=28,
    background=BLANCO,
    fieldbackground=BLANCO
)

columnas = ("Código", "Nombre", "Descripción", "Precio", "Stock", "Categoría")
tabla = ttk.Treeview(contenedor, columns=columnas, show="headings", height=10)

for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, anchor="center", width=150)

tabla.pack(expand=True, fill="both", padx=10, pady=10)
tabla.bind("<ButtonRelease-1>", seleccionar_producto)

# Cargar productos al iniciar
productos = cargar_productos()
actualizar_tabla()

root.mainloop()
