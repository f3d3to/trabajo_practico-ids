# Ajuste del ResponsivePreguntasView y vistas específicas
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.metrics import dp
from logger import logger


# Reutilizable: Crear título
def create_title(text, font_style="H5", text_color=(0.2, 0.8, 0.6, 1)):
    return MDLabel(
        text=text,
        halign="center",
        font_style=font_style,
        theme_text_color="Custom",
        text_color=text_color,
        size_hint=(1, None),
        height=dp(50)
    )


# Reutilizable: Crear preguntas expandibles
def create_expandable_question(question_text, answer_text):
    return MDExpansionPanel(
        content=MDLabel(
            text=answer_text,
            size_hint_y=None,
            valign="top",
            halign="left",
            height=dp(80)
        ),
        panel_cls=MDExpansionPanelOneLine(text=question_text),
    )


# Vista móvil
class MobilePreguntasView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", spacing=dp(10), padding=dp(15))
        layout.add_widget(create_title("Preguntas Frecuentes", font_style="H6"))

        # Preguntas
        layout.add_widget(create_expandable_question(
            "¿Cómo agrego una mascota perdida?",
            "Puedes agregar una mascota perdida desde la sección 'Cargar Mascota'."
        ))
        layout.add_widget(create_expandable_question(
            "¿Cómo elimino una publicación?",
            "Para eliminar una publicación, dirígete a 'Mis Publicaciones'."
        ))
        layout.add_widget(create_expandable_question(
            "¿Puedo editar los datos de mi publicación?",
            "Puedes editar los datos desde 'Mis Publicaciones'."
        ))

        self.add_widget(layout)


# Vista tablet
class TabletPreguntasView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", spacing=dp(20), padding=dp(30))
        layout.add_widget(create_title("Preguntas Frecuentes", font_style="H5"))

        # Preguntas
        layout.add_widget(create_expandable_question(
            "¿Cómo agrego una mascota perdida?",
            "Puedes agregar una mascota perdida desde la sección 'Cargar Mascota'."
        ))
        layout.add_widget(create_expandable_question(
            "¿Cómo elimino una publicación?",
            "Para eliminar una publicación, dirígete a 'Mis Publicaciones'."
        ))
        layout.add_widget(create_expandable_question(
            "¿Puedo editar los datos de mi publicación?",
            "Puedes editar los datos desde 'Mis Publicaciones'."
        ))

        self.add_widget(layout)


# Vista escritorio
class DesktopPreguntasView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", spacing=dp(30), padding=dp(40))
        layout.add_widget(create_title("Preguntas Frecuentes", font_style="H4"))

        # Preguntas
        layout.add_widget(create_expandable_question(
            "¿Cómo agrego una mascota perdida?",
            "Puedes agregar una mascota perdida desde la sección 'Cargar Mascota'."
        ))
        layout.add_widget(create_expandable_question(
            "¿Cómo elimino una publicación?",
            "Para eliminar una publicación, dirígete a 'Mis Publicaciones'."
        ))
        layout.add_widget(create_expandable_question(
            "¿Puedo editar los datos de mi publicación?",
            "Puedes editar los datos desde 'Mis Publicaciones'."
        ))

        self.add_widget(layout)


# Vista responsiva
class ResponsivePreguntasView(MDResponsiveLayout, MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mobile_view = MobilePreguntasView()
        self.tablet_view = TabletPreguntasView()
        self.desktop_view = DesktopPreguntasView()

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

