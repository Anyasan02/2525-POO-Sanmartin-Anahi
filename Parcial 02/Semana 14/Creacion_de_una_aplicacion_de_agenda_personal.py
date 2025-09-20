"""
Agenda Personal - Tkinter
Archivo: agenda_personal_tkinter.py
Descripción: Aplicación GUI para agregar, ver y eliminar eventos/tareas.
Requisitos: Python 3.8+, recomendada instalación: pip install tkcalendar

Cómo usar:
1. Instala dependencias opcionales: pip install tkcalendar
2. Ejecuta: python creacion_de_una_aplicacion_de_agenda_personal.py

Funcionalidades:
- Treeview con columnas: Fecha, Hora, Descripción
- Agregar evento mediante DatePicker (si tkcalendar está instalado) o Entry de fecha si no lo está
- Eliminar evento seleccionado con cuadro de confirmación
- Organización por Frames (vista eventos, formulario, acciones)
- Persistencia simple en archivo JSON (events.json)
"""

import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Intentamos importar DateEntry desde tkcalendar; si no está disponible, usaremos Entry
try:
    from tkcalendar import DateEntry
    TKCALENDAR_AVAILABLE = True
except Exception:
    TKCALENDAR_AVAILABLE = False

DATA_FILE = "events.json"

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Personal")
        self.root.geometry("720x440")
        self.root.resizable(False, False)

        # Contenedores/frames
        self.frame_list = ttk.Frame(self.root, padding=(10, 10))
        self.frame_form = ttk.Frame(self.root, padding=(10, 10))
        self.frame_actions = ttk.Frame(self.root, padding=(10, 10))

        self.frame_list.grid(row=0, column=0, sticky="nsew")
        self.frame_form.grid(row=1, column=0, sticky="ew")
        self.frame_actions.grid(row=2, column=0, sticky="ew")

        # Configurar grid general
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Treeview (lista de eventos)
        self.tree = ttk.Treeview(self.frame_list, columns=("fecha", "hora", "desc"), show="headings", height=12)
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("desc", text="Descripción")
        self.tree.column("fecha", width=120, anchor="center")
        self.tree.column("hora", width=80, anchor="center")
        self.tree.column("desc", width=460, anchor="w")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar para treeview
        self.scrollbar = ttk.Scrollbar(self.frame_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Formulario de entrada
        # Fecha
        lbl_fecha = ttk.Label(self.frame_form, text="Fecha:")
        lbl_fecha.grid(row=0, column=0, padx=(0,6), pady=6, sticky="e")

        if TKCALENDAR_AVAILABLE:
            self.entry_fecha = DateEntry(self.frame_form, date_pattern='yyyy-mm-dd')
        else:
            self.entry_fecha = ttk.Entry(self.frame_form)
            self.entry_fecha.insert(0, "YYYY-MM-DD")
        self.entry_fecha.grid(row=0, column=1, padx=(0,12), pady=6, sticky="w")

        # Hora
        lbl_hora = ttk.Label(self.frame_form, text="Hora (HH:MM):")
        lbl_hora.grid(row=0, column=2, padx=(0,6), pady=6, sticky="e")
        self.entry_hora = ttk.Entry(self.frame_form, width=10)
        self.entry_hora.insert(0, "09:00")
        self.entry_hora.grid(row=0, column=3, padx=(0,12), pady=6, sticky="w")

        # Descripción
        lbl_desc = ttk.Label(self.frame_form, text="Descripción:")
        lbl_desc.grid(row=1, column=0, padx=(0,6), pady=6, sticky="ne")
        self.entry_desc = ttk.Entry(self.frame_form, width=70)
        self.entry_desc.grid(row=1, column=1, columnspan=3, padx=(0,12), pady=6, sticky="w")

        # Botones de acción
        btn_add = ttk.Button(self.frame_actions, text="Agregar Evento", command=self.add_event)
        btn_delete = ttk.Button(self.frame_actions, text="Eliminar Evento Seleccionado", command=self.delete_selected)
        btn_quit = ttk.Button(self.frame_actions, text="Salir", command=self.root.quit)

        btn_add.grid(row=0, column=0, padx=6, pady=6)
        btn_delete.grid(row=0, column=1, padx=6, pady=6)
        btn_quit.grid(row=0, column=2, padx=6, pady=6)

        # Cargar eventos guardados
        self.events = []
        self.load_events()
        self.refresh_treeview()

        # Bind doble clic para editar (opcional simple edición)
        self.tree.bind('<Double-1>', self.on_double_click)

    def validate_date(self, s):
        try:
            datetime.strptime(s, "%Y-%m-%d")
            return True
        except Exception:
            return False

    def validate_time(self, s):
        try:
            datetime.strptime(s, "%H:%M")
            return True
        except Exception:
            return False

    def add_event(self):
        # Obtener valores
        fecha = self.entry_fecha.get().strip()
        hora = self.entry_hora.get().strip()
        desc = self.entry_desc.get().strip()

        # Validaciones
        if not fecha or not hora or not desc:
            messagebox.showwarning("Campos vacíos", "Por favor completa fecha, hora y descripción.")
            return

        if not self.validate_date(fecha):
            messagebox.showerror("Fecha inválida", "Formato de fecha inválido. Use YYYY-MM-DD.")
            return

        if not self.validate_time(hora):
            messagebox.showerror("Hora inválida", "Formato de hora inválido. Use HH:MM en formato 24 horas.")
            return

        # Crear ID simple
        event_id = int(datetime.now().timestamp() * 1000)
        event = {"id": event_id, "fecha": fecha, "hora": hora, "desc": desc}
        self.events.append(event)
        self.save_events()
        self.refresh_treeview()

        # Limpiar campos
        if not TKCALENDAR_AVAILABLE:
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.insert(0, "YYYY-MM-DD")
        else:
            # DateEntry actualiza solo cuando el usuario cambia; no es necesario limpiar
            pass
        self.entry_hora.delete(0, tk.END)
        self.entry_hora.insert(0, "09:00")
        self.entry_desc.delete(0, tk.END)

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Selecciona evento", "Por favor selecciona un evento para eliminar.")
            return

        # confirmación
        answer = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de eliminar el/los evento(s) seleccionado(s)?")
        if not answer:
            return

        for item in sel:
            item_values = self.tree.item(item, 'values')
            # Usamos la combinación fecha+hora+desc para buscar y eliminar el evento en la lista
            fecha, hora, desc = item_values
            # Buscar por coincidencia
            to_remove = None
            for ev in self.events:
                if ev['fecha'] == fecha and ev['hora'] == hora and ev['desc'] == desc:
                    to_remove = ev
                    break
            if to_remove:
                self.events.remove(to_remove)

        self.save_events()
        self.refresh_treeview()

    def refresh_treeview(self):
        # Vaciar tree
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Ordenar por fecha y hora
        def sort_key(ev):
            try:
                return datetime.strptime(ev['fecha'] + ' ' + ev['hora'], '%Y-%m-%d %H:%M')
            except Exception:
                return datetime.max

        self.events.sort(key=sort_key)

        for ev in self.events:
            self.tree.insert('', 'end', values=(ev['fecha'], ev['hora'], ev['desc']))

    def save_events(self):
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.events, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudo guardar en {DATA_FILE}: {e}")

    def load_events(self):
        if not os.path.exists(DATA_FILE):
            self.events = []
            return
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.events = json.load(f)
        except Exception:
            self.events = []

    def on_double_click(self, event):
        # Llenar formulario con los datos seleccionados para editar (edición básica)
        sel = self.tree.selection()
        if not sel:
            return
        item = sel[0]
        fecha, hora, desc = self.tree.item(item, 'values')
        # Poner en el formulario
        if TKCALENDAR_AVAILABLE:
            try:
                # DateEntry tiene set_date
                self.entry_fecha.set_date(fecha)
            except Exception:
                # fallback
                self.entry_fecha.delete(0, tk.END)
                self.entry_fecha.insert(0, fecha)
        else:
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.insert(0, fecha)

        self.entry_hora.delete(0, tk.END)
        self.entry_hora.insert(0, hora)
        self.entry_desc.delete(0, tk.END)
        self.entry_desc.insert(0, desc)

        # El usuario aqui solo puede agregar y eliminar eventos.
        messagebox.showinfo("Editar evento",
                            "Puedes editar los campos y luego pulsar 'Agregar Evento' para agregar la versión modificada.\nNota: esto creará un nuevo registro en lugar de reemplazar el anterior.")


if __name__ == '__main__':
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()
