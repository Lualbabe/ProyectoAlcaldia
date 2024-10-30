import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from file_operations import procesar_archivo
from db_operations import buscar_archivos, actualizar_datos

def subir_archivos():
    archivos = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx")])
    if archivos:
        for archivo in archivos:
            procesar_archivo(archivo)

def buscar_datos(tree, combobox_columna, entry_filtro):
    columna = combobox_columna.get()
    filtro = entry_filtro.get()
    if not columna or not filtro:
        messagebox.showwarning("Advertencia", "Seleccione una columna y escriba un valor para buscar.")
        return
    resultados = buscar_archivos(columna, filtro)
    mostrar_datos(tree, resultados)

def mostrar_datos(tree, datos):
    for row in tree.get_children():
        tree.delete(row)
    for fila in datos:
        tree.insert("", tk.END, values=fila)

def limpiar_tabla(tree):
    for row in tree.get_children():
        tree.delete(row)

def on_enter(event, tree, combobox_columna, entry_filtro):
    buscar_datos(tree, combobox_columna, entry_filtro)

def abrir_ventana_editar(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione una fila para editar.")
        return
    item = tree.item(selected_item)
    values = item['values']

    ventana_editar = tk.Toplevel()
    ventana_editar.title("Editar Datos")
    ventana_editar.geometry("600x400") 

    labels = ["Número Actividad", "Día", "Actividad", "Parroquia", "Dirección", "Mes"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(ventana_editar, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
        if label in ["Actividad", "Dirección"]:
            entry = tk.Text(ventana_editar, height=4, width=50)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(tk.END, values[i])
        else:
            entry = tk.Entry(ventana_editar, width=50)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, values[i])
        entries.append(entry)

    def guardar_cambios():
        nuevos_valores = []
        for entry in entries:
            if isinstance(entry, tk.Text):
                nuevos_valores.append(entry.get("1.0", tk.END).strip())
            else:
                nuevos_valores.append(entry.get())
        actualizar_datos(nuevos_valores)
        tree.item(selected_item, values=nuevos_valores)
        messagebox.showinfo("Éxito", "Datos actualizados correctamente.")
        ventana_editar.destroy()

    btn_guardar = tk.Button(ventana_editar, text="Guardar Cambios", command=guardar_cambios)
    btn_guardar.grid(row=len(labels), column=0, pady=10, padx=10, sticky='e')

    btn_salir = tk.Button(ventana_editar, text="Salir", command=ventana_editar.destroy)
    btn_salir.grid(row=len(labels), column=1, pady=10, padx=10, sticky='w')

def crear_interfaz(ventana):
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(fill=tk.X, pady=20)

    btn_subir = tk.Button(frame_botones, text="Subir Archivos Excel", command=subir_archivos)
    btn_subir.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

    combobox_columna = ttk.Combobox(frame_botones, values=["numero_actividad", "dia", "actividad", "parroquia", "direccion", "mes"], state="readonly")
    combobox_columna.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
    combobox_columna.set("Seleccionar Columna")

    entry_filtro = tk.Entry(frame_botones)
    entry_filtro.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
    entry_filtro.bind("<Return>", lambda event: on_enter(event, tree, combobox_columna, entry_filtro))

    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(fill=tk.BOTH, expand=True, pady=20)

    tree = ttk.Treeview(frame_tabla, columns=("numero_actividad", "dia", "actividad", "parroquia", "direccion", "mes"), show="headings")
    tree.heading("numero_actividad", text="Número Actividad")
    tree.heading("dia", text="Día")
    tree.heading("actividad", text="Actividad")
    tree.heading("parroquia", text="Parroquia")
    tree.heading("direccion", text="Dirección")
    tree.heading("mes", text="Mes")
    tree.pack(fill=tk.BOTH, expand=True)

    # Botones de acciones
    btn_buscar = tk.Button(frame_botones, text="Buscar Archivos", command=lambda: buscar_datos(tree, combobox_columna, entry_filtro))
    btn_buscar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

    btn_editar = tk.Button(frame_botones, text="Editar", command=lambda: abrir_ventana_editar(tree))
    btn_editar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

    frame_inferior = tk.Frame(ventana)
    frame_inferior.pack(fill=tk.X, padx=10, pady=10)

    btn_limpiar = tk.Button(frame_inferior, text="Limpiar Tabla", command=lambda: limpiar_tabla(tree))
    btn_limpiar.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    btn_salir = tk.Button(frame_inferior, text="Salir", command=ventana.quit)
    btn_salir.pack(side=tk.RIGHT, fill=tk.X, expand=True)