USE escuela_de_deportes;

-- Triggers --

-- Tabla turnos --
-- Trigger para que no se puedan insertar turnos con los horarios superpuestas
DELIMITER //
CREATE TRIGGER turnos_fecha_superpuesta BEFORE INSERT ON turnos
FOR EACH ROW
BEGIN
    IF (SELECT COUNT(*) FROM turnos WHERE hora_inicio <= NEW.hora_fin AND hora_fin >= NEW.hora_inicio) > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se pueden insertar turnos con fechas superpuestas';
    END IF;
END //

-- Tabla login --
-- Trigger para que que la contraseña tenga por lo menos caracteres, por lo menos una mayuscula, y por lo menos un numero
DELIMITER //
CREATE TRIGGER login_password_formato BEFORE INSERT ON login
FOR EACH ROW
BEGIN
    IF (SELECT LENGTH(NEW.contraseña) < 8 OR NEW.contraseña REGEXP '^[a-z]+$' OR NEW.contraseña REGEXP '^[A-Z]+$' OR NEW.contraseña REGEXP '^[0-9]+$') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La contraseña debe tener por lo menos 8 caracteres, una mayuscula, y un numero';
    END IF;
END //


-- Pruebas de los triggers --

-- Insertar turnos con horarios superpuestos
INSERT INTO turnos (hora_inicio, hora_fin) VALUES ('08:00:00', '10:00:00');
INSERT INTO turnos (hora_inicio, hora_fin) VALUES ('09:00:00', '11:00:00');
INSERT INTO turnos (hora_inicio, hora_fin) VALUES ('07:00:00', '09:00:00');

-- Insertar contraseña con menos de 8 caracteres
INSERT INTO login (ci, contraseña) VALUES ('12345678', '1234567');
-- Insertar contraseña con solo letras minusculas
INSERT INTO login (ci, contraseña) VALUES ('12345678', 'gonasass');
-- Insertar contraseña con solo letras mayusculas
INSERT INTO login (ci, contraseña) VALUES ('12345678', 'GONASASS');