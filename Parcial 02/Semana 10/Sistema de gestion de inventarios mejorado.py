import json
import os

# -------- Clase Producto --------
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def to_dict(self):
        return {
            "id": self.id_producto,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    def __str__(self):
        return f"ID: {self.id_producto} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"


# -------- Clase Inventario --------
class Inventario:
    def __init__(self, archivo="inventario.json"):
        self.archivo = archivo
        self.productos = {}
        self.cargar_desde_archivo()

    def cargar_desde_archivo(self):
        if not os.path.exists(self.archivo):
            # Crear archivo si no existe
            with open(self.archivo, "w") as f:
                json.dump({}, f)
        try:
            with open(self.archivo, "r") as f:
                self.productos = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.productos = {}
            print("Advertencia: archivo de inventario vacío o dañado. Se inicializó un inventario nuevo.")
        except PermissionError:
            print("Error: no se tienen permisos para leer el archivo.")

    def guardar_en_archivo(self):
        try:
            with open(self.archivo, "w") as f:
                json.dump(self.productos, f, indent=4)
            print("Inventario actualizado en el archivo.")
        except PermissionError:
            print("Error: no se tienen permisos para escribir en el archivo.")

    def agregar_producto(self, producto):
        if producto.id_producto in self.productos:
            print("Error: Ya existe un producto con ese ID.")
            return
        self.productos[producto.id_producto] = producto.to_dict()
        self.guardar_en_archivo()
        print("Producto añadido con éxito.")

    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]
            self.guardar_en_archivo()
            print("Producto eliminado con éxito.")
        else:
            print("Error: Producto no encontrado.")

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        if id_producto in self.productos:
            if nueva_cantidad is not None:
                self.productos[id_producto]["cantidad"] = nueva_cantidad
            if nuevo_precio is not None:
                self.productos[id_producto]["precio"] = nuevo_precio
            self.guardar_en_archivo()
            print("Producto actualizado con éxito.")
        else:
            print("Error: Producto no encontrado.")

    def buscar_producto(self, nombre):
        encontrados = [p for p in self.productos.values() if nombre.lower() in p["nombre"].lower()]
        if encontrados:
            print("Resultados de la búsqueda:")
            for p in encontrados:
                print(f"ID: {p['id']} | Nombre: {p['nombre']} | Cantidad: {p['cantidad']} | Precio: ${p['precio']:.2f}")
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_todos(self):
        if not self.productos:
            print("El inventario está vacío.")
        else:
            print("\nInventario actual:")
            for p in self.productos.values():
                print(f"ID: {p['id']} | Nombre: {p['nombre']} | Cantidad: {p['cantidad']} | Precio: ${p['precio']:.2f}")


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
