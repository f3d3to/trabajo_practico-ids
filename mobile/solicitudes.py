from kivy.network.urlrequest import UrlRequest
import json
import logging
from urllib.parse import quote
from kivy.uix.image import AsyncImage
import requests
from werkzeug.utils import secure_filename
import os
import mimetypes
import os
from dotenv import load_dotenv

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)
env_path_deploy = os.path.join(os.getcwd(),'..', 'deploy', '.env')
load_dotenv(env_path_deploy)

print(env_path_deploy)
API_BASE_URL = os.getenv('BACK_URL_KIVY')
API_SERVICIO_FOTO = f"{API_BASE_URL}/uploads/user_images"

# Verificar si las variables de entorno se cargaron correctamente
print(f"BACKEND_URL: {API_BASE_URL}")
print(f"USER_IMAGES_FOLDER: {API_SERVICIO_FOTO}")
class RequestManager:
    """
    Clase para manejar solicitudes HTTP utilizando UrlRequest.
    Contiene métodos para realizar solicitudes GET y POST con manejo de callbacks.
    """

    def __init__(self):
        self.resultado = None
        self.error = None

    def get(self, url, on_success=None, on_error=None, wait_for_completion=False):
        """
        Realiza una solicitud GET a la URL especificada.

        :param url: La URL a la que se realizará la solicitud GET.
        :param on_success: Callback que se ejecuta en caso de éxito.
        :param on_error: Callback que se ejecuta en caso de error.
        :param wait_for_completion: Si es True, espera a que la solicitud termine.
        :return: El objeto UrlRequest que representa la solicitud.
        """
        self.resultado = None
        self.error = None
        print(f"Iniciando solicitud GET a {url}...")

        def _success(req, result):
            """Maneja la respuesta exitosa."""
            self.resultado = result
            print("Solicitud GET completada con éxito.")
            if on_success:
                on_success(req, result)

        def _error(req, error):
            """Maneja los errores de la solicitud."""
            self.error = error
            print("Error en la solicitud GET.")
            if on_error:
                on_error(req, error)

        req = UrlRequest(url, on_success=_success, on_error=_error)

        if wait_for_completion:
            print("Esperando a que la solicitud GET termine...")
            req.wait()
            print("La solicitud GET ha terminado.")
        return req

    def post(self, url, data, headers=None, on_success=None, on_error=None, wait_for_completion=False):
        """
        Realiza una solicitud POST a la URL especificada.

        :param url: La URL a la que se realizará la solicitud POST.
        :param data: Los datos a enviar en el cuerpo de la solicitud.
        :param headers: Los encabezados de la solicitud.
        :param on_success: Callback que se ejecuta en caso de éxito.
        :param on_error: Callback que se ejecuta en caso de error.
        :param wait_for_completion: Si es True, espera a que la solicitud termine.
        :return: El objeto UrlRequest que representa la solicitud.
        """
        self.resultado = None
        self.error = None
        print(f"Iniciando solicitud POST a {url}...")

        def _success(req, result):
            """Maneja la respuesta exitosa."""
            self.resultado = result
            print("Solicitud POST completada con éxito.")
            if on_success:
                on_success(req, result)

        def _error(req, error):
            """Maneja los errores de la solicitud."""
            self.error = error
            print("Error en la solicitud POST.")
            if on_error:
                on_error(req, error)

        headers = headers or {"Content-Type": "application/json"}
        body = json.dumps(data)

        req = UrlRequest(url, req_body=body, req_headers=headers, on_success=_success, on_error=_error)

        if wait_for_completion:
            print("Esperando a que la solicitud POST termine...")
            req.wait()
            print("La solicitud POST ha terminado.")
        return req

# Callbacks de ejemplo
def manejar_respuesta(req, result):
    print("Respuesta recibida:")
    print(result)

def manejar_error(req, error):
    print("Error recibido:")
    print(error)

# =====================================================
# Funciones específicas para interactuar con el backend
# =====================================================

def cargar_mascota(data, callback):
    """
    Envía información de una nueva mascota al backend.
    """
    url = f"{API_BASE_URL}/agregar_mascota"
    headers = {"Content-Type": "application/json"}
    body = data
    imagen = body.get('foto_url')
    if imagen:
        
        nombre_archivo = secure_filename(os.path.basename(imagen)) 
        mime_tipo = mimetypes.guess_type(nombre_archivo)  #  obtiene el tipo mime
        try:
            if not mime_tipo:
                mime_tipo = 'application/octet-stream' 
            #Enviamos la imagen al backend
            with open(imagen, 'rb') as file:
                files = {'file': (nombre_archivo, file, mime_tipo)}  
                response = requests.post(API_BASE_URL + "/upload", files=files)
                if response.status_code == 201:  
                    file_url = response.json().get('file_url') 
                    print(f"file_url: {file_url}") 
                    body["foto_url"] = file_url  
                else:
                    print(f"Error al cargar la imagen: {response.text}")
                    return callback({"success": False, "error": "No se pudo cargar la imagen"})
        except requests.exceptions.RequestException as e:
            print("No se pudo conectar con el backend:", e)

    logging.debug(f"Enviando datos de mascota: {data}")
    manager.post(
        url,
        data=body,
        headers=headers,
        on_success=lambda req, result: callback({"success": True, "data": result}),
        on_error=lambda req, error: callback({"success": False, "error": error}),
        wait_for_completion=True,
    )


def contacto(data, callback):
    """
    Envía información de contacto al backend.

    :param data: Datos de contacto a enviar.
    :param callback: Función de callback que maneja la respuesta.
    """
    url = f"{API_BASE_URL}/agregar_contacto"
    headers = {"Content-Type": "application/json"}

    logging.debug(f"Enviando datos de contacto: {data}")
    manager.post(
        url,
        data=data,
        headers=headers,
        on_success=lambda req, result: callback({"success": True, "data": result}),
        on_error=lambda req, error: callback({"success": False, "error": error}),
        wait_for_completion=True
    )

def obtener_mascotas_perdidas(callback):
    """
    Recupera la lista de mascotas perdidas desde el backend.

    :param callback: Función de callback que maneja la respuesta.
    """
    url = f"{API_BASE_URL}/api/mascotas?estado=perdida"
    headers = {"Content-Type": "application/json"}

    logging.debug("Solicitando mascotas perdidas")
    manager.get(
        url,
        on_success=lambda req, result: callback({"success": True, "data": result}),
        on_error=lambda req, error: callback({"success": False, "error": error}),
        wait_for_completion=True
    )

def obtener_preguntas_frecuentes(callback):
    """
    Recupera las preguntas frecuentes desde el backend.

    :param callback: Función de callback que maneja la respuesta.
    """
    url = f"{API_BASE_URL}/api/preguntas_frecuentes"
    headers = {"Content-Type": "application/json"}

    logging.debug("Solicitando preguntas frecuentes")
    manager.get(
        url,
        on_success=lambda req, result: callback({"success": True, "data": result}),
        on_error=lambda req, error: callback({"success": False, "error": error}),
        wait_for_completion=True
    )

def buscar_mascota(filtros, callback):
    """
    Realiza una búsqueda de mascotas utilizando los filtros proporcionados.

    :param filtros: Filtros de búsqueda a aplicar.
    :param callback: Función de callback que maneja la respuesta.
    """
    print(f"Filtros originales: {filtros}")
    params = {k: v for k, v in filtros.items() if v}  # Filtra los valores no nulos
    print(f"Filtros aplicados: {params}")

    url = f"{API_BASE_URL}/api/mascotas"
    if params:
        encoded_params = {key: quote(value) for key, value in params.items()}
        query_string = '&'.join([f"{key}={value}" for key, value in encoded_params.items()])
        url = f"{url}?{query_string}"
    headers = {"Content-Type": "application/json"}

    logging.debug(f"Buscando mascotas con filtros: {filtros}")
    manager.get(
        url,
        on_success=lambda req, result: callback({"success": True, "data": result}),
        on_error=lambda req, error: callback({"success": False, "error": error}),
        wait_for_completion=True
    )

def obtener_imagen(url_foto):
    """
    Obtiene la imagen desde la url.
    """
    if not url_foto:
        logging.debug("La URL de la foto es inválida o está vacía.")
        return None
    
    url_completa = f"{API_SERVICIO_FOTO}{url_foto}" 
    
    try:
        return AsyncImage(source=url_completa)
    
    except Exception as e:
        logging.debug(f"Error al cargar la imagen desde {url_completa}: {e}")
        return None

# Instancia global de RequestManager
manager = RequestManager()
