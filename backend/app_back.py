# Third Party
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, false
# Proyecto
from config import DATABASE_URI, verificar_conexion
from queries import MascotaDAO, PreguntasFrecuentesDAO, ContactoDAO
# Python
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)

# Ejemplo de cómo instanciar un DAO para cualquier tabla en la base de datos
# dao = <Tabla>DAO()  # La idea es reemplazar "<Tabla>" con el nombre de la clase DAO
mascota_dao = MascotaDAO()
preguntas_frecuentes_dao = PreguntasFrecuentesDAO()
contacto_dao = ContactoDAO()

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_URI = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?charset=utf8mb4"
engine = create_engine(DATABASE_URI)

@app.route('/obtener_esquema', methods=['POST'])
def obtener_esquema():
    data = request.json
    entidad = data.get("tabla")

    if entidad == mascota_dao.table_name:
        schema = mascota_dao.schema
    else:
        return jsonify(success=False, errors=["Entidad no especificada o no válida."]), 400

    esquema_descripcion = {campo: tipo.__name__ for campo, tipo in schema.items()}
    return jsonify(success=True, entidad=entidad, esquema=esquema_descripcion), 200


@app.route('/obtener_esquema_contacto', methods=['POST'])
def obtener_esquema_contacto():
    data = request.json
    entidad = data.get("tabla")

    if entidad == contacto_dao.table_name:
        schema = contacto_dao.schema
    else:
        return jsonify(success=False, errors=["Entidad no especificada o no válida."]), 400


    esquema_descripcion = {campo: tipo.__name__ for campo, tipo in schema.items()}
    return jsonify(success=True, entidad=entidad, esquema=esquema_descripcion), 200



@app.route('/agregar_mascota', methods=['POST'])
def agregar_mascota():
    data = request.json
    try:
        id_nueva_mascota = mascota_dao.insertar(data)
        if id_nueva_mascota:
            return jsonify({"success": True, "id": id_nueva_mascota}), 201
        else:
            print("Error al insertar la mascota.")
            return jsonify({"success": False, "error": "No se pudo insertar la mascota"}), 500
    except Exception as e:
        print("Excepción al intentar insertar en la base de datos:", e)
        return jsonify({"success": False, "error": str(e)}), 500


# Ejemplo de endpoint para actualizar un registro de la tabla <Tabla> utilizando el DAO.
# @app.route("/api/<tabla>/<int:id>", methods=["PUT"])
# def actualizar_<tabla>(id):
#     """
#     """
#     # data = request.json  # Captura los datos de la solicitud
#     # dao.actualizar(id, data)  # Llama al método del modelo <Tabla>Dao `actualizar` del DAO.
#     # return jsonify({"message": "Registro actualizado correctamente"}), 200

@app.route('/api/mascotas/<int:id>', methods=['GET'])
def obtener_mascota(id):
    try:
        # Usar el DAO para obtener la mascota por ID
        mascota = mascota_dao.obtener_por_id(id)

        if mascota:
            return jsonify({"success": True, "mascota": mascota}), 200
        else:
            return jsonify({"success": False, "error": "Mascota no encontrada"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/mascotas/<int:id>', methods=['PUT'])
def actualizar_mascota(id):
    data = request.json

    try:
        mascota_dao.actualizar(id, data)

        return jsonify({"success": True, "message": "Mascota actualizada correctamente"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/mascotas', methods=['GET'])
def obtener_mascotas():
    # DAtos del form
    filtros = {
        'nombre': request.args.get('nombre'),
        'especie': request.args.get('especie'),
        'raza': request.args.get('raza'),
        'genero': request.args.get('sexo'),
        'zona': request.args.get('zona'),
        'barrio': request.args.get('barrio'),
        'color': request.args.get('color'),
        'informacion_contacto': request.args.get('informacion_contacto'),
        'fecha_publicacion': request.args.get('fecha_publicacion'),
    }
    filtros = {key: value for key, value in filtros.items() if value}
    try:
        mascotas = mascota_dao.obtener_todos(filtros)
        return jsonify(mascotas), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/agregar_contacto', methods=['POST'])
def agregar_contacto():
    data = request.json
    try:
        id_contacto_nuevo = contacto_dao.insertar(data)
        if id_contacto_nuevo:
            return jsonify({"success": True, "id": id_contacto_nuevo}), 201
        else:
            print("Error al enviar el mensaje.")
            return jsonify({"success": False, "error": "No se pudo enviar el mensaje"}), 500
    except Exception as e:
        print("Excepción al intentar insertar en la base de datos:", e)
        return jsonify({"success": False, "error": str(e)}), 500

# Preguntas Frecuentes
@app.route('/api/preguntas_frecuentes', methods=['GET'])
def obtener_preguntas_frecuentes():
    try:
        preguntas = preguntas_frecuentes_dao.obtener_todos()
        return jsonify({"success": True, "preguntas_frecuentes": preguntas}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/mascotas/<int:id>", methods=['DELETE'])
def eliminar_mascotas(id):
    try:
        mascota_dao.borrar(id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/transito/", methods=['GET'])
def obtener_mascotas_transito():
    try:
        data = request.json()
        if data:
            if "estado" not in data:
                data["estado"] = "en transito"
            resultado = mascota_dao.obtener_todos(data)
            if len(resultado) == 0:
                return jsonify({"success": False, "error": "no hubo coincidencias"}), 404
            return jsonify({"success": True, "mascotas_transito": resultado}), 200
        resultado = mascota_dao.obtener_todos({"estado": "en transito"})
        return jsonify({"success": True, "mascotas_transito": resultado}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/reportar-encontrado", methods=['POST'])
def reportar_encontrado(id):
    try:
        data = request.json()
        if "estado" not in data:
            data["estado"] = "encontrada"
        mascota_dao.actualizar(id, data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/transito/", methods=['POST'])
def mascota_reportar_transito(id):
    try:
        data = request.json()
        if "estado" not in data:
            data["estado"] = "en transito"
        mascota_dao.actualizar(id, data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
    verificar_conexion()