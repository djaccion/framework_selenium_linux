import pytest

from pages.wikipedia_articulo_page import WikipediaArticuloPage


@pytest.mark.smoke
def test_prueba_26112026(driver):
    pagina = WikipediaArticuloPage(driver)
    pagina.abrir_url("https://es.wikipedia.org/wiki/Chile")

    pagina.ir_a_america_del_sur()
    pagina.esperar_encabezado("América del Sur")
    pagina.abrir_url("https://es.wikipedia.org/wiki/Am%C3%A9rica_del_Sur")

    pagina.ir_a_martin_waldseemuller()
    pagina.esperar_encabezado("Martin Waldseemüller")
    pagina.abrir_url("https://es.wikipedia.org/wiki/Martin_Waldseem%C3%BCller")

    pagina.ir_a_universalis_cosmographia()
    pagina.esperar_encabezado("Universalis Cosmographia")
    pagina.abrir_url("https://es.wikipedia.org/wiki/Universalis_Cosmographia")

    pagina.ir_a_alexander_von_humboldt()
    pagina.esperar_encabezado("Alexander von Humboldt")
    pagina.abrir_url("https://es.wikipedia.org/wiki/Alexander_von_Humboldt")

    assert pagina.texto_encabezado() == "Alexander von Humboldt"