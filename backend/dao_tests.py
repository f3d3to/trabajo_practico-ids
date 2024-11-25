import requests

BASE_URL = "http://localhost:5000"  # Cambiar si el servidor está en otro host/puerto


def test_obtener_esquema():
    endpoint = f"{BASE_URL}/obtener_esquema"

    # Caso válido: Obtener esquema de mascotas
    payload = {"tabla": "mascotas"}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200, "Debería devolver 200 OK para una tabla válida"
    print(f"POST {endpoint} con payload {payload}")
    print(f"Response: {response.json()}")

    # Caso inválido: Tabla no válida
    payload = {"tabla": "invalida"}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 400, "Debería devolver 400 Bad Request para una tabla no válida"
    print(f"POST {endpoint} con payload {payload}")
    print(f"Response: {response.json()}")


def test_obtener_esquema_contacto():
    endpoint = f"{BASE_URL}/obtener_esquema_contacto"

    # Caso válido: Obtener esquema de contactos
    payload = {"tabla": "contactos"}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200, "Debería devolver 200 OK para una tabla válida"
    print(f"POST {endpoint} con payload {payload}")
    print(f"Response: {response.json()}")

    # Caso inválido: Tabla no válida
    payload = {"tabla": "invalida"}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 400, "Debería devolver 400 Bad Request para una tabla no válida"
    print(f"POST {endpoint} con payload {payload}")
    print(f"Response: {response.json()}")


def test_agregar_mascota():
    endpoint = f"{BASE_URL}/agregar_mascota"

    # Caso válido: Agregar una mascota con todos los campos requeridos
    payload = {
        "especie": "perro",
        "genero": "macho",
        "nombre": "Buddy",
        "raza": "Labrador",
        "color": "dorado",
        "condicion": "sana",
        "estado": "en adopcion",
        "foto_url": "user_images/buddy.png",
        "zona": "Caballito",
        "barrio": "Almagro",
        "latitud": -34.6037,
        "longitud": -58.3816,
        "informacion_contacto": "+54 9 123 456 789"
    }
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 201, "Debería devolver 201 Created para una mascota válida"
    print(f"POST {endpoint} con payload {payload}")
    print(f"Response: {response.json()}")

def test_obtener_mascota():
    # Caso válido: Obtener mascota existente
    endpoint = f"{BASE_URL}/api/mascotas/1"
    response = requests.get(endpoint)
    assert response.status_code in [200, 404], "Debería devolver 200 OK o 404 Not Found"
    print(f"GET {endpoint}")
    print(f"Response: {response.json()}")


def test_actualizar_mascota():
    endpoint = f"{BASE_URL}/api/mascotas/1"
    # Caso válido: Actualizar todos los campos de la mascota
    payload = {
        "nombre": "Buddy Actualizado",
        "raza": "Labrador Negro",
        "estado": "en adopcion",
        "zona": "Villa Crespo",
    }
    response = requests.put(endpoint, json=payload)
    assert response.status_code in [200, 404], "Debería devolver 200 OK o 404 Not Found"
    print(f"PUT {endpoint} con payload {payload}")
    print(f"Response: {response.json()}")


def test_obtener_mascotas():
    endpoint = f"{BASE_URL}/api/mascotas"
    # Caso válido: Filtrar por especie y estado
    params = {"especie": "perro", "estado": "perdida"}
    response = requests.get(endpoint, params=params)
    assert response.status_code == 200, "Debería devolver 200 OK para filtros válidos"
    print(f"GET {endpoint} con params {params}")
    print(f"Response: {response.json()}")


def test_agregar_contacto():
    endpoint = f"{BASE_URL}/agregar_contacto"

    # Caso válido: Agregar un contacto con todos los campos
    payload = {
        "nombre": "Ana López",
        "email": "ana@example.com",
        "mensaje": "Quiero adoptar un perro.",
        "telefono": "12345678",
        "asunto": "Adopción",
    }
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 201, "Debería devolver 201 Created para un contacto válido"
    print(f"POST {endpoint} con payload {payload}")
    print(f"Response: {response.json()}")


def test_obtener_preguntas_frecuentes():
    endpoint = f"{BASE_URL}/api/preguntas_frecuentes"
    # Caso válido: Obtener preguntas frecuentes
    response = requests.get(endpoint)
    assert response.status_code == 200, "Debería devolver 200 OK"
    print(f"GET {endpoint}")
    print(f"Response: {response.json()}")


if __name__ == "__main__":
    print("Iniciando pruebas...")
    test_obtener_esquema()
    test_obtener_esquema_contacto()
    test_agregar_mascota()
    test_obtener_mascota()
    test_actualizar_mascota()
    test_obtener_mascotas()
    test_agregar_contacto()
    test_obtener_preguntas_frecuentes()
    print("Pruebas finalizadas.")
