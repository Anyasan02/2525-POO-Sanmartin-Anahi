# Programa para calcular el costo total con IVA en una tienda de mascotas
# Solicita el precio unitario, porcentaje de IVA y la cantidad de productos,
# y muestra el monto de IVA y el total a pagar.

def calcular_iva(precio_unitario, porcentaje_iva):
    """
    Calcula el monto del IVA para un precio unitario.
    """
    return precio_unitario * (porcentaje_iva / 100)

# Programa principal
print("Calculadora de IVA - Tienda de Mascotas 🐾")

try:
    # Solicitar precio unitario del producto
    precio_input = input("Ingresa el precio unitario del producto para mascotas ($): ")
    precio_unitario = float(precio_input)

    # Solicitar porcentaje de IVA
    porcentaje_input = input("Ingresa el porcentaje de IVA (%): ")
    porcentaje_iva = float(porcentaje_input)

    # Solicitar cantidad de productos
    cantidad_input = input("Ingresa la cantidad de productos: ")
    cantidad_productos = int(cantidad_input)

    # Validar valores positivos
    if precio_unitario < 0 or porcentaje_iva < 0 or cantidad_productos <= 0:
        print("Error: Ingresa valores positivos válidos.")
    else:
        # Calcular el IVA por unidad
        monto_iva_unitario = calcular_iva(precio_unitario, porcentaje_iva)

        # Calcular precio final por unidad con IVA
        precio_unitario_con_iva = precio_unitario + monto_iva_unitario

        # Calcular el total general
        total_pagar = precio_unitario_con_iva * cantidad_productos

        # Booleano para verificar si se considera "compra mayorista"
        compra_mayorista = cantidad_productos >= 10

        # Mostrar resultados
        print(f"\nMonto de IVA por unidad: ${monto_iva_unitario:.2f}")
        print(f"Precio unitario con IVA: ${precio_unitario_con_iva:.2f}")
        print(f"Cantidad de productos: {cantidad_productos}")
        print(f"Total a pagar: ${total_pagar:.2f}")

        if compra_mayorista:
            print("¡Compra mayorista! Aplica descuento en tienda.")
        else:
            print("Compra normal.")
except ValueError:
    print("Error: Ingresa valores numéricos válidos.")
