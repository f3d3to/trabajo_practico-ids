from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from .config import engine

# Esquemas para las tablas
MASCOTA_SCHEMA = {
    "especie": str,
    "genero": str,
    "nombre": str,
    "raza": str,
    "color": str,
    "condicion": str,
    "estado": str,
    "foto_url": str,
    "zona": str,
    "barrio": str,
    "latitud": float,
    "longitud": float,
    "informacion_contacto": str,
}

PREGUNTAS_FRECUENTES_SCHEMA = {
    "pregunta": str,
    "respuesta": str,
}

CONTACTO_SCHEMA = {
    "nombre": str,
    "email": str,
    "mensaje": str,
    "telefono": str,
    "asunto": str,
}

# Función base para ejecutar consultas SQL
def run_query(query, parameters=None, fetch="all"):
    """
    Ejecuta una consulta SQL y maneja errores de SQLAlchemy.

    Parámetros:
    - query (str): Consulta SQL.
    - parameters (dict): Parámetros para la consulta.
    - fetch (str): 'all' para todos los resultados, 'one' para un solo resultado.

    Retorna:
    - Resultados de la consulta, si los hay.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), parameters or {})
            conn.commit()

            if result.returns_rows:
                if fetch == "one":
                    row = result.fetchone()
                    return dict(row._mapping) if row else None
                elif fetch == "all":
                    return [dict(row._mapping) for row in result.fetchall()]

            return None
    except SQLAlchemyError as e:
        print("Error al ejecutar la consulta:", e)
        return None

# Función para validar datos según un esquema
def validate_data(data, schema):
    """
    Valida un conjunto de datos contra un esquema.

    Parámetros:
    - data (dict): Datos a validar.
    - schema (dict): Esquema que define los tipos de datos.

    Retorna:
    - Datos validados listos para insertar o actualizar.
    """
    validated_data = {}
    for key, expected_type in schema.items():
        value = data.get(key)
        if value is None:
            continue  # Permitir campos opcionales
        if not isinstance(value, expected_type):
            raise ValueError(f"{key} debe ser de tipo {expected_type.__name__}.")
        if isinstance(value, str) and len(value) > 255:
            raise ValueError(f"{key} excede la longitud máxima de 255 caracteres.")
        validated_data[key] = value
    return validated_data

# Función para obtener todos los registros con filtros opcionales
def obtener_todos(table_name, schema, filters=None):
    """
    Obtiene todos los registros de una tabla, con filtros opcionales.

    Parámetros:
    - table_name (str): Nombre de la tabla.
    - schema (dict): Esquema para validar filtros.
    - filters (dict): Filtros opcionales.

    Retorna:
    - Lista de registros que cumplen los filtros.
    """
    filters = validate_data(filters, schema) if filters else {}
    query = f"SELECT * FROM {table_name}"
    if filters:
        conditions = " AND ".join([f"{key} = :{key}" for key in filters])
        query += f" WHERE {conditions}"
    return run_query(query, filters)

# Función para obtener un registro por ID
def obtener_por_id(table_name, id):
    """
    Obtiene un registro único por su ID.

    Parámetros:
    - table_name (str): Nombre de la tabla.
    - id (int): ID del registro.

    Retorna:
    - Registro correspondiente al ID.
    """
    query = f"SELECT * FROM {table_name} WHERE id = :id"
    return run_query(query, {"id": id}, fetch="one")

# Función para insertar un nuevo registro
def insertar(table_name, schema, data):
    """
    Inserta un nuevo registro en la tabla.

    Parámetros:
    - table_name (str): Nombre de la tabla.
    - schema (dict): Esquema para validar los datos.
    - data (dict): Datos a insertar.

    Retorna:
    - ID del nuevo registro.
    """
    validated_data = validate_data(data, schema)
    columns = ", ".join(validated_data.keys())
    placeholders = ", ".join([f":{key}" for key in validated_data.keys()])
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    run_query(query, validated_data)
    last_id_query = "SELECT LAST_INSERT_ID() AS id"
    result = run_query(last_id_query, fetch="one")
    return result["id"] if result else None

# Función para actualizar un registro por ID
def actualizar(table_name, schema, id, data):
    """
    Actualiza un registro en la tabla por su ID.

    Parámetros:
    - table_name (str): Nombre de la tabla.
    - schema (dict): Esquema para validar los datos.
    - id (int): ID del registro.
    - data (dict): Datos a actualizar.
    """
    validated_data = validate_data(data, schema)
    validated_data["id"] = id
    set_clause = ", ".join([f"{key} = :{key}" for key in validated_data if key != "id"])
    query = f"UPDATE {table_name} SET {set_clause} WHERE id = :id"
    run_query(query, validated_data)

# Función para eliminar un registro por ID
def borrar(table_name, id):
    """
    Elimina un registro de la tabla por su ID.

    Parámetros:
    - table_name (str): Nombre de la tabla.
    - id (int): ID del registro.
    """
    query = f"DELETE FROM {table_name} WHERE id = :id"
    run_query(query, {"id": id})

# Ejemplo para usar las funciones CRUD en cualquier tabla:
# Para insertar un registro:
#    insertar("<nombre_de_tabla>", <nombre_de_esquema>, {"campo1": valor, "campo2": valor, ...})
# Para obtener todos los registros:
#    obtener_todos("<nombre_de_tabla>", <nombre_de_esquema>, {"campo_filtro": valor})
# Para obtener un registro por ID:
#    obtener_por_id("<nombre_de_tabla>", id)
# Para actualizar un registro:
#    actualizar("<nombre_de_tabla>", <nombre_de_esquema>, id, {"campo": nuevo_valor})
# Para borrar un registro:
#    borrar("<nombre_de_tabla>", id)

# Ejemplo para 'mascotas':
# insertar("mascotas", MASCOTA_SCHEMA, {"nombre": "Buddy", "especie": "perro", "genero": "macho", ...})
# obtener_todos("mascotas", MASCOTA_SCHEMA, {"especie": "perro"})
# obtener_por_id("mascotas", 1)
# actualizar("mascotas", MASCOTA_SCHEMA, 1, {"nombre": "Buddy Actualizado"})
# borrar("mascotas", 1)

# Ejemplo para 'preguntas_frecuentes':
# insertar("preguntas_frecuentes", PREGUNTAS_FRECUENTES_SCHEMA, {"pregunta": "¿Cómo registro una mascota?", "respuesta": "Desde el formulario principal"})
# obtener_todos("preguntas_frecuentes", PREGUNTAS_FRECUENTES_SCHEMA)
# obtener_por_id("preguntas_frecuentes", 1)
# actualizar("preguntas_frecuentes", PREGUNTAS_FRECUENTES_SCHEMA, 1, {"respuesta": "Usa la opción de registro"})
# borrar("preguntas_frecuentes", 1)

# Ejemplo para 'contactos':
# insertar("contactos", CONTACTO_SCHEMA, {"nombre": "Juan", "email": "juan@example.com", "mensaje": "Quiero adoptar", ...})
# obtener_todos("contactos", CONTACTO_SCHEMA)
# obtener_por_id("contactos", 1)
# actualizar("contactos", CONTACTO_SCHEMA, 1, {"mensaje": "Interesado en más detalles"})
# borrar("contactos", 1)
