from flask import Flask, render_template, request, redirect, url_for
import requests, os

app = Flask(__name__)

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
            try:
                requests.post(BACKEND_URL+"/agregar_mascota", json=mascota_data)
            except requests.exceptions.RequestException:
                print("Error de conexión con el backend.")
        return redirect(url_for('cargar_mascota'))
    return render_template('cargarMascotaPerdida.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/')
def index():
    return render_template('home.html')

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

@app.route("/busquedaMascota")
def busquedaMascota():
    return render_template("busquedaMascota.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5001)
