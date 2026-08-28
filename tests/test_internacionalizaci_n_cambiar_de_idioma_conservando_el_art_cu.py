import pytest
from urllib.parse import unquote
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

# Page Object específico para Wikipedia ajustado según DOM real
class WikipediaArticuloPage(BasePage):
    TITULO_ARTICULO = (By.ID, "firstHeading")
    SELECTOR_IDIOMAS = (By.ID, "p-lang-btn")  # Botón para desplegar idiomas (por id)
    # El listado de idiomas está DENTRO del popup/modal tras hacer clic (ver COMPROBACION)
    # Sacamos el selector roto; el correcto es buscar <li> hijos del menú de idiomas
    LISTA_IDIOMAS = (By.CSS_SELECTOR, "#p-lang-btn + .vector-menu-content-lang li a")

    def selector_idiomas_visible(self):
        return self.existe(self.SELECTOR_IDIOMAS, timeout=5)

    def abrir_selector_idiomas(self):
        self.hacer_clic(self.SELECTOR_IDIOMAS)
        return self

    def cantidad_idiomas(self):
        # Abrir el menú para que se muestren los idiomas en DOM
        self.abrir_selector_idiomas()
        # Ahora el desplegable sí contiene los idiomas disponibles
        # Usamos el selector alternativo basado en estructura inspeccionada (hermanos inmediatos del p-lang-btn)
        return len(self.driver.find_elements(By.CSS_SELECTOR, "#p-lang-btn + .vector-menu-content-lang li a"))

    def elegir_idioma_ingles(self):
        # Abrir el selector si aún no
        self.abrir_selector_idiomas()
        # Buscar el enlace de idioma "English" (así como aparece visible)
        ingles_link = self.driver.find_element(By.XPATH, "//div[@id='p-lang-btn']/following-sibling::*//a[.='English']")
        ingles_link.click()
        return WikipediaArticuloPage(self.driver)

    def encabezado(self):
        return self.texto_de(self.TITULO_ARTICULO)

    def interfaz_esta_en_ingles(self):
        # Verifica que existan etiquetas UI típicas en la barra (solo en inglés)
        return (
            self.existe((By.LINK_TEXT, "Read")) and
            self.existe((By.LINK_TEXT, "Edit")) and
            self.existe((By.LINK_TEXT, "View history"))
        )

    def selector_idiomas_tiene_espanol(self):
        # En la versión EN, al abrir el selector debería estar el link 'Español'
        self.abrir_selector_idiomas()
        # Buscar entrada por texto visible 'Español', robusto
        # Usar la misma estrategia que para English (busca 'Español')
        return self.existe((By.XPATH, "//div[@id='p-lang-btn']/following-sibling::*//a[normalize-space(text())='Español']"))

@pytest.mark.smoke
def test_internacionalizacion_cambiar_de_idioma_conservando_el_articulo(driver):
    """
    Verifica que el cambio de idioma en Wikipedia conserva el tema;
    no aterriza en la portada sino en la versión del artículo en el idioma elegido.
    """
    url_inicial = "https://es.wikipedia.org/wiki/Chile"
    driver.get(url_inicial)
    pagina = WikipediaArticuloPage(driver)
    # Paso 1 + 2: selector visible y cantidad de idiomas > 0
    assert pagina.selector_idiomas_visible(), "El selector de idiomas no está visible."
    assert pagina.cantidad_idiomas() > 0, "El selector de idiomas indica 0 opciones."
    # Paso 3: abrir el selector de idiomas
    pagina.abrir_selector_idiomas()
    # Paso 4: elegir inglés
    pagina.elegir_idioma_ingles()
    # Paso 5: Verificar que se navega al dominio en.wikipedia y conserva el artículo
    url_destino = unquote(driver.current_url)
    assert url_destino.startswith("https://en.wikipedia.org/wiki/Chile"), \
        f"No se aterrizó en el artículo en inglés, URL: {url_destino}"
    # Paso 6: encabezado principal muestra "Chile" y la interfaz visible está en inglés
    assert pagina.encabezado().strip().lower() == "chile", \
        f"El encabezado no es 'Chile': {pagina.encabezado()}"
    assert pagina.interfaz_esta_en_ingles(), "La interfaz no está en inglés."
    # Paso 7: El selector de idiomas en inglés permite volver a Español
    assert pagina.selector_idiomas_tiene_espanol(), "No se ofrece volver a Español desde el artículo en inglés."