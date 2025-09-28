import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.configure(bg="#f3e6f9")  # Fondo lila suave
        self.tasks = []

        # ===== Marco superior centrado =====
        top_frame = tk.Frame(root, bg="#f3e6f9")
        top_frame.grid(row=0, column=0, pady=10, sticky="ew")
        top_frame.columnconfigure(0, weight=1)

        center_frame = tk.Frame(top_frame, bg="#f3e6f9")
        center_frame.grid(row=0, column=0)

        # Entrada de texto para la tarea
        self.task_entry = tk.Entry(center_frame, width=30)
        self.task_entry.grid(row=0, column=0, padx=5)

        # Selector de fecha
        self.date_entry = DateEntry(center_frame, width=12, background="darkblue",
                                    foreground="white", borderwidth=2, date_pattern="dd/mm/yyyy")
        self.date_entry.grid(row=0, column=1, padx=5)

        # Entrada de hora con valor por defecto
        self.time_entry = tk.Entry(center_frame, width=8)
        self.time_entry.insert(0, "08:00")  # Valor inicial
        self.time_entry.grid(row=0, column=2, padx=5)

        # Botón para añadir tarea
        self.add_button = tk.Button(center_frame, text="Añadir Tarea", command=self.add_task, bg="#d1b3ff")
        self.add_button.grid(row=0, column=3, padx=5)

        # ===== Tabla de tareas =====
        columns = ("Tarea", "Fecha", "Hora", "Estado")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.tree.heading("Tarea", text="Tarea")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Estado", text="Estado")

        self.tree.column("Tarea", width=200, anchor="center")
        self.tree.column("Fecha", width=100, anchor="center")
        self.tree.column("Hora", width=80, anchor="center")
        self.tree.column("Estado", width=100, anchor="center")

        # ===== Botones de acciones =====
        button_frame = tk.Frame(root, bg="#f3e6f9")
        button_frame.grid(row=2, column=0, pady=10)

        self.complete_button = tk.Button(button_frame, text="Marcar como Completada",
                                         command=self.complete_task, bg="#c1f0c1")
        self.complete_button.grid(row=0, column=0, padx=5)

        self.delete_button = tk.Button(button_frame, text="Eliminar Tarea",
                                       command=self.delete_task, bg="#f5b7b1")
        self.delete_button.grid(row=0, column=1, padx=5)

        self.quit_button = tk.Button(button_frame, text="Salir", command=root.quit, bg="#f8d7da")
        self.quit_button.grid(row=0, column=2, padx=5)

        # ===== Vincular Enter para añadir =====
        self.root.bind("<Return>", lambda event: self.add_task())

        # ===== Cargar tareas guardadas =====
        self.load_tasks()

    # Función para añadir tarea
    def add_task(self):
        task_text = self.task_entry.get().strip()
        task_date = self.date_entry.get_date()
        task_time = self.time_entry.get().strip()

        if not task_text:
            messagebox.showwarning("Aviso", "Escribe una tarea antes de añadir.")
            return

        if not task_time:
            task_time = "08:00"  # Valor por defecto si está vacío

        task = {
            "tarea": task_text,
            "fecha": str(task_date),
            "hora": task_time,
            "estado": "Pendiente"
        }

        self.tasks.append(task)
        self.tree.insert("", "end",
                         values=(task["tarea"], task["fecha"], task["hora"], task["estado"]))
        self.save_tasks()

        # Limpiar entradas y restaurar hora por defecto
        self.task_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "08:00")

    # Marcar tarea como completada
    def complete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            self.tasks[index]["estado"] = "Completada"
            self.tree.item(selected_item, values=(self.tasks[index]["tarea"],
                                                  self.tasks[index]["fecha"],
                                                  self.tasks[index]["hora"],
                                                  "Completada"))
            self.save_tasks()

    # Eliminar tarea seleccionada
    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            del self.tasks[index]
            self.tree.delete(selected_item)
            self.save_tasks()

    # Guardar tareas en JSON
    def save_tasks(self):
        with open("tareas.json", "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=4, ensure_ascii=False)

    # Cargar tareas desde JSON
    def load_tasks(self):
        try:
            with open("tareas.json", "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
                for task in self.tasks:
                    self.tree.insert("", "end",
                                     values=(task["tarea"], task["fecha"], task["hora"], task["estado"]))
        except FileNotFoundError:
            self.tasks = []


# ===== Ejecutar aplicación =====
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
