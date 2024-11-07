from flask import Flask, render_template

app = Flask(__name__)

@app.route('/cargarMascota')
def cargar_mascota():
    return render_template('cargarMascotaPerdida.html')

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/preguntasFrecuentes")
def preguntasFrecuentes():
    return render_template("preguntasFrecuentes.html")

if __name__ == '__main__':
    app.run(debug=True)
