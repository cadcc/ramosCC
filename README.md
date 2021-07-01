# ramosCC
Proyecto para un catálogo detallado de los ramos, con scrapping del catálogo de cursos e información descriptiva agregada.

## Estructura
La idea es usar el código en python para la automatización de la información ya disponible en el [catálogo de cursos](https://ucampus.uchile.cl/m/fcfm_catalogo/), por lo que 'mkejson.py' extrae la información del catalogo de cursos y la guarda en 'scrapeRamos.json'

Por otra parte, habrá información editada manualmente, la cual está almacenada en 'infoRamos.json', esta consiste en aquellas cosas que no son scrapeables, tales como la descripción del ramo y las etiquetas con las cuales identificaremos las categorías a las que corresponde cada ramo.
