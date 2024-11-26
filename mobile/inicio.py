
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image
from kivy.uix.carousel import Carousel
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from logger import logger
from kivy.metrics import dp
from solicitudes import obtener_mascotas_perdidas,obtener_imagen  

# =========================
# Componentes reutilizables
# =========================

def create_title(text, font_style="H5", text_color=(0.2, 0.8, 0.6, 1), padding=20):
    """
    Crea un título con formato y color personalizado.
    """
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


def create_image_carousel(imagenes, size_hint=(1, 0.8)):
    try:
        carousel = Carousel(loop=True, size_hint=size_hint)
        for imagen in imagenes:  # `images` debe ser una lista de objetos AsyncImage
            carousel.add_widget(imagen)  # Añadir cada AsyncImage al carrusel
        return carousel
    except Exception as e:
        logger.error(f"Error al crear carrusel de imágenes: {e}")


# ======================================
# Vista móvil para la pantalla de inicio
# ======================================

class MobileInicioView(MDScreen):
    """
    Vista de inicio optimizada para dispositivos móviles.
    """

    def __init__(self, **kwargs):
        """
        Inicializa la vista móvil de inicio.
        """
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical", spacing=10, padding=20)
        self.carousel = create_image_carousel([])  # Carrusel vacío inicialmente

        # Agregar título
        self.layout.add_widget(create_title("¿Perdiste a tu mascota?", font_style="H5"))

        # Agregar carrusel (se actualiza dinámicamente)
        self.layout.add_widget(self.carousel)
        self.add_widget(self.layout)

        # Cargar imágenes dinámicamente
        self.load_lost_pets()

    def load_lost_pets(self):
        """
        Carga las mascotas perdidas desde el servidor y actualiza el carrusel.
        """
        def handle_response(response):
            """
            Maneja la respuesta del servidor después de obtener las mascotas perdidas.
            """
            if response.get("success"):
                mascotas = response.get("data", [])
                foto_urls = [ mascota.get("foto_url") for mascota in mascotas if mascota.get("foto_url")]
                if foto_urls:
                    self.carousel.clear_widgets()
                    for foto_url in foto_urls:
                        imagen = obtener_imagen(foto_url)
                        self.carousel.add_widget(imagen)
                else:
                    logger.warning("No hay fotos de mascotas perdidas disponibles.")
            else:
                logger.error(f"Error al obtener mascotas: {response.get('error')}")

        # Solicitar las mascotas perdidas al servidor
        obtener_mascotas_perdidas(handle_response)


# ===================================
# Vistas para diferentes dispositivos
# ===================================

class TabletInicioView(MobileInicioView):
    """
    Vista de inicio optimizada para tabletas.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout.padding = 30
        self.layout.spacing = 20


class DesktopInicioView(MobileInicioView):
    """
    Vista de inicio optimizada para pantallas de escritorio.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout.padding = 50
        self.layout.spacing = 30


# =============================
# Pantalla responsiva principal
# =============================

class ResponsiveInicioView(MDResponsiveLayout, MDScreen):
    """
    Vista responsiva que adapta el diseño de inicio según el tamaño de la pantalla.
    """

    def __init__(self, **kwargs):
        """
        Inicializa la vista responsiva, creando vistas para móvil, tablet y escritorio.
        """
        super().__init__(**kwargs)
        self.mobile_view = MobileInicioView()
        self.tablet_view = TabletInicioView()
        self.desktop_view = DesktopInicioView()

    def get_current_view(self, window_width=800, window_height=600):
        """
        Devuelve la vista apropiada según el ancho de la ventana.
        """
        if window_width < 600:  # Móvil
            self.mobile_view.size_hint = (1, None)
            self.mobile_view.height = window_height - dp(150)  # Restar altura de TopBar y Footer
            return self.mobile_view
        elif window_width < 1200:  # Tablet
            self.tablet_view.size_hint = (1, None)
            self.tablet_view.height = window_height - dp(150)
            return self.tablet_view
        else:  # Escritorio
            self.desktop_view.size_hint = (1, None)
            self.desktop_view.height = window_height - dp(150)
            return self.desktop_view
