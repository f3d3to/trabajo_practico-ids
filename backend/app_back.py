# Third Party
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
# Proyecto
from .config import DATABASE_URI, verificar_conexion
from .queries import (
    insertar,
    obtener_todos,
    obtener_por_id,
    actualizar,
    borrar,
    MASCOTA_SCHEMA,
    PREGUNTAS_FRECUENTES_SCHEMA,
    CONTACTO_SCHEMA
)
# Python
import os

UPLOAD_FOLDER = os.getenv('USER_IMAGES_FOLDER', 'uploads/user_images/')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)

engine = create_engine(DATABASE_URI, connect_args={"charset": "utf8mb4"})
app.config['JSON_AS_ASCII'] = False


@app.route('/obtener_esquema', methods=['POST'])
def obtener_esquema():
    data = request.json
    entidad = data.get("tabla")

    if entidad == "mascotas":
        schema = MASCOTA_SCHEMA
    elif entidad == "contactos":
        schema = CONTACTO_SCHEMA
    elif entidad == "preguntas_frecuentes":
        schema = PREGUNTAS_FRECUENTES_SCHEMA
    else:
        return jsonify(success=False, errors=["Entidad no especificada o no válida."]), 400

    esquema_descripcion = {campo: tipo.__name__ for campo, tipo in schema.items()}
    return jsonify(success=True, entidad=entidad, esquema=esquema_descripcion), 200


@app.route('/agregar_mascota', methods=['POST'])
def agregar_mascota():
    data = request.json
    try:
        id_nueva_mascota = insertar("mascotas", MASCOTA_SCHEMA, data)
        if id_nueva_mascota:
            return jsonify({"success": True, "id": id_nueva_mascota}), 201
        else:
            return jsonify({"success": False, "error": "No se pudo insertar la mascota"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/mascotas/<int:id>', methods=['GET'])
def obtener_mascota(id):
    try:
        mascota = obtener_por_id("mascotas", id)
        if mascota:
            return jsonify({"success": True, "mascota": mascota}), 200
        else:
            return jsonify({"success": False, "error": "Mascota no encontrada"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/mascotas/<int:id>', methods=['POST'])
def actualizar_mascota(id):
    data = request.json
    try:
        actualizar("mascotas", MASCOTA_SCHEMA, id, data)
        return jsonify({"success": True, "message": "Mascota actualizada correctamente"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/mascotas', methods=['GET'])
def obtener_mascotas():
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
        mascotas = obtener_todos("mascotas", MASCOTA_SCHEMA, filtros)
        return jsonify(mascotas), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/agregar_contacto', methods=['POST'])
def agregar_contacto():
    data = request.json
    try:
        id_contacto_nuevo = insertar("contactos", CONTACTO_SCHEMA, data)
        if id_contacto_nuevo:
            return jsonify({"success": True, "id": id_contacto_nuevo}), 201
        else:
            return jsonify({"success": False, "error": "No se pudo enviar el mensaje"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/preguntas_frecuentes', methods=['GET'])
def obtener_preguntas_frecuentes():
    try:
        preguntas = obtener_todos("preguntas_frecuentes", PREGUNTAS_FRECUENTES_SCHEMA)
        return jsonify({"success": True, "preguntas_frecuentes": preguntas}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({"success": True, "file_url": f"/user_images/{filename}"}), 201
    return jsonify({"success": False, "error": "Invalid file type"}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/user_images/<filename>')
def serve_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename)

@app.route("/api/mascotas/<int:id>", methods=['DELETE'])
def eliminar_mascotas(id):
    try:
        borrar_mascota = borrar(MASCOTA_SCHEMA, id)
        # mascota_dao.borrar(id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# @app.route("/api/transito/", methods=['GET'])
# def obtener_mascotas_transito():
#     try:
#         data = request.json()
#         if data:
#             if "estado" not in data:
#                 data["estado"] = "en transito"
#             resultado = mascota_dao.obtener_todos(data)
#             if len(resultado) == 0:
#                 return jsonify({"success": False, "error": "no hubo coincidencias"}), 404
#             return jsonify({"success": True, "mascotas_transito": resultado}), 200
#         resultado = mascota_dao.obtener_todos({"estado": "en transito"})
#         return jsonify({"success": True, "mascotas_transito": resultado}), 200
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# @app.route("/api/reportar-encontrado", methods=['POST'])
# def reportar_encontrado(id):
#     try:
#         data = request.json()
#         if "estado" not in data:
#             data["estado"] = "encontrada"
#         mascota_dao.actualizar(id, data)
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# @app.route("/api/transito/", methods=['POST'])
# def mascota_reportar_transito(id):
#     try:
#         data = request.json()
#         if "estado" not in data:
#             data["estado"] = "en transito"
#         mascota_dao.actualizar(id, data)
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
    verificar_conexion()
