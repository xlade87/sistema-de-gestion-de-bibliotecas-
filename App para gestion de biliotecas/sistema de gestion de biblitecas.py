"""
INTERFAZ BIBLIOTECA PERSONAL
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import datetime


class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                database="biblioteca_personal",
                user="root",
                password="",
                autocommit=True
            )
            self.cursor = self.connection.cursor(buffered=True)
            return True
        except mysql.connector.Error as error:
            messagebox.showerror("Error de Conexión", f"Error conectando a la base de datos: {error}")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, parameters=None):
        try:
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)

            if query.strip().upper().startswith('SELECT'):
                return True, self.cursor.fetchall()
            else:
                self.connection.commit()
                return True, "Operación exitosa"
        except mysql.connector.Error as error:
            return False, str(error)


db = DatabaseConnection()


# ========== FUNCIONES PARA LA TABLA LIBROS ==========
def limpiar_libro():
    libro_id.delete(0, tk.END)
    libro_titulo.delete(0, tk.END)
    libro_autor.delete(0, tk.END)
    libro_genero.delete(0, tk.END)
    libro_anio.delete(0, tk.END)
    libro_isbn.delete(0, tk.END)


def guardar_libro():
    if not db.connection and not db.connect():
        return

    titulo = libro_titulo.get().strip()
    autor = libro_autor.get().strip()
    genero = libro_genero.get().strip()
    anio = libro_anio.get().strip()
    isbn = libro_isbn.get().strip()

    # Validaciones
    if not titulo:
        messagebox.showerror("Error", "El título es obligatorio")
        return

    if not autor:
        messagebox.showerror("Error", "El autor es obligatorio")
        return

    if anio and not anio.isdigit():
        messagebox.showerror("Error", "El año debe ser un número")
        return

    query = "INSERT INTO libros (titulo, autor, genero, año_publicacion, isbn) VALUES (%s, %s, %s, %s, %s)"
    params = (titulo, autor, genero or None, int(anio) if anio else None, isbn or None)

    success, result = db.execute_query(query, params)

    if success:
        messagebox.showinfo("Éxito", f"Libro '{titulo}' guardado correctamente")
        limpiar_libro()
        actualizar_lista_libros()
    else:
        messagebox.showerror("Error", f"Error al guardar: {result}")


def actualizar_libro():
    if not db.connection and not db.connect():
        return

    id_libro = libro_id.get().strip()
    titulo = libro_titulo.get().strip()
    autor = libro_autor.get().strip()

    if not id_libro or not id_libro.isdigit():
        messagebox.showerror("Error", "ID de libro inválido")
        return

    if not titulo:
        messagebox.showerror("Error", "El título es obligatorio")
        return

    query = """UPDATE libros SET titulo=%s, autor=%s, genero=%s, año_publicacion=%s, isbn=%s 
               WHERE id=%s"""
    params = (titulo, autor, libro_genero.get().strip() or None,
              int(libro_anio.get()) if libro_anio.get().strip() else None,
              libro_isbn.get().strip() or None, int(id_libro))

    success, result = db.execute_query(query, params)

    if success:
        messagebox.showinfo("Éxito", "Libro actualizado correctamente")
        limpiar_libro()
        actualizar_lista_libros()
    else:
        messagebox.showerror("Error", f"Error al actualizar: {result}")


def eliminar_libro():
    if not db.connection and not db.connect():
        return

    id_libro = libro_id.get().strip()

    if not id_libro or not id_libro.isdigit():
        messagebox.showerror("Error", "ID de libro inválido")
        return

    if not messagebox.askyesno("Confirmar", f"¿Eliminar el libro ID {id_libro}?"):
        return

    query = "DELETE FROM libros WHERE id = %s"
    success, result = db.execute_query(query, (int(id_libro),))

    if success:
        messagebox.showinfo("Éxito", "Libro eliminado correctamente")
        limpiar_libro()
        actualizar_lista_libros()
    else:
        messagebox.showerror("Error", f"Error al eliminar: {result}")


def buscar_libro_por_id():
    if not db.connection and not db.connect():
        return

    id_libro = libro_id.get().strip()

    if not id_libro or not id_libro.isdigit():
        messagebox.showerror("Error", "Ingrese un ID válido")
        return

    query = "SELECT * FROM libros WHERE id = %s"
    success, result = db.execute_query(query, (int(id_libro),))

    if success and result:
        libro = result[0]
        libro_titulo.delete(0, tk.END)
        libro_titulo.insert(0, libro[1])
        libro_autor.delete(0, tk.END)
        libro_autor.insert(0, libro[2])
        libro_genero.delete(0, tk.END)
        libro_genero.insert(0, libro[3] or "")
        libro_anio.delete(0, tk.END)
        libro_anio.insert(0, str(libro[4]) if libro[4] else "")
        libro_isbn.delete(0, tk.END)
        libro_isbn.insert(0, libro[5] or "")
    else:
        messagebox.showinfo("Búsqueda", "Libro no encontrado")


def actualizar_lista_libros():
    if not db.connection and not db.connect():
        return

    # Limpiar treeview
    for item in tree_libros.get_children():
        tree_libros.delete(item)

    query = "SELECT id, titulo, autor, genero, año_publicacion FROM libros ORDER BY titulo"
    success, result = db.execute_query(query)

    if success:
        for libro in result:
            tree_libros.insert("", tk.END, values=libro)


# ========== FUNCIONES PARA LA TABLA USUARIOS ==========
def limpiar_usuario():
    usuario_id.delete(0, tk.END)
    usuario_nombre.delete(0, tk.END)
    usuario_email.delete(0, tk.END)
    usuario_telefono.delete(0, tk.END)


def guardar_usuario():
    if not db.connection and not db.connect():
        return

    nombre = usuario_nombre.get().strip()
    email = usuario_email.get().strip()
    telefono = usuario_telefono.get().strip()

    if not nombre:
        messagebox.showerror("Error", "El nombre es obligatorio")
        return

    if not email:
        messagebox.showerror("Error", "El email es obligatorio")
        return

    query = "INSERT INTO usuarios (nombre, email, telefono) VALUES (%s, %s, %s)"
    params = (nombre, email, telefono or None)

    success, result = db.execute_query(query, params)

    if success:
        messagebox.showinfo("Éxito", f"Usuario '{nombre}' guardado correctamente")
        limpiar_usuario()
        actualizar_lista_usuarios()
    else:
        messagebox.showerror("Error", f"Error al guardar: {result}")


def actualizar_lista_usuarios():
    if not db.connection and not db.connect():
        return

    for item in tree_usuarios.get_children():
        tree_usuarios.delete(item)

    query = "SELECT id, nombre, email, telefono FROM usuarios ORDER BY nombre"
    success, result = db.execute_query(query)

    if success:
        for usuario in result:
            tree_usuarios.insert("", tk.END, values=usuario)


# ========== FUNCIONES PARA PRÉSTAMOS ==========
def realizar_prestamo():
    if not db.connection and not db.connect():
        return

    libro_id = prestamo_libro_id.get().strip()
    usuario_id = prestamo_usuario_id.get().strip()

    if not libro_id or not libro_id.isdigit():
        messagebox.showerror("Error", "ID de libro inválido")
        return

    if not usuario_id or not usuario_id.isdigit():
        messagebox.showerror("Error", "ID de usuario inválido")
        return

    # Verificar si el libro está disponible
    query = "SELECT disponible FROM libros WHERE id = %s"
    success, result = db.execute_query(query, (int(libro_id),))

    if not success or not result:
        messagebox.showerror("Error", "Libro no encontrado")
        return

    if not result[0][0]:
        messagebox.showerror("Error", "El libro no está disponible")
        return

    # Realizar préstamo
    query = "INSERT INTO prestamos (libro_id, usuario_id) VALUES (%s, %s)"
    success, result = db.execute_query(query, (int(libro_id), int(usuario_id)))

    if success:
        # Marcar libro como no disponible
        db.execute_query("UPDATE libros SET disponible = FALSE WHERE id = %s", (int(libro_id),))
        messagebox.showinfo("Éxito", "Préstamo realizado correctamente")
        prestamo_libro_id.delete(0, tk.END)
        prestamo_usuario_id.delete(0, tk.END)
        actualizar_lista_prestamos()
        actualizar_lista_libros()
    else:
        messagebox.showerror("Error", f"Error al realizar préstamo: {result}")


def devolver_libro():
    if not db.connection and not db.connect():
        return

    prestamo_id = devolucion_id.get().strip()

    if not prestamo_id or not prestamo_id.isdigit():
        messagebox.showerror("Error", "ID de préstamo inválido")
        return

    # Obtener información del préstamo
    query = "SELECT libro_id FROM prestamos WHERE id = %s AND devuelto = FALSE"
    success, result = db.execute_query(query, (int(prestamo_id),))

    if not success or not result:
        messagebox.showerror("Error", "Préstamo no encontrado o ya devuelto")
        return

    libro_id = result[0][0]

    # Marcar como devuelto
    query = "UPDATE prestamos SET devuelto = TRUE, fecha_devolucion = CURDATE() WHERE id = %s"
    success, result = db.execute_query(query, (int(prestamo_id),))

    if success:
        # Marcar libro como disponible
        db.execute_query("UPDATE libros SET disponible = TRUE WHERE id = %s", (libro_id,))
        messagebox.showinfo("Éxito", "Libro devuelto correctamente")
        devolucion_id.delete(0, tk.END)
        actualizar_lista_prestamos()
        actualizar_lista_libros()
    else:
        messagebox.showerror("Error", f"Error al devolver libro: {result}")


def actualizar_lista_prestamos():
    if not db.connection and not db.connect():
        return

    for item in tree_prestamos.get_children():
        tree_prestamos.delete(item)

    query = """SELECT p.id, l.titulo, u.nombre, p.fecha_prestamo, 
               CASE WHEN p.devuelto THEN 'Sí' ELSE 'No' END
               FROM prestamos p
               JOIN libros l ON p.libro_id = l.id
               JOIN usuarios u ON p.usuario_id = u.id
               ORDER BY p.fecha_prestamo DESC"""
    success, result = db.execute_query(query)

    if success:
        for prestamo in result:
            tree_prestamos.insert("", tk.END, values=prestamo)


# ========== INTERFAZ GRÁFICA ==========
root = tk.Tk()
root.title("Sistema de Gestión de Biblioteca")
root.geometry("1000x700")

# Crear pestañas
notebook = ttk.Notebook(root)

# Pestaña 1: Libros
tab_libros = ttk.Frame(notebook)
notebook.add(tab_libros, text="Libros")

# Pestaña 2: Usuarios
tab_usuarios = ttk.Frame(notebook)
notebook.add(tab_usuarios, text="Usuarios")

# Pestaña 3: Préstamos
tab_prestamos = ttk.Frame(notebook)
notebook.add(tab_prestamos, text="Préstamos")

notebook.pack(expand=True, fill="both")

# ========== CONTENIDO PESTAÑA LIBROS ==========
# Frame para formulario
frame_form_libro = ttk.LabelFrame(tab_libros, text="Gestión de Libros", padding=10)
frame_form_libro.pack(fill="x", padx=10, pady=5)

# Campos del formulario
ttk.Label(frame_form_libro, text="ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
libro_id = ttk.Entry(frame_form_libro, width=10)
libro_id.grid(row=0, column=1, padx=5, pady=2)

ttk.Button(frame_form_libro, text="Buscar por ID", command=buscar_libro_por_id).grid(row=0, column=2, padx=5)

ttk.Label(frame_form_libro, text="Título:*").grid(row=1, column=0, padx=5, pady=2, sticky="w")
libro_titulo = ttk.Entry(frame_form_libro, width=40)
libro_titulo.grid(row=1, column=1, padx=5, pady=2, columnspan=2)

ttk.Label(frame_form_libro, text="Autor:*").grid(row=2, column=0, padx=5, pady=2, sticky="w")
libro_autor = ttk.Entry(frame_form_libro, width=40)
libro_autor.grid(row=2, column=1, padx=5, pady=2, columnspan=2)

ttk.Label(frame_form_libro, text="Género:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
libro_genero = ttk.Entry(frame_form_libro, width=40)
libro_genero.grid(row=3, column=1, padx=5, pady=2, columnspan=2)

ttk.Label(frame_form_libro, text="Año:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
libro_anio = ttk.Entry(frame_form_libro, width=10)
libro_anio.grid(row=4, column=1, padx=5, pady=2, sticky="w")

ttk.Label(frame_form_libro, text="ISBN:").grid(row=4, column=2, padx=5, pady=2, sticky="w")
libro_isbn = ttk.Entry(frame_form_libro, width=20)
libro_isbn.grid(row=4, column=3, padx=5, pady=2)

# Botones
frame_botones_libro = ttk.Frame(frame_form_libro)
frame_botones_libro.grid(row=5, column=0, columnspan=4, pady=10)

ttk.Button(frame_botones_libro, text="Guardar", command=guardar_libro).pack(side="left", padx=5)
ttk.Button(frame_botones_libro, text="Actualizar", command=actualizar_libro).pack(side="left", padx=5)
ttk.Button(frame_botones_libro, text="Eliminar", command=eliminar_libro).pack(side="left", padx=5)
ttk.Button(frame_botones_libro, text="Limpiar", command=limpiar_libro).pack(side="left", padx=5)

# Lista de libros
frame_lista_libros = ttk.LabelFrame(tab_libros, text="Lista de Libros", padding=10)
frame_lista_libros.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("ID", "Título", "Autor", "Género", "Año")
tree_libros = ttk.Treeview(frame_lista_libros, columns=columns, show="headings", height=12)

for col in columns:
    tree_libros.heading(col, text=col)
    tree_libros.column(col, width=100)

tree_libros.pack(fill="both", expand=True)

# ========== CONTENIDO PESTAÑA USUARIOS ==========
frame_form_usuario = ttk.LabelFrame(tab_usuarios, text="Gestión de Usuarios", padding=10)
frame_form_usuario.pack(fill="x", padx=10, pady=5)

ttk.Label(frame_form_usuario, text="ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
usuario_id = ttk.Entry(frame_form_usuario, width=10)
usuario_id.grid(row=0, column=1, padx=5, pady=2)

ttk.Label(frame_form_usuario, text="Nombre:*").grid(row=1, column=0, padx=5, pady=2, sticky="w")
usuario_nombre = ttk.Entry(frame_form_usuario, width=30)
usuario_nombre.grid(row=1, column=1, padx=5, pady=2)

ttk.Label(frame_form_usuario, text="Email:*").grid(row=2, column=0, padx=5, pady=2, sticky="w")
usuario_email = ttk.Entry(frame_form_usuario, width=30)
usuario_email.grid(row=2, column=1, padx=5, pady=2)

ttk.Label(frame_form_usuario, text="Teléfono:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
usuario_telefono = ttk.Entry(frame_form_usuario, width=20)
usuario_telefono.grid(row=3, column=1, padx=5, pady=2, sticky="w")

frame_botones_usuario = ttk.Frame(frame_form_usuario)
frame_botones_usuario.grid(row=4, column=0, columnspan=2, pady=10)

ttk.Button(frame_botones_usuario, text="Guardar", command=guardar_usuario).pack(side="left", padx=5)
ttk.Button(frame_botones_usuario, text="Limpiar", command=limpiar_usuario).pack(side="left", padx=5)

# Lista de usuarios
frame_lista_usuarios = ttk.LabelFrame(tab_usuarios, text="Lista de Usuarios", padding=10)
frame_lista_usuarios.pack(fill="both", expand=True, padx=10, pady=5)

columns_usuarios = ("ID", "Nombre", "Email", "Teléfono")
tree_usuarios = ttk.Treeview(frame_lista_usuarios, columns=columns_usuarios, show="headings", height=12)

for col in columns_usuarios:
    tree_usuarios.heading(col, text=col)
    tree_usuarios.column(col, width=120)

tree_usuarios.pack(fill="both", expand=True)

# ========== CONTENIDO PESTAÑA PRÉSTAMOS ==========
# Sección de préstamos
frame_prestamo = ttk.LabelFrame(tab_prestamos, text="Realizar Préstamo", padding=10)
frame_prestamo.pack(fill="x", padx=10, pady=5)

ttk.Label(frame_prestamo, text="ID Libro:*").grid(row=0, column=0, padx=5, pady=2, sticky="w")
prestamo_libro_id = ttk.Entry(frame_prestamo, width=10)
prestamo_libro_id.grid(row=0, column=1, padx=5, pady=2)

ttk.Label(frame_prestamo, text="ID Usuario:*").grid(row=0, column=2, padx=5, pady=2, sticky="w")
prestamo_usuario_id = ttk.Entry(frame_prestamo, width=10)
prestamo_usuario_id.grid(row=0, column=3, padx=5, pady=2)

ttk.Button(frame_prestamo, text="Realizar Préstamo", command=realizar_prestamo).grid(row=0, column=4, padx=10)

# Sección de devoluciones
frame_devolucion = ttk.LabelFrame(tab_prestamos, text="Devolver Libro", padding=10)
frame_devolucion.pack(fill="x", padx=10, pady=5)

ttk.Label(frame_devolucion, text="ID Préstamo:*").grid(row=0, column=0, padx=5, pady=2, sticky="w")
devolucion_id = ttk.Entry(frame_devolucion, width=10)
devolucion_id.grid(row=0, column=1, padx=5, pady=2)

ttk.Button(frame_devolucion, text="Devolver Libro", command=devolver_libro).grid(row=0, column=2, padx=10)

# Lista de préstamos
frame_lista_prestamos = ttk.LabelFrame(tab_prestamos, text="Préstamos Activos", padding=10)
frame_lista_prestamos.pack(fill="both", expand=True, padx=10, pady=5)

columns_prestamos = ("ID", "Libro", "Usuario", "Fecha Préstamo", "Devuelto")
tree_prestamos = ttk.Treeview(frame_lista_prestamos, columns=columns_prestamos, show="headings", height=12)

for col in columns_prestamos:
    tree_prestamos.heading(col, text=col)
    tree_prestamos.column(col, width=120)

tree_prestamos.pack(fill="both", expand=True)


# ========== FUNCIONES INICIALES ==========
def cargar_datos_iniciales():
    if db.connect():
        actualizar_lista_libros()
        actualizar_lista_usuarios()
        actualizar_lista_prestamos()
        messagebox.showinfo("Conexión", "Conectado a la base de datos correctamente")
    else:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")


# Cargar datos al iniciar
root.after(100, cargar_datos_iniciales)


# Configurar cierre seguro
def on_closing():
    db.disconnect()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

# Información de la aplicación
info_label = ttk.Label(root, text="Sistema de Gestión de Biblioteca - Base de Datos Adaptada",
                       font=("Arial", 10, "italic"))
info_label.pack(side="bottom", pady=5)

root.mainloop()