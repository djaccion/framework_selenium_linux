"""Configuración por variables de entorno (sin credenciales en el repositorio)."""
import os


class Settings:
    """Toda la configuración se lee del entorno para poder cambiarla en el pipeline."""

    def __init__(self):
        self.base_url = os.getenv("AUTOMATION_BASE_URL", "https://commons.wikimedia.org")
        self.browser = os.getenv("AUTOMATION_BROWSER", "chrome")
        self.headless = os.getenv("AUTOMATION_HEADLESS", "true").lower() in ("1", "true", "si", "yes")
        self.timeout = int(os.getenv("AUTOMATION_TIMEOUT", "15"))
        self.page_load_timeout = int(os.getenv("AUTOMATION_PAGE_TIMEOUT", "45"))
        self.window_width = int(os.getenv("AUTOMATION_WIDTH", "1440"))
        self.window_height = int(os.getenv("AUTOMATION_HEIGHT", "900"))
        self.evidence_dir = os.getenv("AUTOMATION_EVIDENCE", "evidencias")
        # Rutas opcionales: si están vacías, Selenium Manager resuelve el driver
        self.chrome_binary = os.getenv("AUTOMATION_CHROME_BIN", "")
        self.chromedriver_path = os.getenv("AUTOMATION_CHROMEDRIVER", "")
        # Credenciales de prueba (nunca se escriben en el código)
        self.usuario = os.getenv("AUTOMATION_USER", "")
        self.clave = os.getenv("AUTOMATION_PASSWORD", "")


settings = Settings()
