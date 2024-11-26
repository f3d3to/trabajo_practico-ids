from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from solicitudes import obtener_preguntas_frecuentes  # Importar endpoint

# ========================
# Componente reutilizables
# ========================

def create_title(text, font_style="H5", text_color=(0.2, 0.8, 0.6, 1)):
    """
    Crea un título con las configuraciones personalizables.
    """
    return MDLabel(
        text=text,
        halign="center",
        font_style=font_style,
        theme_text_color="Custom",
        text_color=text_color,
        size_hint=(1, None),
        height="50dp"
    )

def create_expandable_question(question_text, answer_text):
    """
    Crea un panel expandible para una pregunta frecuente.
    """
    return MDExpansionPanel(
        content=MDLabel(
            text=answer_text,
            size_hint_y=None,
            valign="top",
            halign="left",
            height="100dp"
        ),
        panel_cls=MDExpansionPanelOneLine(text=question_text),
    )

def fetch_questions_and_update(layout):
    """
    Obtiene preguntas frecuentes desde el backend y actualiza la vista.
    """
    def update_view(response):
        """
        Callback para actualizar la vista con la respuesta de la API.
        """
        # Verifica si la respuesta es exitosa
        if not response.get("success", False):
            layout.add_widget(
                MDLabel(
                    text="Error al cargar las preguntas frecuentes.",
                    halign="center",
                    theme_text_color="Error",
                )
            )
            return

        # Extraer preguntas frecuentes del formato proporcionado
        preguntas_frecuentes = response.get("data", {}).get("preguntas_frecuentes", [])
        if not preguntas_frecuentes:
            layout.add_widget(
                MDLabel(
                    text="No hay preguntas disponibles.",
                    halign="center",
                    theme_text_color="Custom",
                    text_color=(0.5, 0.5, 0.5, 1),
                )
            )
        else:
            # Agrega cada pregunta y su respuesta al layout
            for pregunta in preguntas_frecuentes:
                question_text = pregunta.get("pregunta", "Pregunta no disponible")
                answer_text = pregunta.get("respuesta", "Respuesta no disponible")
                layout.add_widget(create_expandable_question(question_text, answer_text))

    # Llamada al endpoint para obtener las preguntas frecuentes
    obtener_preguntas_frecuentes(update_view)

# ===================================
# Vistas para diferentes dispositivos
# ===================================

class MobilePreguntasView(MDScreen):
    """
    Vista para dispositivos móviles.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=20)
        layout.add_widget(create_title("Preguntas Frecuentes"))
        self.add_widget(layout)

        # Cargar preguntas desde el backend
        fetch_questions_and_update(layout)

class TabletPreguntasView(MDScreen):
    """
    Vista para tabletas.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)
        layout.add_widget(create_title("Preguntas Frecuentes", font_style="H4", text_color=(0.1, 0.7, 0.5, 1)))
        self.add_widget(layout)

        fetch_questions_and_update(layout)

class DesktopPreguntasView(MDScreen):
    """
    Vista para escritorio.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", spacing=30, padding=50)
        layout.add_widget(create_title("Preguntas Frecuentes", font_style="H3", text_color=(0.0, 0.6, 0.4, 1)))
        self.add_widget(layout)

        fetch_questions_and_update(layout)

# ==========================
# Vista responsiva principal
# ==========================

class ResponsivePreguntasView(MDResponsiveLayout, MDScreen):
    """
    Vista responsiva que ajusta la interfaz según el tamaño de pantalla.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mobile_view = MobilePreguntasView()
        self.tablet_view = TabletPreguntasView()
        self.desktop_view = DesktopPreguntasView()

    def get_current_view(self, window_width=800):
        """
        Seleccionar la vista según el tamaño de la pantalla.
        Si no hay tamaño disponible, usa un valor predeterminado.
        """
        if window_width < 600:  # Móvil
            return self.mobile_view
        elif window_width < 1200:  # Tablet
            return self.tablet_view
        else:  # Escritorio
            return self.desktop_view
