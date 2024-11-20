from kivy.uix.scrollview import ScrollView
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label.label import MDIcon
from kivy.metrics import dp
from logger import logger

# Componente reutilizable: Crear título
def create_title(text, font_style="H5", text_color=(0.2, 0.8, 0.6, 1)):
    return MDLabel(
        text=text,
        size_hint=(1, None),
        height=dp(50),
        halign="center",
        font_style=font_style,
        theme_text_color="Custom",
        text_color=text_color,
    )

# Componente reutilizable: Crear formulario
def create_contact_form():
    form_layout = MDGridLayout(
        cols=2, adaptive_height=True, padding=dp(10), spacing=dp(10)
    )
    form_layout.add_widget(MDTextField(hint_text="Su nombre", size_hint=(1, None), height=dp(40)))
    form_layout.add_widget(MDTextField(hint_text="Su correo", size_hint=(1, None), height=dp(40)))
    form_layout.add_widget(MDTextField(hint_text="Teléfono", size_hint=(1, None), height=dp(40)))
    form_layout.add_widget(MDTextField(hint_text="Asunto", size_hint=(1, None), height=dp(40)))
    form_layout.add_widget(
        MDTextField(
            hint_text="Mensaje",
            multiline=True,
            size_hint=(1, None),
            height=dp(100),
        )
    )
    return form_layout

# Componente reutilizable: Crear tarjeta informativa
def create_info_card(title, description, icon):
    card = MDCard(
        orientation="vertical",
        padding=dp(10),
        size_hint=(None, None),
        size=(dp(300), dp(150)),
        md_bg_color=(0.9, 0.9, 0.9, 1),
    )
    layout = MDBoxLayout(orientation="vertical", spacing=dp(10))
    layout.add_widget(
        MDIcon(icon=icon, halign="center", theme_text_color="Custom", text_color=(0.2, 0.4, 1, 1))
    )
    layout.add_widget(MDLabel(text=title, font_style="H6", halign="center"))
    layout.add_widget(MDLabel(text=description, halign="center"))
    card.add_widget(layout)
    return card

# Vista móvil para contacto
class MobileContactoView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll = ScrollView()
        layout = MDBoxLayout(orientation="vertical", spacing=dp(20), padding=[dp(20), dp(20), dp(20), dp(10)], size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))

        layout.add_widget(create_title("Contactar"))

        # Información de contacto
        contact_info = MDBoxLayout(orientation="vertical", spacing=dp(10), size_hint=(1, None))
        contact_info.add_widget(MDLabel(text="Correo electrónico: huellas@fi.uba.ar", halign="left"))
        contact_info.add_widget(MDLabel(text="WhatsApp: +54 222 111 333", halign="left"))
        layout.add_widget(contact_info)

        # Formulario de contacto
        layout.add_widget(create_contact_form())

        # Botón de enviar mensaje
        layout.add_widget(
            MDRaisedButton(
                text="Enviar mensaje",
                size_hint=(None, None),
                size=(dp(200), dp(40)),
                md_bg_color=(0.91, 0.64, 0.45, 1),
                pos_hint={"center_x": 0.5},
            )
        )

        # Tarjetas informativas
        cards_layout = MDGridLayout(cols=1, adaptive_height=True, spacing=dp(10))
        cards_layout.add_widget(create_info_card("Campañas", "Cronograma de campañas sociales y de adopción para mascotas.", "account-group"))
        cards_layout.add_widget(create_info_card("Vacunación", "Consulta al veterinario para desparasitar y vacunar a tu mascota.", "needle"))
        cards_layout.add_widget(create_info_card("Cuidado", "Consejos útiles para el cuidado de tu mascota.", "heart"))
        layout.add_widget(cards_layout)

        scroll.add_widget(layout)
        self.add_widget(scroll)

# Vista responsiva para contacto
class ResponsiveContactoView(MDResponsiveLayout, MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mobile_view = MobileContactoView()
        self.tablet_view = self.mobile_view  # Reusar para simplificar
        self.desktop_view = self.mobile_view  # Reusar para simplificar

    def get_current_view(self, window_width=800):
        if window_width < 600:
            return self.mobile_view
        elif window_width < 1200:
            return self.tablet_view
        else:
            return self.desktop_view
