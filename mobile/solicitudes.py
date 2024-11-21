from kivy.network.urlrequest import UrlRequest
import urllib
import logging
import json
# Configuración de logging
logging.basicConfig(level=logging.DEBUG)

# Base URL del backend
API_BASE_URL = "http://127.0.0.1:5000"  # Cambia esto por la URL de tu servidor



class RequestManager:
    """
    Clase para manejar solicitudes HTTP usando UrlRequest.
    Incluye métodos para GET y POST con manejo de callbacks.
    """

    def __init__(self):
        self.resultado = None
        self.error = None

    def get(self, url, on_success=None, on_error=None, wait_for_completion=False):
        """
        Realiza una solicitud GET al URL especificado.
        """
        print(f"Iniciando solicitud GET a {url}...")
        self.resultado = None
        self.error = None

        def _success(req, result):
            self.resultado = result
            print("Solicitud GET completada con éxito.")
            if on_success:
                on_success(req, result)

        def _error(req, error):
            self.error = error
            print("Error en la solicitud GET.")
            if on_error:
                on_error(req, error)

        req = UrlRequest(
            url,
            on_success=_success,
            on_error=_error,
        )

        if wait_for_completion:
            print("Esperando a que la solicitud GET termine...")
            req.wait()
            print("La solicitud GET ha terminado.")
        return req

    def post(self, url, data, headers=None, on_success=None, on_error=None, wait_for_completion=False):
        """
        Realiza una solicitud POST al URL especificado.
        """
        print(f"Iniciando solicitud POST a {url}...")
        self.resultado = None
        self.error = None

        def _success(req, result):
            self.resultado = result
            print("Solicitud POST completada con éxito.")
            if on_success:
                on_success(req, result)

        def _error(req, error):
            self.error = error
            print("Error en la solicitud POST.")
            if on_error:
                on_error(req, error)

        headers = headers or {"Content-Type": "application/json"}
        body = json.dumps(data)
    

        req = UrlRequest(
            url,
            req_body=body,
            req_headers=headers,
            on_success=_success,
            on_error=_error,
        )

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

# Instancia global de RequestManager
manager = RequestManager()

# Funciones de endpoints específicas
def cargar_mascota(data, callback):
    """
    Envía información de una nueva mascota al backend.
    """
    url = f"{API_BASE_URL}/agregar_mascota"
    headers = {"Content-Type": "application/json"}
    body = data

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
    """
    url = f"{API_BASE_URL}/agregar_contacto"
    headers = {"Content-Type": "application/json"}
    
    # Convierte el diccionario `data` a una cadena JSON
    body = data
    logging.debug(f"Enviando datos de contacto: {data}")
    manager.post(
        url,
        data=body,  # Usamos `data` para enviar la cadena JSON
        headers=headers,
        on_success=lambda req, result: callback({"success": True, "data": result}),
        on_error=lambda req, error: callback({"success": False, "error": error}),
        wait_for_completion=True,
    )


def obtener_mascotas_perdidas(callback):
    """
    Recupera las mascotas perdidas desde el backend.
    """
    url = f"{API_BASE_URL}/api/mascotas?estado=perdida"
    headers = {"Content-Type": "application/json"}

    logging.debug("Solicitando mascotas perdidas")
    manager.get(
        url,
        on_success=lambda req, result: callback({"success": True, "data": result}),
        on_error=lambda req, error: callback({"success": False, "error": error}),
        wait_for_completion=True,
    )

def obtener_preguntas_frecuentes(callback):
    """
    Recupera las preguntas frecuentes desde el backend.
    """
    url = f"{API_BASE_URL}/api/preguntas_frecuentes"
    headers = {"Content-Type": "application/json"}

    logging.debug("Solicitando preguntas frecuentes")
    manager.get(
        url,
        on_success=lambda req, result: callback({"success": True, "data": result}),
        on_error=lambda req, error: callback({"success": False, "error": error}),
        wait_for_completion=True,
    )

def buscar_mascota(filtros, callback):
    """
    Busca mascotas basadas en los filtros proporcionados.
    """
    url = f"{API_BASE_URL}/api/mascotas"
    query_string = "&".join([f"{key}={value}" for key, value in filtros.items()])
    full_url = f"{url}?{query_string}"
    headers = {"Content-Type": "application/json"}

    logging.debug(f"Buscando mascotas con filtros: {filtros}")
    manager.get(
        full_url,
        on_success=lambda req, result: callback({"success": True, "data": result}),
        on_error=lambda req, error: callback({"success": False, "error": error}),
        wait_for_completion=True,
    )
