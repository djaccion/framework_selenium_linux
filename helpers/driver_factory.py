"""Construcción del WebDriver.

Pensado para Linux/CI: Selenium 4 trae **Selenium Manager**, que descarga y
resuelve el driver correcto automáticamente, así que no hay que versionar
chromedriver ni geckodriver en el repositorio.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.settings import settings


def _opciones_chrome():
    opciones = ChromeOptions()
    if settings.headless:
        opciones.add_argument("--headless=new")
    # Necesarios en contenedores y servidores sin entorno gráfico
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")
    opciones.add_argument("--disable-gpu")
    opciones.add_argument(f"--window-size={settings.window_width},{settings.window_height}")
    opciones.add_argument("--lang=es-ES")
    if settings.chrome_binary:
        opciones.binary_location = settings.chrome_binary
    return opciones


def _opciones_firefox():
    opciones = FirefoxOptions()
    if settings.headless:
        opciones.add_argument("-headless")
    opciones.add_argument(f"--width={settings.window_width}")
    opciones.add_argument(f"--height={settings.window_height}")
    return opciones


def crear_driver():
    """Devuelve un WebDriver listo, según AUTOMATION_BROWSER (chrome|firefox)."""
    navegador = settings.browser.lower()
    if navegador == "firefox":
        driver = webdriver.Firefox(options=_opciones_firefox())
    else:
        if settings.chromedriver_path:
            servicio = ChromeService(executable_path=settings.chromedriver_path)
            driver = webdriver.Chrome(service=servicio, options=_opciones_chrome())
        else:
            # Selenium Manager resuelve el driver automáticamente
            driver = webdriver.Chrome(options=_opciones_chrome())

    driver.set_page_load_timeout(settings.page_load_timeout)
    driver.implicitly_wait(0)      # se usan esperas explícitas, nunca implícitas
    return driver
