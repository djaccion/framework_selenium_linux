"""Página base: esperas explícitas y acciones comunes.

Todas las páginas heredan de acá. La regla del framework es **nunca usar esperas
fijas** (`time.sleep`): siempre esperas explícitas sobre una condición, que es lo
que evita las pruebas inestables.
"""
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings


class BasePage:
    """Comportamiento común a todas las páginas."""

    # Cada página concreta define su ruta relativa (se une a base_url)
    ruta = "/"

    def __init__(self, driver):
        self.driver = driver
        self.espera = WebDriverWait(driver, settings.timeout)

    # --- navegación --------------------------------------------------------
    def abrir(self, ruta=None):
        destino = ruta if ruta is not None else self.ruta
        self.driver.get(settings.base_url.rstrip("/") + destino)
        return self

    @property
    def url_actual(self):
        return self.driver.current_url

    @property
    def titulo(self):
        return self.driver.title

    # --- consultas ---------------------------------------------------------
    def elemento(self, localizador):
        """Espera a que el elemento esté presente y lo devuelve."""
        return self.espera.until(EC.presence_of_element_located(localizador))

    def elemento_visible(self, localizador):
        return self.espera.until(EC.visibility_of_element_located(localizador))

    def elementos(self, localizador):
        self.espera.until(EC.presence_of_all_elements_located(localizador))
        return self.driver.find_elements(*localizador)

    def existe(self, localizador, timeout=3):
        """True si el elemento aparece dentro del tiempo indicado (no lanza)."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(localizador))
            return True
        except TimeoutException:
            return False

    def texto_de(self, localizador):
        return self.elemento_visible(localizador).text.strip()

    # --- acciones ----------------------------------------------------------
    def hacer_clic(self, localizador):
        self.espera.until(EC.element_to_be_clickable(localizador)).click()
        return self

    def escribir(self, localizador, texto, limpiar=True):
        campo = self.elemento_visible(localizador)
        if limpiar:
            campo.clear()
        campo.send_keys(texto)
        return self

    def esperar_texto(self, localizador, texto):
        """Espera a que el elemento contenga el texto indicado."""
        self.espera.until(EC.text_to_be_present_in_element(localizador, texto))
        return self

    def esperar_url_contiene(self, fragmento):
        self.espera.until(EC.url_contains(fragmento))
        return self
