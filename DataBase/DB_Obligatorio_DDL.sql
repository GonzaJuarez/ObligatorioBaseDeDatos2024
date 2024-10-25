-- Creacion de la base de datos --

CREATE DATABASE IF NOT EXISTS escuela_de_deportes;

USE escuela_de_deportes;

-- Creacion de tablas --

-- actividades (id,descripcion, costo)
CREATE TABLE IF NOT EXISTS actividades (
    id INT PRIMARY KEY AUTO_INCREMENT, -- 0, 1, 2
    descripcion VARCHAR(50) NOT NULL, -- snowboard, ski y moto de nieve
    costo DECIMAL(10,2) NOT NULL -- 100.00, 150.00, 200.00
);

-- equipamiento (id, id_actividad, descripcion, costo)
CREATE TABLE IF NOT EXISTS equipamiento (
    id INT PRIMARY KEY AUTO_INCREMENT, -- 0, 1, 2
    id_actividad INT NOT NULL, -- 0, 1, 2
    descripcion VARCHAR(50) NOT NULL, -- tabla, botas, casco
    costo DECIMAL(10,2) NOT NULL, -- 50.00, 30.00, 20.00
    FOREIGN KEY (id_actividad) REFERENCES actividades(id)
);

-- turnos (id, hora_inicio, hora_fin)
CREATE TABLE IF NOT EXISTS turnos (
    id INT PRIMARY KEY AUTO_INCREMENT, -- 0, 1, 2
    hora_inicio TIME NOT NULL, -- 08:00:00, 10:00:00, 12:00:00
    hora_fin TIME NOT NULL -- 10:00:00, 12:00:00, 14:00:00
);

-- roles (id, descripcion)
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT, -- 0, 1, 2
    descripcion VARCHAR(50), -- administrador, instructor, alumno
    PRIMARY KEY (id, descripcion)
);

-- personas (ci, nombre, apellido, fecha_nacimiento, rol, cel, correo)
CREATE TABLE IF NOT EXISTS personas (
    ci INT PRIMARY KEY, -- 12345678
    id_rol INT NOT NULL, -- 0, 1, 2
    nombre VARCHAR(50) NOT NULL, -- Juan
    apellido VARCHAR(50) NOT NULL, -- Perez
    fecha_nacimiento DATE NOT NULL, -- 1990-01-01
    cel INT NOT NULL, -- 091234567
    correo VARCHAR(50) NOT NULL, -- juanperez@gmail.com
    FOREIGN KEY (id_rol) REFERENCES roles(id)
);

-- login (correo, contraseña)
CREATE TABLE IF NOT EXISTS login (
    ci INT PRIMARY KEY, -- 12345678
    contraseña VARCHAR(50) NOT NULL, -- 123456
    FOREIGN KEY (ci) REFERENCES personas(ci)
);

-- clase (id, ci_instructor, id_actividad, id_turno, dictada)
-- si el ci de la persona tiene el rol de instructor, entonces es un instructor
CREATE TABLE IF NOT EXISTS clase (
    id INT PRIMARY KEY AUTO_INCREMENT, -- 0, 1, 2
    ci_instructor INT NOT NULL, -- 12345678
    id_actividad INT NOT NULL, -- 0, 1, 2
    id_turno INT NOT NULL, -- 0, 1, 2
    dictada BOOLEAN NOT NULL, -- true, false
    FOREIGN KEY (ci_instructor) REFERENCES personas(ci),
    FOREIGN KEY (id_actividad) REFERENCES actividades(id),
    FOREIGN KEY (id_turno) REFERENCES turnos(id)
);

-- alumno_clase (id_clase, ci_alumno, id_equipamiento)
-- si el ci de la persona tiene el rol de alumno, entonces es un alumno
CREATE TABLE IF NOT EXISTS alumno_clase (
    id_clase INT NOT NULL, -- 0, 1, 2
    ci_alumno INT NOT NULL, -- 12345678
    id_equipamiento INT NOT NULL, -- 0, 1, 2
    PRIMARY KEY (id_clase, ci_alumno),
    FOREIGN KEY (id_clase) REFERENCES clase(id),
    FOREIGN KEY (ci_alumno) REFERENCES personas(ci),
    FOREIGN KEY (id_equipamiento) REFERENCES equipamiento(id)
);

-- Cmabie las tablas de alumnos e instructores por personas, y cree una tabla de roles para diferenciarlos
-- Cambie la tabla login para que tenga una clave foranea sea ci referenciaso a la tabla personas

-- Insertar datos --

-- actividades
INSERT INTO actividades (descripcion, costo) VALUES
('snowboard', 100.00),
('ski', 150.00),
('moto de nieve', 200.00);

-- equipamiento
INSERT INTO equipamiento (id_actividad, descripcion, costo) VALUES
(1, 'tabla', 50.00),
(1, 'botas', 30.00),
(1, 'casco', 20.00),
(2, 'tabla', 50.00),
(2, 'botas', 30.00),
(2, 'casco', 20.00),
(3, 'tabla', 50.00),
(3, 'botas', 30.00),
(3, 'casco', 20.00);

-- turnos
INSERT INTO turnos (hora_inicio, hora_fin) VALUES
('08:00:00', '10:00:00'),
('10:00:00', '12:00:00'),
('12:00:00', '14:00:00');

-- roles
INSERT INTO roles (descripcion) VALUES
('Administrador'),
('Instructor'),
('Alumno');

-- personas
INSERT INTO personas (ci, id_rol, nombre, apellido, fecha_nacimiento, cel, correo) VALUES
(12345678, 1, 'Juan', 'Perez', '1990-01-01', 091234567, 'juanperez@gmail.com'),
(23456789, 2, 'Pedro', 'Gomez', '1980-01-01', 091234567, 'pedrogomez@gmail.com'),
(34567890, 3, 'Maria', 'Lopez', '2000-01-01', 091234567, 'marialopez@gmail.com');

-- login
INSERT INTO login (ci, contraseña) VALUES
('12345678', '123456'),
('23456789', '123456'),
('34567890', '123456');

-- clase
INSERT INTO clase (ci_instructor, id_actividad, id_turno, dictada) VALUES
(23456789, 1, 1, true),
(23456789, 2, 2, true),
(23456789, 3, 3, true);

-- alumno_clase
INSERT INTO alumno_clase (id_clase, ci_alumno, id_equipamiento) VALUES
(1, 34567890, 1),
(2, 34567890, 4),
(3, 34567890, 7);
