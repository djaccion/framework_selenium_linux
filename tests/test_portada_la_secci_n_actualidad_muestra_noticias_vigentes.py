import pytest
from pages.wikipedia_portada_page import WikipediaPortadaPage

@pytest.mark.smoke
def test_portada_la_seccion_actualidad_muestra_noticias_vigentes(driver):
    """
    Verifica que en la portada de Wikipedia en español, la sección 'Actualidad'
    esté visible, sea identificable por su encabezado y contenga un listado de
    noticias vigentes (con al menos un ítem no vacío).
    """
    pagina = WikipediaPortadaPage(driver).abrir()

    # 1. La sección debe estar presente e identificada por su encabezado
    assert pagina.existe_seccion_actualidad(), "No existe la sección 'Actualidad' en la portada."
    texto_encabezado = pagina.texto_seccion_actualidad().lower()
    assert "actualidad" in texto_encabezado, f"El encabezado de la sección no contiene 'Actualidad' (actual: '{texto_encabezado}')"

    # 2. El bloque debe estar presente
    assert pagina.existe_bloque_actualidad(), "No se halló el bloque de noticias de actualidad en la portada."

    # 3. Debe haber al menos una noticia visible/no vacía
    noticias = pagina.textos_noticias_actualidad()
    assert noticias, "La sección 'Actualidad' no muestra ninguna noticia."

    # 4. Cada noticia debe tener texto
    for idx, noticia in enumerate(noticias, 1):
        assert noticia.strip(), f"La noticia {idx} de Actualidad está vacía."