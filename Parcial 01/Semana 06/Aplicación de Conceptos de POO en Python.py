# tienda de electrodomesticos

# Clase base que representa un producto de la tienda (un electrodoméstico)
class Producto:
    def __init__(self, nombre, precio, stock, garantia_meses=0):
        # Atributos protegidos o privados para aplicar encapsulación
        self._nombre = nombre                   # Nombre del producto
        self._precio = precio                   # Precio del producto
        self.__stock = stock                    # Stock privado (encapsulado)
        self._garantia_meses = garantia_meses   # Garantía en meses (por defecto 0)

    # Metodo para mostrar la información del producto
    def mostrar_info(self):
        print(f"Electrodoméstico: {self._nombre}, Precio: ${self._precio:.2f}, "
              f"Stock: {self.__stock} unidades, Garantía: {self._garantia_meses} meses")

    # Metodo para modificar el stock (solo si es válido)
    def actualizar_stock(self, cantidad):
        if cantidad >= 0:
            self.__stock = cantidad
        else:
            print("Cantidad inválida")

    # Metodo para consultar el stock actual
    def get_stock(self):
        return self.__stock

    # Metodo para vender cierta candidad de productos
    def vender(self, cantidad):
        if cantidad <= self.__stock:
            self.__stock -= cantidad
            print(f"Se vendieron {cantidad} unidades de {self._nombre}")
        else:
            print(f"No hay suficiente stock de {self._nombre}")


# Clase derivada: representa productos electrónicos con garantía extendida
# HERENCIA: ProductoElectronico hereda de Producto
class ProductoElectronico(Producto):
    def __init__(self, nombre, precio, stock, garantia_meses):
        # Llamamos al constructor de la clase base con super()
        super().__init__(nombre, precio, stock, garantia_meses)

    # POLIMORFISMO: Sobrescribimos el metodo mostra_info
    def mostrar_info(self):
        print(f"[GARANTÍA EXTENDIDA] {self._nombre} - ${self._precio:.2f} | "
              f"Garantía: {self._garantia_meses} meses | Stock: {self.get_stock()}")


# Función principal donde se crean los productos y se prueban los métodos
def main():
    # Creamos dos productos: uno normal y otro con garantía extendida
    Cocina = Producto("Cocina ", 500.95, 30, 12) # Producto normal
    Batidora = ProductoElectronico("Batidora", 700.99, 10, 24) # Producto con garantía extendida

    # Mostramos la información de ambos productos
    Cocina.mostrar_info()
    Batidora.mostrar_info()

    # Probamos la encapsulación: acceder al stock solo por métodos
    print(f"\nStock actual de {Cocina._nombre}: {Cocina.get_stock()}")
    Cocina.actualizar_stock(25)  # Cambiar el stock
    print(f"Nuevo stock de {Cocina._nombre}: {Cocina.get_stock()}")

    # Vendemos unidades de ambos productos
    Cocina.vender(5)
    Batidora.vender(3)

    # Mostramos información actualizada después de las ventas
    print()
    Cocina.mostrar_info()
    Batidora.mostrar_info()


# Ejecutamos la función principal si el archivo se corre directamente
if __name__ == "__main__":
    main()

