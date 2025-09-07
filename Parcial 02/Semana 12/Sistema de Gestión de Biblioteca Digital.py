import json
import os
from datetime import datetime, timedelta

# ===============================
# Clase Libro
# ===============================
class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        self.info = (titulo, autor)   # Tupla inmutable (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn

    def to_dict(self):
        return {
            "titulo": self.info[0],
            "autor": self.info[1],
            "categoria": self.categoria,
            "isbn": self.isbn
        }

# ===============================
# Clase Usuario
# ===============================
class Usuario:
    def __init__(self, nombre, user_id):
        self.nombre = nombre
        self.user_id = user_id
        self.libros_prestados = []  # lista de ISBN prestados

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "user_id": self.user_id,
            "libros_prestados": self.libros_prestados
        }

# ===============================
# Clase Biblioteca
# ===============================
class Biblioteca:
    def __init__(self, archivo_libros, archivo_usuarios, archivo_prestamos):
        self.archivo_libros = archivo_libros
        self.archivo_usuarios = archivo_usuarios
        self.archivo_prestamos = archivo_prestamos

        self.libros = self.cargar_datos(archivo_libros)
        self.usuarios = self.cargar_datos(archivo_usuarios)
        self.prestamos = self.cargar_datos(archivo_prestamos)

    # Cargar y guardar datos en JSON
    def cargar_datos(self, archivo):
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def guardar_datos(self, archivo, datos):
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    # ===============================
    # Métodos principales
    # ===============================
    def agregar_libro(self, libro):
        if libro.isbn in self.libros:
            print(" El libro ya existe en la biblioteca.")
        else:
            self.libros[libro.isbn] = libro.to_dict()
            self.guardar_datos(self.archivo_libros, self.libros)
            print("Libro agregado correctamente.")

    def quitar_libro(self, isbn):
        if isbn in self.libros:
            if isbn in self.prestamos and self.prestamos[isbn]["estado"] == "prestado":
                print("No se puede eliminar, el libro está prestado.")
            else:
                del self.libros[isbn]
                self.guardar_datos(self.archivo_libros, self.libros)
                print("Libro eliminado.")
        else:
            print(" Libro no encontrado.")

    def registrar_usuario(self, usuario):
        if usuario.user_id in self.usuarios:
            print(" El usuario ya está registrado.")
        else:
            self.usuarios[usuario.user_id] = usuario.to_dict()
            self.guardar_datos(self.archivo_usuarios, self.usuarios)
            print(" Usuario registrado correctamente.")

    def eliminar_usuario(self, user_id):
        if user_id in self.usuarios:
            if self.usuarios[user_id]["libros_prestados"]:
                print(" No se puede eliminar, el usuario tiene libros prestados.")
            else:
                del self.usuarios[user_id]
                self.guardar_datos(self.archivo_usuarios, self.usuarios)
                print(" Usuario eliminado.")
        else:
            print(" Usuario no encontrado.")

    def listar_usuarios(self):
        if not self.usuarios:
            print("No hay usuarios registrados.")
            return
        print("👥 Usuarios registrados:")
        for user in self.usuarios.values():
            print(f"- {user['nombre']} (ID: {user['user_id']})")

    def prestar_libro(self, user_id, isbn):
        if user_id not in self.usuarios:
            print("Usuario no encontrado.")
            return
        if isbn not in self.libros:
            print("Libro no encontrado.")
            return
        if isbn in self.prestamos and self.prestamos[isbn]["estado"] == "prestado":
            print("El libro ya está prestado.")
            return

        fecha_prestamo = datetime.now().strftime("%Y-%m-%d")
        fecha_devolucion = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        self.usuarios[user_id]["libros_prestados"].append(isbn)
        self.prestamos[isbn] = {
            "usuario": user_id,
            "fecha_prestamo": fecha_prestamo,
            "fecha_devolucion": fecha_devolucion,
            "estado": "prestado"
        }

        self.guardar_datos(self.archivo_usuarios, self.usuarios)
        self.guardar_datos(self.archivo_prestamos, self.prestamos)

        print("Libro prestado correctamente.")

    def devolver_libro(self, user_id, isbn):
        if isbn not in self.prestamos:
            print("Ese libro no estaba prestado.")
            return
        if self.prestamos[isbn]["usuario"] != user_id:
            print("Ese libro no lo tiene este usuario.")
            return

        self.usuarios[user_id]["libros_prestados"].remove(isbn)
        self.prestamos[isbn]["estado"] = "devuelto"

        self.guardar_datos(self.archivo_usuarios, self.usuarios)
        self.guardar_datos(self.archivo_prestamos, self.prestamos)

        print("Libro devuelto correctamente.")

    def buscar_libro(self, clave):
        resultados = []
        for libro in self.libros.values():
            if (clave.lower() in libro["titulo"].lower() or
                clave.lower() in libro["autor"].lower() or
                clave.lower() in libro["categoria"].lower()):
                resultados.append(libro)
        return resultados

    def listar_libros_prestados(self, user_id=None):
        if user_id:  # Lista libros de un usuario específico
            if user_id not in self.usuarios:
                print("Usuario no encontrado.")
                return []
            return self.usuarios[user_id]["libros_prestados"]
        else:  # Lista todos los libros prestados
            todos_prestados = []
            for isbn, info in self.prestamos.items():
                if info["estado"] in ["prestado", "atrasado"]:
                    usuario_nombre = self.usuarios[info["usuario"]]["nombre"]
                    libro_titulo = self.libros[isbn]["titulo"]
                    todos_prestados.append(f"{libro_titulo} (ISBN: {isbn}) - Prestado a {usuario_nombre}")
            return todos_prestados

# ===============================
# Menú principal
# ===============================
def menu():
    biblioteca = Biblioteca("libros.json", "usuarios.json", "prestamos.json")

    while True:
        print("\n MENÚ BIBLIOTECA")
        print("1. Agregar libro")
        print("2. Quitar libro")
        print("3. Registrar usuario")
        print("4. Eliminar usuario")
        print("5. Prestar libro")
        print("6. Devolver libro")
        print("7. Buscar libro")
        print("8. Listar libros prestados")
        print("9. Salir")
        print("10. Listar todos los usuarios registrados")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            categoria = input("Categoría: ")
            isbn = input("ISBN: ")
            libro = Libro(titulo, autor, categoria, isbn)
            biblioteca.agregar_libro(libro)

        elif opcion == "2":
            isbn = input("ISBN del libro a eliminar: ")
            biblioteca.quitar_libro(isbn)

        elif opcion == "3":
            nombre = input("Nombre del usuario: ")
            user_id = input("ID de usuario: ")
            usuario = Usuario(nombre, user_id)
            biblioteca.registrar_usuario(usuario)

        elif opcion == "4":
            user_id = input("ID del usuario a eliminar: ")
            biblioteca.eliminar_usuario(user_id)

        elif opcion == "5":
            user_id = input("ID del usuario: ")
            isbn = input("ISBN del libro: ")
            biblioteca.prestar_libro(user_id, isbn)

        elif opcion == "6":
            user_id = input("ID del usuario: ")
            isbn = input("ISBN del libro: ")
            biblioteca.devolver_libro(user_id, isbn)

        elif opcion == "7":
            clave = input("Buscar por título, autor o categoría: ")
            resultados = biblioteca.buscar_libro(clave)
            if resultados:
                print("Libros encontrados:")
                for r in resultados:
                    print(r)
            else:
                print("No se encontraron resultados.")

        elif opcion == "8":
            libros = biblioteca.listar_libros_prestados()
            if libros:
                print("Libros prestados:")
                for l in libros:
                    print("-", l)
            else:
                print(" No hay libros prestados.")

        elif opcion == "9":
            print("Saliendo del sistema...")
            break

        elif opcion == "10":
            biblioteca.listar_usuarios()

        else:
            print("Opción no válida.")

# ===============================
# Ejecución segura del programa
# ===============================
if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n Programa interrumpido por el usuario. Saliendo de forma segura...")
