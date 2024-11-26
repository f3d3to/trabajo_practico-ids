import unittest
from solicitudes import obtener_mascotas_perdidas, obtener_preguntas_frecuentes, buscar_mascota

class TestApiEndpoints(unittest.TestCase):
    """
    Conjunto de pruebas para los endpoints de la API relacionados con
    mascotas perdidas, preguntas frecuentes y búsqueda de mascotas.
    """
    def setUp(self):
        """
        Configura el entorno antes de cada prueba.
        Inicializa la variable que almacenará el resultado del callback.
        """
        self.test_callback_result = None

    def callback(self, response):
        """
        Callback genérico que almacena la respuesta de la API.
        Respuesta de la API que se almacena en `test_callback_result`.
        """
        self.test_callback_result = response

    def test_obtener_mascotas_perdidas(self):
        """
        Prueba el endpoint de obtener mascotas perdidas.
        """
        obtener_mascotas_perdidas(self.callback)
        self.assertIsNotNone(self.test_callback_result, "La respuesta no debe ser nula")
        self.assertTrue(self.test_callback_result["success"], "La respuesta debe ser exitosa")
        print("Resultado test_obtener_mascotas_perdidas:", self.test_callback_result)

    def test_obtener_preguntas_frecuentes(self):
        """
        Prueba el endpoint para obtener preguntas frecuentes.
        """
        obtener_preguntas_frecuentes(self.callback)
        self.assertIsNotNone(self.test_callback_result, "La respuesta no debe ser nula")
        self.assertTrue(self.test_callback_result["success"], "La respuesta debe ser exitosa")
        print("Resultado test_obtener_preguntas_frecuentes:", self.test_callback_result)

    def test_buscar_mascota(self):
        """
        Prueba el endpoint de búsqueda de mascotas con filtros.
        """
        filtros = {
            "tipo": "Gato",
            "estado": "encontrado"
        }
        buscar_mascota(filtros, self.callback)
        self.assertIsNotNone(self.test_callback_result, "La respuesta no debe ser nula")
        self.assertTrue(self.test_callback_result["success"], "La respuesta debe ser exitosa")
        print("Resultado test_buscar_mascota:", self.test_callback_result)

if __name__ == "__main__":
    unittest.main()
