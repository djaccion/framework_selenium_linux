"""Page Object de la página de resultados de búsqueda."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SearchResultsPage(BasePage):

    ruta = "/w/index.php?search="

    TITULO = (By.ID, "firstHeading")
    RESULTADOS = (By.CSS_SELECTOR, "li.mw-search-result")
    ENLACES_RESULTADO = (By.CSS_SELECTOR, "li.mw-search-result .mw-search-result-heading a")
    CONTENIDO = (By.ID, "mw-content-text")

    # Texto que muestra el sitio cuando la búsqueda no encuentra nada
    TEXTO_SIN_RESULTADOS = "no results matching"

    def titulo_resultados(self):
        """Encabezado de la página de resultados (visible, a diferencia de la portada)."""
        return self.texto_de(self.TITULO)

    def cantidad_resultados(self):
        return len(self.driver.find_elements(*self.RESULTADOS))

    def hay_resultados(self):
        return self.cantidad_resultados() > 0

    def sin_coincidencias(self):
        """True si el sitio informa explícitamente que no hubo coincidencias."""
        texto = self.texto_de(self.CONTENIDO).lower()
        return self.TEXTO_SIN_RESULTADOS in texto

    def titulos_resultados(self):
        return [e.text.strip() for e in self.driver.find_elements(*self.ENLACES_RESULTADO)
                if e.text.strip()]

    def abrir_primer_resultado(self):
        self.elemento_visible(self.ENLACES_RESULTADO).click()
        return self
