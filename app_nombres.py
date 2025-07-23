import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

conn = sqlite3.connect("nombres.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
""")
conn.commit()


# Guarda el nombre que esté en la caja de texto en la base de datos
def guardar_nombre():
    nombre = entrada_nombre.get().strip()
    if nombre == "":
        messagebox.showwarning("Error", "Por favor, escribe tu nombre.")
        return
    cursor.execute("INSERT INTO usuarios (nombre) VALUES (?)", (nombre,))
    conn.commit()
    entrada_nombre.delete(0, tk.END)
    actualizar_lista()


# Elimina el nombre seleccionado de la base de datos
def eliminar_nombre():
    seleccion = lista_nombres.selection()
    if not seleccion:
        messagebox.showwarning("Sin selección", "Selecciona un nombre para eliminar.")
        return
    item = lista_nombres.item(seleccion[0])
    id_seleccionado = item["values"][0]
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_seleccionado,))
    conn.commit()
    actualizar_lista()


# Edita el nombre seleccionado con el texto de la caja de entrada
def editar_nombre():
    seleccion = lista_nombres.selection()
    if not seleccion:
        messagebox.showwarning("Sin selección", "Selecciona un nombre para editar.")
        return
    nuevo_nombre = entrada_nombre.get().strip()
    if nuevo_nombre == "":
        messagebox.showwarning("Error", "Escribe un nombre para actualizar.")
        return
    item = lista_nombres.item(seleccion[0])
    id_seleccionado = item["values"][0]
    cursor.execute("UPDATE usuarios SET nombre = ? WHERE id = ?", (nuevo_nombre, id_seleccionado))
    conn.commit()
    actualizar_lista()
    entrada_nombre.delete(0, tk.END)


# Carga en la caja de texto el nombre seleccionado en la tabla
def seleccionar_nombre(event):
    seleccion = lista_nombres.selection()
    if seleccion:
        item = lista_nombres.item(seleccion[0])
        entrada_nombre.delete(0, tk.END)
        entrada_nombre.insert(0, item["values"][1])


# Refresca la lista de nombres con los datos actuales de la base de datos
def actualizar_lista():
    lista_nombres.delete(*lista_nombres.get_children())
    cursor.execute("SELECT id, nombre FROM usuarios")
    for fila in cursor.fetchall():
        lista_nombres.insert("", "end", values=fila)


# Cierra la ventana y la conexión a la base de datos
def cerrar():
    conn.close()
    ventana.destroy()


# Ejecuta guardar o editar dependiendo si hay algo seleccionado en la tabla
def accion_enter():
    if lista_nombres.selection():
        editar_nombre()
    else:
        guardar_nombre()


ventana = tk.Tk()
ventana.title("Gestión de Nombres")
ventana.geometry("450x400")
ventana.config(bg="#f5f6fa")
ventana.bind('<Return>', lambda event: accion_enter())

style = ttk.Style()
style.configure("TButton", font=("Arial", 10), padding=6)
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
style.configure("Treeview", rowheight=25, font=("Arial", 10))

frame_superior = tk.Frame(ventana, bg="#f5f6fa")
frame_superior.pack(pady=10)

tk.Label(frame_superior, text="¿Cuál es tu nombre?", bg="#f5f6fa", font=("Arial", 12)).pack()
entrada_nombre = tk.Entry(frame_superior, width=30, font=("Arial", 11))
entrada_nombre.pack(pady=5)

frame_botones = tk.Frame(ventana, bg="#f5f6fa")
frame_botones.pack(pady=5)
ttk.Button(frame_botones, text="Guardar", command=guardar_nombre).grid(row=0, column=0, padx=5)
ttk.Button(frame_botones, text="Editar seleccionado", command=editar_nombre).grid(row=0, column=1, padx=5)
ttk.Button(frame_botones, text="Eliminar seleccionado", command=eliminar_nombre).grid(row=0, column=2, padx=5)

frame_tabla = tk.Frame(ventana)
frame_tabla.pack(pady=10, fill="both", expand=True)

lista_nombres = ttk.Treeview(frame_tabla, columns=("ID", "Nombre"), show="headings", height=8)
lista_nombres.heading("ID", text="ID")
lista_nombres.heading("Nombre", text="Nombre")
lista_nombres.column("ID", width=60, anchor="center")
lista_nombres.column("Nombre", width=250, anchor="w")
lista_nombres.pack(pady=5, fill="both", expand=True)

lista_nombres.bind("<<TreeviewSelect>>", seleccionar_nombre)

actualizar_lista()
ventana.protocol("WM_DELETE_WINDOW", cerrar)
ventana.mainloop()
