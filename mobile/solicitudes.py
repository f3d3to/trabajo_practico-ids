# TO-DO: versión en revisión: no está probando, se puede mejorar

from kivy.network.urlrequest import UrlRequest
import json

API_BASE_URL = "http://127.0.0.1:5000"  # BACKEND

class SolicitudError(Exception):
    """
    Excepción personalizada para errores en las solicitudes HTTP.
    """
    def __init__(self, mensaje, detalles=None):
        super().__init__(mensaje)
        self.detalles = detalles

def manejar_respuesta(req, resultado, callback, es_error=False):
    """
    Maneja la respuesta de una solicitud, delegando al callback correcto o lanzando un error.
    """
    if es_error:
        error_message = f"Error en la solicitud a {req.url}"
        raise SolicitudError(error_message, detalles=resultado)
    else:
        callback(resultado)

def ejecutar_solicitud(url, method="GET", headers=None, body=None, callback=None):
    """
    Envuelve UrlRequest para manejar la respuesta de forma modular.
    """
    def exito(req, result):
        try:
            manejar_respuesta(req, result, callback, es_error=False)
        except SolicitudError as e:
            callback({"success": False, "error": str(e), "detalles": e.detalles})

    def error(req, result):
        try:
            manejar_respuesta(req, result, callback, es_error=True)
        except SolicitudError as e:
            callback({"success": False, "error": str(e), "detalles": e.detalles})

    UrlRequest(
        url,
        req_headers=headers,
        req_body=body,
        method=method,
        on_success=exito,
        on_error=error,
        on_failure=error,
    )

def obtener_mascotas(filtros, callback):
    """
    Obtiene una lista de mascotas desde el backend.
    """
    query_string = "&".join([f"{key}={value}" for key, value in filtros.items()])
    url = f"{API_BASE_URL}/api/mascotas?{query_string}"
    headers = {"Content-Type": "application/json"}

    ejecutar_solicitud(url, headers=headers, callback=callback)

def agregar_mascota(data, callback):
    """
    Agrega una nueva mascota al backend.
    """
    url = f"{API_BASE_URL}/agregar_mascota"
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data)

    ejecutar_solicitud(url, method="POST", headers=headers, body=body, callback=callback)

def obtener_preguntas_frecuentes(callback):
    """
    Obtiene la lista de preguntas frecuentes.
    """
    url = f"{API_BASE_URL}/api/preguntas_frecuentes"
    headers = {"Content-Type": "application/json"}

    ejecutar_solicitud(url, headers=headers, callback=callback)
