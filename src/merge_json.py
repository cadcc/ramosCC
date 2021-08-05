import json


def merge_dicts(d1, d2):
    res = d2
    for k in d1.keys():
        if k not in d2.keys():
            res[k] = d1[k]
    return res


with open("src/scrapeRamos.json", 'r') as f:
    scrape_ramos = json.load(f)

with open("src/infoRamos.json", 'r') as f:
    info_ramos = json.load(f)

with open("src/from_excel.json", 'r') as f:
    from_excel = json.load(f)

res = {}

for codigo in scrape_ramos.keys():
    res[codigo] = scrape_ramos[codigo]

for codigo in info_ramos.keys():
    ramo_i = info_ramos[codigo]
    ramo_f = res[codigo]
    res[codigo] = merge_dicts(ramo_f, ramo_i)

for codigo in from_excel.keys():
    ramo_i = from_excel[codigo]
    ramo_f = res[codigo]
    res[codigo] = merge_dicts(ramo_f, ramo_i)

# Clean and format
for codigo in res.keys():

    res[codigo]["codigo"] = codigo

    if res[codigo]["descripcion"] != "" and "dificultad" not in res[codigo].keys():
        res[codigo]["dificultad"] = -1
        res[codigo]["opiniones"] = 1

    if "comentarios" not in res[codigo].keys():
        res[codigo]["comentarios"] = []
        
    res[codigo]["descripcion"] = [s.replace("\n", " ") for s in res[codigo]["descripcion"]]
    res[codigo]["comentarios"] = [s.replace("\n", " ") for s in res[codigo]["comentarios"]]


# Intro a Minería de Datos equivale a Minería de Datos
if "CC5206" in res.keys():
    res["CC5205"] = {k: v for (k, v) in res["CC5206"].items()}
    res["CC5205"]["nombre"] = "Minería de Datos"
    res["CC5205"]["codigo"] = "CC5205"
    res["CC5205"]["malla"] = True

with open("src/ramos.json", 'w') as f:
    json.dump(res, f, indent=2)
