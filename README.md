# Framework Selenium para Linux — TSOFT

Framework de automatización de pruebas funcionales web, **preparado para correr en Linux**
(servidores y CI, sin entorno gráfico). Python + pytest + Selenium 4 con Page Objects.

## 1. Stack

| Componente | Detalle |
|---|---|
| Lenguaje | Python 3.10+ |
| Runner | pytest |
| Automatización | Selenium 4 (WebDriver) |
| Navegadores | Chrome/Chromium o Firefox, en modo headless |
| Drivers | **Selenium Manager** los resuelve solo: no se versionan binarios en el repo |
| Evidencias | Captura de pantalla automática al fallar |

## 2. Estructura de carpetas

```
config/     settings.py        configuración por variables de entorno
helpers/    driver_factory.py  construcción del WebDriver (chrome/firefox, headless)
            evidence.py        capturas de evidencia
pages/      base_page.py       esperas explícitas y acciones comunes
            *_page.py          un Page Object por pantalla
tests/      conftest.py        fixtures (driver, evidencia al fallar)
            test_*.py          las pruebas
```

**Una prueba nueva va en `tests/` con el nombre `test_<caso>.py`.**
Si necesita una pantalla nueva, se agrega su Page Object en `pages/`.

## 3. Instalación

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Se necesita Chrome/Chromium (o Firefox) instalado en la máquina. En Ubuntu/Debian:

```bash
sudo apt-get install -y chromium-browser        # o: google-chrome-stable / firefox
```

## 4. Ejecución

```bash
python3 -m pytest                                   # toda la suite
python3 -m pytest -m smoke                          # solo pruebas de humo
python3 -m pytest tests/test_busqueda_commons.py    # un archivo
python3 -m pytest tests/test_busqueda_commons.py::test_portada_carga_con_titulo   # una prueba
```

Con reporte HTML:

```bash
python3 -m pytest --html=reportes/reporte.html --self-contained-html
```

## 5. Configuración (variables de entorno)

Ninguna credencial vive en el código.

| Variable | Por defecto | Para qué |
|---|---|---|
| `AUTOMATION_BASE_URL` | `https://commons.wikimedia.org` | URL del sistema bajo prueba |
| `AUTOMATION_BROWSER` | `chrome` | `chrome` o `firefox` |
| `AUTOMATION_HEADLESS` | `true` | `false` para ver el navegador |
| `AUTOMATION_TIMEOUT` | `15` | Segundos de espera explícita |
| `AUTOMATION_WIDTH` / `AUTOMATION_HEIGHT` | `1440` / `900` | Tamaño de ventana |
| `AUTOMATION_EVIDENCE` | `evidencias` | Carpeta de capturas |
| `AUTOMATION_USER` / `AUTOMATION_PASSWORD` | vacío | Credenciales de prueba |
| `AUTOMATION_CHROME_BIN` | vacío | Ruta del navegador, si no está en el PATH |
| `AUTOMATION_CHROMEDRIVER` | vacío | Ruta del driver, si no se quiere Selenium Manager |

Ejemplo:

```bash
AUTOMATION_BASE_URL=https://mi-sistema.cl AUTOMATION_HEADLESS=true python3 -m pytest -m smoke
```

## 6. Convenciones

- **Archivos de prueba:** `test_<caso>.py`; funciones `test_<comportamiento>()` en español.
- **Page Objects:** `pages/<pantalla>_page.py`, clase en PascalCase terminada en `Page`.
- **Localizadores:** constantes de clase en MAYÚSCULAS, con esta prioridad:
  `By.ID` → `By.NAME` → `By.CSS_SELECTOR` → `By.XPATH` (último recurso).
- **Esperas:** siempre explícitas (`WebDriverWait`). **Nunca `time.sleep`.**
- **Aserciones:** toda prueba termina verificando un resultado concreto, con mensaje
  que explique el fallo. No se usan comprobaciones triviales del tipo "el elemento existe".
- Los métodos de los Page Objects describen acciones del usuario (`buscar`, `abrir`),
  no detalles técnicos.

## 7. Plantilla de una prueba nueva

```python
import pytest

from pages.commons_home_page import CommonsHomePage


@pytest.mark.smoke
def test_descripcion_del_comportamiento(driver):
    """Qué comprueba esta prueba, en una línea."""
    pagina = CommonsHomePage(driver).abrir()

    resultado = pagina.buscar("término")

    assert resultado.hay_resultados(), "La búsqueda no devolvió resultados"
```

## 8. Integración continua

El framework no requiere entorno gráfico ni drivers versionados, así que corre
directo en un agente Linux:

```yaml
# Ejemplo para un pipeline
- pip install -r requirements.txt
- pytest -m smoke --html=reportes/reporte.html --self-contained-html
```

---

Generado para probar la funcionalidad **Automation QA** del TSOFT AI Framework.
