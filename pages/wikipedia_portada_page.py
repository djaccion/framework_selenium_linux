import pytest
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class WikipediaPortadaPage(BasePage):
    ruta = "/wiki/Wikipedia:Portada"
    # El título visible de la sección "Actualidad"
    SECCION_ACTUALIDAD = (By.CSS_SELECTOR, "#Actualidad")  # h2 que contiene el título de la sección
    # El bloque visual contenedor de las noticias de actualidad
    CUERPO_ACTUALIDAD = (By.CSS_SELECTOR, "#main-cur")
    # Las noticias (items) dentro del bloque actualidad
    ITEMS_NOTICIAS = (By.CSS_SELECTOR, "#main-cur ul > li")

    def existe_seccion_actualidad(self):
        return self.existe(self.SECCION_ACTUALIDAD, timeout=4)

    def texto_seccion_actualidad(self):
        return self.texto_de(self.SECCION_ACTUALIDAD)

    def existe_bloque_actualidad(self):
        return self.existe(self.CUERPO_ACTUALIDAD, timeout=4)

    def noticias_actualidad(self):
        if not self.existe_bloque_actualidad():
            return []
        return self.elementos(self.ITEMS_NOTICIAS)

    def textos_noticias_actualidad(self):
        return [e.text.strip() for e in self.noticias_actualidad() if e.text.strip()]
