import pytest
from selenium.webdriver.common.by import By
from urllib.parse import unquote

from pages.base_page import BasePage

class WikipediaPortadaPage(BasePage):
    ruta = "/wiki/Wikipedia:Portada"
    CAMPO_BUSQUEDA = (By.CSS_SELECTOR, "[aria-label='Buscar en Wikipedia']")
    BOTON_BUSCAR = (By.CSS_SELECTOR, "#searchform > div.cdx-search-input > button.cdx-button")
    FORM_BUSQUEDA = (By.ID, "searchform")

    def buscar(self, termino):
        self.escribir(self.CAMPO_BUSQUEDA, termino)
        # botón Buscar
        self.hacer_clic(self.BOTON_BUSCAR)
        # Normalmente Wikipedia hace submit() luego de click, pero Selenium ejecuta nativo.
        # En el flujo se ve un submit, pero el click al botón generalmente lo hace.
        return WikipediaResultadoPage(self.driver)

class WikipediaResultadoPage(BasePage):
    # El encabezado de artículo de Wikipedia por id
    PRIMER_ENLACE_GENERO = (By.ID, "mwCQ")  # 'masculino' generalmente
    TITULO_ARTICULO = (By.ID, "firstHeading")

    def click_enlace_genero(self):
        self.hacer_clic(self.PRIMER_ENLACE_GENERO)
        return WikipediaMasculinoPage(self.driver)

    def titulo(self):
        return self.texto_de(self.TITULO_ARTICULO)

class WikipediaMasculinoPage(BasePage):
    ENLACE_VARON = (By.ID, "mwZw")  # Enlace "Varón"
    TITULO_ARTICULO = (By.ID, "firstHeading")

    def click_enlace_varon(self):
        self.hacer_clic(self.ENLACE_VARON)
        return WikipediaVaronPage(self.driver)

    def titulo(self):
        return self.texto_de(self.TITULO_ARTICULO)

class WikipediaVaronPage(BasePage):
    TITULO_ARTICULO = (By.ID, "firstHeading")

    def titulo(self):
        return self.texto_de(self.TITULO_ARTICULO)

@pytest.mark.smoke
def test_home_navegacion_generos(driver):
    """
    Verifica la navegación: portada -> buscar 'nahum' -> artículo 'Nahum' -> género 'masculino' -> artículo 'Varón'.
    """
    # Paso 1: ir a la portada principal
    portada = WikipediaPortadaPage(driver).abrir("/wiki/Wikipedia:Portada")

    # Paso 2: campo de búsqueda, escribir "nahum"
    # Paso 3: click en botón Buscar
    resultado = portada.buscar("nahum")
    
    # Paso 4: el flujo hace submit al form (post click); debería quedar en /wiki/Nahum
    resultado.esperar_url_contiene("/wiki/Nahum")

    # Paso 5: ya estamos en el artículo "Nahum". Click en enlace 'masculino' (id #mwCQ)
    pag_masculino = resultado.click_enlace_genero()
    pag_masculino.esperar_url_contiene("/wiki/Masculino")

    # Paso 6: click en enlace 'Varón' (id #mwZw)
    pag_varon = pag_masculino.click_enlace_varon()
    pag_varon.esperar_url_contiene("/wiki/Var%C3%B3n")

    # ASERCIONES de resultado:
    titulo = pag_varon.titulo()
    assert titulo.lower() == "varón", f"El título final debe ser 'Varón', se obtuvo: {titulo}"
    # Extra: comprobamos la URL decodificada
    assert "varón" in unquote(driver.current_url).lower(), "La URL final no corresponde a la esperada para el artículo 'Varón'"