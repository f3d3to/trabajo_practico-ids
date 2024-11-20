from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDRoundFlatButton
from kivy_garden.mapview import MapView
from kivymd.uix.boxlayout import MDBoxLayout
from logger import logger
from kivy.metrics import dp
from kivy.core.window import Window

# Componente reutilizable: Título
def create_step_title(text, font_style="H5", text_color=(0.2, 0.8, 0.6, 1)):
    # logger.debug(f"Creando título: {text}")
    return MDLabel(
        text=text,
        halign="center",
        font_style=font_style,
        theme_text_color="Custom",
        text_color=text_color,
        size_hint=(1, None),
        height="50dp",
    )


# Componente reutilizable: Selector de opciones


def create_option_selector(options, callback):
    # GridLayout para las opciones
    layout = MDGridLayout(
        cols=len(options),  # Inicialmente tantas columnas como opciones
        spacing=dp(20),
        adaptive_size=True,
        size_hint=(None, None),  # Para que podamos centrar el layout
        padding=[dp(20), dp(0), dp(20), dp(0)],  # Espaciado horizontal y vertical
    )

    # Ajusta el número de columnas y la posición basado en el ancho de la ventana
    def adjust_layout_size(*args):
        if Window.width < dp(400):  # Pantallas pequeñas
            layout.cols = 1  # Apilar las tarjetas en una columna
        elif Window.width < dp(600):  # Pantallas medianas
            layout.cols = 2  # Dos tarjetas por fila
        else:
            layout.cols = len(options)  # Todas las tarjetas en una fila

        # Asegurar que el layout esté centrado horizontalmente
        layout.size_hint_x = None
        layout.width = layout.cols * dp(170)  # Ajustar el ancho total del layout
        layout.pos_hint = {"center_x": 0.5}  # Centrar el layout

    # Enlaza la función de ajuste al evento de cambio de tamaño de ventana
    Window.bind(on_resize=adjust_layout_size)

    # Añade las tarjetas al layout
    for label, icon in options:
        card = MDCard(
            orientation="vertical",
            size_hint=(None, None),
            size=(dp(150), dp(100)),
            md_bg_color=(0.95, 0.95, 0.95, 1),
            ripple_behavior=True,
            on_release=lambda x, lbl=label: callback(lbl),
        )
        card_layout = BoxLayout(orientation="vertical", padding=10)
        card_layout.add_widget(MDLabel(text=label, halign="center"))
        card_layout.add_widget(MDIconButton(icon=icon, pos_hint={"center_x": 0.5}))
        card.add_widget(card_layout)
        layout.add_widget(card)

    adjust_layout_size()  # Ajusta al inicializar
    return layout


# Componente reutilizable: Formulario dinámico
def create_form(fields):
    # logger.debug(f"Creando formulario con campos: {fields}")
    layout = MDGridLayout(
        cols=2, spacing=10, size_hint=(1, None), adaptive_height=True
    )
    layout.pos_hint = {"center_x": 0.5}
    for field in fields:
        layout.add_widget(MDTextField(hint_text=f"Ejem: {field}"))
    return layout


# Componente reutilizable: Mapa interactivo
def create_map(lat=-34.6037, lon=-58.3816, zoom=10):
    # logger.debug(f"Creando mapa interactivo en latitud {lat}, longitud {lon}, zoom {zoom}")
    return MapView(lat=lat, lon=lon, zoom=zoom, size_hint=(1, 0.7))


# Componente reutilizable: Botones de navegación
# Componente reutilizable: Botones de navegación
def create_navigation_buttons(previous_callback, next_callback):
    # Contenedor principal para centrar el layout
    wrapper = BoxLayout(
        orientation="horizontal",
        size_hint=(None, None),  # El tamaño del contenedor no depende del padre
        width=dp(120),  # Ancho ajustado dinámicamente
        height=dp(50),  # Altura fija para los botones
        pos_hint={"center_x": 0.5},  # Centra el contenedor en el eje horizontal
    )

    # Contenedor para los botones
    layout = BoxLayout(
        orientation="horizontal",
        spacing=dp(20),  # Espaciado entre botones
        size_hint=(None, None),  # Tamaño independiente
    )

    # Botón de navegación anterior
    if previous_callback:
        layout.add_widget(
            MDIconButton(
                icon="arrow-left",
                on_release=lambda x: previous_callback(),
                size_hint=(None, None),  # Ajuste para no deformar
                size=(dp(40), dp(40)),
            )
        )

    # Botón de navegación siguiente
    if next_callback:
        layout.add_widget(
            MDIconButton(
                icon="arrow-right",
                on_release=lambda x: next_callback(),
                size_hint=(None, None),  # Ajuste para no deformar
                size=(dp(40), dp(40)),
            )
        )

    # Ajusta el ancho del contenedor principal al contenido de los botones
    wrapper.add_widget(layout)
    return wrapper



# Vista de carga para dispositivos móviles
class MobileCargarMascotaView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # logger.info("Inicializando MobileCargarMascotaView")
        self.current_step = 1
        self.build_step_1()

    def clear_screen(self):
        # logger.debug("Limpiando pantalla")
        self.clear_widgets()

    def build_step_1(self):
        # logger.info("Construyendo paso 1: Seleccionar especie")
        self.clear_screen()
        layout = MDBoxLayout(
            orientation="vertical", spacing=20, padding=[20, 40, 20, 0],
        )

        layout.add_widget(create_step_title("Completá los datos de tu mascota"))
        layout.add_widget(create_step_title("Selecciona la especie:", font_style="Subtitle1"))

        species_options = [("Perro", "dog"), ("Gato", "cat"), ("Otro", "bird")]
        layout.add_widget(create_option_selector(species_options, self.on_species_selected))

        layout.add_widget(create_navigation_buttons(None, self.build_step_2))
        self.add_widget(layout)

    def build_step_2(self):
        # logger.info("Construyendo paso 2: Seleccionar sexo")
        self.clear_screen()
        layout = MDBoxLayout(
            orientation="vertical", spacing=20, padding=[20, 40, 20, 0]
        )

        layout.add_widget(create_step_title("Selecciona el sexo:"))
        sex_options = [("Macho", "gender-male"), ("Hembra", "gender-female")]
        layout.add_widget(create_option_selector(sex_options, self.on_sex_selected))

        layout.add_widget(create_navigation_buttons(self.build_step_1, self.build_step_3))
        self.add_widget(layout)

    def build_step_3(self):
        # logger.info("Construyendo paso 3: Formulario de datos")
        self.clear_screen()
        layout = MDBoxLayout(
            orientation="vertical", spacing=20, padding=[20, 40, 20, 0]
        )

        fields = ["Nombre", "Raza", "Color", "Condición", "Estado", "Foto URL"]
        layout.add_widget(create_step_title("Completá los datos de tu mascota"))
        layout.add_widget(create_form(fields))

        layout.add_widget(create_navigation_buttons(self.build_step_2, self.build_step_4))
        self.add_widget(layout)

    def build_step_4(self):
        # logger.info("Construyendo paso 4: Seleccionar ubicación")
        self.clear_screen()
        layout = MDBoxLayout(
            orientation="vertical", spacing=20, padding=[20, 40, 20, 0]
        )

        layout.add_widget(create_step_title("Selecciona la ubicación en el mapa"))
        layout.add_widget(create_map())

        layout.add_widget(create_navigation_buttons(self.build_step_3, self.build_step_5))
        self.add_widget(layout)

    def build_step_5(self):
        # logger.info("Construyendo paso 5: Contacto")
        self.clear_screen()
        layout = MDBoxLayout(
            orientation="vertical", spacing=20, padding=[20, 40, 20, 0]
        )

        layout.add_widget(create_step_title("Ingresa información de contacto"))
        layout.add_widget(MDTextField(hint_text="Ej: 1120405533 o email@ejemplo.com"))

        layout.add_widget(create_navigation_buttons(self.build_step_4, None))
        layout.add_widget(
            MDRoundFlatButton(
                text="Guardar",
                md_bg_color=(0.2, 0.8, 0.6, 1),
                text_color=(1, 1, 1, 1),
                pos_hint={"center_x": 0.5},
                size_hint=(None, None),
                size=("200dp", "40dp"),
            )
        )
        self.add_widget(layout)

    def on_species_selected(self, species):
        logger.info(f"Especie seleccionada: {species}")

    def on_sex_selected(self, sex):
        logger.info(f"Sexo seleccionado: {sex}")


# Vista responsiva principal para cargar mascota
class ResponsiveCargarMascotaView(MDResponsiveLayout, MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # logger.info("Inicializando ResponsiveCargarMascotaView")
        self.mobile_view = MobileCargarMascotaView()
        self.tablet_view = MobileCargarMascotaView()
        self.desktop_view = MobileCargarMascotaView()

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
