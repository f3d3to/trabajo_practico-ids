"""
Módulo principal para la vista de búsqueda de mascotas. 
Incluye una interfaz responsiva y componentes para filtrar y visualizar mascotas en un mapa interactivo.
"""

from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy_garden.mapview import MapView, MapMarker
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from logger import logger
from solicitudes import obtener_mascotas_perdidas, buscar_mascota


# =========================
# Componentes reutilizables
# =========================

def create_step_title(text, font_style="H5", text_color=(0.2, 0.8, 0.6, 1)):
    """
    Crea un título estilizado para los pasos de la interfaz.
    """
    return MDLabel(
        text=text,
        halign="center",
        font_style=font_style,
        theme_text_color="Custom",
        text_color=text_color,
        size_hint=(1, None),
        height=dp(40),
    )


def create_search_filters(filter_fields):
    """
    Crea un layout con los campos de filtro para la búsqueda de mascotas.
    """
    layout = MDGridLayout(cols=2, spacing=dp(10), adaptive_height=True, padding=[dp(20), dp(10)])
    filters = [
        ("Especie", "especie"),
        ("Sexo", "genero"),
        ("Raza", "raza"),
        ("Color", "color"),
        ("Zona", "zona"),
        ("Barrio", "barrio"),
        ("Contacto", "informacion_contacto"),
        ("Fecha de publicación (dd/mm/aaaa)", "fecha"),
    ]

    for hint, id_name in filters:
        text_field = MDTextField(hint_text=hint, size_hint_x=0.9, pos_hint={"center_x": 0.5})
        filter_fields[id_name] = text_field
        layout.add_widget(text_field)
    
    return layout


def create_search_button(filters, callback):
    """
    Crea el botón de búsqueda que invoca un callback al ser presionado.
    """
    return MDRoundFlatButton(
        text="Buscar",
        md_bg_color=(0.2, 0.8, 0.6, 1),
        text_color=(1, 1, 1, 1),
        size_hint=(None, None),
        size=(dp(200), dp(40)),
        pos_hint={"center_x": 0.5},
        on_release=lambda _: callback(filters),
    )


def create_clear_filters_button(callback):
    """
    Crea el botón para limpiar los filtros de búsqueda.
    """
    return MDRoundFlatButton(
        text="Limpiar Filtros",
        md_bg_color=(0.2, 0.8, 0.6, 1),
        text_color=(1, 1, 1, 1),
        size_hint=(None, None),
        size=(dp(200), dp(40)),
        pos_hint={"center_x": 0.5},
        on_release=lambda _: callback(),
    )


def create_interactive_map(lat=-34.6076, lon=-58.4188, zoom=10):
    """
    Crea un mapa interactivo para mostrar marcadores de mascotas.
    """
    return MapView(
        lat=lat,
        lon=lon,
        zoom=zoom,
        size_hint=(1, None),
        height=dp(300),
        double_tap_zoom=True,
    )


# ==================
# Clases Especificas
# ==================

class MascotaPopup(Popup):
    """
    Popup que muestra información detallada de una mascota.
    """
    def __init__(self, mascota, **kwargs):
        super().__init__(**kwargs)
        self.title = f"Buscamos a {mascota.get('nombre', 'Mascota desconocida')}"
        self.size_hint = (1, 0.8)
        self.content = Label(text=self.get_mascota_info(mascota))

    def get_mascota_info(self, mascota):
        """
        Devuelve una cadena con la información de la mascota.
        """
        info = "\n".join(
            [
                f"Nombre: {mascota.get('nombre', 'Desconocida')}",
                f"Especie: {mascota.get('especie', 'Desconocida')}",
                f"Raza: {mascota.get('raza', 'Desconocida')}",
                f"Estado: {mascota.get('estado', 'Desconocida')}",
                f"Color: {mascota.get('color', 'Desconocido')}",
                f"Zona: {mascota.get('zona', 'Desconocida')}",
                f"Barrio: {mascota.get('barrio', 'Desconocida')}",
                f"Fecha: {mascota.get('fecha_publicacion', 'Desconocida')}",
                f"Contacto: {mascota.get('informacion_contacto', 'No disponible')}",
            ]
        )
        return info


class CustomMapMarker(MapMarker):
    """
    Marcador de mapa personalizado que cambia de ícono según la especie de la mascota.
    """
    def __init__(self, especie_mascota, **kwargs):
        super().__init__(**kwargs)
        self.especie_mascota = especie_mascota
        self.source = f"assets/images/{especie_mascota}.png" if especie_mascota in ["perro", "gato"] else "assets/images/pajaro.png"
        self.size = (25, 25)


class MobileBuscarMascotaView(MDScreen):
    """
    Vista principal para la búsqueda de mascotas en dispositivos móviles.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.map_view = create_interactive_map()
        self.filter_fields = {}
        self.map_markers = []
        self.build_view()

    def build_view(self):
        """
        Construye la interfaz principal.
        """
        scroll = ScrollView()
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            size_hint_y=None,
        )
        layout.bind(minimum_height=layout.setter("height"))

        layout.add_widget(create_step_title("Buscar Mascota"))
        layout.add_widget(create_search_filters(self.filter_fields))
        layout.add_widget(create_search_button({}, self.perform_search))
        layout.add_widget(create_clear_filters_button(self.clear_filters_and_search))
        layout.add_widget(self.map_view)

        scroll.add_widget(layout)
        self.add_widget(scroll)

    def perform_search(self, filtros):
        """
        Realiza la búsqueda de mascotas según los filtros.
        """
        filtros = {key: field.text for key, field in self.filter_fields.items()}
        logger.info(f"Ejecutando búsqueda con filtros: {filtros}")
        buscar_mascota(filtros, self.update_map_with_markers)

    def clear_filters_and_search(self):
        """
        Limpia los campos de búsqueda y obtiene todas las mascotas.
        """
        for field in self.filter_fields.values():
            field.text = ""
        obtener_mascotas_perdidas(self.update_map_with_markers)

    def update_map_with_markers(self, response):
        """
        Actualiza los marcadores en el mapa según la respuesta.
        """
        if not response.get("success", False):
            logger.error(f"Error al obtener los datos de mascotas: {response.get('error', '')}")
            return

        mascotas = response.get("data", [])
        logger.info(f"Se encontraron {len(mascotas)} mascotas.")
        self.remove_all_markers()

        for mascota in mascotas:
            lat, lon, especie = mascota.get("latitud"), mascota.get("longitud"), mascota.get("especie")
            if lat and lon:
                marker = CustomMapMarker(especie_mascota=especie, lat=lat, lon=lon)
                marker.bind(on_release=lambda marker, mascota=mascota: 
                            MascotaPopup(mascota=mascota).open())
                self.map_view.add_widget(marker)
                self.map_markers.append(marker)

    def remove_all_markers(self):
        """
        Elimina todos los marcadores del mapa.
        """
        for marker in self.map_markers:
            self.map_view.remove_widget(marker)
        self.map_markers.clear()


class ResponsiveBuscarMascotaView(MDResponsiveLayout, MDScreen):
    """
    Vista responsiva que adapta la interfaz a distintos tamaños de pantalla.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mobile_view = MobileBuscarMascotaView()
        self.tablet_view = self.mobile_view  # Reutilización simplificada
        self.desktop_view = self.mobile_view

    def get_current_view(self, window_width=800, window_height=600):
        """
        Devuelve la vista actual según el ancho de la ventana.
        """
        if window_width < 600:  # Mobile
            return self.mobile_view
        elif window_width < 1200:  # Tablet
            return self.tablet_view
        else:  # Desktop
            return self.desktop_view
