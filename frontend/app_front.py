from flask import Flask, render_template, request, redirect, url_for
import requests, os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/user_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

BACKEND_URL = os.getenv("BACKEND_URL")

def decodificar_utf8(cadena):
    """
    Recibe una cadena con caracteres codificados y los decodifica a UTF-8.
    """
    return {key: value.encode('latin1').decode('utf-8') if isinstance(value, str) else value for key, value in cadena.items()}

def castear_valores(data, esquema):
    tipos_y_valores = {"str": str, "int": int, "float": float, "bool": bool}
    valores_cast = {
        campo: tipos_y_valores[tipo_str](data[campo]) if campo in data else None
        for campo, tipo_str in esquema.items()
    }
    return valores_cast

@app.route('/cargarMascota', methods=['GET', 'POST'])
def cargar_mascota():
    if request.method == 'POST':
        esquema_response = requests.post(BACKEND_URL+"/obtener_esquema", json={"tabla": "mascotas"})
        if esquema_response.status_code == 200 and esquema_response.json().get("success"):
            esquema = esquema_response.json().get("esquema")
            mascota_data = castear_valores(request.form, esquema)

            imagen = request.files.get('foto')
            if imagen:
                filename = secure_filename(imagen.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagen.save(filepath)  # Guardar la imagen en 'static/user_images'
                mascota_data['foto_url'] = f"user_images/{filename}" if filename else None

            try:
                requests.post(BACKEND_URL+"/agregar_mascota", json=mascota_data)
            except requests.exceptions.RequestException:
                print("Error de conexión con el backend.")
        return redirect(url_for('cargar_mascota'))
    return render_template('cargarMascotaPerdida.html')


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        esquema_response = requests.post(BACKEND_URL+"/obtener_esquema_contacto", json={"tabla": "contactos"})
        if esquema_response.status_code == 200 and esquema_response.json().get("success"):
            esquema = esquema_response.json().get("esquema")
            contacto_data = castear_valores(request.form, esquema)
            try:
                requests.post(BACKEND_URL+"/agregar_contacto", json=contacto_data)
            except requests.exceptions.RequestException:
                print("Error de conexión con el backend.")
        return redirect(url_for('contacto'))
    return render_template('contacto.html')

@app.route("/")
def index():
    try:
        response = requests.get(f"{BACKEND_URL}/api/mascotas", params={'estado': 'perdida'})
        if response.status_code == 200:
            mascotas_perdidas = response.json()
        else:
            mascotas_perdidas = []
            print("Error al obtener mascotas perdidas:", response.json().get("error"))
    except requests.exceptions.RequestException as e:
        print("Error de conexión con el backend:", e)
        mascotas_perdidas = []
    return render_template("home.html", mascotas_perdidas=mascotas_perdidas)

@app.route("/preguntasFrecuentes")
def preguntasFrecuentes():
    try:
        response = requests.get(BACKEND_URL + "/api/preguntas_frecuentes")
        fq = []
        if response.status_code == 200 and response.json().get("success"):
            fq = [decodificar_utf8(pregunta) for pregunta in response.json().get("preguntas_frecuentes", [])]
    except requests.exceptions.RequestException:
        print("Error de conexión con el backend.")
        fq = []
    return render_template("preguntasFrecuentes.html", preguntas=fq)

@app.route("/busquedaMascota", methods=['GET'])
def busquedaMascota():
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
    filtros = {k: v for k, v in filtros.items() if v is not None and v != ''}
    try:
        response = requests.get(BACKEND_URL + "/api/mascotas", params=filtros)
        mascotas = response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException:
        print("Error de conexión con el backend.")
        mascotas = []

    return render_template("busquedaMascota.html", mascotas=mascotas)

<<<<<<< HEAD
@app.route("/detalleMascota")
def detalleMascota():
    return render_template("detalleMascota.html")
=======

@app.route('/updateMascota', methods=['GET', 'POST'])
def update_mascota():
    if request.method == 'POST':
        esquema_response = requests.post(BACKEND_URL+"/obtener_esquema", json={"tabla": "mascotas"})
        if esquema_response.status_code == 200 and esquema_response.json().get("success"):
            esquema = esquema_response.json().get("esquema")
            mascota_data = castear_valores(request.form, esquema)

            imagen = request.files.get('foto')
            if imagen:
                filename = secure_filename(imagen.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagen.save(filepath)  # Guardar la imagen en 'static/user_images'
                mascota_data['foto_url'] = f"user_images/{filename}" if filename else None

            try:
                requests.post(BACKEND_URL+"/agregar_mascota", json=mascota_data)
            except requests.exceptions.RequestException:
                print("Error de conexión con el backend.")
        return redirect(url_for('cargar_mascota'))
    return render_template('update.html')
>>>>>>> origin/update-mascota

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5001)
