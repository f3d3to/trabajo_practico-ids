from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_garden.mapview import MapView
import requests

# Pantallas de la aplicación
class HomeScreen(Screen):
    pass

class ContactScreen(Screen):
    pass

class SearchScreen(Screen):
    pass

class AddPetScreen(Screen):
    pass

class MapScreen(Screen):
    def on_enter(self):
        # Aquí puedes agregar lógica para cargar puntos en el mapa desde la API
        pass

# Configuración de la aplicación y administración de pantallas
class HuellasApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(ContactScreen(name="contact"))
        sm.add_widget(SearchScreen(name="search"))
        sm.add_widget(AddPetScreen(name="add_pet"))
        sm.add_widget(MapScreen(name="map"))
        return sm

if __name__ == "__main__":
    HuellasApp().run()
