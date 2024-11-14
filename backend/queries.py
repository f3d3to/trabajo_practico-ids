from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from .config import engine

class BaseDAO:
    """
    Clase base para crear DAOs (Data Access Objects) para cualquier tabla.
    - Implementa métodos CRUD (Create, Read, Update, Delete).
    - Valida tipos de datos de los campos.
    """

    def __init__(self, table_name, schema):
        """
        Inicializa el DAO con el nombre de la tabla y un esquema de validación.

        Parámetros:
        - table_name (str): Nombre de la tabla en la base de datos.
        - schema (dict): Esquema que define los tipos de datos de cada campo.

        Ejemplo de uso:
            Para crear un DAO para la tabla 'mascotas' con un esquema:
                schema = {"nombre": str, "especie": str, ...}
                dao = BaseDAO("mascotas", schema)
        """
        self.table_name = table_name
        self.schema = schema

    def _run_query(self, query, parameters=None, fetch="all"):
        """
        Ejecuta una consulta SQL y maneja errores de SQLAlchemy.

        Parámetros:
        - query (str): Consulta SQL en formato de cadena.
        - parameters (dict): Parámetros para la consulta.
        - fetch (str): 'all' para todos los resultados, 'one' para un solo resultado.

        Retorna:
        - El resultado de la consulta, si lo hay.
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
            print(f"Error de base de datos en {self.table_name}:", e)
            return None

    def obtener_todos(self, filters=None):
        """
        Obtiene todos los registros de la tabla, con filtros opcionales.

        Parámetros:
        - filters (dict): Filtros para la consulta. Ejemplo: {"especie": "perro"}

        Retorna:
        - Lista de todos los registros que cumplen los filtros.

        Ejemplo de uso:
            mascota_dao.obtener_todos({"especie": "perro"})
        """
        filters = self._validate_data(filters, self.schema) if filters else {}
        query = f"SELECT * FROM {self.table_name}"
        if filters:
            conditions = " AND ".join([f"{key} = :{key}" for key in filters])
            query += f" WHERE {conditions}"
        return self._run_query(query, filters)

    def obtener_por_id(self, id):
        """
        Obtiene un registro único de la tabla por su ID.

        Parámetros:
        - id (int): ID del registro a obtener.

        Retorna:
        - El registro correspondiente al ID.

        Ejemplo de uso:
            mascota_dao.obtener_por_id(1)
        """
        self._validate_data({"id": id}, {"id": int})
        query = f"SELECT * FROM {self.table_name} WHERE id = :id"
        return self._run_query(query, {"id": id}, fetch="one")

    def insertar(self, data):
        """
        Inserta un nuevo registro en la tabla.

        Parámetros:
        - data (dict): Datos a insertar, validados contra el esquema.

        Retorna:
        - El ID del nuevo registro.

        Ejemplo de uso:
            data = {"nombre": "Max", "especie": "perro", ...}
            mascota_dao.insertar(data)
        """
        validated_data = self._validate_data(data, self.schema)
        validated_data = self._flatten_data(validated_data)
        columns = ", ".join(validated_data.keys())
        placeholders = ", ".join([f":{key}" for key in validated_data.keys()])
        insert_query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        self._run_query(insert_query, validated_data)
        last_id_query = "SELECT LAST_INSERT_ID() AS id"
        result = self._run_query(last_id_query, fetch="one")
        return result["id"] if result else None

    def actualizar(self, id, data):
        """
        Actualiza un registro en la tabla por su ID.

        Parámetros:
        - id (int): ID del registro a actualizar.
        - data (dict): Datos a actualizar, validados contra el esquema.

        Ejemplo de uso:
            data = {"estado": "adoptado"}
            mascota_dao.actualizar(1, data)
        """
        validated_data = self._validate_data({"id": id, **data}, {"id": int, **self.schema})
        validated_data = self._flatten_data(validated_data)
        set_clause = ", ".join([f"{key} = :{key}" for key in validated_data if key != "id"])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = :id"
        self._run_query(query, validated_data)

    def borrar(self, id):
        """
        Elimina un registro de la tabla por su ID.

        Parámetros:
        - id (int): ID del registro a eliminar.

        Ejemplo de uso:
            mascota_dao.borrar(1)
        """
        self._validate_data({"id": id}, {"id": int})
        query = f"DELETE FROM {self.table_name} WHERE id = :id"
        self._run_query(query, {"id": id})

    def _validate_data(self, data, schema):
        """
        Valida los datos contra el esquema proporcionado.

        Parámetros:
        - data (dict): Datos a validar.
        - schema (dict): Esquema de tipos de datos.

        Retorna:
        - Datos validados listos para insertar o actualizar.
        """
        validated_data = {}
        for key, expected_type in schema.items():
            value = data.get(key)
            if value is None:
                continue  # Omite la validación para campos opcionales
            if isinstance(expected_type, dict):
                if not isinstance(value, dict):
                    raise ValueError(f"{key} debe ser un diccionario.")
                validated_data[key] = self._validate_data(value, expected_type)
            else:
                if not isinstance(value, expected_type):
                    raise ValueError(f"{key} debe ser de tipo {expected_type.__name__}.")
                if isinstance(value, str) and len(value) > 255:
                    raise ValueError(f"{key} excede la longitud máxima de 255 caracteres.")
                validated_data[key] = value
        return validated_data

    def _flatten_data(self, data, parent_key=""):
        """
        Convierte diccionarios anidados en un solo nivel con claves compuestas.

        Parámetros:
        - data (dict): Datos posiblemente anidados.

        Retorna:
        - Datos en un nivel.
        """
        flattened = {}
        for key, value in data.items():
            new_key = f"{parent_key}{key}" if not parent_key else f"{parent_key}_{key}"
            if isinstance(value, dict):
                flattened.update(self._flatten_data(value, new_key))
            else:
                flattened[new_key] = value
        return flattened


# DAOs específicos para tablas con esquemas únicos
class MascotaDAO(BaseDAO):
    """
    DAO para la tabla de 'mascotas' con un esquema específico.

    Ejemplo de ejecución del DAO:
        mascota_dao = MascotaDAO()
        mascota_dao.insertar({"nombre": "Max", "especie": "perro", ...})
    """
    def __init__(self):
        schema = {
            "especie": str,
            "genero":str,
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
        super().__init__("mascotas", schema)


# Ejemplo para implementar un <Tabla>DAO.
# class <Tabla>DAO(BaseDAO):
#     """
#     Implementación del DAO para la tabla '<nombre de la tabla>'.
#     Proporciona métodos CRUD para la tabla específica.
#     """
#     def __init__(self):
#         schema = {
#             "campo1": tipo_dato,
#             "campo2": tipo_dato,
#             (...),
#             "ubicacion": {  # Ejemplo de campo anidado para 'ubicacion' si aplica
#                 "latitud": float,
#                 "longitud": float
#             }
#         }
#         super().__init__("<nombre de la tabla>", schema)

# Ejemplo de uso de <Tabla>DAO:
# dao = <Tabla>DAO()
# 1. Insertar un nuevo registro en <Tabla>:
#    data = {"campo1": valor, "campo2": valor, (...)}
#    dao.insertar(data)
# 2. Obtener todos los registros de <Tabla>:
#    dao.obtener_todos()
# 3. Obtener un registro por ID en <Tabla>:
#    dao.obtener_por_id(id)
# 4. Actualizar un registro por ID en <Tabla>:
#    dao.actualizar(id, {"campo_actualizar": nuevo_valor, (...)})
# 5. Borrar un registro por ID en <Tabla>:
#    dao.borrar(id)
