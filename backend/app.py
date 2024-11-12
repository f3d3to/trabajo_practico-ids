from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from backend.config import DATABASE_URI
from backend.queries import MascotaDAO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)

# Ejemplo de cómo instanciar un DAO para cualquier tabla en la base de datos
# dao = <Tabla>DAO()  # La idea es reemplazar "<Tabla>" con el nombre de la clase DAO
mascota_dao = MascotaDAO()

# Ejemplo de endpoint para actualizar un registro de la tabla <Tabla> utilizando el DAO.
# @app.route("/api/<tabla>/<int:id>", methods=["PUT"])
# def actualizar_<tabla>(id):
#     """
#     """
#     # data = request.json  # Captura los datos de la solicitud
#     # dao.actualizar(id, data)  # Llama al método del modelo <Tabla>Dao `actualizar` del DAO.
#     # return jsonify({"message": "Registro actualizado correctamente"}), 200

if __name__ == '__main__':
    app.run(debug=True)