# -------- Clase Producto --------
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Getters
    def get_id(self):
        return self.id_producto

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio

    # Setters
    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def set_precio(self, precio):
        self.precio = precio

    def __str__(self):
        return f"ID: {self.id_producto} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"


# -------- Clase Inventario --------
class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        for p in self.productos:
            if p.get_id() == producto.get_id():
                print("Error: Ya existe un producto con ese ID.")
                return
        self.productos.append(producto)
        print("Producto añadido con éxito.")

    def eliminar_producto(self, id_producto):
        for p in self.productos:
            if p.get_id() == id_producto:
                self.productos.remove(p)
                print("Producto eliminado con éxito.")
                return
        print("Error: Producto no encontrado.")

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        for p in self.productos:
            if p.get_id() == id_producto:
                if nueva_cantidad is not None:
                    p.set_cantidad(nueva_cantidad)
                if nuevo_precio is not None:
                    p.set_precio(nuevo_precio)
                print("Producto actualizado con éxito.")
                return
        print("Error: Producto no encontrado.")

    def buscar_producto(self, nombre):
        encontrados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        if encontrados:
            print("Resultados de la búsqueda:")
            for p in encontrados:
                print(p)
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_todos(self):
        if not self.productos:
            print("El inventario está vacío.")
        else:
            print("\nInventario actual:")
            for p in self.productos:
                print(p)


# -------- Menú de Consola --------
def menu():
    inventario = Inventario()

    while True:
        print("\n=== Sistema de Gestión de Inventario ===")
        print("1. Añadir producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar producto (cantidad y/o precio)")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")

        try:
            opcion = input("Seleccione una opción: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSe interrumpió la ejecución. Saliendo del sistema...")
            break

        if opcion == "1":
            id_p = input("Ingrese ID del producto: ").strip()
            nombre = input("Ingrese nombre del producto: ").strip()
            try:
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
            except ValueError:
                print("Error: cantidad y precio deben ser numéricos.")
                continue
            producto = Producto(id_p, nombre, cantidad, precio)
            inventario.agregar_producto(producto)

        elif opcion == "2":
            id_p = input("Ingrese ID del producto a eliminar: ").strip()
            inventario.eliminar_producto(id_p)

        elif opcion == "3":
            id_p = input("Ingrese ID del producto a actualizar: ").strip()
            nueva_cantidad = input("Ingrese nueva cantidad (o deje en blanco): ").strip()
            nuevo_precio = input("Ingrese nuevo precio (o deje en blanco): ").strip()

            nueva_cantidad = int(nueva_cantidad) if nueva_cantidad else None
            nuevo_precio = float(nuevo_precio) if nuevo_precio else None

            inventario.actualizar_producto(id_p, nueva_cantidad, nuevo_precio)

        elif opcion == "4":
            nombre = input("Ingrese nombre a buscar: ").strip()
            inventario.buscar_producto(nombre)

        elif opcion == "5":
            inventario.mostrar_todos()

        elif opcion == "6":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida, intente de nuevo.")


# -------- Punto de Entrada --------
if __name__ == "__main__":
    menu()
