"""Page Object de la página de resultados de búsqueda."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SearchResultsPage(BasePage):

    ruta = "/w/index.php?search="

    TITULO_PAGINA = (By.ID, "firstHeading")
    RESULTADOS = (By.CSS_SELECTOR, ".mw-search-result-heading a, .searchresults .mw-search-result a")
    SIN_RESULTADOS = (By.CSS_SELECTOR, ".mw-search-nonefound")
    CAMPO_BUSQUEDA = (By.NAME, "search")

    def hay_resultados(self):
        """True si la búsqueda devolvió al menos un resultado."""
        if self.existe(self.SIN_RESULTADOS, timeout=3):
            return False
        return len(self.driver.find_elements(*self.RESULTADOS)) > 0

    def cantidad_resultados(self):
        return len(self.driver.find_elements(*self.RESULTADOS))

    def titulos_resultados(self):
        return [e.text.strip() for e in self.driver.find_elements(*self.RESULTADOS) if e.text.strip()]

    def abrir_primer_resultado(self):
        self.elemento_visible(self.RESULTADOS).click()
        return self
