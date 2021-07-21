import json
import requests
import sys
from bs4 import BeautifulSoup

# Malla nueva (v5)
malla = ["CC1000", "CC1002",
         "CC3001", "CC3002", "CC3101", "CC3102", "CC3201", "CC3301", "CC3501",
         "CC4101", "CC4102", "CC4302", "CC4303", "CC4401", "CC4402", "CC4901",
         "CC5402", "CC5901",
         "CC6908", "CC6909"]


def full_strip(st):
    return st.replace("\n", "").replace("\t", "").strip(" ")


def scrape(year, semester, description=False):
    print("Scraping catalog...")
    cursos_cnt = 0

    dept_id = "5"  # DCC
    catalogo = requests.get(f"https://ucampus.uchile.cl/m/fcfm_catalogo/?semestre={year}{semester}&depto={dept_id}")
    result = {}
    soup = BeautifulSoup(catalogo.content, "html.parser")

    for curso_tag in soup.find_all("div", class_="ramo"):
        cursos_cnt += 1
        curso_str = full_strip(curso_tag.find("h2").contents[0]).split(" ", 1)
        curso_id = curso_str[0]
        curso_nombre = curso_str[1]
        last_sem = str(year) + "-" + str(semester)
        profes = []
        for seccion_tag in curso_tag.find("tbody").find_all("tr"):
            seccion_data = seccion_tag.find_all("td")
            for tag in seccion_data[0].find("ul", class_="profes").find_all("h1"):
                if full_strip(tag.text) not in profes:
                    profes.append(full_strip(tag.text))
        if description:
            result[curso_id] = {"nombre": curso_nombre,
                                "tags": [],
                                "descripcion": "lorem ipsum",
                                "malla": curso_id in malla}
        else:
            result[curso_id] = {"nombre": curso_nombre,
                                "ultimoSemestre": last_sem,
                                "profes": profes}

    print(f"Finished scraping, found {cursos_cnt} cursos")
    return result


def check(semesters, description=False):
    result = scrape(semesters[0][0], semesters[0][1], description)
    semesters.pop(0)
    for i in semesters:
        temp = scrape(i[0], i[1], description)
        for j in temp:
            if j not in result:
                result[j] = temp[j]
    filename = "infoRamos.json" if description else "scrapeRamos.json"
    with open(filename, "w") as out_file:
        print(f"Writing to {filename}")
        json.dump(result, out_file, ensure_ascii=False, sort_keys=False, indent=4)


sem = [(2021, 1), (2020, 2), (2020, 1), (2019, 2), (2019, 1), (2018, 2)]
descriptionMode = (len(sys.argv) > 1 and eval(sys.argv[1]))  # if argv[1]: hace infoRamos, else scrapeRamos

check(sem, descriptionMode)
