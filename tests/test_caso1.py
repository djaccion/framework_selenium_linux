import pytest
from selenium.webdriver.common.by import By
from urllib.parse import unquote

from pages.base_page import BasePage

class WikipediaPage(BasePage):
    ruta = "/wiki/Chile"

    # Selectores corregidos según el flujo grabado
    # Paso 1: click en "cordillera de los Andes"
    ANDES_LINK = (By.LINK_TEXT, "cordillera de los Andes")
    # Paso 2: click en "Cretácico tardío"
    CRETACICO_LINK = (By.LINK_TEXT, "Cretácico tardío")
    # Paso 3: click en "Mar interior occidental"
    MAR_INTERIOR_LINK = (By.LINK_TEXT, "Mar interior occidental")
    # Paso 4: click en categoría "Antiguos océanos" (ajuste: usar selector CSS, pues el heading incluye prefijo "Categoría:")
    CAT_ANTIGUOS_OCEANOS = (By.CSS_SELECTOR, "#mw-normal-catlinks > ul > li:nth-of-type(1) > a")
    
    def ir_a_cordillera_andes(self):
        self.hacer_clic(self.ANDES_LINK)
        return self

    def ir_a_cretacico_tardio(self):
        self.hacer_clic(self.CRETACICO_LINK)
        return self

    def ir_a_mar_interior(self):
        self.hacer_clic(self.MAR_INTERIOR_LINK)
        return self

    def ir_a_categoria_antiguos_oceanos(self):
        self.hacer_clic(self.CAT_ANTIGUOS_OCEANOS)
        return self

    def texto_en_heading(self):
        heading = (By.ID, "firstHeading")
        return self.texto_de(heading)

@pytest.mark.smoke
def test_caso1(driver, base_url):
    """
    1. Abrir la página https://es.wikipedia.org/wiki/Chile
    2. Click en enlace "cordillera de los Andes"
    3. Click en "Cretácico tardío"
    4. Click en "Mar interior occidental"
    5. Click en categoría "Antiguos océanos"
    Verificación: Encabezado de página dice "Categoría:Antiguos océanos"
    """
    
    pagina = WikipediaPage(driver).abrir()
    pagina.ir_a_cordillera_andes()
    pagina.ir_a_cretacico_tardio()
    pagina.ir_a_mar_interior()
    pagina.ir_a_categoria_antiguos_oceanos()
    
    # Verificamos el resultado: título en el "heading" de la página destino
    heading = pagina.texto_en_heading().strip().lower()
    assert heading == "categoría:antiguos océanos", f"El heading actual es: {heading}"