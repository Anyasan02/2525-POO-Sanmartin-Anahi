import os

def mostrar_codigo_y_ejecutar(ruta_script):
    # Asegúrate de que la ruta al script es absoluta
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
            print(f"\n--- Código de {ruta_script} ---\n")
            print(codigo)
            print("\n--- Resultado de la ejecución ---\n")
            exec(codigo, globals())
    except FileNotFoundError:
        print(" El archivo no se encontró.")
    except Exception as e:
        print(f" Ocurrió un error al leer o ejecutar el archivo: {e}")

def mostrar_menu():
    # Define la ruta base donde se encuentra el dashboard.py
    ruta_base = os.path.dirname(__file__)


    opciones = {
        '1': 'Parcial 01/Semana 02/2.1. Tarea Semana 02.py',
        '2': 'Parcial 01/Semana 03/Promedio clima POO.py',
        '3': 'Parcial 01/Semana 03/Promedio clima  tradicional.py',
        '4': 'Parcial 01/Semana 04/EjemplosMundoReal_POO.py',
        '5': 'Parcial 01/Semana 05/Desarrollo de un Programa en Python.py',
        '6': 'Parcial 01/Semana 06/Aplicación de Conceptos de POO en Python.py',
        '7': 'Parcial 01/Semana 07/Constructores y Destructores.py',
    }

    while True:
        print("\n Menú Principal - Dashboard")
        for key in opciones:
            print(f"{key} - {opciones[key]}")
        print("0 - Salir")

        eleccion = input(" Elige un script para ver su código y ejecutarlo, o '0' para salir: ")
        if eleccion == '0':
            print("Saliendo del dashboard...")
            break
        elif eleccion in opciones:
            ruta_script = os.path.join(ruta_base, opciones[eleccion])
            mostrar_codigo_y_ejecutar(ruta_script)
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    mostrar_menu()
