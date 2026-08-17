"""Evidencia paso a paso de la ejecución.

Una captura al fallar dice *que* algo se rompió, pero no *cómo se llegó* ahí. Este
módulo envuelve las operaciones de Selenium que representan una acción real del
usuario —navegar, hacer clic, escribir— y guarda una captura de cada una junto con
el rótulo del elemento y la URL resultante.

Se activa desde `conftest.py`. Es opcional: con `AUTOMATION_PASOS=false` no se
instrumenta nada, útil en suites de regresión largas donde el disco importa.
"""
import json
import os
import time

_PASOS = []
_ACTIVO = False
_DIR = os.path.join(os.getenv("AUTOMATION_EVIDENCE", "evidencias"), "pasos")

ACCIONES = ("navegar", "clic", "escribir", "fallo")

# Cada captura pesa del orden de 200 KB y el informe las embebe: en una prueba larga
# el archivo se vuelve inmanejable. Pasado el tope se sigue ejecutando normalmente,
# solo se deja de capturar (el paso del fallo siempre se guarda).
MAXIMO = int(os.getenv("AUTOMATION_PASOS_MAX", "40"))


def activo():
    return os.getenv("AUTOMATION_PASOS", "true").lower() not in ("0", "false", "no")


def reiniciar():
    """Vacía la lista antes de cada caso: los pasos son de un test, no de la sesión."""
    del _PASOS[:]


def pasos():
    return list(_PASOS)


def capturar(driver, accion, detalle=""):
    """Guarda una captura del estado actual. Nunca lanza: la evidencia no debe romper la prueba."""
    if driver is None or not activo():
        return
    if accion != "fallo" and len(_PASOS) >= MAXIMO:
        return
    try:
        os.makedirs(_DIR, exist_ok=True)
        n = len(_PASOS) + 1
        archivo = os.path.join(_DIR, "paso-%03d.png" % n)
        driver.save_screenshot(archivo)
        _PASOS.append({
            "n": n,
            "accion": accion,
            "detalle": str(detalle)[:140],
            "url": (driver.current_url or "")[:300],
            "titulo": (driver.title or "")[:150],
            "archivo": archivo,
            "ts": time.time(),
        })
    except Exception as e:                       # noqa: BLE001 - nunca romper el test
        print("No se pudo capturar el paso: %s" % e)


def _rotulo(elemento):
    """Texto con el que un humano reconocería el elemento."""
    for obtener in (lambda: elemento.text,
                    lambda: elemento.get_attribute("aria-label"),
                    lambda: elemento.get_attribute("value"),
                    lambda: elemento.get_attribute("name"),
                    lambda: elemento.tag_name):
        try:
            valor = (obtener() or "").strip()
            if valor:
                return valor[:80]
        except Exception:
            continue
    return ""


def instrumentar():
    """Envuelve las acciones de Selenium. Idempotente: se puede llamar varias veces."""
    if not activo():
        return
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement

    global _ACTIVO
    if _ACTIVO:
        return
    _ACTIVO = True

    navegar_original = WebDriver.get

    def get(self, url):
        resultado = navegar_original(self, url)
        capturar(self, "navegar", url)
        return resultado

    WebDriver.get = get

    clic_original = WebElement.click

    def click(self):
        rotulo = _rotulo(self)
        resultado = clic_original(self)
        capturar(getattr(self, "_parent", None), "clic", rotulo)
        return resultado

    WebElement.click = click

    escribir_original = WebElement.send_keys

    def send_keys(self, *valores):
        resultado = escribir_original(self, *valores)
        capturar(getattr(self, "_parent", None), "escribir",
                 " ".join(str(v) for v in valores)[:60])
        return resultado

    WebElement.send_keys = send_keys


def volcar_manifiesto(caso, estado, duracion_s, destino=None):
    """Deja un JSON con los pasos del caso, junto a las capturas."""
    if not activo():
        return None
    try:
        ruta = destino or os.path.join(os.getenv("AUTOMATION_EVIDENCE", "evidencias"),
                                       "pasos.json")
        os.makedirs(os.path.dirname(ruta) or ".", exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump({"caso": caso, "estado": estado,
                       "duracion_s": round(duracion_s or 0, 2),
                       "pasos": _PASOS}, f, ensure_ascii=False, indent=1)
        return ruta
    except Exception as e:                       # noqa: BLE001
        print("No se pudo escribir el manifiesto de pasos: %s" % e)
        return None
