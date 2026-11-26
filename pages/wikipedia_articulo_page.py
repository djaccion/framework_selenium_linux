"""Navegación entre artículos de Wikipedia en español."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class WikipediaArticuloPage(BasePage):
    ENCABEZADO = (By.ID, "firstHeading")
    AMERICA_DEL_SUR = (By.LINK_TEXT, "América del Sur")
    MARTIN_WALDSEEMULLER = (By.LINK_TEXT, "Martin Waldseemüller")
    UNIVERSALIS_COSMOGRAPHIA = (
        By.PARTIAL_LINK_TEXT,
        "Universalis Cosmographia secundum Ptholo",
    )
    ALEXANDER_VON_HUMBOLDT = (By.LINK_TEXT, "Alexander von Humboldt")

    def abrir_url(self, url):
        self.driver.get(url)
        return self

    def ir_a_america_del_sur(self):
        return self.hacer_clic(self.AMERICA_DEL_SUR)

    def ir_a_martin_waldseemuller(self):
        return self.hacer_clic(self.MARTIN_WALDSEEMULLER)

    def ir_a_universalis_cosmographia(self):
        return self.hacer_clic(self.UNIVERSALIS_COSMOGRAPHIA)

    def ir_a_alexander_von_humboldt(self):
        return self.hacer_clic(self.ALEXANDER_VON_HUMBOLDT)

    def esperar_encabezado(self, texto):
        return self.esperar_texto(self.ENCABEZADO, texto)

    def texto_encabezado(self):
        return self.texto_de(self.ENCABEZADO)
