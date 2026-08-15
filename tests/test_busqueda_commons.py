"""Pruebas funcionales de la búsqueda en Wikimedia Commons.

Ejemplo de referencia del framework: usa Page Objects, esperas explícitas y
aserciones concretas sobre el resultado (no comprobaciones triviales).
"""
import pytest

from pages.commons_home_page import CommonsHomePage


@pytest.mark.smoke
def test_portada_carga_con_contenido(driver):
    """La portada abre, tiene el título del sitio y muestra su contenido."""
    portada = CommonsHomePage(driver).abrir()

    assert "Wikimedia Commons" in portada.titulo, \
        f"El título de la página no corresponde a Commons: {portada.titulo}"
    assert "Wikimedia Commons" in portada.texto_contenido(), \
        "La portada no muestra el contenido esperado"
    assert portada.logo_visible(), "No se muestra el logo del sitio"


@pytest.mark.smoke
def test_busqueda_devuelve_resultados(driver):
    """Una búsqueda con un término conocido devuelve resultados listados."""
    portada = CommonsHomePage(driver).abrir()

    resultados = portada.buscar("Santiago Chile")

    assert resultados.titulo_resultados() == "Search results", \
        f"No se llegó a la página de resultados: {resultados.titulo_resultados()}"
    assert resultados.cantidad_resultados() >= 1, \
        f"Se esperaba al menos 1 resultado, se obtuvieron {resultados.cantidad_resultados()}"
    assert len(resultados.titulos_resultados()) >= 1, \
        "Los resultados no muestran títulos"


def test_busqueda_sin_coincidencias_informa_al_usuario(driver):
    """Un término inexistente no devuelve resultados e informa al usuario."""
    portada = CommonsHomePage(driver).abrir()

    resultados = portada.buscar("zzzqxwv-termino-inexistente-12345")

    assert resultados.cantidad_resultados() == 0, \
        f"Se esperaban 0 resultados, se obtuvieron {resultados.cantidad_resultados()}"
    assert resultados.sin_coincidencias(), \
        "La página no informa que no hubo coincidencias"
