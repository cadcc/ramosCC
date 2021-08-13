import json
import requests
import sys
from bs4 import BeautifulSoup


def full_strip(st):
    return st.replace("\n", "").replace("\t", "").strip(" ")


def scrape(year, semester):
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
        print(f"{curso_id} {curso_nombre}")

    print(f"Finished scraping, found {cursos_cnt} cursos")
    return result


def check(semesters, description=False):
    result = scrape(semesters[0][0], semesters[0][1])
    semesters.pop(0)
    for i in semesters:
        temp = scrape(i[0], i[1])
        for j in temp:
            if j not in result:
                result[j] = temp[j]


sem = [(2021, 2)]

check(sem)
