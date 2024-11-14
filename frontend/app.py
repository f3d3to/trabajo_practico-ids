from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno del archivo .env

app = Flask(__name__)

# Configura la URL del backend desde variables de entorno
BACKEND_URL = os.getenv("BACKEND_URL")

@app.route('/cargarMascota', methods=['GET', 'POST'])
def cargar_mascota():
    if request.method == 'POST':
        # Recoge los datos del formulario
        data = {
            "nombre": request.form.get("nombreMascota"),
            "especie": request.form.get("especie"),
            "raza": request.form.get("razaMascota"),
            "color": request.form.get("color"),
            "condicion": request.form.get("condicion"),
            "zona": request.form.get("zona"),
            "barrio": request.form.get("barrio"),
            "latitud": request.form.get("latitud"),
            "longitud": request.form.get("longitud"),
            "foto_url": request.form.get("foto_url"),
            "estado": request.form.get("estado"),
            "informacion_contacto": request.form.get("infoAdicional")
        }

        # Envía los datos al backend
        response = requests.post(f"{BACKEND_URL}/mascotas", json=data)

        if response.status_code == 201:
            return redirect(url_for('index'))  # Redirige a la página principal si se creó correctamente

    # Renderiza el formulario si es una solicitud GET
    return render_template('cargarMascotaPerdida.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/preguntasFrecuentes")
def preguntasFrecuentes():
    return render_template("preguntasFrecuentes.html")

@app.route("/busquedaMascota")
def busquedaMascota():
    return render_template("busquedaMascota.html")

if __name__ == '__main__':
    app.run(debug=True)
