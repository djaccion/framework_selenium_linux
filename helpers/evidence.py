"""Evidencias de la ejecución: capturas de pantalla al fallar."""
import os
from datetime import datetime

from config.settings import settings


def guardar_captura(driver, nombre):
    """Guarda una captura y devuelve la ruta, o None si no se pudo."""
    try:
        os.makedirs(settings.evidence_dir, exist_ok=True)
        limpio = "".join(c if c.isalnum() or c in "-_" else "_" for c in nombre)[:80]
        ruta = os.path.join(settings.evidence_dir,
                            f"{datetime.now():%Y%m%d-%H%M%S}-{limpio}.png")
        driver.save_screenshot(ruta)
        return ruta
    except Exception as e:                       # la evidencia nunca debe romper el test
        print(f"No se pudo guardar la captura: {e}")
        return None
