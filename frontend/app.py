from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def cargar_mascota():
    return render_template('cargarMascotaPerdida.html')

if __name__ == '__main__':
    app.run(debug=True)
