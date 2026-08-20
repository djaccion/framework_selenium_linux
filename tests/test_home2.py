import pytest
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.search_results_page import SearchResultsPage

class WikipediaPortadaPage(BasePage):
    ruta = "/wiki/Wikipedia:Portada"
    CAMPO_BUSQUEDA = (By.CSS_SELECTOR, "[aria-label='Buscar en Wikipedia']")
    BOTON_BUSCAR = (By.CSS_SELECTOR, "#searchform > div.cdx-search-input > button.cdx-button")
    FORM_BUSQUEDA = (By.ID, "searchform")

    def buscar(self, termino):
        self.escribir(self.CAMPO_BUSQUEDA, termino)
        self.hacer_clic(self.BOTON_BUSCAR)
        return SearchResultsPage(self.driver)

class CarlosPenaPage(BasePage):
    # Se asume que la ruta es dinámica según el artículo, se trabaja directo sobre URL después de búsqueda
    TOC_TAMPA = (By.CSS_SELECTOR, "#toc-Tampa_Bay_Rays > a.vector-toc-link")
    TOC_DE_NUEVO_TAMPA = (By.CSS_SELECTOR, "#toc-De_nuevo_con_Tampa_Bay_Rays > a.vector-toc-link")
    TOC_SEGUNDA_OPORTUNIDAD = (By.CSS_SELECTOR, "#toc-Segunda_oportunidad_con_los_Rangers > a.vector-toc-link")
    MW_TW = (By.ID, "mwtw")

    def ir_a_tampa_bay(self):
        self.hacer_clic(self.TOC_TAMPA)
    def ir_de_nuevo_tampa(self):
        self.hacer_clic(self.TOC_DE_NUEVO_TAMPA)
    def ir_segunda_oportunidad(self):
        self.hacer_clic(self.TOC_SEGUNDA_OPORTUNIDAD)
    def ir_al_mwtw(self):
        self.hacer_clic(self.MW_TW)

@pytest.mark.smoke
def test_navegacion_wikipedia_home2(driver):
    """
    Reproduce el flujo de consulta, navegación y exploraciones internas sobre el artículo de Wikipedia.
    - Busca "Kevin Peña", navega por los resultados, y sigue enlaces de la tabla de contenidos.
    """
    # Paso 1: Ir a la portada
    portada = WikipediaPortadaPage(driver).abrir()

    # Paso 2: Escribir en búsqueda
    portada.escribir(WikipediaPortadaPage.CAMPO_BUSQUEDA, "Kevin Peña")

    # Paso 3: Hacer clic en botón Buscar
    portada.hacer_clic(WikipediaPortadaPage.BOTON_BUSCAR)

    # Paso 4: (Flujo grabado: submit al form) -- Lo consideramos implícito por el clic al botón
    # Paso 5: Esperar a que la URL cambie a resultados y asegurar que hay resultados
    resultados = SearchResultsPage(driver)
    assert resultados.hay_resultados(), "La búsqueda no devolvió resultados para 'Kevin Peña'"

    # Paso 6: Clic en el segundo resultado (CSS grabado)
    segundo = driver.find_elements(By.CSS_SELECTOR, "li.mw-search-result .mw-search-result-heading a")[1]
    segundo.click()

    # Paso 7: Ya en la página de Carlos Peña, seguir las anclas de la tabla de contenido en secuencia
    carlos = CarlosPenaPage(driver)

    # Paso 8: Clic en 'Tampa Bay Rays' dentro del TOC
    carlos.ir_a_tampa_bay()
    # Paso 9: Espera navegación anchor a #Tampa_Bay_Rays
    assert "#Tampa_Bay_Rays" in driver.current_url, "No se navegó correctamente a la sección 'Tampa Bay Rays'"

    # Paso 10: Clic en 'De nuevo con Tampa Bay Rays'
    carlos.ir_de_nuevo_tampa()
    # Paso 11: Espera navegación anchor
    assert "#De_nuevo_con_Tampa_Bay_Rays" in driver.current_url, "No se navegó correctamente a sección 'De nuevo con Tampa Bay Rays'"

    # Paso 12: Clic en 'Segunda oportunidad con los Rangers'
    carlos.ir_segunda_oportunidad()
    assert "#Segunda_oportunidad_con_los_Rangers" in driver.current_url, "No se navegó a sección 'Segunda oportunidad con los Rangers'"

    # Paso 13: Clic en el enlace externo destacado bajo la sección (mwtw)
    carlos.ir_al_mwtw()
    # Paso 14-15: El browser es dirigido a "chrome-error://chromewebdata/"
    # Esto es un error del entorno de automatización, no debe ser verificado como éxito.
    # Se verifica que después del clic se haya intentado navegar fuera de es.wikipedia.org
    assert not driver.current_url.startswith("https://es.wikipedia.org/"), "El clic a referencia externa no disparó navegación fuera de Wikipedia"