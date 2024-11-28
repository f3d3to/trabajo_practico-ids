import unittest
from solicitudes import obtener_mascotas_perdidas, obtener_preguntas_frecuentes, buscar_mascota

class TestApiEndpoints(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial antes de cada prueba.
        """
        self.test_callback_result = None

    def callback(self, response):
        """
        Callback genérico para pruebas.
        Almacena el resultado en self.test_callback_result.
        """
        self.test_callback_result = response

    def test_obtener_mascotas_perdidas(self):
        """
        Prueba el endpoint para obtener mascotas perdidas.
        """
        obtener_mascotas_perdidas(self.callback)
        self.assertIsNotNone(self.test_callback_result)
        self.assertTrue(self.test_callback_result["success"])
        print("Resultado test_obtener_mascotas_perdidas:", self.test_callback_result)

    def test_obtener_preguntas_frecuentes(self):
        """
        Prueba el endpoint para obtener preguntas frecuentes.
        """
        obtener_preguntas_frecuentes(self.callback)
        self.assertIsNotNone(self.test_callback_result)
        self.assertTrue(self.test_callback_result["success"])
        print("Resultado test_obtener_preguntas_frecuentes:", self.test_callback_result)

    def test_buscar_mascota(self):
        """
        Prueba el endpoint para buscar mascotas con filtros.
        """
        filtros = {
            "tipo": "Gato",
            "estado": "encontrado"
        }
        buscar_mascota(filtros, self.callback)
        self.assertIsNotNone(self.test_callback_result)
        self.assertTrue(self.test_callback_result["success"])
        print("Resultado test_buscar_mascota:", self.test_callback_result)

if __name__ == "__main__":
    unittest.main()
