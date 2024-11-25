from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import requests, os
from werkzeug.utils import secure_filename

app = Flask(__name__)

BACKEND_URL = os.getenv("BACKEND_URL")

def decodificar_utf8(cadena):
    """
    Recibe una cadena con caracteres codificados y los decodifica a UTF-8.
    """
    return {key: value.encode('latin1').decode('utf-8') if isinstance(value, str) else value for key, value in cadena.items()}

def decodificar_objeto_utf8(objeto):
    """
    Recibe un objeto/diccionario/lista y lo decodifica a UTF-8
    """
    if isinstance(objeto, dict):
        return {key: decodificar_objeto_utf8(value) for key, value in objeto.items()}
    elif isinstance(objeto, list):
        
        return [decodificar_objeto_utf8(elemento) for elemento in objeto]
    
    else:
        return objeto

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
                try:
                    # Subir la imagen al backend
                    filename = secure_filename(imagen.filename)
                    files = {'file': (filename, imagen.stream, imagen.mimetype)}
                    upload_response = requests.post(BACKEND_URL + "/upload", files=files)

                    # Verificar si la subida fue exitosa
                    if upload_response.status_code == 201 and upload_response.json().get("success"):
                        mascota_data['foto_url'] = upload_response.json().get("file_url")
                    else:
                        print("Error al subir la imagen:", upload_response.json())
                except requests.exceptions.RequestException as e:
                    print("Error al conectar con el backend para subir la imagen:", e)

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
    return render_template("home.html", mascotas_perdidas=decodificar_objeto_utf8(mascotas_perdidas))
    # return render_template("home.html", mascotas_perdidas=mascotas_perdidas)

@app.route("/preguntasFrecuentes")
def preguntasFrecuentes():
    try:
        response = requests.get(BACKEND_URL + "/api/preguntas_frecuentes")
        fq = []
        if response.status_code == 200 and response.json().get("success"):
            fq = response.json().get("preguntas_frecuentes", [])
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

    return render_template("busquedaMascota.html", mascotas=mascotas, image_url_backend="http://127.0.0.1:5000"+"/uploads/") # TO-DO: Cambiar URL harcodeada


@app.route("/detalleMascota/<int:id>")
def detalleMascota(id):
    try:
        response = requests.get(f"{BACKEND_URL}/api/mascotas/{id}")
        mascota = {}
        if response.status_code == 200 and response.json().get("success"):
            mascota = decodificar_objeto_utf8(response.json().get("mascota", {}))
            if 'fecha_publicacion' in mascota: # Darle formato a fecha_publicacion 
                try:
                    mascota['fecha_publicacion'] = datetime.strptime(mascota['fecha_publicacion'], "%a, %d %b %Y %H:%M:%S %Z")
                except ValueError as e:
                    print(f"Error al convertir fecha_publicacion: {e}")
            print(mascota)  
        elif response.status_code == 404:
            return render_template("detalleMascota.html", error="Mascota no encontrada.")
        else:
            return render_template("detalleMascota.html", error="Error inesperado al obtener los detalles.")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al backend: {e}")
        return render_template("detalleMascota.html", error="Error de conexión con el backend.")

    return render_template("detalleMascota.html", mascota=mascota)


@app.route('/actualizarMascota/<int:id>', methods=['GET', 'POST'])
def actualizarMascota(id):
    if request.method == 'GET':
        try:
            response = requests.get(f"{BACKEND_URL}/api/mascotas/{id}")
            mascota = {}
            if response.status_code == 200 and response.json().get("success"):
                mascota = response.json().get("mascota", {})
                print(mascota)  
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión al backend: {e}")
            return render_template("busquedaMascota.html", error="Error de conexión con el backend.")
        

    if request.method == 'POST':
        esquema_response = requests.post(BACKEND_URL+"/obtener_esquema", json={"tabla": "mascotas"})
        if esquema_response.status_code == 200 and esquema_response.json().get("success"):
            esquema = esquema_response.json().get("esquema")
            #mascota_data = castear_valores(request.form, esquema)

                    # mascota_data = {"especie": request.form.get("especie"),
                    #                 "genero": request.form.get("genero"),
                    #                 "nombre": request.form.get("nombre"),             
                    #                 "raza": request.form.get("raza"),             
                    #                 "color": request.form.get("color"),             
                    #                 "condicion": request.form.get("condicion"),             
                    #                 "estado": request.form.get("estado"),             
                    #                 "zona": request.form.get("zona"),             
                    #                 "barrio": request.form.get("barrio"),             
                    #                 "latitud": request.form.get("latitud"), 
                    #                 "longitud": request.form.get("longitud"), 
                    #                 "informacion_contacto": request.form.get("informacion_contacto"), }
             
            mascota_data = { "nombre": request.form.get("nombre"),
                            "raza": request.form.get("raza"),             
                            "color": request.form.get("color"),             
                            "condicion": request.form.get("condicion"),             
                            "estado": request.form.get("estado"),
                            "informacion_contacto": request.form.get("informacion_contacto")
                            }
            print(mascota_data)
            try:
                #requests.post(BACKEND_URL+"/agregar_mascota", json=mascota_data)
                response = requests.post(f"{BACKEND_URL}/api/mascotas/{id}", json=mascota_data)
                if response.status_code == 200 and response.json().get("success"):
                    print(f"Respuesta del backend: {response.json()}")
                    print("Mascota actualizada exitosamente.")
            except requests.exceptions.RequestException:
                print("Error de conexión con el backend.")
        return render_template('home.html')
    
    return render_template('actualizarMascota.html', mascota=mascota)


@app.route("/eliminarMascota/<int:id>", methods = ['DELETE'])
def eliminarMascota(id):
    try:
        delete = requests.delete(f"{BACKEND_URL}/api/mascotas/{id}")
        if delete.status_code == 200:
            success = delete.json()
            return redirect(url_for("busquedaMascota"))
        else:
            success = delete.json()
    except requests.exceptions.RequestException:
        print("Error de conexión con el backend.") 

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5001)
