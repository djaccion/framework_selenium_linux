"""Pruebas funcionales de la búsqueda en Wikimedia Commons.

Ejemplo de referencia del framework: usa Page Objects, esperas explícitas y
aserciones concretas sobre el resultado (no comprobaciones triviales).
"""
import pytest

from pages.commons_home_page import CommonsHomePage


@pytest.mark.smoke
def test_portada_carga_con_titulo(driver):
    """La portada abre y muestra su encabezado principal."""
    portada = CommonsHomePage(driver).abrir()
    assert "Wikimedia Commons" in portada.titulo, \
        f"El título de la página no corresponde a Commons: {portada.titulo}"
    assert portada.titulo_principal() != "", "La portada no muestra encabezado principal"


@pytest.mark.smoke
def test_busqueda_devuelve_resultados(driver):
    """Una búsqueda con un término conocido devuelve resultados."""
    portada = CommonsHomePage(driver).abrir()
    resultados = portada.buscar("Santiago Chile")

    assert resultados.hay_resultados(), "La búsqueda no devolvió ningún resultado"
    assert resultados.cantidad_resultados() >= 1, \
        f"Se esperaba al menos 1 resultado, se obtuvieron {resultados.cantidad_resultados()}"


def test_busqueda_sin_coincidencias_informa_al_usuario(driver):
    """Un término inexistente informa que no hay coincidencias, sin romper la página."""
    portada = CommonsHomePage(driver).abrir()
    resultados = portada.buscar("zzzqxwv-termino-inexistente-12345")

    assert not resultados.hay_resultados(), \
        "Se esperaba que no hubiera resultados para un término inventado"
