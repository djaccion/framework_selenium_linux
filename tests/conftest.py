"""Fixtures compartidas por todas las pruebas."""
import pytest

from config.settings import settings
from helpers.driver_factory import crear_driver
from helpers.evidence import guardar_captura


@pytest.fixture(scope="function")
def driver(request):
    """Un navegador por prueba. Si la prueba falla, se guarda una captura."""
    navegador = crear_driver()
    yield navegador
    try:
        reporte = getattr(request.node, "reporte_call", None)
        if reporte is not None and reporte.failed:
            ruta = guardar_captura(navegador, request.node.name)
            if ruta:
                print(f"\nEvidencia del fallo: {ruta}")
    finally:
        navegador.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Expone el resultado de la prueba a las fixtures (para la evidencia)."""
    salida = yield
    reporte = salida.get_result()
    if reporte.when == "call":
        item.reporte_call = reporte


@pytest.fixture(scope="session")
def base_url():
    return settings.base_url
