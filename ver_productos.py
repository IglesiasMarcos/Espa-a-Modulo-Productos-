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
        self.root.geometry("1200x800")

        # ==============================
        #   PALETA DE COLORES ESPAÑA
        # ==============================
        ROJO = "#AA151B"
        AMARILLO = "#F1BF00"
        ROJO_OSCURO = "#7A1015"
        BLANCO = "#FFFFFF"

        self.root.configure(bg=ROJO)

        # ==============================
        #   CARRITO (diccionario)
        # ==============================
        self.carrito = {}  # {id_producto: {"nombre": ..., "precio": ..., "cantidad": ...}}
        self.carrito_expandido = False  # Estado del carrito (expandido/contraído)

        # Marco exterior amarillo 🇪🇸
        marco = tk.Frame(self.root, bg=AMARILLO, bd=5)
        marco.pack(expand=True, fill="both", padx=20, pady=20)

        # Contenedor interior blanco (con dos secciones: productos y carrito)
        contenedor = tk.Frame(marco, bg=BLANCO)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)

        # ==============================
        #   DIVISIÓN PRINCIPAL (L y R)
        # ==============================
        # Lado izquierdo: Productos
        left_frame = tk.Frame(contenedor, bg=BLANCO)
        left_frame.pack(side="left", expand=True, fill="both", padx=5, pady=5)

        # Título (LEFT)
        titulo = tk.Label(
            left_frame,
            text="📦 Catálogo de Productos",
            font=("Arial", 26, "bold"),
            bg=BLANCO,
            fg=ROJO_OSCURO
        )
        titulo.pack(pady=5)

        # Lado derecho: Carrito (inicialmente colapsado)
        right_frame = tk.Frame(contenedor, bg=BLANCO)
        right_frame.pack(side="right", fill="y", padx=5, pady=5)
        
        # Frame para el botón de toggle y el carrito
        self.carrito_container = tk.Frame(right_frame, bg=BLANCO, relief="solid", bd=2)
        self.carrito_container.pack(fill="y")
        
        # Botón para expandir/contraer carrito
        self.btn_carrito_toggle = tk.Button(
            self.carrito_container,
            text="🛒",
            font=("Arial", 18, "bold"),
            bg=AMARILLO,
            fg=ROJO_OSCURO,
            command=self.toggle_carrito,
            padx=5,
            pady=5,
            relief="solid",
            bd=2
        )
        self.btn_carrito_toggle.pack(fill="x", padx=2, pady=2)

        # ==============================
        #   BUSCADOR 🔍 (LEFT)
        # ==============================
        buscador_frame = tk.Frame(left_frame, bg=BLANCO)
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
            left_frame,
            columns=columnas,
            show="headings"
        )

        for col in columnas:
            self.tabla.heading(col, text=col)
            if col == "Descripción":
                self.tabla.column(col, width=250, anchor="w")
            else:
                self.tabla.column(col, width=120, anchor="center")

        self.tabla.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Botón para agregar al carrito (LEFT)
        btn_agregar = tk.Button(
            left_frame,
            text="➕ Agregar al carrito",
            bg=AMARILLO,
            fg=ROJO_OSCURO,
            font=("Arial", 11, "bold"),
            padx=10,
            pady=5,
            command=self.agregar_al_carrito
        )
        btn_agregar.pack(pady=5)

        self.tabla.tag_configure("fila_par", background="#FFF7CC")
        self.tabla.tag_configure("fila_impar", background="#FFFFFF")

        # Cargar datos
        self.productos_completos = []
        self.cargar_productos()

        # ==============================
        #   PANEL DEL CARRITO (RIGHT)
        # ==============================
        titulo_carrito = tk.Label(
            self.carrito_container,
            text="🛒 Carrito de Compras",
            font=("Arial", 16, "bold"),
            bg=BLANCO,
            fg=ROJO_OSCURO
        )
        titulo_carrito.pack(pady=5)

        # Tabla del carrito
        columnas_carrito = ("Nombre", "Precio", "Cant.", "Subtotal")
        
        self.tabla_carrito = ttk.Treeview(
            self.carrito_container,
            columns=columnas_carrito,
            show="headings",
            height=10
        )
        
        for col in columnas_carrito:
            self.tabla_carrito.heading(col, text=col)
            if col == "Nombre":
                self.tabla_carrito.column(col, width=120, anchor="w")
            else:
                self.tabla_carrito.column(col, width=80, anchor="center")
        
        self.tabla_carrito.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Botón para quitar del carrito
        btn_quitar = tk.Button(
            self.carrito_container,
            text="❌ Quitar seleccionado",
            bg=ROJO,
            fg=BLANCO,
            font=("Arial", 10, "bold"),
            command=self.quitar_del_carrito
        )
        btn_quitar.pack(pady=5, fill="x", padx=5)
        
        # Total del carrito
        total_frame = tk.Frame(self.carrito_container, bg=BLANCO)
        total_frame.pack(fill="x", padx=5, pady=10)
        
        tk.Label(
            total_frame,
            text="Total:",
            font=("Arial", 13, "bold"),
            bg=BLANCO,
            fg=ROJO_OSCURO
        ).pack(side="left")
        
        self.label_total = tk.Label(
            total_frame,
            text="$0.00",
            font=("Arial", 13, "bold"),
            bg=BLANCO,
            fg=ROJO
        )
        self.label_total.pack(side="right")
        
        # Botón limpiar carrito
        btn_limpiar_carrito = tk.Button(
            self.carrito_container,
            text="🗑️ Limpiar carrito",
            bg=AMARILLO,
            fg=ROJO_OSCURO,
            font=("Arial", 10, "bold"),
            command=self.limpiar_carrito
        )
        btn_limpiar_carrito.pack(pady=5, fill="x", padx=5)
        
        # Inicialmente contraer el carrito (ocultar contenido excepto botón)
        self.contraer_carrito()

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

        # Normalizar y calcular stock numérico en memoria para cada producto
        STOCK_MAP = {
            "Alto": 30,
            "alto": 30,
            "Medio": 15,
            "medio": 15,
            "Bajo": 5,
            "bajo": 5,
            "Sin Stock": 0,
            "sin stock": 0,
            "SinStock": 0,
            "nostock": 0,
        }

        for p in productos:
            # Preferir campos numéricos existentes
            qty = None
            # Algunos JSON pueden tener un campo 'stock' como número o como texto
            stock_field = p.get("stock")
            if isinstance(stock_field, int):
                qty = stock_field
            else:
                try:
                    # si es string con dígitos (ej '10')
                    if isinstance(stock_field, str) and stock_field.strip().isdigit():
                        qty = int(stock_field.strip())
                except Exception:
                    qty = None

            if qty is None:
                # Mapear por etiqueta cualitativa
                if isinstance(stock_field, str) and stock_field in STOCK_MAP:
                    qty = STOCK_MAP[stock_field]
                else:
                    # fallback: si no hay campo, 0
                    qty = 0

            # almacenar en campo interno para manejo en runtime (no sobrescribe JSON original)
            p["_stock_qty"] = qty

        self.productos_completos = productos
        self.mostrar_productos(productos)

    def buscar_producto_por_id(self, id_producto):
        """Buscar producto en la lista `productos_completos` por su id (usar obtener_id)."""
        for p in self.productos_completos:
            if str(obtener_id(p)) == str(id_producto):
                return p
        return None

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
                    prod.get("_stock_qty", prod.get("stock", "")),
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
#         MÉTODOS PARA EXPANDIR/CONTRAER CARRITO
# _______________________________________________
    def toggle_carrito(self):
        """Alterna entre expandir y contraer el carrito"""
        if self.carrito_expandido:
            self.contraer_carrito()
        else:
            self.expandir_carrito()
    
    def expandir_carrito(self):
        """Mostrar el contenido del carrito"""
        self.carrito_expandido = True
        self.btn_carrito_toggle.config(text="🛒 ▲")
        
        # Mostrar widgets del carrito
        for widget in self.carrito_container.winfo_children():
            if widget != self.btn_carrito_toggle:
                widget.pack(side="top", fill="x", expand=True, pady=2)
    
    def contraer_carrito(self):
        """Ocultar el contenido del carrito"""
        self.carrito_expandido = False
        # Ocultar widgets del carrito (excepto el botón toggle)
        for widget in self.carrito_container.winfo_children():
            if widget != self.btn_carrito_toggle:
                widget.pack_forget()


# _______________________________________________
#              MÉTODOS DEL CARRITO
# _______________________________________________
    def agregar_al_carrito(self):
        """Agregar producto seleccionado al carrito"""
        seleccion = self.tabla.selection()
        
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un producto primero")
            return
        
        item = self.tabla.item(seleccion[0])
        valores = item["values"]
        
        id_producto = valores[0]
        nombre = valores[1]

        # Limpiar precio: remover $, puntos y convertir a float
        precio_str = str(valores[2]).replace("$", "").replace(".", "").strip()
        try:
            precio = float(precio_str) if precio_str else 0
        except ValueError:
            precio = 0

        # Buscar producto real y verificar stock
        producto = self.buscar_producto_por_id(id_producto)
        if producto is None:
            messagebox.showerror("Error", "No se encontró el producto en la lista interna.")
            return

        disponible = int(producto.get("_stock_qty", 0))
        if disponible <= 0:
            messagebox.showwarning("Sin stock", f"El producto '{nombre}' no tiene stock disponible")
            return

        # Decrementar stock disponible en memoria
        producto["_stock_qty"] = disponible - 1

        # Si ya está en el carrito, aumentar cantidad
        if id_producto in self.carrito:
            self.carrito[id_producto]["cantidad"] += 1
        else:
            self.carrito[id_producto] = {
                "nombre": nombre,
                "precio": precio,
                "cantidad": 1
            }

        # Actualizar vistas
        self.actualizar_carrito()
        self.mostrar_productos(self.productos_completos)

        # Expandir carrito automáticamente
        if not self.carrito_expandido:
            self.expandir_carrito()

        messagebox.showinfo("Éxito", f"✅ {nombre} agregado al carrito")
    
    def quitar_del_carrito(self):
        """Quitar producto seleccionado del carrito"""
        seleccion = self.tabla_carrito.selection()
        
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un item del carrito")
            return
        
        item = self.tabla_carrito.item(seleccion[0])
        valores = item["values"]
        nombre = valores[0]
        
        # Buscar y eliminar por nombre; restaurar stock en la lista de productos
        for id_prod, datos in list(self.carrito.items()):
            if datos["nombre"] == nombre:
                cantidad = datos.get("cantidad", 1)
                producto = self.buscar_producto_por_id(id_prod)
                if producto is not None:
                    producto["_stock_qty"] = producto.get("_stock_qty", 0) + cantidad
                # eliminar del carrito
                del self.carrito[id_prod]
                break

        self.actualizar_carrito()
        self.mostrar_productos(self.productos_completos)
        messagebox.showinfo("Éxito", f"❌ {nombre} removido del carrito")
    
    def limpiar_carrito(self):
        """Vaciar el carrito completamente"""
        if not self.carrito:
            messagebox.showinfo("Información", "El carrito ya está vacío")
            return
        
        confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de limpiar el carrito?")
        if confirmar:
            self.carrito = {}
            self.actualizar_carrito()
            messagebox.showinfo("Éxito", "🗑️ Carrito vaciado")
    
    def actualizar_carrito(self):
        """Actualizar la visualización del carrito y el total"""
        self.tabla_carrito.delete(*self.tabla_carrito.get_children())
        
        total = 0
        
        for id_prod, datos in self.carrito.items():
            nombre = datos["nombre"]
            precio = datos["precio"]
            cantidad = datos["cantidad"]
            subtotal = precio * cantidad
            total += subtotal
            
            self.tabla_carrito.insert(
                "",
                "end",
                values=(
                    nombre,
                    f"${precio:.2f}",
                    cantidad,
                    f"${subtotal:.2f}"
                )
            )
        
        # Actualizar total
        self.label_total.config(text=f"${total:.2f}")


# _______________________________________________
#                  EJECUCIÓN DIRECTA
# _______________________________________________
if __name__ == "__main__":
    root = tk.Tk()
    VerProductos(root)
    root.mainloop()
