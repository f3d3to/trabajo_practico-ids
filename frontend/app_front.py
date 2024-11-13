from flask import Flask, render_template

app = Flask(__name__)

@app.route('/cargarMascota/')
def cargar_mascota():
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
    app.run(host='0.0.0.0',debug=True, port=5001)
