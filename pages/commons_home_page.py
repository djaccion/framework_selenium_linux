"""Page Object de la portada de Wikimedia Commons (sitio de ejemplo).

Sirve como plantilla: los localizadores van como constantes de clase con la
prioridad del framework (id > name > css > xpath), y los métodos describen
acciones del usuario, no detalles técnicos.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.search_results_page import SearchResultsPage


class CommonsHomePage(BasePage):

    ruta = "/wiki/Main_Page"

    # Localizadores: preferir id/name; css como alternativa estable
    CAMPO_BUSQUEDA = (By.NAME, "search")
    BOTON_BUSCAR = (By.CSS_SELECTOR, "button.cdx-search-input__end-button")
    TITULO_PAGINA = (By.ID, "firstHeading")
    ENLACE_PORTADA = (By.CSS_SELECTOR, "#p-navigation a")

    def buscar(self, termino):
        """Escribe el término y confirma la búsqueda. Devuelve la página de resultados."""
        self.escribir(self.CAMPO_BUSQUEDA, termino)
        self.hacer_clic(self.BOTON_BUSCAR)
        return SearchResultsPage(self.driver)

    def titulo_principal(self):
        return self.texto_de(self.TITULO_PAGINA)
