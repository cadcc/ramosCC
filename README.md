# ramosCC
Proyecto para un catálogo detallado de los ramos, con scrapping del catálogo de cursos e información descriptiva agregada.

## Estructura
La idea es usar el código en python para la automatización de la información ya disponible en el [catálogo de cursos](https://ucampus.uchile.cl/m/fcfm_catalogo/), por lo que 'mkejson.py' extrae la información del catalogo de cursos y la guarda en 'scrapeRamos.json'

Por otra parte, habrá información editada manualmente, la cual está almacenada en 'infoRamos.json', esta consiste en aquellas cosas que no son scrapeables, tales como la descripción del ramo y las etiquetas con las cuales identificaremos las categorías a las que corresponde cada ramo.

## Como usar "mkejson.py"
Desde una terminal basta con correr "python mkejson.py" para generar "scrapeRamos.json" con la información actualizada de los últimos 6 semestres (esto está harcodeado en el código, por lo que se tiene que actualizar).

El código tambien incluye un modo de uso "description" el cual genera un template para rellenar con información a mano. NO USAR ESTE COMANDO A MENOS DE QUE SEPAS LO QUE HACES, la idea de este es usarlo solo cuando hayan ramos nuevos en un semestre, por lo que usarlo solo sobreesciribirá la información que ya llevemos ingresada manualmente. El comando es "python mkejson.py True", y la idea es no usarlo, solo una vez por semestre :)
