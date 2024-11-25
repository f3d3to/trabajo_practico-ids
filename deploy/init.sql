-- Eliminar tablas si ya existen (en orden inverso de dependencias)
DROP TABLE IF EXISTS contactos;
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
    estado ENUM('perdida', 'en transito', 'en adopcion', 'encontrada') NOT NULL,
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
    telefono VARCHAR(50) NOT NULL,
    asunto VARCHAR(255) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos de prueba en la tabla de mascotas con las imágenes proporcionadas
INSERT INTO mascotas (nombre, especie, raza, color, condicion, zona, barrio, latitud, longitud, foto_url, estado, informacion_contacto)
VALUES
    ('Rocky', 'perro', 'Golden Retriever', 'dorado', 'sana', 'Palermo', 'Recoleta', -34.6037, -58.3816, 'rocky.png', 'perdida', '+54 9 111 222 3333'),
    ('Nina', 'gato', 'Maine Coon', 'blanco y marrón', 'lastimada', 'Belgrano', 'Nuñez', -34.5614, -58.4567, 'nina.png', 'en transito', '+54 9 111 333 4444'),
    ('Charlie', 'otro', 'Cacatúa', 'blanco con amarillo', 'sana', 'Caballito', 'Parque Chacabuco', -34.6234, -58.4011, 'charlie.png', 'en adopcion', '+54 9 111 555 6666'),
    ('Lola', 'perro', 'Bulldog Francés', 'gris', 'sana', 'San Telmo', 'Constitución', -34.6158, -58.3897, 'lola.png', 'encontrada', '+54 9 111 444 5555'),
    ('Max', 'perro', 'Pastor Alemán', 'negro y marrón', 'sana', 'Retiro', 'Villa Crespo', -34.5957, -58.3822, 'max.png', 'perdida', '+54 9 111 123 4567'),
    ('Mimi', 'otro', 'Cabra', 'marrón con manchas', 'lastimada', 'Villa Urquiza', 'Coghlan', -34.5761, -58.4809, 'mimi.png', 'perdida', '+54 9 111 765 4321'),
    ('Coco', 'perro', 'Cocker Spaniel', 'marrón claro', 'sana', 'Almagro', 'Boedo', -34.6076, -58.4188, 'coco.png', 'perdida', '+54 9 111 999 8888');

-- Insertar datos de prueba en la tabla de preguntas frecuentes
INSERT INTO preguntas_frecuentes (pregunta, respuesta)
VALUES
    ('¿Cómo agrego una mascota perdida?', 'Para agregar una mascota perdida, completa el formulario en la sección "Agregar Mascota".'),
    ('¿Cómo elimino una publicación?', 'Para eliminar una publicación, ve a tu perfil y selecciona la opción de eliminar.'),
    ('¿Puedo editar los datos de mi publicación?', 'Sí, puedes editar los datos desde la sección de edición de publicaciones.');

-- Insertar datos de prueba en la tabla de contactos
INSERT INTO contactos (nombre, email, mensaje, telefono, asunto)
VALUES
    ('Juan Pérez', 'juanperez@example.com', 'Hola, quisiera saber cómo puedo publicar una mascota que encontré.', '22334455', 'Publicar mascota'),
    ('Maria Garcia', 'maria@example.com', '¿Es posible actualizar la ubicación de una mascota que publiqué?', '33445533', 'Actualizar mascota');
