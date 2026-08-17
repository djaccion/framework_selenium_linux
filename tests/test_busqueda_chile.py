import pytest
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import unicodedata
from urllib.parse import urlparse, unquote

# ---- PageObjects ----

class WikipediaPortadaPage(BasePage):
    ruta = "/wiki/Wikipedia:Portada"
    # Selectores acorde a flujo.json y al criterio del contexto
    CAMPO_BUSQUEDA = (By.CSS_SELECTOR, '[aria-label="Buscar en Wikipedia"]')
    BOTON_BUSCAR = (By.CSS_SELECTOR, '#searchform > div.cdx-search-input > button.cdx-button')

    def buscar(self, termino):
        self.escribir(self.CAMPO_BUSQUEDA, termino)
        self.hacer_clic(self.BOTON_BUSCAR)
        return WikipediaResultadosPage(self.driver)

class WikipediaResultadosPage(BasePage):
    TITULO = (By.ID, "firstHeading")
    def titulo(self):
        return self.texto_de(self.TITULO)

# ------ TEST -------
@pytest.mark.smoke
def test_busqueda_chile(driver):
    """Verifica búsqueda de 'chile', navegación de anclas y links en Wikipedia ES."""
    # 1. Ir a portada
    portada = WikipediaPortadaPage(driver).abrir()
    assert "Wikipedia:Portada" in portada.url_actual
    # 2. Buscar "chile"
    resultados = portada.buscar("chile")
    # 3. Asegura que el título sea "Chile - Wikipedia, la enciclopedia libre" o contenga "Chile"
    assert "Chile" in resultados.titulo(), "No se llegó a la página de Chile"

    # 4. Navegar a sección Estado, gobierno y política
    # Selector directo con rol de TOC, text="Estado" (usar fragmento visible)
    link_estado = driver.find_element(By.PARTIAL_LINK_TEXT, "Estado")
    link_estado.click()
    # 5. Verifica que la URL tenga el anchor correcto
    assert "#Estado,_gobierno_y_pol%C3%ADtica" in driver.current_url

    # 6. Click a enlace 'Peso chileno' dentro de tabla (no hay id, usar xpath por contexto de flujo)
    link_peso = driver.find_element(By.LINK_TEXT, "Peso chileno")
    link_peso.click()

    # 7. Verifica que la URL es la del peso
    assert "/wiki/Peso_(moneda_de_Chile)" in driver.current_url
    
    # 8. Click en "José Miguel Carrera" (aparentemente id #mwAtw en esta versión)
    link_carrera = driver.find_element(By.ID, "mwAtw")
    link_carrera.click()
    # 9. Verifica llegamos a su biografía
    # --- Corrección: normalizar URL para quitar acentos antes de comparar ---
    url_path = urlparse(driver.current_url).path  # /wiki/Jos%C3%A9_Miguel_Carrera
    url_path_unquoted = unquote(url_path)         # /wiki/José_Miguel_Carrera
    def sin_acentos(txt):
        return ''.join(c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')
    assert "Jose_Miguel_Carrera" in sin_acentos(url_path_unquoted), "No se llegó al artículo de José Miguel Carrera"

    # 10. REVISAR: aserción sobre contenido, si hiciera falta aquí (por defecto, URL concreta)