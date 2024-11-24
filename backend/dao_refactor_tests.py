import requests

BASE_URL = "http://localhost:5000"  # Cambiar si tu servidor está en otro host o puerto

# Tests para cada endpoint
def test_obtener_esquema():
    # Caso válido: Obtener el esquema de la tabla 'mascotas'
    endpoint = f"{BASE_URL}/obtener_esquema"
    payload = {"tabla": "mascotas"}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200, "Debería devolver 200 OK"
    data = response.json()
    assert data["success"] is True, "El esquema debería devolverse correctamente"
    print(f"POST {endpoint} con payload {payload}")
    print(f"Response: {data}")

    # Caso inválido: Tabla no válida
    payload = {"tabla": "invalida"}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 400, "Debería devolver 400 Bad Request para tablas inválidas"
    print(f"POST {endpoint} con payload {payload}")
    print(f"Response: {response.json()}")


def test_agregar_mascota():
    # Caso válido: Insertar una nueva mascota
    endpoint = f"{BASE_URL}/agregar_mascota"
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
    data = response.json()
    assert data["success"] is True, "La inserción debería ser exitosa"
    print(f"POST {endpoint} con payload {payload}")
    print(f"Response: {data}")

    return data["id"]  # Devuelve el ID para usar en otros tests


def test_obtener_mascota(id_mascota):
    # Caso válido: Obtener la mascota recién creada por ID
    endpoint = f"{BASE_URL}/api/mascotas/{id_mascota}"
    response = requests.get(endpoint)
    assert response.status_code == 200, "Debería devolver 200 OK para un ID válido"
    data = response.json()
    assert data["success"] is True, "El registro debería encontrarse"
    print(f"GET {endpoint}")
    print(f"Response: {data}")

    # Caso inválido: ID inexistente
    endpoint = f"{BASE_URL}/api/mascotas/9999"
    response = requests.get(endpoint)
    assert response.status_code == 404, "Debería devolver 404 Not Found para un ID inexistente"
    print(f"GET {endpoint}")
    print(f"Response: {response.json()}")


def test_actualizar_mascota(id_mascota):
    # Caso válido: Actualizar la mascota recién creada
    endpoint = f"{BASE_URL}/api/mascotas/{id_mascota}"
    payload = {"nombre": "Buddy Actualizado", "estado": "adoptado"}
    response = requests.put(endpoint, json=payload)
    assert response.status_code == 200, "Debería devolver 200 OK para una actualización válida"
    data = response.json()
    assert data["success"] is True, "La actualización debería ser exitosa"
    print(f"PUT {endpoint} con payload {payload}")
    print(f"Response: {data}")


def test_obtener_mascotas():
    # Caso válido: Obtener todas las mascotas con filtros
    endpoint = f"{BASE_URL}/api/mascotas"
    params = {"especie": "perro"}
    response = requests.get(endpoint, params=params)
    assert response.status_code == 200, "Debería devolver 200 OK para filtros válidos"
    data = response.json()
    assert isinstance(data, list), "Debería devolver una lista de registros"
    print(f"GET {endpoint} con params {params}")
    print(f"Response: {data}")


def test_agregar_contacto():
    # Caso válido: Insertar un contacto
    endpoint = f"{BASE_URL}/agregar_contacto"
    payload = {
        "nombre": "Juan Pérez",
        "email": "juan.perez@example.com",
        "mensaje": "Estoy interesado en adoptar una mascota.",
        "telefono": "5551234",
        "asunto": "Adopción"
    }
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 201, "Debería devolver 201 Created para un contacto válido"
    data = response.json()
    assert data["success"] is True, "El contacto debería insertarse correctamente"
    print(f"POST {endpoint} con payload {payload}")
    print(f"Response: {data}")

    return data["id"]


def test_obtener_preguntas_frecuentes():
    # Caso válido: Obtener todas las preguntas frecuentes
    endpoint = f"{BASE_URL}/api/preguntas_frecuentes"
    response = requests.get(endpoint)
    assert response.status_code == 200, "Debería devolver 200 OK"
    data = response.json()
    assert data["success"] is True, "Las preguntas frecuentes deberían devolverse correctamente"
    print(f"GET {endpoint}")
    print(f"Response: {data}")


# Ejecutar los tests
if __name__ == "__main__":
    print("Iniciando pruebas para app_back.py...")

    test_obtener_esquema()
    id_mascota = test_agregar_mascota()
    test_obtener_mascota(id_mascota)
    test_actualizar_mascota(id_mascota)
    test_obtener_mascotas()
    test_agregar_contacto()
    test_obtener_preguntas_frecuentes()

    print("Pruebas finalizadas.")
