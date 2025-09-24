-- =============================================
-- BASE DE DATOS: BIBLIOTECA PERSONAL
-- =============================================

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS biblioteca_personal;
USE biblioteca_personal;

-- =============================================
-- 1. TABLA: autores
-- =============================================
CREATE TABLE autores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    nacionalidad VARCHAR(50),
    fecha_nacimiento DATE
);

-- =============================================
-- 2. TABLA: libros
-- =============================================
CREATE TABLE libros (
    id INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(100) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    genero VARCHAR(50),
    año_publicacion INT,
    isbn VARCHAR(20),
    disponible BOOLEAN DEFAULT TRUE
);

-- =============================================
-- 3. TABLA: usuarios
-- =============================================
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    fecha_registro DATE DEFAULT CURRENT_DATE
);

-- =============================================
-- 4. TABLA: prestamos
-- =============================================
CREATE TABLE prestamos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    libro_id INT,
    usuario_id INT,
    fecha_prestamo DATE DEFAULT CURRENT_DATE,
    fecha_devolucion DATE,
    devuelto BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (libro_id) REFERENCES libros(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- =============================================
-- 5. TABLA: reseñas
-- =============================================
CREATE TABLE reseñas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    libro_id INT,
    usuario_id INT,
    calificacion INT CHECK (calificacion >= 1 AND calificacion <= 5),
    comentario TEXT,
    fecha_reseña DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (libro_id) REFERENCES libros(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- =============================================
-- INSERCIÓN DE DATOS DE EJEMPLO
-- =============================================

-- Insertar autores
INSERT INTO autores (nombre, nacionalidad, fecha_nacimiento) VALUES
('Gabriel García Márquez', 'Colombiano', '1927-03-06'),
('Isabel Allende', 'Chilena', '1942-08-02'),
('Mario Vargas Llosa', 'Peruano', '1936-03-28'),
('Julio Cortázar', 'Argentino', '1914-08-26'),
('Laura Esquivel', 'Mexicana', '1950-09-30');

-- Insertar libros
INSERT INTO libros (titulo, autor, genero, año_publicacion, isbn, disponible) VALUES
('Cien años de soledad', 'Gabriel García Márquez', 'Realismo mágico', 1967, '978-8437604947', TRUE),
('La casa de los espíritus', 'Isabel Allende', 'Novela', 1982, '978-8401337208', TRUE),
('La ciudad y los perros', 'Mario Vargas Llosa', 'Novela', 1963, '978-8466337241', TRUE),
('Rayuela', 'Julio Cortázar', 'Novela experimental', 1963, '978-8432216460', TRUE),
('Como agua para chocolate', 'Laura Esquivel', 'Novela romántica', 1989, '978-8420472667', TRUE),
('El amor en los tiempos del cólera', 'Gabriel García Márquez', 'Novela romántica', 1985, '978-8437604948', TRUE),
('Paula', 'Isabel Allende', 'Memorias', 1994, '978-8401337215', TRUE);

-- Insertar usuarios
INSERT INTO usuarios (nombre, email, telefono, fecha_registro) VALUES
('Ana García', 'ana.garcia@email.com', '555-1234', '2024-01-15'),
('Carlos López', 'carlos.lopez@email.com', '555-5678', '2024-01-20'),
('María Rodríguez', 'maria.rodriguez@email.com', '555-9012', '2024-02-01'),
('Pedro Martínez', 'pedro.martinez@email.com', '555-3456', '2024-02-10');

-- Insertar préstamos
INSERT INTO prestamos (libro_id, usuario_id, fecha_prestamo, fecha_devolucion, devuelto) VALUES
(1, 1, '2024-02-01', '2024-02-15', TRUE),
(2, 2, '2024-02-05', NULL, FALSE),
(3, 3, '2024-02-10', NULL, FALSE),
(4, 1, '2024-02-12', NULL, FALSE);

-- Insertar reseñas
INSERT INTO reseñas (libro_id, usuario_id, calificacion, comentario, fecha_reseña) VALUES
(1, 1, 5, 'Una obra maestra de la literatura latinoamericana. Absolutamente imprescindible.', '2024-02-16'),
(1, 2, 4, 'Muy bueno, aunque un poco confuso con tantos personajes.', '2024-02-18'),
(2, 3, 5, 'Isabel Allende en su máximo esplendor. Historia fascinante.', '2024-02-20'),
(3, 1, 3, 'Interesante, pero me costó engancharme con la historia.', '2024-02-22');

-- =============================================
-- VISTAS ÚTILES
-- =============================================

-- Vista: Libros disponibles
CREATE VIEW vista_libros_disponibles AS
SELECT l.id, l.titulo, l.autor, l.genero, l.año_publicacion
FROM libros l
WHERE l.disponible = TRUE;

-- Vista: Préstamos activos
CREATE VIEW vista_prestamos_activos AS
SELECT 
    p.id,
    l.titulo AS libro,
    u.nombre AS usuario,
    p.fecha_prestamo,
    DATEDIFF(CURRENT_DATE, p.fecha_prestamo) AS dias_prestado
FROM prestamos p
JOIN libros l ON p.libro_id = l.id
JOIN usuarios u ON p.usuario_id = u.id
WHERE p.devuelto = FALSE;

-- Vista: Reseñas con detalles
CREATE VIEW vista_reseñas_detalladas AS
SELECT 
    r.id,
    l.titulo AS libro,
    u.nombre AS usuario,
    r.calificacion,
    r.comentario,
    r.fecha_reseña
FROM reseñas r
JOIN libros l ON r.libro_id = l.id
JOIN usuarios u ON r.usuario_id = u.id;

-- =============================================
-- PROCEDIMIENTOS ALMACENADOS
-- =============================================

-- Procedimiento: Prestar un libro
DELIMITER //
CREATE PROCEDURE prestar_libro(IN p_libro_id INT, IN p_usuario_id INT)
BEGIN
    DECLARE libro_disponible BOOLEAN;
    
    -- Verificar si el libro está disponible
    SELECT disponible INTO libro_disponible FROM libros WHERE id = p_libro_id;
    
    IF libro_disponible THEN
        -- Registrar el préstamo
        INSERT INTO prestamos (libro_id, usuario_id, fecha_prestamo, devuelto)
        VALUES (p_libro_id, p_usuario_id, CURRENT_DATE, FALSE);
        
        -- Marcar libro como no disponible
        UPDATE libros SET disponible = FALSE WHERE id = p_libro_id;
        
        SELECT 'Préstamo registrado exitosamente' AS resultado;
    ELSE
        SELECT 'El libro no está disponible' AS resultado;
    END IF;
END //
DELIMITER ;

-- Procedimiento: Devolver un libro
DELIMITER //
CREATE PROCEDURE devolver_libro(IN p_prestamo_id INT)
BEGIN
    DECLARE v_libro_id INT;
    
    -- Obtener el ID del libro
    SELECT libro_id INTO v_libro_id FROM prestamos WHERE id = p_prestamo_id;
    
    -- Marcar préstamo como devuelto
    UPDATE prestamos 
    SET devuelto = TRUE, fecha_devolucion = CURRENT_DATE 
    WHERE id = p_prestamo_id;
    
    -- Marcar libro como disponible
    UPDATE libros SET disponible = TRUE WHERE id = v_libro_id;
    
    SELECT 'Devolución registrada exitosamente' AS resultado;
END //
DELIMITER ;

-- =============================================
-- CONSULTAS DE EJEMPLO
-- =============================================

-- Consulta 1: Mostrar todos los libros disponibles
SELECT '=== LIBROS DISPONIBLES ===' AS '';
SELECT titulo, autor, genero, año_publicacion 
FROM vista_libros_disponibles;

-- Consulta 2: Mostrar préstamos activos
SELECT '=== PRÉSTAMOS ACTIVOS ===' AS '';
SELECT libro, usuario, fecha_prestamo, dias_prestado 
FROM vista_prestamos_activos;

-- Consulta 3: Mostrar reseñas
SELECT '=== RESEÑAS ===' AS '';
SELECT libro, usuario, calificacion, comentario, fecha_reseña 
FROM vista_reseñas_detalladas;

-- Consulta 4: Libros por autor
SELECT '=== LIBROS POR AUTOR ===' AS '';
SELECT autor, COUNT(*) as total_libros 
FROM libros 
GROUP BY autor 
ORDER BY total_libros DESC;

-- Consulta 5: Calificación promedio por libro
SELECT '=== CALIFICACIONES PROMEDIO ===' AS '';
SELECT l.titulo, AVG(r.calificacion) as promedio_calificacion
FROM libros l
LEFT JOIN reseñas r ON l.id = r.libro_id
GROUP BY l.id, l.titulo
ORDER BY promedio_calificacion DESC;

-- =============================================
-- INSTRUCCIONES PARA USAR LA BASE DE DATOS
-- =============================================

SELECT '=== INSTRUCCIONES DE USO ===' AS '';
SELECT '1. Para prestar un libro: CALL prestar_libro(1, 1);' AS instruccion;
SELECT '2. Para devolver un libro: CALL devolver_libro(1);' AS instruccion;
SELECT '3. Ver libros disponibles: SELECT * FROM vista_libros_disponibles;' AS instruccion;
SELECT '4. Ver préstamos activos: SELECT * FROM vista_prestamos_activos;' AS instruccion;

-- =============================================
-- FIN DEL SCRIPT
-- =============================================