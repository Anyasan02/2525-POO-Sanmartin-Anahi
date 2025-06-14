
# Programa para calcular el promedio semanal del clima utilizando POO

class DiaClima:
    """
    Clase que representa la temperatura de un día específico.
    """
    def __init__(self, dia, temperatura):
        self._dia = dia  # Encapsulamiento
        self._temperatura = temperatura

    def obtener_temperatura(self):
        """
        Retorna la temperatura del día.
        """
        return self._temperatura


class SemanaClimatica:
    """
    Clase que representa una semana de temperaturas.
    """
    def __init__(self):
        self._dias = []

    def ingresar_temperaturas(self):
        """
        Solicita ingresar la temperatura de cada día y las guarda como objetos DiaClima.
        """
        for i in range(1, 6):
            temp = float(input(f"Ingrese la temperatura del día {i}: "))
            dia_clima = DiaClima(i, temp)
            self._dias.append(dia_clima)

    def calcular_promedio_semanal(self):
        """
        Calcula el promedio semanal de las temperaturas registradas.
        """
        total = sum(dia.obtener_temperatura() for dia in self._dias)
        return total / len(self._dias)

def main():
    print("PROMEDIO SEMANAL DEL CLIMA - PROGRAMACIÓN ORIENTADA A OBJETOS")
    semana = SemanaClimatica()
    semana.ingresar_temperaturas()
    promedio = semana.calcular_promedio_semanal()
    print(f"\nEl promedio semanal de temperatura es: {promedio:.2f}°C")

if __name__ == "__main__":
    main()
