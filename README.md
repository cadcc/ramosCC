# ramosCC
Proyecto para un catálogo detallado de los ramos, con scrapping del catálogo de cursos e información descriptiva
agregada por les alumnes.

## Estructura
Obtenemos datos desde una encuesta en Google Forms, la cual almacena los resultados en un libro de Excel. Este libro de
Excel es leído y genera, en conjunto con un _scraping_ de los ramos desde Ucampus, una base de datos en formato JSON, la
cual es visualizada en la página `index.html`.

### src

Contiene los scripts de Python que scrapean la información de los ramos desde Ucampus, que obtienen los comentarios de
los ramos desde el Excel y que une todos los datos recopilados en `ramos.json`.

### scripts

Contiene el código de JavaScript que es ejecutado en la página para obtener los datos de los ramos. Los datos de
`ramos.json` deben ser copiados a mano al archivo `ramos.js`, ya que intentamos durante 7 horas leer un JSON con
JavaScript, pero no lo logramos.

### css

Contiene el archivo CSS es la página.

## Cómo ejecutar

* Previamente debe descargarse el libro de Excel generado por Google Forms y renombrarlo a `respuestas.xlsx`.
* El archivo `main.py` ejecuta todos los scripts para obtener datos y unirlos, dejando sus resultados en `ramos.json`.
Estos scripts pueden ser modificados para usar distintas configuraciones al llenar dicho archivo.
* El contenido de `ramos.json` debe copiarse y pegarse en la variable `ramos` de `ramos.js`.
* Luego de esto, la información será visualizable en `index.html`.

## TODO:

* Mostrar la cantidad de gente que seleccionó cierta área para un ramo.
* Mostrar comentarios opcionales
* Hacerlo más bonito (?)