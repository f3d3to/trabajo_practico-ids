-- Eliminar tablas si ya existen (en orden inverso de dependencias)
DROP TABLE IF EXISTS contactos;
DROP TABLE IF EXISTS casas_transito;
DROP TABLE IF EXISTS preguntas_frecuentes;
DROP TABLE IF EXISTS mascotas;

-- Crear la tabla de mascotas
CREATE TABLE IF NOT EXISTS mascotas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    especie ENUM('perro', 'gato', 'otro') NOT NULL,
    genero ENUM('macho', 'hembra') NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    raza VARCHAR(255),
    color VARCHAR(255),
    condicion ENUM('lastimada', 'sana'),
    estado ENUM('perdida', 'en transito', 'en adopcion') NOT NULL,
    foto_url VARCHAR(255),
    zona VARCHAR(255),
    barrio VARCHAR(255),
    latitud FLOAT,
    longitud FLOAT,
    informacion_contacto VARCHAR(255),
    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear la tabla de casas de tránsito
CREATE TABLE IF NOT EXISTS casas_transito (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_mascota INT NOT NULL,
    latitud FLOAT,   -- Coordenada de latitud para ubicación de tránsito
    longitud FLOAT,  -- Coordenada de longitud para ubicación de tránsito
    informacion_contacto VARCHAR(255) NOT NULL,
    fecha_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_mascota) REFERENCES mascotas(id) ON DELETE CASCADE
);

-- Crear la tabla de preguntas frecuentes
CREATE TABLE IF NOT EXISTS preguntas_frecuentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pregunta TEXT NOT NULL,
    respuesta TEXT NOT NULL
);

-- Crear la tabla de contactos
CREATE TABLE IF NOT EXISTS contactos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    mensaje TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos de prueba en la tabla de mascotas con las imágenes proporcionadas
INSERT INTO mascotas (nombre, especie, raza, color, condicion, zona, barrio, latitud, longitud, foto_url, estado, informacion_contacto)
VALUES
    ('Teddy', 'perro', 'Husky', 'blanco y negro', 'sana', 'Palermo', 'Recoleta', -34.6037, -58.3816, 'https://unsplash.com/es/fotos/perro-blanco-y-negro-de-pelo-largo-durante-el-dia-mx0DEnfYxic', 'perdida', '+54 9 111 222 3333'),
    ('Milo', 'gato', 'Siames', 'gris', 'lastimada', 'Belgrano', 'Nuñez', -34.5614, -58.4567, 'https://unsplash.com/es/fotos/white-and-gray-cat-IFxjDdqK_0U', 'en transito', '+54 9 111 333 4444'),
    ('Pepito', 'otro', 'Loro', 'verde', 'sana', 'Caballito', 'Parque Chacabuco', -34.6234, -58.4011, 'https://unsplash.com/es/fotos/un-loro-verde-sentado-encima-de-un-trozo-de-madera-veSNcVHgjYU', 'en adopcion', '+54 9 111 555 6666');

-- Insertar datos de prueba en la tabla de casas de tránsito
INSERT INTO casas_transito (id_mascota, latitud, longitud, informacion_contacto)
VALUES
    (2, -34.5614, -58.4567, '+54 9 111 333 4444');

-- Insertar datos de prueba en la tabla de preguntas frecuentes
INSERT INTO preguntas_frecuentes (pregunta, respuesta)
VALUES
    ('¿Cómo agrego una mascota perdida?', 'Para agregar una mascota perdida, completa el formulario en la sección "Agregar Mascota".'),
    ('¿Cómo elimino una publicación?', 'Para eliminar una publicación, ve a tu perfil y selecciona la opción de eliminar.'),
    ('¿Puedo editar los datos de mi publicación?', 'Sí, puedes editar los datos desde la sección de edición de publicaciones.');

-- Insertar datos de prueba en la tabla de contactos
INSERT INTO contactos (nombre, email, mensaje)
VALUES
    ('Juan Pérez', 'juanperez@example.com', 'Hola, quisiera saber cómo puedo publicar una mascota que encontré.'),
    ('Maria Garcia', 'maria@example.com', '¿Es posible actualizar la ubicación de una mascota que publiqué?');
