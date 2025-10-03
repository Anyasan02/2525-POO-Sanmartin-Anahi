import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
import os

DATA_FILE = "tareas.json"

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.geometry("750x450")
        self.root.configure(bg="#f3d1e8")  # Fondo rosita suave

        # ==== Frame de formulario ====
        frame_form = tk.Frame(root, bg="#f3d1e8")
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="Tarea:", bg="#f3d1e8").grid(row=0, column=0, padx=5)
        self.entry_task = tk.Entry(frame_form, width=25)
        self.entry_task.grid(row=0, column=1, padx=5)
        self.entry_task.bind("<KeyRelease>", self.capitalize_first_letter)  # Capitalizar primera letra

        tk.Label(frame_form, text="Fecha:", bg="#f3d1e8").grid(row=0, column=2, padx=5)
        self.entry_date = DateEntry(frame_form, width=12, background="darkblue",
                                    foreground="white", date_pattern="dd/mm/yyyy")
        self.entry_date.grid(row=0, column=3, padx=5)

        tk.Label(frame_form, text="Hora:", bg="#f3d1e8").grid(row=0, column=4, padx=5)
        self.entry_hour = tk.Entry(frame_form, width=8)
        self.entry_hour.insert(0, "6:00")  # Hora por defecto
        self.entry_hour.grid(row=0, column=5, padx=5)

        self.btn_add = tk.Button(frame_form, text="Añadir Tarea (Enter)", command=self.add_task, bg="#d1c4e9")
        self.btn_add.grid(row=0, column=6, padx=5)

        # ==== Tabla de tareas ====
        self.tree = ttk.Treeview(root, columns=("Tarea", "Fecha", "Hora", "Estado"), show="headings", height=10)
        self.tree.heading("Tarea", text="Tarea")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Estado", text="Estado")

        # Centrar el contenido en cada columna
        self.tree.column("Tarea", width=200, anchor="center")
        self.tree.column("Fecha", width=100, anchor="center")
        self.tree.column("Hora", width=80, anchor="center")
        self.tree.column("Estado", width=100, anchor="center")

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # ==== Botones ====
        frame_buttons = tk.Frame(root, bg="#f3d1e8")
        frame_buttons.pack(pady=10)

        self.btn_complete = tk.Button(frame_buttons, text="Marcar Completada (C)", command=self.complete_task, bg="#c8e6c9")
        self.btn_complete.grid(row=0, column=0, padx=5)

        self.btn_edit = tk.Button(frame_buttons, text="Editar Tarea", command=self.edit_task, bg="#ffecb3")
        self.btn_edit.grid(row=0, column=1, padx=5)

        self.btn_delete = tk.Button(frame_buttons, text="Eliminar Tarea (D/Delete)", command=self.delete_task, bg="#ffcdd2")
        self.btn_delete.grid(row=0, column=2, padx=5)

        self.btn_exit = tk.Button(frame_buttons, text="Salir (Escape)", command=self.exit_app, bg="#b0bec5")
        self.btn_exit.grid(row=0, column=3, padx=5)

        # ==== Atajos de teclado ====
        root.bind("<Return>", lambda e: self.add_task())
        root.bind("<c>", self.key_complete_task)
        root.bind("<d>", self.key_delete_task)
        root.bind("<Delete>", self.key_delete_task)
        root.bind("<Escape>", lambda e: self.exit_app())

        # ==== Cargar datos previos ====
        self.load_tasks()

    # ==== Capitalizar primera letra ====
    def capitalize_first_letter(self, event):
        text = self.entry_task.get()
        if text and text[0].islower():
            self.entry_task.delete(0, tk.END)
            self.entry_task.insert(0, text[0].upper() + text[1:])

    # ==== Funciones de atajos protegidos ====
    def key_complete_task(self, event):
        if self.root.focus_get() not in (self.entry_task, self.entry_hour):
            self.complete_task()

    def key_delete_task(self, event):
        if self.root.focus_get() not in (self.entry_task, self.entry_hour):
            self.delete_task()

    # ==== Funciones principales ====
    def add_task(self):
        task = self.entry_task.get().strip()
        date = self.entry_date.get()
        hour = self.entry_hour.get().strip()

        if not task:
            messagebox.showwarning("Atención", "Debe escribir una tarea.")
            return
        if not hour:
            hour = "6:00"  # Si no ponen nada, siempre se queda en 6:00

        self.tree.insert("", "end", values=(task, date, hour, "Pendiente"))
        self.clear_form()
        self.save_tasks()

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione una tarea para editar.")
            return
        item = selected[0]
        values = self.tree.item(item, "values")

        # Poner datos en el formulario
        self.entry_task.delete(0, tk.END)
        self.entry_task.insert(0, values[0])
        self.entry_date.set_date(values[1])
        self.entry_hour.delete(0, tk.END)
        self.entry_hour.insert(0, values[2])

        # Borrar la tarea antigua para reemplazar
        self.tree.delete(item)
        self.save_tasks()

    def complete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione una tarea.")
            return
        for item in selected:
            values = self.tree.item(item, "values")
            if values[3] == "Pendiente":
                self.tree.item(item, values=(values[0], values[1], values[2], "Completada ✔"))
        self.save_tasks()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione una tarea para eliminar.")
            return
        for item in selected:
            self.tree.delete(item)
        self.save_tasks()

    def exit_app(self):
        self.save_tasks()
        self.root.quit()

    def clear_form(self):
        self.entry_task.delete(0, tk.END)
        self.entry_hour.delete(0, tk.END)
        self.entry_hour.insert(0, "6:00")  # Siempre vuelve a 6:00

    # ==== Guardado y carga de datos ====
    def save_tasks(self):
        tasks = []
        for item in self.tree.get_children():
            tasks.append(self.tree.item(item, "values"))
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                tasks = json.load(f)
                for task in tasks:
                    self.tree.insert("", "end", values=task)


# ==== Ejecutar la aplicación ====
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
