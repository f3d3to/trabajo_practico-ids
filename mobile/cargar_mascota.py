from kivy.uix.boxlayout import BoxLayout
from kivy.app import App  
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDRoundFlatButton
from kivy_garden.mapview import MapView, MapMarker
from kivymd.uix.boxlayout import MDBoxLayout
from logger import logger
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.selectioncontrol import MDCheckbox 
from kivy.uix.screenmanager import Screen
from plyer import filechooser

from kivy import platform

if platform == "android":
    from android.permissions import request_permissions, Permission, check_permission  
    request_permissions([Permission.READ_EXTERNAL_STORAGE,
                        Permission.WRITE_EXTERNAL_STORAGE])



    
from solicitudes import cargar_mascota  # Importa el endpoint

# =========================
# COMPONENTES REUTILIZABLES
# =========================

def create_step_title(text, font_style="H5", text_color=(0.42, 0.26, 0.12, 1)):
    """
    Crea un título para cada paso del formulario.
    """
    return MDLabel(
        text=text,
        halign="center",
        font_style=font_style,
        theme_text_color="Custom",
        text_color=text_color,
        size_hint=(1, None),
        height="50dp",
    )
def create_option_selector(options, callback):
    """
    Crea un selector de opciones representado por tarjetas con íconos.
    """
    layout = MDGridLayout(
        cols=len(options),
        spacing=dp(20),
        adaptive_size=True,
        size_hint=(None, None),
        padding=[dp(20), dp(0), dp(20), dp(0)],
    )

    # Diccionario para almacenar la tarjeta seleccionada
    dicc_tarjeta = {}

    def adjust_layout_size(*args):
        """Ajusta el número de columnas y la posición con base en el ancho de la ventana."""
        if Window.width < dp(400):
            layout.cols = 1
        elif Window.width < dp(600):
            layout.cols = 2
        else:
            layout.cols = len(options)
        layout.size_hint_x = None
        layout.width = layout.cols * dp(170)
        layout.pos_hint = {"center_x": 0.5}

    Window.bind(on_resize=adjust_layout_size)

    for label, icon in options:
        card = MDCard(
            orientation="vertical",
            size_hint=(None, None),
            size=(dp(150), dp(100)),
            md_bg_color=(0.862745, 0.796078, 0.705882, 1),  # Color de fondo inicial
            ripple_behavior=True,
        )

        card_layout = BoxLayout(orientation="vertical", padding=5)

        card_layout.add_widget(MDLabel(text=label, halign="center"))
        img = Image(source=f"assets/images/{icon}.png", size_hint=(None, None), size=("80dp", "80dp"))
        card_layout.add_widget(img)
        card.add_widget(card_layout)

        def on_card_click(instance, label=label):
            if dicc_tarjeta.get("selected"):
                dicc_tarjeta["selected"].md_bg_color = (0.862745, 0.796078, 0.705882, 1)
            instance.md_bg_color = (124 / 255, 88 / 255, 54 / 255, 1) 
            dicc_tarjeta["selected"] = instance
            callback(label)

        card.bind(on_release=on_card_click)
        layout.add_widget(card)

    adjust_layout_size()
    return layout


def create_navigation_buttons(previous_callback, next_callback):
    """
    Crea botones de navegación para moverse entre pasos.
    """
    # Contenedor para los botones, centrado horizontalmente
    layout = BoxLayout(
        orientation="horizontal",
        spacing=dp(20),
        size_hint=(None, None),
        width=dp(120),
        pos_hint={"center_x": 0.5},
    )

    # Botón de navegación anterior
    if previous_callback:
        layout.add_widget(
            MDIconButton(
                icon="arrow-left",
                on_release=lambda x: previous_callback(),
                size_hint=(None, None),
                size=(dp(40), dp(40)),
            )
        )

    # Botón de navegación siguiente
    if next_callback:
        layout.add_widget(
            MDIconButton(
                icon="arrow-right",
                on_release=lambda x: next_callback(),
                size_hint=(None, None),
                size=(dp(40), dp(40)),  
            )
        )

    return layout

# ===============
# CLASE PRINCIPAL
# ===============

class MobileCargarMascotaView(MDScreen):
    """
    Vista principal para cargar una mascota, dividida en pasos.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {
            "especie": None,
            "genero": None,
            "nombre": None,
            "raza": None,
            "color": None,
            "condicion": None,
            "estado": None,
            "foto_url": None,
            "zona": None,
            "barrio": None,
            "latitud": None,
            "longitud": None,
            "informacion_contacto": None,
        }# Almacena los datos de la mascota
        self.text_fields = {}  # Almacena los campos de texto
        self.md_bg_color = (0.8745, 0.8118, 0.7216, 1)
        self.build_step_1()


    def requerir_permisos(self):
        request_permissions([Permission.READ_EXTERNAL_STORAGE,Permission.WRITE_EXTERNAL_STORAGE])

    def clear_screen(self):
        """Limpia todos los widgets de la pantalla."""
        self.clear_widgets()

    def build_step_1(self):
        """
        Construye el primer paso para seleccionar la especie de la mascota.
        """
        self.clear_screen()
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=[1, 40, 1, 0])
        layout.add_widget(create_step_title("Selecciona la especie:"))
        species_options = [("Perro", "perro2"), ("Gato", "gato2"), ("Otro", "pajaro")]
        layout.add_widget(create_option_selector(species_options, self.on_species_selected))
        layout.add_widget(create_navigation_buttons(None, self.build_step_2))
        self.add_widget(layout)

    def build_step_2(self):
        """
        Construye el segundo paso para seleccionar el género de la mascota.
        """
        self.clear_screen()
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=[20, 3, 20, 0])
        layout.add_widget(create_step_title("Selecciona el género:"))
        gender_options = [("Macho", "macho"), ("Hembra", "hembra")]
        layout.add_widget(create_option_selector(gender_options, self.on_gender_selected))
        layout.add_widget(create_navigation_buttons(self.build_step_1, self.build_step_3))
        self.add_widget(layout)

    def build_step_3(self):
        """
        Construye el tercer paso para ingresar los datos básicos de la mascota.
        """
        self.clear_screen()
        fields = ["Nombre", "Raza", "Color"]
        layout = MDBoxLayout(orientation="vertical", spacing=1, padding=dp(10),adaptive_height=True)
        layout.add_widget(create_step_title("Datos básicos de la mascota:"))
        
        form_layout = MDGridLayout(cols=1, spacing=10, adaptive_height=True)
        for field in fields:
            hint = field.split("(")[0].strip()  # Mostrar solo el campo limpio en el hint
            key = field.split()[0].lower()  # Usar el campo base como clave en data
            text_field = MDTextField(hint_text=hint)
            self.text_fields[key] = text_field
            form_layout.add_widget(text_field)
        layout.add_widget(form_layout)

        button_layout = MDBoxLayout(orientation="vertical", size_hint=(1, None), height="50dp")
        load_image_button = MDRaisedButton(
        text="Cargar Imagen",
        on_release=self.open_filechooser,
        size_hint=(None, None),
        size=("200dp", "50dp"),  # Tamaño del botón
        pos_hint={"center_x": 0.5}  # Centrado
        )
        button_layout.add_widget(load_image_button)
        layout.add_widget(button_layout)
        self.image_status_label = MDLabel(
        text="",
        halign="center",
        theme_text_color="Custom",
        text_color= (0.42, 0.26, 0.12, 1),  
        )
        form_layout.add_widget(self.image_status_label)
        layout.add_widget(create_navigation_buttons(self.build_step_2, self.next_step))
      
        self.add_widget(layout)
    

    def build_step_4(self):
        """
        Construye el cuarto paso para seleccionar la ubicación de la mascota en el mapa.
        """
        self.clear_screen()
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=[20, 35, 20, 0])
        layout.add_widget(create_step_title("Selecciona la ubicación en el mapa"))
        
        # Crear el mapa y marcador
        self.map_view = MapView(lat=-34.6037, lon=-58.3816, zoom=10, size_hint=(1, 0.7))
        self.marker = MapMarker(lat=-0.1, lon=-0.1)
        self.map_view.add_marker(self.marker)
        self.map_view.bind(on_touch_up=self.update_location)
        layout.add_widget(self.map_view)

        # Botones de navegación, centrados
        nav_buttons = create_navigation_buttons(self.build_step_3, self.build_step_5)
        layout.add_widget(nav_buttons)

        # Centrar el layout dentro de la pantalla
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.add_widget(layout)

    def build_step_5(self):
        """
        Construye el quinto paso para ingresar la información de contacto.
        """
        self.clear_screen()
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=[20, 3, 20, 0])
        layout.add_widget(create_step_title("Ingresa información de contacto"))
        
        # Campo para información de contacto
        contact_field = MDTextField(hint_text="Ej: 1120405533 o email@ejemplo.com")
        self.text_fields["informacion_contacto"] = contact_field
        layout.add_widget(contact_field)
        
        # Botón de navegación
        nav_buttons = create_navigation_buttons(self.build_step_4, None)
        layout.add_widget(nav_buttons)

        # Botón de guardar
        layout.add_widget(
            MDRoundFlatButton(
                text="Guardar",
                md_bg_color= (0.42, 0.26, 0.12, 1),
                text_color= (0.98, 0.94, 0.86, 1),
                pos_hint={"center_x": 0.5},
                size_hint=(None, None),
                size=("250dp", "50dp"),
                on_release=self.save_pet,
            )
        )

        # Centrar el layout dentro de la pantalla
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.add_widget(layout)

    
    def open_filechooser(self, instance):
        """Función para abrir el selector de archivos y verificar permisos."""
        if platform == "android":
            if check_permission(Permission.READ_EXTERNAL_STORAGE) and check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                logger.info("Permisos concedidos. Abriendo filechooser...")
                filechooser.open_file(on_selection=self.on_image_selected)
            else:
                print("Permisos no concedidos. Solicitando permisos.")
                logger.warning("Permisos no concedidos. Solicitando permisos...")
                self.requerir_permisos()
        else:
            filechooser.open_file(on_selection=self.on_image_selected)



    def on_image_selected(self, selection):
        if selection:
            print(f"Imagen seleccionada: {selection[0]}")
            self.data["foto_url"] = selection[0]  # Procesar el archivo
            self.image_status_label.text = "¡Imagen cargada!"

        else:
            self.image_status_label.text = "No se seleccionó ninguna imagen."

    def update_location(self, instance, touch):
        """
        Actualiza la ubicación en el mapa cuando se toca sobre él.
        """
        if self.map_view.collide_point(*touch.pos):
            lat, lon = self.map_view.get_latlon_at(*touch.pos)
            if lat is not None and lon is not None:
                self.marker.lat, self.marker.lon = lat, lon
                self.data["latitud"] = lat
                self.data["longitud"] = lon
            else:
                logger.warning("No se pudo obtener la ubicación en el mapa.")

    def save_pet(self, *args):
        """
        Guarda la mascota enviando los datos al servidor.
        """
        for key, field in self.text_fields.items():
            self.data[key] = field.text.strip()

        
        logger.info(f"Enviando datos: {self.data}")
        cargar_mascota(self.data, self.handle_response)
        self.build_step_1()     
        app = App.get_running_app()  # Nos redirije a busqueda de masquetas
        app.screen_manager.current = 'buscar_mascota'  
        

        
    def handle_response(self, response):
        """
        Maneja la respuesta del servidor después de cargar la mascota.
        """
        if response.get("success"):
            logger.info("Mascota cargada exitosamente.")
        else:
            error_message = response.get("error", "Desconocido")
            logger.error(f"Error al cargar la mascota: {error_message}")

    def on_species_selected(self, species):
        """
        Maneja la selección de especie.
        """
        if species:
            self.data["especie"] = species
            logger.info(f"Especie seleccionada: {species}")
        else:
            logger.warning("No se seleccionó ninguna especie.")

    def on_gender_selected(self, gender):
        """
        Maneja la selección de género.
        """
        if gender:
            self.data["genero"] = gender
            logger.info(f"Género seleccionado: {gender}")
        else:
            logger.warning("No se seleccionó ningún género.")

    def validate_form(self):
        """
        Valida si los campos de texto y la imagen están completos.
        """
        for field, text_field in self.text_fields.items():
            if not text_field.text.strip():  
                text_field.error = True 
                Snackbar(text=f"El campo {field} es obligatorio").open()
                return False
            else:
                text_field.error = False 
        if not self.data["foto_url"]: 
            Snackbar(text="Debe seleccionar una imagen antes de continuar").open()
            return False

        return True

    def next_step(self):
        """
        Avanza al siguiente paso si el formulario es válido.
        """
        if self.validate_form():  # Si la validación es correcta
            self.build_step_4()  # Avanza al siguiente paso
        else:
            # Aquí puedes agregar un mensaje indicando que falta completar algunos campos
            logger.warning("Por favor complete todos los campos obligatorios.")
        
# ===========================
# RESPONSIVE LAYOUT
# ===========================

class ResponsiveCargarMascotaView(MDResponsiveLayout, MDScreen):
    """
    Vista responsiva para cargar una mascota, adaptada a móvil, tablet y escritorio.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Inicializa las vistas para móvil, tablet y escritorio.
        self.mobile_view = MobileCargarMascotaView()
        self.tablet_view = MobileCargarMascotaView()
        self.desktop_view = MobileCargarMascotaView()

    def get_current_view(self, window_width=800, window_height=600):
        """
        Selecciona la vista adecuada según el ancho de la ventana.
        
        Args:
            window_width (int): El ancho actual de la ventana.
            window_height (int): El alto actual de la ventana.

        Returns:
            Widget: Vista seleccionada (móvil, tablet o escritorio).
        """
        # Vista para dispositivos móviles
        if window_width < 600:
            self.mobile_view.size_hint = (1, None)
            self.mobile_view.height = window_height - dp(150)  # Restar altura del TopBar y Footer
            return self.mobile_view
        
        # Vista para tabletas
        elif window_width < 1200:
            self.tablet_view.size_hint = (1, None)
            self.tablet_view.height = window_height - dp(150)
            return self.tablet_view
        
        # Vista para escritorio
        else:
            self.desktop_view.size_hint = (1, None)
            self.desktop_view.height = window_height - dp(150)
            return self.desktop_view

