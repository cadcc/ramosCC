import json
from statistics import mean

import openpyxl

from censurame import censurar

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


def check_dict(key, dic):
    try:
        return dic[key]
    except KeyError:
        return key


json_filename = "src/infoRamos.json"
with open(json_filename, 'r') as f:
    ramos = json.load(f)

excel_filename = "src/respuestas.xlsx"
spreadsheet = openpyxl.load_workbook(filename=excel_filename)
sheet = spreadsheet["Respuestas de formulario 1"]

i = 2

dicc = {}

for coord in censurar:
    sheet[coord] = ":^)"

while sheet[f"B{i}"].value is not None:
    cell = sheet[f"B{i}"].value
    codigo = cell[:6]

    if codigo not in dicc.keys():
        dicc[codigo] = {
            "tags": {check_dict(x, tag_dict) for x in sheet[f"C{i}"].value.split(", ")},        # these are sets to avoid repetitions
            "descripcion": [sheet[f"D{i}"].value],
            "dificultad": [sheet[f"E{i}"].value],
            "comentarios": [sheet[f"F{i}"].value if sheet[f"F{i}"].value is not None else ""],
            "opiniones": 1
        }

    else:
        dicc[codigo]["tags"].update([check_dict(x, tag_dict) for x in sheet[f"C{i}"].value.split(", ")])
        dicc[codigo]["descripcion"].append(sheet[f"D{i}"].value)
        dicc[codigo]["dificultad"].append(sheet[f"E{i}"].value)
        dicc[codigo]["comentarios"].append(sheet[f"F{i}"].value if sheet[f"F{i}"].value is not None else "")
        dicc[codigo]["opiniones"] += 1

    i += 1


# Transform all tag sets into lists
for k in dicc.keys():
    dicc[k]["tags"] = list(dicc[k]["tags"])
    dicc[k]["dificultad"] = round(mean([check_dict(x, diff_dict) for x in dicc[k]["dificultad"]]), 1)

with open("src/from_excel.json", 'w') as f:
    json.dump(dicc, f, indent=2)
