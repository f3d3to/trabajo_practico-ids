from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image  # Imagenes
from kivy.uix.carousel import Carousel  # Carrusel para imágenes
from kivymd.uix.label import MDLabel  # Etiquetas de texto
from kivymd.uix.boxlayout import MDBoxLayout  # Layout vertical
from logger import logger
from kivy.metrics import dp


# Componente reutilizable: Título destacado
def create_title(text, font_style="H5", text_color=(0.2, 0.8, 0.6, 1), padding=20):
    # logger.debug(f"Creando título: {text}")
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
    # logger.debug(f"Creando carrusel de imágenes: {images}")
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
        # logger.info("Inicializando MobileInicioView")
        try:
            layout = MDBoxLayout(orientation="vertical", spacing=10, padding=20)

            # Título y carrusel
            layout.add_widget(create_title("¿Perdiste a tu mascota?", font_style="H5"))
            layout.add_widget(create_image_carousel(["assets/images/lydia.png", "assets/images/gato.png", "assets/images/otro.png"]))

            self.add_widget(layout)
        except Exception as e:
            logger.error(f"Error al construir MobileInicioView: {e}")


# Vista tablet para la pantalla de inicio
class TabletInicioView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # logger.info("Inicializando TabletInicioView")
        try:
            layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)

            # Título y carrusel
            layout.add_widget(create_title("¿Perdiste a tu mejor amigo?", font_style="H4", text_color=(0.1, 0.7, 0.5, 1)))
            layout.add_widget(create_image_carousel(["assets/images/lydia.png", "assets/images/gato.png", "assets/images/otro.png"]))

            self.add_widget(layout)
        except Exception as e:
            logger.error(f"Error al construir TabletInicioView: {e}")


# Vista escritorio para la pantalla de inicio
class DesktopInicioView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # logger.info("Inicializando DesktopInicioView")
        try:
            layout = MDBoxLayout(orientation="vertical", spacing=30, padding=50)

            # Título y carrusel
            layout.add_widget(create_title("¿Perdiste a tu mejor amigo?", font_style="H3"))
            layout.add_widget(create_image_carousel(["assets/images/perro.png", "assets/images/gato.png", "assets/images/otro.png"]))

            self.add_widget(layout)
        except Exception as e:
            logger.error(f"Error al construir DesktopInicioView: {e}")


# Pantalla responsiva principal para inicio
class ResponsiveInicioView(MDResponsiveLayout, MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # logger.info("Inicializando ResponsiveInicioView")
        try:
            self.mobile_view = MobileInicioView()
            self.tablet_view = TabletInicioView()
            self.desktop_view = DesktopInicioView()
        except Exception as e:
            logger.error(f"Error al inicializar ResponsiveInicioView: {e}")

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

