#tienda virtual

# Clase Producto representa un producto que se vende en la tienda
class Producto:
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def mostrar_info(self):
        print(f"Producto: {self.nombre} - Precio: ${self.precio} - Stock: {self.stock} unidades")

    def actualizar_stock(self, cantidad):
        self.stock += cantidad

# Clase Cliente representa un cliente que puede comprar productos
class Cliente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.carrito = []

    def agregar_al_carrito(self, producto, cantidad):
        if producto.stock >= cantidad:
            self.carrito.append((producto, cantidad))
            producto.stock -= cantidad
            print(f"{cantidad} unidad(es) de {producto.nombre} agregadas al carrito.")
        else:
            print(f"No hay suficiente stock de {producto.nombre}.")

    def ver_carrito(self):
        print(f"Carrito de {self.nombre}:")
        for producto, cantidad in self.carrito:
            print(f"  - {producto.nombre} x{cantidad}")

# Clase Tienda para gestionar productos y clientes
class Tienda:
    def __init__(self, nombre):
        self.nombre = nombre
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def mostrar_productos(self):
        print(f"Productos disponibles en {self.nombre}:")
        for producto in self.productos:
            producto.mostrar_info()


# Ejemplo de uso
if __name__ == "__main__":
    # Crear una tienda
    tienda = Tienda("TechStore")

    # Crear productos
    producto1 = Producto("Teclado", 25.50, 10)
    producto2 = Producto("Parlante", 15.99, 20)

    # Agregar productos a la tienda
    tienda.agregar_producto(producto1)
    tienda.agregar_producto(producto2)

    # Mostrar productos
    tienda.mostrar_productos()

    # Crear cliente
    cliente = Cliente("Coraline")

    # Cliente agrega productos al carrito
    cliente.agregar_al_carrito(producto1, 2)
    cliente.agregar_al_carrito(producto2, 1)

    # Ver carrito del cliente
    cliente.ver_carrito()

    # Mostrar productos después de la compra
    tienda.mostrar_productos()
