import io
import threading
import contextlib

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from sipi_motor import Interprete

NOMBRE_PROGRAMA = "generar_apps.sipi"


class PantallaPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.salida = Label(
            text="Toca 'Ejecutar programa' para correr MiPrimeraApp.",
            size_hint_y=None, halign="left", valign="top", font_size=16,
        )
        self.salida.bind(width=lambda *a: self.salida.setter("text_size")(self.salida, (self.salida.width, None)))
        self.salida.bind(texture_size=lambda *a: self.salida.setter("height")(self.salida, self.salida.texture_size[1]))

        scroll = ScrollView()
        scroll.add_widget(self.salida)
        self.add_widget(scroll)

        boton = Button(text="Ejecutar programa", size_hint_y=None, height=60, font_size=20)
        boton.bind(on_press=self.al_presionar)
        self.add_widget(boton)

    def al_presionar(self, instancia):
        self.salida.text = "Ejecutando..."
        hilo = threading.Thread(target=self._correr_programa, daemon=True)
        hilo.start()

    def _correr_programa(self):
        buffer_salida = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer_salida):
                interprete = Interprete(NOMBRE_PROGRAMA)
                interprete.ejecutar()
            texto = buffer_salida.getvalue() or "(El programa no imprimio nada con 'decir'.)"
        except Exception as e:
            texto = buffer_salida.getvalue() + f"\n[Error al ejecutar el programa]\n{e}"
        Clock.schedule_once(lambda dt: setattr(self.salida, "text", texto))


class MiPrimeraAppApp(App):
    def build(self):
        self.title = "MiPrimeraApp"
        return PantallaPrincipal()


if __name__ == "__main__":
    MiPrimeraAppApp().run()
