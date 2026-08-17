"""Configuración de pytest a nivel raíz: evidencia paso a paso.

Vive acá y no en `tests/` porque instrumenta Selenium antes de que cualquier prueba
se ejecute. El fixture del navegador sigue estando en `tests/conftest.py`.

Se desactiva con `AUTOMATION_PASOS=false` para suites largas donde el disco y el
tiempo de las capturas pesan más que la evidencia.
"""
import os

import pytest

from helpers import informe, pasos

CARPETA_REPORTES = os.getenv("AUTOMATION_REPORTES", "reportes")


def pytest_configure(config):
    pasos.instrumentar()


@pytest.fixture(autouse=True)
def _pasos_del_caso():
    """Los pasos son de un caso, no de la sesión: se limpian antes de cada prueba."""
    pasos.reiniciar()
    yield


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    reporte = yield
    resultado = reporte.get_result()
    if resultado.when != "call":
        return

    driver = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
    detalle = ""
    if resultado.failed:
        detalle = resultado.longreprtext or ""
        # Una captura del momento exacto del fallo: sin ella hay que deducir el estado
        # final leyendo el traceback.
        pasos.capturar(driver, "fallo", detalle[-140:])

    registrados = pasos.pasos()
    if not registrados:
        return

    pasos.volcar_manifiesto(item.name, resultado.outcome, resultado.duration)
    try:
        ruta = informe.escribir(item.name, resultado.outcome, resultado.duration,
                                registrados, CARPETA_REPORTES, detalle)
        print("\nInforme de la ejecución: %s" % ruta)
    except Exception as e:                       # noqa: BLE001 - nunca romper la corrida
        print("No se pudo generar el informe: %s" % e)
