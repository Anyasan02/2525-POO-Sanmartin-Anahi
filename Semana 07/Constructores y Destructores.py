class Accesorio:
    """
    Clase que representa un accesorio para mascotas.
    """

    def __init__(self, nombre, tipo, precio):
        """
        Constructor: Se ejecuta al crear un nuevo accesorio.
        Inicializa el nombre, tipo (ej. arena de gato, cama) y precio del accesorio.
        """
        self.nombre = nombre
        self.tipo = tipo
        self.precio = precio
        print(f"[NUEVO] Accesorio agregado: {self.nombre} ({self.tipo}) - ${self.precio:.2f}")

    def mostrar_info(self):
        """
        Muestra la informacion del accesorio.
        """
        print(f"🐶 {self.nombre} - Tipo: {self.tipo} - Precio: ${self.precio:.2f}")

    def __del__(self):
        """
        Destructor: Se ejecuta automáticamente cuando el objeto es destruido.
        Simula la eliminación del accesorio del inventario.
        """
        print(f"[ELIMINADO] Accesorio '{self.nombre}' eliminado del inventario.")


class TiendaMascotas:
    """
    Clase que representa la tienda virtual de accesorios para mascotas.
    """

    def __init__(self):
        """
        Constructor: Inicializa una lista vacía de accesorios.
        """
        self.inventario = []
        print("[INICIO] Tienda virtual de mascotas iniciada.")

    def agregar_accesorio(self, nombre, tipo, precio):
        """
        Agrega un nuevo accesorio al inventario.
        """
        nuevo_accesorio = Accesorio(nombre, tipo, precio)
        self.inventario.append(nuevo_accesorio)

    def mostrar_inventario(self):
        """
        Muestra todos los accesorios disponibles.
        """
        print("\n📦 Inventario actual:")
        for accesorio in self.inventario:
            accesorio.mostrar_info()

    def cerrar_tienda(self):
        """
        Vacía el inventario y activa los destructores.
        """
        print("\n[CERRANDO] Cerrando tienda. Eliminando accesorios del inventario...")
        self.inventario.clear()  # Al borrar las referencias, los destructores se activan


# Programa principal
if __name__ == "__main__":
    tienda = TiendaMascotas()

    tienda.agregar_accesorio("Cama acolchada", "Cama", 30.99)
    tienda.agregar_accesorio("Arena para gato", "Arena", 10.50)
    tienda.agregar_accesorio("Alimento humedo ", "Alimento", 9.75)

    tienda.mostrar_inventario()

    # Al finalizar el programa, o al llamar este metodo, se eliminan los objetos
    tienda.cerrar_tienda()
