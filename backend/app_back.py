from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from .config import DATABASE_URI, verificar_conexion
from .queries import MascotaDAO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)

# Ejemplo de cómo instanciar un DAO para cualquier tabla en la base de datos
# dao = <Tabla>DAO()  # La idea es reemplazar "<Tabla>" con el nombre de la clase DAO
mascota_dao = MascotaDAO()


# app_back.py
from flask import Flask, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import os

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_URI = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URI)



@app.route('/test_db_connection')
def test_db_connection():
    try:
        # Intenta conectar a la base de datos y ejecuta una consulta de prueba
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return jsonify({"connected": True, "result": [row[0] for row in result]})
    except OperationalError:
        return jsonify({"connected": False, "error": "No se pudo conectar a la base de datos"}), 500

@app.route('/')
def get_mascota():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM mascotas LIMIT 1"))
            mascota = result.fetchone()
            if mascota:
                mascota_data = {
                    "id": mascota[0],
                    "nombre": mascota[1],
                    "especie": mascota[2],
                    "raza": mascota[3],
                    "color": mascota[4],
                    "condicion": mascota[5],
                    "zona": mascota[6],
                    "barrio": mascota[7],
                    "latitud": mascota[8],
                    "longitud": mascota[9],
                    "foto_url": mascota[10],
                    "estado": mascota[11],
                    "informacion_contacto": mascota[12],
                    "fecha_publicacion": mascota[13]
                }
                return jsonify({"mascota": mascota_data})
            else:
                return jsonify({"error": "No se encontraron mascotas"}), 404
    except OperationalError as e:
        return jsonify({"connected": False, "error": str(e)}), 500


# Ejemplo de endpoint para actualizar un registro de la tabla <Tabla> utilizando el DAO.
# @app.route("/api/<tabla>/<int:id>", methods=["PUT"])
# def actualizar_<tabla>(id):
#     """
#     """
#     # data = request.json  # Captura los datos de la solicitud
#     # dao.actualizar(id, data)  # Llama al método del modelo <Tabla>Dao `actualizar` del DAO.
#     # return jsonify({"message": "Registro actualizado correctamente"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
    verificar_conexion()