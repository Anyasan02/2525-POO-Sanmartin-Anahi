"""
Aplicación GUI Básica con Tkinter

Descripción:
    Este programa implementa una interfaz gráfica de usuario (GUI) sencilla
    utilizando la librería Tkinter. La aplicación permite al usuario ingresar
    información mediante un campo de texto y almacenarla en una lista visual.
    Además, incluye botones para agregar nuevos datos y limpiar datos existentes.
"""

import tkinter as tk
from tkinter import messagebox

# ------------------ Funciones ------------------

def agregar_dato():
    """
    Captura el texto del campo de entrada y lo agrega a la lista.
    Si el campo está vacío, muestra un mensaje de advertencia.
    """
    dato = entry_dato.get().strip()  # Obtener el texto ingresado
    if dato:
        lista_datos.insert(tk.END, dato)  # Agregar a la lista
        entry_dato.delete(0, tk.END)      # Limpiar el campo de texto
    else:
        messagebox.showwarning("Advertencia", "Por favor ingresa un dato.")


def limpiar_datos():
    """
    Elimina el dato seleccionado de la lista.
    Si no hay selección, elimina todos los datos de la lista.
    """
    seleccion = lista_datos.curselection()
    if seleccion:  # Si hay un elemento seleccionado
        lista_datos.delete(seleccion)
    else:  # Si no hay selección, borrar toda la lista
        lista_datos.delete(0, tk.END)


# ------------------ Ventana Principal ------------------

ventana = tk.Tk()
ventana.title("Aplicación GUI Básica - Lista de Datos")
ventana.geometry("400x300")  # Tamaño fijo de la ventana

# ------------------ Etiqueta de Título ------------------
label_titulo = tk.Label(
    ventana,
    text="Gestor de Datos",
    font=("Arial", 14, "bold")
)
label_titulo.pack(pady=10)

# ------------------ Campo de Texto ------------------
entry_dato = tk.Entry(ventana, width=30)
entry_dato.pack(pady=5)

# ------------------ Frame para los Botones ------------------
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=5)

btn_agregar = tk.Button(frame_botones, text="Agregar", command=agregar_dato)
btn_agregar.grid(row=0, column=0, padx=5)

btn_limpiar = tk.Button(frame_botones, text="Limpiar", command=limpiar_datos)
btn_limpiar.grid(row=0, column=1, padx=5)

# ------------------ Lista para Mostrar Datos ------------------
lista_datos = tk.Listbox(ventana, width=40, height=10)
lista_datos.pack(pady=10)

# ------------------ Iniciar la Aplicación ------------------
ventana.mainloop()
