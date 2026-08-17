import pytest
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.search_results_page import SearchResultsPage

class WikipediaPortadaPage(BasePage):
    ruta = "/wiki/Wikipedia:Portada"
    ENLACE_1926 = (By.LINK_TEXT, "1926")
    ENLACE_3_DE_FEBRERO = (By.LINK_TEXT, "3 de febrero")
    CAMPO_BUSQUEDA = (By.CSS_SELECTOR, "[aria-label='Buscar en Wikipedia']")
    BOTON_BUSCAR = (By.CSS_SELECTOR, "#searchform > div.cdx-search-input > button.cdx-button")

    def click_enlace_1926(self):
        self.hacer_clic(self.ENLACE_1926)
        return WikipediaAnioPage(self.driver)

    def click_enlace_3_de_febrero(self):
        self.hacer_clic(self.ENLACE_3_DE_FEBRERO)
        return WikipediaFebreroPage(self.driver)

    def buscar(self, termino):
        self.escribir(self.CAMPO_BUSQUEDA, termino)
        self.hacer_clic(self.BOTON_BUSCAR)
        return SearchResultsPage(self.driver)

class WikipediaAnioPage(BasePage):
    # /wiki/1926
    ENLACE_3_DE_FEBRERO = (By.LINK_TEXT, "3 de febrero")
    def click_enlace_3_de_febrero(self):
        self.hacer_clic(self.ENLACE_3_DE_FEBRERO)
        return WikipediaFebreroPage(self.driver)

class WikipediaFebreroPage(BasePage):
    CAMPO_BUSQUEDA = (By.CSS_SELECTOR, "[aria-label='Buscar en Wikipedia']")
    BOTON_BUSCAR = (By.CSS_SELECTOR, "#searchform > div.cdx-search-input > button.cdx-button")

    def buscar(self, termino):
        self.escribir(self.CAMPO_BUSQUEDA, termino)
        self.hacer_clic(self.BOTON_BUSCAR)
        return SearchResultsPage(self.driver)

@pytest.mark.smoke
def test_navegacion_home(driver):
    """
    Verifica la navegación por enlaces históricos y búsqueda desde la portada de Wikipedia.
    """
    # Paso 1: ir a la portada
    pagina = WikipediaPortadaPage(driver).abrir("/wiki/Wikipedia:Portada")

    # Paso 2: click en enlace "1926"
    pagina_anio = pagina.click_enlace_1926()
    assert "1926" in driver.current_url, "No se navegó a la página del año 1926"

    # Paso 3: click en "3 de febrero" (en el año)
    pagina_febrero = pagina_anio.click_enlace_3_de_febrero()
    assert "3_de_febrero" in driver.current_url, "No se navegó a la fecha 3 de febrero"

    # Paso 4-7: buscar "miguel vivanco" desde esa página
    resultados = pagina_febrero.buscar("miguel vivanco")

    # Paso 8: aserción
    assert "miguel+vivanco" in driver.current_url, "La búsqueda de 'miguel vivanco' no redirigió correctamente"
    assert resultados.cantidad_resultados() > 0 or resultados.sin_coincidencias(), "No hay resultados ni advertencia por búsqueda sin coincidencias"