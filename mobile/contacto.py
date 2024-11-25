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

from solicitudes import contacto  # Importar el endpoint


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

    form_fields = {
        "nombre": MDTextField(hint_text="Su nombre", size_hint=(1, None), height=dp(40)),
        "email": MDTextField(hint_text="Su correo", size_hint=(1, None), height=dp(40)),
        "telefono": MDTextField(hint_text="Teléfono", size_hint=(1, None), height=dp(40)),
        "asunto": MDTextField(hint_text="Asunto", size_hint=(1, None), height=dp(40)),
        "mensaje": MDTextField(
            hint_text="Mensaje",
            multiline=True,
            size_hint=(1, None),
            height=dp(100),
        ),
    }

    for field in form_fields.values():
        form_layout.add_widget(field)

    return form_layout, form_fields


# Vista móvil para contacto
class MobileContactoView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contact_form, self.form_fields = create_contact_form()
        scroll = ScrollView()
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=[dp(20), dp(20), dp(20), dp(10)],
            size_hint_y=None,
        )
        layout.bind(minimum_height=layout.setter("height"))

        layout.add_widget(create_title("Contactar"))

        # Información de contacto
        contact_info = MDBoxLayout(orientation="vertical", spacing=dp(10), size_hint=(1, None))
        contact_info.add_widget(MDLabel(text="Correo electrónico: huellas@fi.uba.ar", halign="left"))
        contact_info.add_widget(MDLabel(text="WhatsApp: +54 222 111 333", halign="left"))
        layout.add_widget(contact_info)

        # Formulario de contacto
        layout.add_widget(self.contact_form)

        # Botón de enviar mensaje
        layout.add_widget(
            MDRaisedButton(
                text="Enviar mensaje",
                size_hint=(None, None),
                size=(dp(200), dp(40)),
                md_bg_color=(0.91, 0.64, 0.45, 1),
                pos_hint={"center_x": 0.5},
                on_release=self.submit_contact_form,
            )
        )

        scroll.add_widget(layout)
        self.add_widget(scroll)

    def submit_contact_form(self, *args):
        """
        Envía los datos del formulario al backend.
        """
        data = {
            "nombre": self.form_fields["nombre"].text.strip(),
            "email": self.form_fields["email"].text.strip(),
            "telefono": self.form_fields["telefono"].text.strip(),
            "asunto": self.form_fields["asunto"].text.strip(),
            "mensaje": self.form_fields["mensaje"].text.strip(),
        }

        if not self.validate_form(data):
            logger.error("Errores en el formulario, por favor corríjalos.")
            return

        logger.info("Enviando datos del formulario al servidor...")
        contacto(data, self.handle_contact_response)

    def validate_form(self, data):
        """
        Valida los datos del formulario antes de enviarlos.
        """
        valid = True

        for key, value in data.items():
            field = self.form_fields[key]
            if not value:
                field.helper_text = "Este campo es obligatorio."
                field.helper_text_mode = "on_error"
                field.error = True
                valid = False
            else:
                field.helper_text = ""
                field.error = False

        return valid

    def handle_contact_response(self, response):
        """
        Maneja la respuesta del servidor tras enviar el formulario.
        """
        if response.get("success", False):
            logger.info("Mensaje enviado con éxito.")
            self.reset_form()
        else:
            logger.error(f"Error al enviar el mensaje: {response.get('error', 'Desconocido')}.")
            self.highlight_errors(response.get("details", {}))

    def reset_form(self):
        """
        Resetea el formulario después de un envío exitoso.
        """
        for field in self.form_fields.values():
            field.text = ""
            field.helper_text = ""
            field.error = False

    def highlight_errors(self, errors):
        """
        Resalta los campos específicos con errores proporcionados por el servidor.
        """
        for key, message in errors.items():
            if key in self.form_fields:
                field = self.form_fields[key]
                field.helper_text = message
                field.helper_text_mode = "on_error"
                field.error = True


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
