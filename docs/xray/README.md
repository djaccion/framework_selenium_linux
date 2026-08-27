# Batería de pruebas · Regresión Wikipedia ES

Casos de prueba manuales del proyecto **Tsoft Global Chile**, listos para importar
en cualquier instancia de Xray. Se versionan aquí para que la batería pueda
recrearse en otro ambiente sin rehacerla a mano.

| | |
|---|---|
| Sistema bajo prueba | `https://es.wikipedia.org` |
| Framework | Selenium · Python · pytest |
| Casos | 19 |
| Pasos | 135 |
| Origen | Proyecto `XT` de Xray Cloud |

## Archivos

| Archivo | Para qué sirve |
|---|---|
| `bateria_wikipedia.csv` | Formato del **Test Case Importer** de Xray. Es el que se sube. |
| `bateria_wikipedia.json` | La batería completa con criterios de aceptación y notas de automatización. Fuente de verdad para revisar o regenerar el CSV. |

El CSV lleva **una fila por paso**. Los campos del caso (resumen, descripción,
prioridad, etiquetas) van solo en la primera fila de cada caso; el importador
agrupa las filas por la columna `TCID`. El archivo está en UTF-8 con BOM, que es
lo que espera el importador para no romper las tildes.

## Cómo importar en Xray Cloud

1. En Jira, abrí el proyecto destino → **Xray** → *Test Case Importer*.
2. Subí `bateria_wikipedia.csv`.
3. En el mapeo de columnas:
   - `TCID` → *Test Case Identifier*
   - `Summary` → *Summary*
   - `Description` → *Description*
   - `Test Type` → *Test Type*
   - `Priority` → *Priority*
   - `Labels` → *Labels* (separador `;`)
   - `Action` / `Data` / `Result` → los tres campos del paso manual
4. Confirmá la previsualización y ejecutá la importación.

Las columnas `Precondition` y `Folder` van como referencia. El importador no
crea precondiciones ni carpetas: si el ambiente destino las necesita, hay que
crearlas antes y asociarlas después.

## Cómo está organizada

Los casos se agrupan de dos formas, que responden preguntas distintas:

**Carpetas del Test Repository** — por área funcional. Un caso vive en una sola.

```
/Wikipedia/Busqueda
/Wikipedia/Navegacion
/Wikipedia/Contenido del articulo
/Wikipedia/Preferencias e idioma
```

**Test Sets** — por propósito, cruzando las carpetas. Un caso puede estar en varios.
Smoke · Internacionalización · Accesibilidad · Contenido variable · Casos negativos.

## Criterio con el que están escritos

Cada paso dice **qué** hacer, **con qué dato** y **cómo** se sabe que salió bien.
Un resultado esperado sirve si dos personas distintas lo marcan igual sin discutir;
por eso se nombran URLs, encabezados y textos concretos en lugar de «se muestra
correctamente».

Cada caso declara además **qué NO cubre**. El alcance que no se escribe se
termina discutiendo cuando aparece un defecto.

### Casos con contenido variable

Cuatro casos (`Artículo aleatorio`, `Actualidad`, `Historial`, `Cambios recientes`)
trabajan sobre contenido que cambia entre ejecuciones. Están agrupados en el Test
Set *Contenido variable* y sus notas lo dicen de forma explícita: **validan
estructura y vigencia, nunca un valor concreto**.

No es una recomendación teórica. Uno de estos scripts se generó con una aserción
sobre un titular de portada y falló al día siguiente, cuando la noticia cambió.
Es el primer lugar donde mirar cuando un script se vuelve intermitente.

### Casos de mayor riesgo

- **Tildes y ñ** — la URL viaja codificada (`Jos%C3%A9`). Compararla en crudo
  contra el texto acentuado produce un falso negativo. Hay que decodificar antes.
- **Accesibilidad por teclado** — un sitio puede pasar todas las demás pruebas y
  ser inutilizable sin ratón. El foco tiene que **verse**.
- **Cambio de idioma** — cruza dos dominios. En redes corporativas es habitual que
  el proxy permita uno y bloquee el otro; eso se manifiesta como fallo del caso
  sin que haya defecto.

## Regenerar el CSV

El JSON es la fuente de verdad. Si se editan casos en Xray, conviene volver a
exportar desde ahí en lugar de editar el CSV a mano: un export que sale del
guion original deja de reflejar la realidad en cuanto alguien toca algo.
