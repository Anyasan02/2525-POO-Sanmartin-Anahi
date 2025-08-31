import json
import os

class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

class Inventario:
    def __init__(self, archivo="inventario.json"):
        self.archivo = archivo
        self.productos = {}
        self.cargar()

    def cargar(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                data = json.load(f)
                for item in data.values():
                    producto = Producto(item["id"], item["nombre"], item["cantidad"], item["precio"])
                    self.productos[item["id"]] = producto

    def guardar(self):
        data = {id: vars(p) for id, p in self.productos.items()}
        with open(self.archivo, "w") as f:
            json.dump(data, f, indent=4)

    def agregar(self, producto):
        if producto.id in self.productos:
            print("\nYa existe un producto con ese ID.\n")
        else:
            self.productos[producto.id] = producto
            print("\nProducto agregado correctamente.\n")

    def eliminar(self, id):
        if id in self.productos:
            del self.productos[id]
            print("\nProducto eliminado correctamente.\n")
        else:
            print("\nNo se encontró un producto con ese ID.\n")

    def actualizar_cantidad(self, id, nueva_cantidad):
        if id in self.productos:
            self.productos[id].cantidad = nueva_cantidad
            print("\nCantidad actualizada correctamente.\n")
        else:
            print("\nNo se encontró un producto con ese ID.\n")

    def actualizar_precio(self, id, nuevo_precio):
        if id in self.productos:
            self.productos[id].precio = nuevo_precio
            print("\nPrecio actualizado correctamente.\n")
        else:
            print("\nNo se encontró un producto con ese ID.\n")

    def buscar_por_nombre(self, nombre):
        encontrados = [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]
        if encontrados:
            print("\n" + "-" * 50)
            print(f"{'ID':<8} | {'Nombre':<15} | {'Cantidad':<10} | {'Precio':<10}")
            print("-" * 50)
            for producto in encontrados:
                print(f"{producto.id:<8} | {producto.nombre:<15} | {producto.cantidad:<10} | ${producto.precio:<10.2f}")
            print("-" * 50 + "\n")
        else:
            print("\nNo se encontraron productos con ese nombre.\n")

    def mostrar_todo(self):
        if not self.productos:
            print("\nEl inventario está vacío.\n")
            return

        print("\n" + "-" * 50)
        print(f"{'ID':<8} | {'Nombre':<15} | {'Cantidad':<10} | {'Precio':<10}")
        print("-" * 50)

        for producto in self.productos.values():
            print(f"{producto.id:<8} | {producto.nombre:<15} | {producto.cantidad:<10} | ${producto.precio:<10.2f}")

        print("-" * 50 + "\n")


# =============================
# Menú principal
# =============================
def menu():
    inventario = Inventario()

    try:
        while True:
            print("====== MENÚ DE INVENTARIO ======")
            print("1. Añadir producto")
            print("2. Eliminar producto")
            print("3. Actualizar cantidad")
            print("4. Actualizar precio")
            print("5. Buscar producto por nombre")
            print("6. Mostrar todo el inventario")
            print("7. Guardar inventario manualmente")
            print("8. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                id = input("Ingrese ID: ")
                nombre = input("Ingrese nombre: ")
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
                inventario.agregar(Producto(id, nombre, cantidad, precio))

            elif opcion == "2":
                id = input("Ingrese ID del producto a eliminar: ")
                inventario.eliminar(id)

            elif opcion == "3":
                id = input("Ingrese ID del producto: ")
                cantidad = int(input("Ingrese nueva cantidad: "))
                inventario.actualizar_cantidad(id, cantidad)

            elif opcion == "4":
                id = input("Ingrese ID del producto: ")
                precio = float(input("Ingrese nuevo precio: "))
                inventario.actualizar_precio(id, precio)

            elif opcion == "5":
                nombre = input("Ingrese nombre del producto: ")
                inventario.buscar_por_nombre(nombre)

            elif opcion == "6":
                inventario.mostrar_todo()

            elif opcion == "7":
                inventario.guardar()
                print("\nInventario guardado correctamente.\n")

            elif opcion == "8":
                inventario.guardar()
                print("\nSaliendo del sistema. Hasta luego!\n")
                break

            else:
                print("\nOpción inválida. Intente de nuevo.\n")

    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
        inventario.guardar()
        print("Inventario guardado antes de salir.\n")


# Ejecutar programa
if __name__ == "__main__":
    menu()
