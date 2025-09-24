Sistema de Gestión de Biblioteca Personal

1.Descripción del Proyecto

Sistema desarrollado en Python con interfaz gráfica Tkinter para la gestión completa de una biblioteca personal. Permite administrar libros, usuarios y controlar préstamos de manera eficiente mediante una aplicación de escritorio.

2.Características Principales

Gestión completa de libros (agregar, editar, eliminar, buscar)

Registro y administración de usuarios

Sistema de préstamos y devoluciones

Interfaz intuitiva organizada en pestañas

Base de datos MySQL para almacenamiento persistente

Validación de datos en tiempo real

3.Tecnologías Utilizadas

Lenguaje de programación: Python

Interfaz gráfica: Tkinter

Base de datos: MySQL

Herramientas de desarrollo: XAMPP, HeidiSQL

Control de versiones: Git

4.Requisitos del Sistema

Python 3.8 o superior

XAMPP (para servidor MySQL)

HeidiSQL (opcional, para gestión de BD)

Conexión a internet (para instalación de dependencias)

5.Configurar Base de Datos

Iniciar XAMPP y asegurar que MySQL esté ejecutándose

Ejecutar el script docs/database-schema.sql en HeidiSQL o phpMyAdmin

Verificar que la base de datos biblioteca_personal esté creada

6.Estructura de la Base de Datos

Tabla: libros
id (INT, PRIMARY KEY, AUTO_INCREMENT)

titulo (VARCHAR(100), NOT NULL)

autor (VARCHAR(100), NOT NULL)

genero (VARCHAR(50))

año_publicacion (INT)

isbn (VARCHAR(20))

disponible (BOOLEAN, DEFAULT TRUE)

Tabla: usuarios
id (INT, PRIMARY KEY, AUTO_INCREMENT)

nombre (VARCHAR(100), NOT NULL)

email (VARCHAR(100), UNIQUE, NOT NULL)

telefono (VARCHAR(15))

fecha_registro (DATE, DEFAULT CURRENT_DATE)

Tabla: prestamos
id (INT, PRIMARY KEY, AUTO_INCREMENT)

libro_id (INT, FOREIGN KEY)

usuario_id (INT, FOREIGN KEY)

fecha_prestamo (DATE, DEFAULT CURRENT_DATE)

fecha_devolucion (DATE)

devuelto (BOOLEAN, DEFAULT FALSE)

7.Funcionalidades Implementadas

Módulo de Libros
Registro de nuevos libros con todos sus datos

Búsqueda y edición de información existente

Eliminación controlada de registros

Validación de campos obligatorios

Módulo de Usuarios
Registro de usuarios con datos de contacto

Gestión de información personal

Control de duplicados por email

Módulo de Préstamos
Registro de préstamos vinculando libros y usuarios

Control de devoluciones y estados

Actualización automática de disponibilidad

Historial completo de transacciones

8.Uso de la Aplicación

Gestión de Libros: Utilice la pestaña "Libros" para agregar, modificar o eliminar libros del inventario.

Registro de Usuarios: En la pestaña "Usuarios" puede gestionar los miembros de la biblioteca.

Control de Préstamos: La pestaña "Préstamos" permite registrar préstamos y devoluciones.

9.Desarrollo

Este proyecto fue desarrollado como parte de un trabajo académico para demostrar habilidades en:

Programación orientada a objetos

Diseño de interfaces gráficas

Gestión de bases de datos 
