
# Programa para calcular el promedio semanal del clima utilizando programación tradicional

def ingresar_temperaturas():
    """
    Solicita al usuario ingresar la temperatura diaria durante 5 días.
    Retorna una lista con las temperaturas ingresadas.
    """
    temperaturas = []
    for dia in range(1, 6):
        temp = float(input(f"Ingrese la temperatura del día {dia}: "))
        temperaturas.append(temp)
    return temperaturas

def calcular_promedio(temperaturas):
    """
    Calcula el promedio de una lista de temperaturas.
    """
    return sum(temperaturas) / len(temperaturas)

def main():
    print("PROMEDIO SEMANAL DEL CLIMA - PROGRAMACIÓN TRADICIONAL")
    temperaturas = ingresar_temperaturas()
    promedio = calcular_promedio(temperaturas)
    print(f"\nEl promedio semanal de temperatura es: {promedio:.2f}°C")

if __name__ == "__main__":
    main()
