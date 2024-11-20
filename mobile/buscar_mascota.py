from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivy.uix.scrollview import ScrollView
from kivy_garden.mapview import MapView
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from logger import logger


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
        size_hint=(1, None),  # Cambiar el tamaño para que se ajuste
        height=dp(300),  # Altura específica para el mapa
        double_tap_zoom=True,
    )


# Mobile view with scrolling enabled
class MobileBuscarMascotaView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_view()

    def build_view(self):
        scroll = ScrollView()  # Envolvemos todo el contenido en un ScrollView
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            size_hint_y=None,
        )
        layout.bind(minimum_height=layout.setter("height"))  # Ajusta la altura para ScrollView

        layout.add_widget(create_step_title("Buscar Mascota", font_style="H5"))
        layout.add_widget(create_search_filters())
        layout.add_widget(create_search_button(self.perform_search))
        layout.add_widget(create_interactive_map())  # Añade el mapa al final

        scroll.add_widget(layout)
        self.add_widget(scroll)

    def perform_search(self):
        logger.info("Ejecutando búsqueda en móvil...")


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
