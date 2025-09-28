import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
import os


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.geometry("700x500")
        self.root.config(bg="#f3e5f5")  # Fondo lila claro

        self.file_name = "tareas.json"
        self.tasks = self.load_tasks()

        # ====== Frame de entrada ======
        entry_frame = tk.Frame(self.root, bg="#f3e5f5")
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Tarea:", bg="#f3e5f5", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        self.task_entry = tk.Entry(entry_frame, width=25)
        self.task_entry.grid(row=0, column=1, padx=5)

        tk.Label(entry_frame, text="Fecha:", bg="#f3e5f5", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)
        self.date_entry = DateEntry(entry_frame, width=12, background="purple", foreground="white", borderwidth=2,
                                    date_pattern="dd/mm/yyyy")
        self.date_entry.grid(row=0, column=3, padx=5)

        tk.Label(entry_frame, text="Hora:", bg="#f3e5f5", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5)
        self.time_entry = tk.Entry(entry_frame, width=8)
        self.time_entry.insert(0, "08:00")  # Valor por defecto
        self.time_entry.grid(row=0, column=5, padx=5)

        add_button = tk.Button(entry_frame, text="Añadir Tarea", command=self.add_task,
                               bg="#d1c4e9", font=("Arial", 10, "bold"))
        add_button.grid(row=0, column=6, padx=5)

        # ====== Tabla de tareas ======
        columns = ("Tarea", "Fecha", "Hora", "Estado")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=12)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(pady=10)

        # ====== Botones de acciones ======
        button_frame = tk.Frame(self.root, bg="#f3e5f5")
        button_frame.pack(pady=10)

        self.complete_button = tk.Button(button_frame, text="Marcar Completada", command=self.complete_task,
                                         bg="#c8e6c9", font=("Arial", 10, "bold"))
        self.complete_button.grid(row=0, column=0, padx=10)

        self.delete_button = tk.Button(button_frame, text="Eliminar Tarea", command=self.delete_task,
                                       bg="#ffcdd2", font=("Arial", 10, "bold"))
        self.delete_button.grid(row=0, column=1, padx=10)

        self.quit_button = tk.Button(button_frame, text="Salir", command=self.root.quit,
                                     bg="#bbdefb", font=("Arial", 10, "bold"))
        self.quit_button.grid(row=0, column=2, padx=10)

        # ====== Cargar tareas existentes ======
        self.refresh_table()

    # ====== Funciones ======
    def add_task(self):
        task = self.task_entry.get().strip()
        date = self.date_entry.get()
        time = self.time_entry.get().strip() or "--:--"

        if task:
            self.tasks.append({"task": task, "date": date, "time": time, "status": "Pendiente"})
            self.save_tasks()
            self.refresh_table()
            self.task_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, "08:00")  # Valor por defecto al limpiar
        else:
            messagebox.showwarning("Aviso", "Por favor, escribe una tarea.")

    def complete_task(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            index = self.tree.index(item)
            self.tasks[index]["status"] = "Completada"
            self.save_tasks()
            self.refresh_table()
        else:
            messagebox.showwarning("Aviso", "Selecciona una tarea para marcarla como completada.")

    def delete_task(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            index = self.tree.index(item)
            del self.tasks[index]
            self.save_tasks()
            self.refresh_table()
        else:
            messagebox.showwarning("Aviso", "Selecciona una tarea para eliminar.")

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for task in self.tasks:
            self.tree.insert("", tk.END, values=(task["task"], task["date"], task["time"], task["status"]))

    def save_tasks(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def load_tasks(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

# Ejecutar aplicacion
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
