from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivy.uix.scrollview import ScrollView
from kivy_garden.mapview import MapView, MapMarker,MapMarkerPopup
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from logger import logger

#anado gabyo
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from solicitudes import obtener_mascotas_perdidas  # Importa el endpoint


# Reusable components
def create_step_title(text, font_style="H5", text_color=(0.2, 0.8, 0.6, 1)):
    return MDLabel(
        text=text,
        halign="center",
        font_style=font_style,
        theme_text_color="Custom",
        text_color=text_color,
        size_hint=(1, None),
        height=dp(40),
    )


def create_search_filters():
    layout = MDGridLayout(
        cols=2, spacing=dp(10), adaptive_height=True, padding=[dp(20), dp(10)]
    )
    filters = [
        "Especie", "Sexo", "Raza", "Color", "Zona", "Barrio",
        "Contacto", "Fecha de publicación (dd/mm/aaaa)"
    ]
    for hint in filters:
        layout.add_widget(MDTextField(
            hint_text=hint,
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5}
        ))
    return layout


def create_search_button(callback):
    return MDRoundFlatButton(
        text="Buscar",
        md_bg_color=(0.2, 0.8, 0.6, 1),
        text_color=(1, 1, 1, 1),
        size_hint=(None, None),
        size=(dp(200), dp(40)),
        pos_hint={"center_x": 0.5},
        on_release=lambda _: callback(),
    )


def create_interactive_map(lat=-34.6037, lon=-58.3816, zoom=10):
    return MapView(
        lat=lat,
        lon=lon,
        zoom=zoom,
        size_hint=(1, None),
        height=dp(300),
        double_tap_zoom=True,
    )

# class para el popup
class MascotaPopup(Popup):
    def __init__(self, mascota, **kwargs):
        super().__init__(**kwargs)
        self.title = f"Buscamos a {mascota.get('nombre', 'Mascota desconocida')}"
        self.size_hint = (0.8, 0.7)  # Tamaño del popup
        self.content = Label(text=self.get_mascota_info(mascota))

    def get_mascota_info(self, mascota):
        # cadena con informacion de la mascota
        info = f"Nombre: {mascota.get('nombre', 'Desconocida')}\n"
        info += f"Especie: {mascota.get('especie', 'Desconocida')}\n"
        info += f"Raza: {mascota.get('raza', 'Desconocida')}\n"
        info += f"Estado: {mascota.get('estado', 'Desconocida')}\n"
        info += f"Color: {mascota.get('color', 'Desconocido')}\n"
        info += f"Zona: {mascota.get('zona', 'Desconocida')}\n"
        info += f"Barrio: {mascota.get('barrio', 'Desconocida')}\n"
        info += f"Fecha: {mascota.get('fecha_publicacion', 'Desconocida')}\n"
        info += f"Contacto: {mascota.get('informacion_contacto', 'No disponible')}\n"  

        return info


# Clase personalizada para el marcador
class CustomMapMarker(MapMarker):
    def __init__(self, especie_mascota, **kwargs):
        super().__init__(**kwargs)
        # Elegir el ícono según el tipo de mascota
        if especie_mascota == 'perro':
            self.icon = Image(source="assets/images/perro.png", size=(50, 50))
        elif especie_mascota == 'gato':
            self.icon = Image(source="assets/images/gato.png", size=(50, 50))
        else:
            self.icon = Image(source="assets/images/pajaro.png", size=(50, 50))

        self.add_widget(self.icon)




# Mobile view with scrolling enabled
class MobileBuscarMascotaView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.map_view = create_interactive_map()  # Mapa interactivo
        self.build_view()
        self.dialog = None  # Para mantener la referencia al dialogo

    def build_view(self):
        scroll = ScrollView()
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            size_hint_y=None,
        )
        layout.bind(minimum_height=layout.setter("height"))

        layout.add_widget(create_step_title("Buscar Mascota", font_style="H5"))
        layout.add_widget(create_search_filters())
        layout.add_widget(create_search_button(self.perform_search))
        layout.add_widget(self.map_view)

        scroll.add_widget(layout)
        self.add_widget(scroll)

    def perform_search(self):
        logger.info("Ejecutando búsqueda en móvil...")
        # Llama al endpoint para obtener los datos
        obtener_mascotas_perdidas(self.update_map_with_markers)

    def update_map_with_markers(self, response):
        """
        Actualiza el mapa con los marcadores de mascotas.
        """
        if not response.get("success", False):
            logger.error("Error al obtener los datos de mascotas: " + response.get("error", ""))
            return

        mascotas = response.get("data", [])
        logger.info(f"Se encontraron {len(mascotas)} mascotas.")

        
        if not self.map_view or not self.map_view.parent:
            logger.error("El mapa no está correctamente inicializado.")
            return

        #elimina marcadores existentes
        for marker in self.map_view.children[:]:
            if isinstance(marker, MapMarker):
                self.map_view.remove_widget(marker)

        for mascota in mascotas:
            lat = mascota.get("latitud")
            lon = mascota.get("longitud")
            especie = mascota.get("especie")

            if lat and lon:
                marker = CustomMapMarker(especie_mascota=especie, lat=lat, lon=lon)

                def on_marker_touch(marker, mascota=mascota):
                    popup = MascotaPopup(mascota=mascota)
                    popup.open()
                #  muestra la tarjeta al tocar el marcador
                

                marker.bind(on_release=on_marker_touch)

                self.map_view.add_widget(marker)



class ResponsiveBuscarMascotaView(MDResponsiveLayout, MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mobile_view = MobileBuscarMascotaView()
        self.tablet_view = self.mobile_view  # Reutilizar para simplificar
        self.desktop_view = self.mobile_view  # Reutilizar para simplificar

    def get_current_view(self, window_width=800, window_height=600):
        if window_width < 600:  # Mobile
            return self.mobile_view
        elif window_width < 1200:  # Tablet
            return self.tablet_view
        else:  # Desktop
            return self.desktop_view
        

