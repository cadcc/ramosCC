import json

import openpyxl

from censurame import a_censurar
from merge_utils import merge_ramos
from scrape_utils import batch_scrape
from spreadsheet_utils import censurar, feed_ramos

semestres = [
    (2022, 1),
    (2021, 1), (2021, 2),
    (2020, 1), (2020, 2),
    (2019, 1), (2019, 2),
]

print(f"Empezando a scrapear para los semestres: {semestres}")

ramos = batch_scrape(semestres)
excel_filename = "respuestas.xlsx"
spreadsheet = openpyxl.load_workbook(filename=excel_filename)
sheet = spreadsheet["Respuestas de formulario 1"]

print(f"Procesando hoja de respuestas...")
censurar(sheet, a_censurar)
respuestas = feed_ramos(sheet)

print(f"Obtenidas respuestas para {len(respuestas.keys())} ramos.")

print("Uniendo...")
el_json = merge_ramos(ramos, respuestas)

path = "ramos.json"
with open(path, 'w') as f:
    json.dump(el_json, f, indent=2)

print(f"JSON guardado en {path}")
