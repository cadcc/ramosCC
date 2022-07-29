def merge_dicts(d1: dict, d2: dict):
    """Une dos diccionarios en uno solo. De repetirse alguna llave, se conservan los valores del primero."""
    res = d2
    for k in d1.keys():
        if k not in d2.keys():
            res[k] = d1[k]
    return res


def merge_ramos(scraped: dict, respuestas: dict) -> dict:
    """Une los diccionarios resultado de scrapear Ucampus y de la hoja de cálculo de respuestas."""
    res = scraped

    for codigo in respuestas.keys():
        ramo_scraped = res[codigo]
        ramo_respuesta = respuestas[codigo]
        res[codigo] = merge_dicts(ramo_scraped, ramo_respuesta)

    for codigo in res.keys():

        res[codigo]["codigo"] = codigo

        if "descripciones" not in res[codigo].keys():
            res[codigo]["descripciones"] = {}
        if "dificultad" not in res[codigo].keys():
            res[codigo]["dificultad"] = -1
        if "tiempo" not in res[codigo].keys() or res[codigo]["tiempo"] == []:
            res[codigo]["tiempo"] = -1
        if "comentarios" not in res[codigo].keys():
            res[codigo]["comentarios"] = {}

        if res[codigo]["descripciones"] != {} and "dificultad" not in res[codigo].keys():
            res[codigo]["dificultad"] = -1
            res[codigo]["opiniones"] = 1

        if res[codigo]["descripciones"] != {}:
            res[codigo]["descripciones"] = [{
                "fecha": x["fecha"],
                "texto": x["texto"].replace("\n", " ")
            } for x in res[codigo]["descripciones"]]

        if res[codigo]["comentarios"] != {}:
            res[codigo]["comentarios"] = [{
                "fecha": x["fecha"],
                "texto": x["texto"].replace("\n", " ")
            } for x in res[codigo]["comentarios"]]

        res[codigo]["descripciones"] = sorted(res[codigo]["descripciones"], key=lambda x: x["fecha"], reverse=True)
        res[codigo]["comentarios"] = sorted(res[codigo]["comentarios"], key=lambda x: x["fecha"], reverse=True)

    # CC5206 Intro a Minería de Datos equivale a CC5205 Minería de Datos
    if "CC5206" in res.keys():
        res["CC5205"] = {k: v for (k, v) in res["CC5206"].items()}
        res["CC5205"]["nombre"] = "Minería de Datos"
        res["CC5205"]["codigo"] = "CC5205"
        res["CC5205"]["malla"] = True

    # CC5327 Intro a la Seguridad Computacional equivale a CC5312 Seguridad de Datos
    if "CC5312" in res.keys():
        res["CC5327"] = {k: v for (k, v) in res["CC5312"].items()}
        res["CC5327"]["nombre"] = "Introducción a la Seguridad Computacional"
        res["CC5327"]["codigo"] = "CC5327"
        res["CC5327"]["malla"] = False

    return res
