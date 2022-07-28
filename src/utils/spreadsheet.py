from statistics import mean
from typing import Union

from openpyxl.worksheet.worksheet import Worksheet

tag_dict = {
    "Programación (como Algoritmos)": "Programación",
    "Teoría (como Discretas)": "Teoría",
    "Datos (como Bases de Datos)": "Datos",
    "Arquitectura (como Mateu)": "Arquitectura",
    "Redes (como Redes)": "Redes",
    "Desarrollo de software (como Ing. de Software)": "Software",
    "Gráfica (como Computa Gráfica)": "Gráfica",
    "Seguridad y Criptografía": "Seguridad",
    "Interacción Humanx-Computador": "HCI",
}

diff_dict = {
    "Muy baja": 1,
    "Baja": 2,
    "Media": 3,
    "Alta": 4,
    "Muy alta": 5
}

tiempo_dict = {
    "Mucho menos de su valor en créditos": 1,
    "Menos de su valor en créditos": 2,
    "Aproximadamente su valor en créditos": 3,
    "Más de su valor en créditos": 4,
    "Mucho más de su valor en créditos": 5
}


def get_or_key(d: dict, k: object) -> Union[dict, object]:
    """Si la llave es parte del diccionario, entrega su valor. Si no, entrega la misma llave.
    Esta función es necesaria para agregar los tags que no son estándar en el formulario."""
    try:
        return d[k]
    except KeyError:
        return k


def censurar(sh: Worksheet, coords: list[str]) -> None:
    """Reemplaza el contenido de las celdas especificadas por algo estándar, borrando su información."""
    for coord in coords:
        sh[coord] = ":^)"


def feed_ramos(sh: Worksheet) -> dict:
    """Crea un diccionario con la información de los ramos obtenidas de la hoja de cálculo de respuestas.

    El diccionario tiene las siguientes llaves:

    {
    Código del ramo (llave primaria): {
        "tags": (list[str]) Categorías a las que pertenece el ramo,
        "descripcion": (list[list[str, str]]) Descripciones obtenidas del ramo ordenadas por fecha,
        "comentarios": (list[list[str, str]]) Comentarios obtenidos del ramo ordenadas por fecha,
        "dificultad": (float) Promedio de las dificultades percibidas del ramo,
        "tiempo": (float) Promedio de las cargas temporales percibidas del ramo,
        "opiniones": (int) Cantidad de opiniones recibidas del ramo
        }
    ...
    }"""

    y = 2
    res = {}
    while sh[f"B{y}"].value is not None:
        codigo = sh[f"B{y}"].value.split(" ")[0]

        if codigo not in res.keys():
            res[codigo] = {
                "tags": [],
                "descripciones": [],
                "comentarios": [],
                "dificultad": [],
                "tiempo": [],
                "opiniones": 0
            }

        tags = [get_or_key(tag_dict, x) for x in sh[f"C{y}"].value.split(", ")]
        for tag in tags:
            if tag not in res[codigo]["tags"]:
                res[codigo]["tags"].append(tag)

        date = sh[f"A{y}"].value
        anyo_y_mes = f"{date.year}-{str(date.month).zfill(2)}"

        res[codigo]["descripciones"].append({
            "fecha": anyo_y_mes,
            "texto": sh[f"D{y}"].value
        })

        if sh[f"F{y}"].value is not None:
            res[codigo]["comentarios"].append({
                "fecha": anyo_y_mes,
                "texto": sh[f"F{y}"].value
            })

        res[codigo]["dificultad"].append(sh[f"E{y}"].value)

        if sh[f"G{y}"].value is not None and sh[f"G{y}"].value in tiempo_dict.keys():
            res[codigo]["tiempo"].append(sh[f"G{y}"].value)

        res[codigo]["opiniones"] += 1

        y += 1

    for k in res.keys():
        res[k]["dificultad"] = round(mean([diff_dict[x] for x in res[k]["dificultad"]]), 1)

        if res[k]["tiempo"]:
            res[k]["tiempo"] = round(mean([tiempo_dict[x] for x in res[k]["tiempo"]]), 1)

    return res
