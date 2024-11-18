# Kivy
from kivy.uix.image import Image  # Imagenes
from kivy.uix.boxlayout import BoxLayout  # Layout de caja
from kivy.uix.carousel import Carousel  # Carrusel para imágenes
# KivyMD
from kivymd.app import MDApp  # Clase principal de la app
from kivymd.uix.screenmanager import MDScreenManager  # Gestor de pantallas
from kivymd.uix.screen import MDScreen  # Pantallas
from kivymd.uix.button import MDRaisedButton, MDRoundFlatButton, MDIconButton  # Botones
from kivymd.uix.label import MDLabel  # Etiquetas de texto
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem  # Footer navegación
from kivymd.uix.textfield import MDTextField  # Campos de texto
from kivymd.uix.gridlayout import MDGridLayout  # Layout de cuadrícula
from kivymd.uix.card import MDCard  # Tarjetas
from kivymd.uix.boxlayout import MDBoxLayout  # BoxLayout en KivyMD
from kivymd.uix.label.label import MDIcon  # Iconos
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
# Kivy Garden
from kivy_garden.mapview import MapView  # Mapa interactivo

class InicioScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=20)

        # Título destacado
        message_label = MDLabel(
            text="¿Perdiste a tu mascota?",
            size_hint=(1, 0.1),
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0.2, 0.8, 0.6, 1)  # Verde
        )
        layout.add_widget(message_label)

        # Carrusel de imágenes
        carousel = Carousel(loop=True, size_hint=(1, 0.9))
        images = ["assets/images/perro.png", "assets/images/gato.png", "assets/images/otro.png"]
        for img_path in images:
            carousel.add_widget(Image(source=img_path, allow_stretch=True))

        layout.add_widget(carousel)
        self.add_widget(layout)

class CargarMascotaScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_step = 1
        self.build_step_1()

    def clear_screen(self):
        """Limpia la pantalla para cargar el contenido de un nuevo paso."""
        self.clear_widgets()

    def build_step_1(self):
        """Construye el paso 1: Seleccionar la especie de la mascota."""
        self.clear_screen()
        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=20)


        layout.add_widget(MDLabel(
            text="Completá los datos de tu mascota",
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0.2, 0.8, 0.6, 1)  # Verde
        ))
        layout.add_widget(MDLabel(text="Especie:", halign="center"))

        # Botones para seleccionar especie
        species_layout = MDGridLayout(cols=3, spacing=20, size_hint=(1, 0.5))
        for species, icon in [("Perro", "dog"), ("Gato", "cat"), ("Otro", "bird")]:
            species_card = self.create_selection_card(species, icon)
            species_layout.add_widget(species_card)

        layout.add_widget(species_layout)

        # Botón siguiente

        next_button = MDIconButton(
            icon="arrow-right",
            size_hint=(None, None),
            size=("100dp", "50dp"),
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.build_step_2(),
        )
        layout.add_widget(next_button)
        self.add_widget(layout)

    def build_step_2(self):
        """Construye el paso 2: Seleccionar el sexo de la mascota."""
        self.clear_screen()
        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=20)

        layout.add_widget(MDLabel(
            text="Completá los datos de tu mascota",
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0.2, 0.8, 0.6, 1)  # Verde
        ))
        layout.add_widget(MDLabel(text="Selecciona el sexo:", halign="center"))

        # Botones para seleccionar el sexo
        sex_layout = MDGridLayout(cols=2, spacing=20, size_hint=(1, 0.5))
        for sex, icon in [("Macho", "gender-male"), ("Hembra", "gender-female")]:
            sex_card = self.create_selection_card(sex, icon)
            sex_layout.add_widget(sex_card)

        layout.add_widget(sex_layout)

        # Botones de navegación
        nav_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height="50dp", spacing=20)
        nav_layout.add_widget(MDIconButton(
            icon="arrow-left",
            on_release=lambda x: self.build_step_1(),
        ))
        nav_layout.add_widget(MDIconButton(
            icon="arrow-right",
            on_release=lambda x: self.build_step_3(),
        ))
        layout.add_widget(nav_layout)
        self.add_widget(layout)

    def build_step_3(self):
        """Construye el paso 3: Formulario de datos."""
        self.clear_screen()
        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=20)

        layout.add_widget(MDLabel(
            text="Completá los datos de tu mascota",
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0.2, 0.8, 0.6, 1)  # Verde
        ))

        # Campos del formulario
        form_layout = MDGridLayout(cols=2, adaptive_height=True, spacing=10)
        fields = ["Nombre", "Raza", "Color", "Condición", "Estado", "Foto URL"]
        for field in fields:
            form_layout.add_widget(MDTextField(hint_text=f"Ejem: {field}"))

        layout.add_widget(form_layout)

        # Botones de navegación
        nav_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height="50dp", spacing=20)
        nav_layout.add_widget(MDIconButton(
            icon="arrow-left",
            on_release=lambda x: self.build_step_2(),
        ))
        nav_layout.add_widget(MDIconButton(
            icon="arrow-right",
            on_release=lambda x: self.build_step_4(),
        ))
        layout.add_widget(nav_layout)
        self.add_widget(layout)

    def build_step_4(self):
        """Construye el paso 4: Seleccionar ubicación en el mapa."""
        self.clear_screen()
        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=20)


        layout.add_widget(MDLabel(
            text="Completá los datos de tu mascota",
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0.2, 0.8, 0.6, 1)  # Verde
        ))
        layout.add_widget(MDLabel(text="Selecciona la ubicación en el mapa:", halign="center"))

        # Mapa interactivo
        map_view = MapView(zoom=10, lat=-34.6037, lon=-58.3816, size_hint=(1, 0.7))
        layout.add_widget(map_view)

        # Botones de navegación
        nav_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height="50dp", spacing=20)
        nav_layout.add_widget(MDIconButton(
            icon="arrow-left",
            on_release=lambda x: self.build_step_4(),
        ))
        nav_layout.add_widget(MDIconButton(
            icon="arrow-right",
            on_release=lambda x: self.build_step_5(),
        ))
        layout.add_widget(nav_layout)
        self.add_widget(layout)

    def build_step_5(self):
        """Construye el paso 5: Información de contacto."""
        self.clear_screen()
        layout = BoxLayout(orientation="vertical", spacing=20, padding=20)

        layout.add_widget(MDLabel(
            text="Completá los datos de tu mascota",
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0.2, 0.8, 0.6, 1)  # Verde
        ))
        layout.add_widget(MDLabel(text="Información de Contacto:", halign="center"))

        # Campo de contacto
        contact_field = MDTextField(
            hint_text="Ej: 1120405533 o email@ejemplo.com",
            size_hint=(0.8, None),
            height="50dp",
            pos_hint={"center_x": 0.5},
        )
        layout.add_widget(contact_field)

        # Botones de navegación
        nav_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height="50dp", spacing=20)
        nav_layout.add_widget(MDIconButton(
            icon="arrow-left",
            on_release=lambda x: self.build_step_4(),
        ))
        nav_layout.add_widget(MDRoundFlatButton(
            text="Guardar",
            md_bg_color=(0.2, 0.8, 0.6, 1),
        ))
        layout.add_widget(nav_layout)
        self.add_widget(layout)

    def create_selection_card(self, text, icon):
        """Crea una tarjeta para las opciones de selección (especie/sexo)."""
        card = MDCard(
            orientation="vertical",
            size_hint=(None, None),
            size=("150dp", "100dp"),
            md_bg_color=(0.95, 0.95, 0.95, 1),
            ripple_behavior=True,
        )
        layout = BoxLayout(orientation="vertical", padding=10)
        layout.add_widget(MDLabel(text=text, halign="center"))
        layout.add_widget(MDIcon(icon=icon, halign="center", theme_text_color="Custom", text_color=(0.2, 0.4, 1, 1)))
        card.add_widget(layout)
        return card

class ContactoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = MDBoxLayout(orientation="vertical", spacing=20, padding=20)

        # Título
        title = MDLabel(
            text="Contactar",
            size_hint_y=None,
            height="40dp",
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0.2, 0.8, 0.6, 1)  # Verde
        )
        main_layout.add_widget(title)

        # Información de contacto (Correo y WhatsApp)
        contact_info = MDBoxLayout(orientation="horizontal", spacing=20, size_hint_y=None, height="60dp")
        contact_info.add_widget(MDLabel(text="Correo electrónico:\nhuellas@fi.uba.ar", halign="left"))
        contact_info.add_widget(MDLabel(text="WhatsApp:\n222111333", halign="left"))
        main_layout.add_widget(contact_info)

        # Formulario de contacto
        form_layout = MDGridLayout(cols=2, row_default_height="50dp", adaptive_height=True, padding=10, spacing=10)

        form_layout.add_widget(MDTextField(hint_text="Su nombre"))
        form_layout.add_widget(MDTextField(hint_text="Su correo"))
        form_layout.add_widget(MDTextField(hint_text="Teléfono"))
        form_layout.add_widget(MDTextField(hint_text="Asunto"))
        message_field = MDTextField(hint_text="Mensaje", multiline=True, size_hint_y=None, height="100dp")
        form_layout.add_widget(message_field)

        main_layout.add_widget(form_layout)

        # Botón enviar mensaje
        send_button = MDRaisedButton(
            text="ENVIAR MENSAJE",
            md_bg_color=(0.91, 0.64, 0.45, 1),  # Marrón claro
            text_color=(1, 1, 1, 1),  # Blanco
            size_hint=(None, None),
            size=("200dp", "40dp"),
            pos_hint={"center_x": 0.5},
        )
        main_layout.add_widget(send_button)

        # Tarjetas informativas (Campañas, Calendario, Cuidado)
        cards_layout = MDGridLayout(cols=3, adaptive_height=True, spacing=20, padding=10)

        cards_layout.add_widget(self.create_card("CAMPAÑAS", "Cronograma de campañas sociales y de adopción para mascotas.", "account-group"))
        cards_layout.add_widget(self.create_card("CALENDARIO DE VACUNACIÓN", "Consulta al veterinario para desparasitar y vacunar a tu mascota.", "needle"))
        cards_layout.add_widget(self.create_card("CUIDÁ A TU MASCOTA", "Consejos útiles para el correcto cuidado de tu mascota.", "heart"))

        main_layout.add_widget(cards_layout)
        self.add_widget(main_layout)

    def create_card(self, title, text,
                    icon_name):
        """Crea una tarjeta con un ícono, título y texto descriptivo."""
        card = MDCard(
            orientation="vertical",
            padding=10,
            size_hint=(None, None),
            size=("300dp", "150dp"),
            md_bg_color=(0.9, 0.9, 0.9, 1),  # Fondo gris claro
        )
        card_layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10)
        icon = MDIcon(icon=icon_name, halign="center", theme_text_color="Custom", text_color=(0.2, 0.4, 1, 1))
        title_label = MDLabel(text=title, font_style="H6", halign="center", size_hint_y=None, height="30dp")
        text_label = MDLabel(text=text, halign="center", size_hint_y=None, height="60dp")
        card_layout.add_widget(icon)
        card_layout.add_widget(title_label)
        card_layout.add_widget(text_label)
        card.add_widget(card_layout)
        return card

class PreguntasScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=20)

        # Título de la sección
        title = MDLabel(
            text="Preguntas Frecuentes",
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0.2, 0.8, 0.6, 1),  # Verde
            size_hint=(1, None),
        )
        layout.add_widget(title)

        # Pregunta 1
        panel1 = MDExpansionPanel(
            content=MDLabel(
                text="Puedes agregar una mascota perdida desde la sección 'Cargar Mascota'. Completa el formulario con los datos de la mascota.",
                size_hint_y=None,
                valign="top",
                halign="left",
                height="100dp",
            ),
            panel_cls=MDExpansionPanelOneLine(text="¿Cómo agrego una mascota perdida?"),
        )
        layout.add_widget(panel1)

        # Pregunta 2
        panel2 = MDExpansionPanel(
            content=MDLabel(
                text="Para eliminar una publicación, dirígete a 'Mis Publicaciones' y selecciona la opción 'Eliminar'.",
                size_hint_y=None,
                valign="top",
                halign="left",
                height="100dp",
            ),
            panel_cls=MDExpansionPanelOneLine(text="¿Cómo elimino una publicación?"),
        )
        layout.add_widget(panel2)

        # Pregunta 3
        panel3 = MDExpansionPanel(
            content=MDLabel(
                text="Puedes editar los datos desde 'Mis Publicaciones'. Haz clic en la publicación que deseas editar y actualiza la información.",
                size_hint_y=None,
                valign="top",
                halign="left",
                height="100dp",
            ),
            panel_cls=MDExpansionPanelOneLine(text="¿Puedo editar los datos de mi publicación?"),
        )
        layout.add_widget(panel3)

        self.add_widget(layout)

class BuscarMascotaScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=20)

        # Título
        layout.add_widget(MDLabel(
            text="Búsqueda",
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0.2, 0.8, 0.6, 1)  # Verde
        ))

        # Grid para los filtros
        filter_layout = MDGridLayout(cols=3, row_default_height="50dp", adaptive_height=True, spacing=20)

        # Campos de filtro
        filter_layout.add_widget(MDTextField(hint_text="Especie:"))
        filter_layout.add_widget(MDTextField(hint_text="Sexo:"))
        filter_layout.add_widget(MDTextField(hint_text="Raza:"))
        filter_layout.add_widget(MDTextField(hint_text="Color:"))
        filter_layout.add_widget(MDTextField(hint_text="Zona:"))
        filter_layout.add_widget(MDTextField(hint_text="Barrio:"))
        filter_layout.add_widget(MDTextField(hint_text="Información de contacto:"))
        filter_layout.add_widget(MDTextField(hint_text="Fecha de publicación:", helper_text="mm/dd/yyyy", helper_text_mode="on_focus"))

        layout.add_widget(filter_layout)

        # Botón de búsqueda
        search_button = MDRoundFlatButton(
            text="Buscar",
            md_bg_color=(0.2, 0.8, 0.6, 1),  # Verde
            text_color=(1, 1, 1, 1),  # Blanco
            size_hint=(None, None),
            size=("200dp", "40dp"),
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.perform_search()  # Placeholder para función de búsqueda
        )
        layout.add_widget(search_button)

        # Mapa interactivo
        map_view = MapView(zoom=10, lat=-34.6037, lon=-58.3816, size_hint=(1, 0.7))
        layout.add_widget(map_view)

        self.add_widget(layout)

    def perform_search(self):
        """Función placeholder para realizar búsqueda."""
        print("Buscando mascotas con los filtros seleccionados...")

class CustomTopBar(BoxLayout):
    def __init__(self, switch_screen_callback, **kwargs):
        super().__init__(**kwargs)

        self.size_hint_y= None
        self.height= "100dp"
        self.md_bg_color= (0.91, 0.64, 0.45, 1)  # Marrón claro
        self.padding= "10dp"
        self.spacing= "120dp"

        # Logo alineado a la izquierda
        logo = Image(
            source="assets/images/logo.png",
            size_hint=(None, None),
            allow_stretch=True,

        )
        self.add_widget(logo)

        # Espaciador para empujar el botón hacia la derecha
        spacer = BoxLayout(size_hint_x=1)
        self.add_widget(spacer)

        # Botón "Iniciá tu búsqueda" alineado a la derecha
        search_button = MDRoundFlatButton(
            text="Iniciá tu Búsqueda",
            icon="arrow-right-thin",
            md_bg_color=(0.2, 0.8, 0.6, 1),  # Verde
            text_color=(1, 1, 1, 1),  # Blanco
            size_hint=(None, None),
            size=("180dp", "40dp"),
            on_release=lambda x: switch_screen_callback("cargar_mascota"),
        )
        self.add_widget(search_button)

class CustomFooter(MDBottomNavigation):
    def __init__(self, switch_screen_callback, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(
            MDBottomNavigationItem(
                name="inicio",
                text="Inicio",
                icon="home",
                on_tab_press=lambda x: switch_screen_callback("inicio")
            )
        )
        self.add_widget(
            MDBottomNavigationItem(
                name="contacto",
                text="Contacto",
                icon="phone",
                on_tab_press=lambda x: switch_screen_callback("contacto")
            )
        )
        self.add_widget(
            MDBottomNavigationItem(
                name="preguntas",
                text="Preguntas",
                icon="help-circle",
                on_tab_press=lambda x: switch_screen_callback("preguntas")
            )
        )
        self.add_widget(
            MDBottomNavigationItem(
                name="buscar_mascota",
                text="Buscar",
                icon="map-search-outline",
                on_tab_press=lambda x: switch_screen_callback("buscar_mascota")
            )
        )

class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Brown"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Light"
        self.title = "Huellas a casa"

        # Crear el ScreenManager
        self.screen_manager = MDScreenManager()

        # Agregar pantallas
        self.screen_manager.add_widget(InicioScreen(name="inicio"))
        self.screen_manager.add_widget(CargarMascotaScreen(name="cargar_mascota"))
        self.screen_manager.add_widget(ContactoScreen(name="contacto"))
        self.screen_manager.add_widget(PreguntasScreen(name="preguntas"))
        self.screen_manager.add_widget(BuscarMascotaScreen(name="buscar_mascota"))

        # Contenedor principal
        root = BoxLayout(orientation="vertical")
        root.add_widget(self.create_top_bar())
        root.add_widget(self.screen_manager)
        root.add_widget(self.create_footer())

        return root

    def create_top_bar(self):
        return CustomTopBar(switch_screen_callback=self.switch_screen)

    def create_footer(self):
        return CustomFooter(switch_screen_callback=self.switch_screen)

    def switch_screen(self, screen_name):
        self.screen_manager.current = screen_name


if __name__ == "__main__":
    MyApp().run()
