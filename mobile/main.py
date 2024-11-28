from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.image import Image
from kivymd.uix.button import MDRoundFlatButton
import logging
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout

# Importación de vistas
from inicio import ResponsiveInicioView
from cargar_mascota import ResponsiveCargarMascotaView
from contacto import ResponsiveContactoView
from buscar_mascota import ResponsiveBuscarMascotaView
from preguntas import ResponsivePreguntasView

# ========================
# Configuración del logger
# ========================
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MyApp(MDApp):
    """
    Clase principal de la aplicación que maneja la interfaz y la navegación.
    """
    def build(self):
        """
        Construye la interfaz de la aplicación, configurando el tema, la pantalla principal y
        el sistema de navegación.
        """

        # Configuración del tema de la app
        self.theme_cls.primary_palette = "Brown"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Light"
        self.title = "Huellas a Casa"
        logger.info(f"Aplicación iniciada: {self.title}")

        # Crear el ScreenManager
        self.screen_manager = MDScreenManager()

        # Agregar pantallas al ScreenManager
        self.screen_manager.add_widget(ResponsiveInicioView(name="inicio"))
        self.screen_manager.add_widget(ResponsiveCargarMascotaView(name="cargar_mascota"))
        self.screen_manager.add_widget(ResponsiveContactoView(name="contacto"))
        self.screen_manager.add_widget(ResponsiveBuscarMascotaView(name="buscar_mascota"))
        self.screen_manager.add_widget(ResponsivePreguntasView(name="preguntas"))

        logger.info(f"Pantallas registradas: {self.screen_manager.screen_names}")

        # Contenedor principal
        root = MDBoxLayout(orientation="vertical", size_hint=(1, 1))

        # Crear y agregar el TopBar
        top_bar = self.create_top_bar()
        top_bar.size_hint_y = 0.5
        root.add_widget(top_bar)

        # Agregar el ScreenManager al layout
        self.screen_manager.size_hint_y = 4.1
        root.add_widget(self.screen_manager)

        # Crear y agregar el Footer
        footer = self.create_footer()
        root.add_widget(footer)

        
        return root
   
    def create_top_bar(self):
        """
        Crea el TopBar que contiene el logo y el botón de inicio de búsqueda.
        """
        top_bar = MDTopAppBar(
            md_bg_color=(0.91, 0.64, 0.45, 1),  # Color de fondo
            specific_text_color=(1, 1, 1, 1),  # Color del texto
            elevation=0,
        )

        # Contenedor horizontal para los elementos del TopBar
        top_bar_content = BoxLayout(
            orientation="horizontal",
            padding="8dp",
            size_hint=(1, None),
            height="56dp",  # Ajusta la altura al tamaño del TopBar
        )

        # Agregar logo a la izquierda
        logo = Image(
            source="assets/images/logo.png",  # Cambia a la ruta de tu logo
            size_hint=(None, 1),  # Ajusta la altura al TopBar
            allow_stretch=True,  # Permite que el logo se escale
            keep_ratio=True,  # Mantén la proporción
        )
        top_bar_content.add_widget(logo)

        # Espaciador (para centrar el título)
        top_bar_content.add_widget(BoxLayout(size_hint=(1, 1)))

        # Agregar botón a la derecha
        button = MDRoundFlatButton(
            text="Iniciá tu Búsqueda",
            md_bg_color=(0.2, 0.8, 0.6, 1),  # Verde
            text_color=(1, 1, 1, 1),  # Blanco
            size_hint=(None, None),
            size=("180dp", "40dp"),
            pos_hint={"center_y": 0.5},  # Centra verticalmente el botón en el TopBar
            on_release=lambda x: self.switch_screen("cargar_mascota"),
        )
        top_bar_content.add_widget(button)

        # Agregar el contenedor de contenido al TopBar
        top_bar.add_widget(top_bar_content)

        return top_bar

    def create_footer(self):
        """
        Crea el Footer con MDBottomNavigation para navegar entre las pantallas principales.
        """
        footer = MDBottomNavigation(
            selected_color_background="orange",
            text_color_active="lightgrey",
            panel_color=(0.91, 0.64, 0.45, 1),
        )

        footer.add_widget(MDBottomNavigationItem(
            name="inicio",
            text="Inicio",
            icon="home",
            on_tab_press=lambda _: self.switch_screen("inicio"),
        ))

        footer.add_widget(MDBottomNavigationItem(
            name="preguntas",
            text="Preguntas",
            icon="help-circle",
            on_tab_press=lambda _: self.switch_screen("preguntas"),
        ))

        footer.add_widget(MDBottomNavigationItem(
            name="contacto",
            text="Contacto",
            icon="phone",
            on_tab_press=lambda _: self.switch_screen("contacto"),
        ))

        footer.add_widget(MDBottomNavigationItem(
            name="buscar_mascota",
            text="Buscar",
            icon="map-search-outline",
            on_tab_press=lambda _: self.switch_screen("buscar_mascota"),
        ))

        return footer

    def switch_screen(self, screen_name):
        """
        Cambia la pantalla activa en el ScreenManager.
        """
        try:
            logger.info(f"Cambiando a la pantalla: {screen_name}")
            if screen_name not in self.screen_manager.screen_names:
                logger.warning(f"Pantalla '{screen_name}' no está registrada en el ScreenManager.")
                return
            self.screen_manager.current = screen_name
            logger.debug(f"Pantalla actual: {self.screen_manager.current}")
        except Exception as e:
            logger.error(f"Error al cambiar a la pantalla '{screen_name}': {e}")


if __name__ == "__main__":
    MyApp().run()