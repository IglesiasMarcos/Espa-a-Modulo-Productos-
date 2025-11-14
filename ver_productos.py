import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

PRODUCTOS_FILE = "productos.json"

# _______________________________________________
#   Función para obtener ID aunque tenga otro nombre
# _______________________________________________
def obtener_id(prod):
    return (
        prod.get("id")
        or prod.get("ID")
        or prod.get("Id")
        or prod.get("codigo")
        or prod.get("codigo_id")
        or prod.get("id_producto")
        or "N/A"
    )

class VerProductos:
    def __init__(self, root):
        self.root = root
        self.root.title("Listado de Productos — Spain CORP")
        self.root.geometry("1000x720")

        # ==============================
        #   PALETA DE COLORES ESPAÑA
        # ==============================
        ROJO = "#AA151B"
        AMARILLO = "#F1BF00"
        ROJO_OSCURO = "#7A1015"
        BLANCO = "#FFFFFF"

        self.root.configure(bg=ROJO)

        # Marco exterior amarillo 🇪🇸
        marco = tk.Frame(self.root, bg=AMARILLO, bd=5)
        marco.pack(expand=True, fill="both", padx=20, pady=20)

        # Contenedor interior blanco
        contenedor = tk.Frame(marco, bg=BLANCO)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)

        # Título
        titulo = tk.Label(
            contenedor,
            text="📦 Catálogo de Productos",
            font=("Arial", 26, "bold"),
            bg=BLANCO,
            fg=ROJO_OSCURO
        )
        titulo.pack(pady=5)

        # ==============================
        #   BUSCADOR 🔍
        # ==============================
        buscador_frame = tk.Frame(contenedor, bg=BLANCO)
        buscador_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            buscador_frame,
            text="🔍 Buscar:",
            font=("Arial", 14, "bold"),
            fg=ROJO_OSCURO,
            bg=BLANCO
        ).pack(side="left", padx=5)

        self.buscador_var = tk.StringVar()
        self.buscador_var.trace_add("write", self.filtrar_productos)

        entry_buscador = tk.Entry(
            buscador_frame,
            textvariable=self.buscador_var,
            font=("Arial", 13),
            width=40,
            relief="solid",
            bd=1
        )
        entry_buscador.pack(side="left", padx=10)

        # Botón limpiar
        tk.Button(
            buscador_frame,
            text="❌ Limpiar",
            font=("Arial", 11, "bold"),
            bg=ROJO,
            fg=BLANCO,
            command=self.limpiar_busqueda
        ).pack(side="left", padx=10)

        # ==============================
        #   CONFIGURACIÓN DEL TREEVIEW
        # ==============================
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview.Heading",
            background=ROJO,
            foreground=BLANCO,
            font=("Arial", 13, "bold"),
            borderwidth=1
        )

        style.configure(
            "Treeview",
            font=("Arial", 11),
            rowheight=28,
            fieldbackground=BLANCO,
            background=BLANCO
        )

        style.map("Treeview", background=[("selected", AMARILLO)])

        columnas = ("ID", "Nombre", "Precio", "Stock", "Descripción")

        self.tabla = ttk.Treeview(
            contenedor,
            columns=columnas,
            show="headings"
        )

        for col in columnas:
            self.tabla.heading(col, text=col)
            if col == "Descripción":
                self.tabla.column(col, width=350, anchor="w")
            else:
                self.tabla.column(col, width=150, anchor="center")

        self.tabla.pack(expand=True, fill="both", padx=10, pady=10)

        self.tabla.tag_configure("fila_par", background="#FFF7CC")
        self.tabla.tag_configure("fila_impar", background="#FFFFFF")

        # Cargar datos
        self.productos_completos = []
        self.cargar_productos()

        # Botón volver
        tk.Button(
            contenedor,
            text="⬅ Volver al menú",
            bg=ROJO,
            fg=BLANCO,
            font=("Arial", 12, "bold"),
            padx=10,
            pady=5,
            command=self.root.destroy
        ).pack(pady=10)

    # _______________________________________________
    #           Cargar productos del JSON
    # _______________________________________________
    def cargar_productos(self):
        if not os.path.exists(PRODUCTOS_FILE):
            messagebox.showerror("Error", "No se encontró productos.json")
            return

        with open(PRODUCTOS_FILE, "r", encoding="utf-8") as file:
            try:
                productos = json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "El archivo JSON está corrupto.")
                return

        self.productos_completos = productos
        self.mostrar_productos(productos)

    # _______________________________________________
    #           Mostrar productos en el treeview
    # _______________________________________________
    def mostrar_productos(self, lista):
        self.tabla.delete(*self.tabla.get_children())

        for i, prod in enumerate(lista):
            tag = "fila_par" if i % 2 == 0 else "fila_impar"
            self.tabla.insert(
                "",
                "end",
                values=(
                    obtener_id(prod),
                    prod.get("nombre", ""),
                    prod.get("precio", ""),
                    prod.get("stock", ""),
                    prod.get("descripcion", "")
                ),
                tags=(tag,)
            )

    # _______________________________________________
    #       Filtrado en tiempo real
    # _______________________________________________
    def filtrar_productos(self, *args):
        texto = self.buscador_var.get().lower().strip()

        if texto == "":
            self.mostrar_productos(self.productos_completos)
            return

        filtrados = []
        for p in self.productos_completos:
            cadena = (
                str(obtener_id(p)) + " " +
                str(p.get("nombre", "")) + " " +
                str(p.get("precio", "")) + " " +
                str(p.get("stock", "")) + " " +
                str(p.get("descripcion", ""))
            ).lower()

            if texto in cadena:
                filtrados.append(p)

        self.mostrar_productos(filtrados)

    # _______________________________________________
    #              Limpiar búsqueda
    # _______________________________________________
    def limpiar_busqueda(self):
        self.buscador_var.set("")
        self.mostrar_productos(self.productos_completos)


# _______________________________________________
#                  EJECUCIÓN DIRECTA
# _______________________________________________
if __name__ == "__main__":
    root = tk.Tk()
    VerProductos(root)
    root.mainloop()
