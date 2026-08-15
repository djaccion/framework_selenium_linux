"""Page Object de la portada de Wikimedia Commons (sitio de ejemplo).

Sirve como plantilla: los localizadores van como constantes de clase con la
prioridad del framework (id > name > css > xpath), y los métodos describen
acciones del usuario, no detalles técnicos.
"""
from urllib.parse import quote_plus

from selenium.webdriver.common.by import By

from config.settings import settings
from pages.base_page import BasePage
from pages.search_results_page import SearchResultsPage


class CommonsHomePage(BasePage):

    ruta = "/wiki/Main_Page"

    # El encabezado #firstHeading existe en la portada pero está OCULTO por estilos:
    # se verifica el contenido, que sí es visible.
    CONTENIDO = (By.ID, "mw-content-text")
    CAMPO_BUSQUEDA = (By.NAME, "search")
    LOGO = (By.CSS_SELECTOR, ".mw-logo, #p-logo")

    def texto_contenido(self):
        return self.texto_de(self.CONTENIDO)

    def logo_visible(self):
        return self.existe(self.LOGO, timeout=5)

    def buscar(self, termino):
        """Ejecuta la búsqueda y devuelve la página de resultados.

        Se usa la búsqueda clásica (`/w/index.php?search=`) en lugar del botón de
        la cabecera: ese botón deriva a `Special:MediaSearch`, una aplicación Vue
        cuyo marcado cambia seguido y no da resultados estables para verificar.
        """
        self.escribir(self.CAMPO_BUSQUEDA, termino)
        destino = "/w/index.php?search=" + quote_plus(termino)
        self.driver.get(settings.base_url.rstrip("/") + destino)
        return SearchResultsPage(self.driver)
