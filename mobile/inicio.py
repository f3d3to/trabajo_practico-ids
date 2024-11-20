from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image  # Imagenes
from kivy.uix.carousel import Carousel  # Carrusel para imágenes
from kivymd.uix.label import MDLabel  # Etiquetas de texto
from kivymd.uix.boxlayout import MDBoxLayout  # Layout vertical
from logger import logger
from kivy.metrics import dp


from solicitudes import obtener_mascotas_perdidas  # Importa el endpoint para obtener mascotas perdidas

# Componente reutilizable: Título destacado
def create_title(text, font_style="H5", text_color=(0.2, 0.8, 0.6, 1), padding=20):
    try:
        layout = MDBoxLayout(orientation="vertical", padding=padding)
        title = MDLabel(
            text=text,
            size_hint=(1, None),
            height="50dp",
            halign="center",
            font_style=font_style,
            theme_text_color="Custom",
            text_color=text_color,
        )
        layout.add_widget(title)
        return layout
    except Exception as e:
        logger.error(f"Error al crear título '{text}': {e}")


# Componente reutilizable: Carrusel de imágenes
def create_image_carousel(images, size_hint=(1, 0.8)):
    try:
        carousel = Carousel(loop=True, size_hint=size_hint)
        for img_path in images:
            carousel.add_widget(Image(source=img_path, allow_stretch=True))
        return carousel
    except Exception as e:
        logger.error(f"Error al crear carrusel de imágenes: {e}")


# Vista móvil para la pantalla de inicio
class MobileInicioView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical", spacing=10, padding=20)
        self.carousel = create_image_carousel([])  # Carrusel vacío inicialmente

        # Título
        self.layout.add_widget(create_title("¿Perdiste a tu mascota?", font_style="H5"))

        # Carrusel (se actualizará dinámicamente)
        self.layout.add_widget(self.carousel)

        self.add_widget(self.layout)

        # Cargar imágenes dinámicamente
        self.load_lost_pets()

    def load_lost_pets(self):
        def handle_response(response):
            if response.get("success"):
                pets = response.get("data", [])
                image_urls = ["assets/"+pet["foto_url"] for pet in pets if pet.get("foto_url")]
                if image_urls:
                    self.carousel.clear_widgets()
                    for img_url in image_urls:
                        self.carousel.add_widget(Image(source=img_url, allow_stretch=True))
                else:
                    logger.warning("No hay fotos de mascotas perdidas disponibles.")
            else:
                logger.error(f"Error al obtener mascotas: {response.get('error')}")

        obtener_mascotas_perdidas(handle_response)


# Vista tablet para la pantalla de inicio
class TabletInicioView(MobileInicioView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout.padding = 30
        self.layout.spacing = 20


# Vista escritorio para la pantalla de inicio
class DesktopInicioView(MobileInicioView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout.padding = 50
        self.layout.spacing = 30


# Pantalla responsiva principal para inicio
class ResponsiveInicioView(MDResponsiveLayout, MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mobile_view = MobileInicioView()
        self.tablet_view = TabletInicioView()
        self.desktop_view = DesktopInicioView()

    def get_current_view(self, window_width=800, window_height=600):
        # Ajustar la vista según el ancho
        if window_width < 600:  # Móvil
            self.mobile_view.size_hint = (1, None)
            self.mobile_view.height = window_height - dp(150)  # Restar altura del TopBar y Footer
            return self.mobile_view
        elif window_width < 1200:  # Tablet
            self.tablet_view.size_hint = (1, None)
            self.tablet_view.height = window_height - dp(150)
            return self.tablet_view
        else:  # Escritorio
            self.desktop_view.size_hint = (1, None)
            self.desktop_view.height = window_height - dp(150)
            return self.desktop_view
