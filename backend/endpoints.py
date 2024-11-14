
from flask import Flask, request, render_template, session, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
app = Flask(__name__)
engine = create_engine('mysql://root:capoeze25@localhost:3306/huellas a casa')
Session = scoped_session(sessionmaker(bind=engine))

QUERY_DELETE = "delete from mascotas where nombre = :nombre and especie = :especie and sexo = :sexo"
QUERY_CHEQUEO = "select id from mascotas where nombre = :nombre and especie = :especie and sexo = :sexo"

@app.route('/api/mascota/', methods=['DELETE'])
def eliminar_mascota():
     data = request.get_json()
     keys =["nombre", "especie", "sexo"]
     for key in keys:
         if key not in data:
             return jsonify({"error": "falta" + key + "!"}), 400
     try:
        conn = Session()
        check = conn.execute(text(QUERY_CHEQUEO), params = data).fetchall()
        if len(check) == 0:
            return  jsonify({"error": "no se encontro" }), 404
        result = conn.execute(text(QUERY_DELETE), params = data)
        conn.commit()
        conn.close()
        return jsonify({"nombre": data["nombre"], "especie": data["especie"], "sexo":data["sexo"]}), 200
     except Exception as e:
         return jsonify({"error": str(e)}), 404


if __name__ == '__main__':
    app.run(debug=True)