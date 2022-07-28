import requests
from bs4 import BeautifulSoup

malla_v5 = [
    "CC1000", "CC1002",
    "CC3001", "CC3002", "CC3101", "CC3102", "CC3201", "CC3301", "CC3501",
    "CC4101", "CC4102", "CC4302", "CC4303", "CC4401", "CC4402", "CC4901",
    "CC5205", "CC5402", "CC5901",
    "CC6908", "CC6909"
]


def full_strip(s: str) -> str:
    """Elimina saltos de línea, tabulaciones y espacios innecesarios en un string."""
    return s.replace("\n", "").replace("\t", "").strip(" ")


def scrape(year: int, semester: int) -> dict:
    """Scrapea la página de Ucampus que muestra el catálogo de cursos DCC de un semestre en particular.

    Entrega un diccionario con las siguientes llaves:

    {
    Código del ramo (llave primaria): {
        "nombre": (str) Nombre del ramo,
        "malla": (bool) Si el ramo es de malla o no,
        "ultimoSemestre": (str) El último semestre en el que se dictó el ramo,
        "profes": (list[str]) Profesores que han dictado el ramo los últimos semestres
        }
    ...
    }
    """
    print(f"Scrapeando el catálogo del semestre {year}-{semester}...")

    cursos_cnt = 0
    dcc_id = "5"
    catalogo = requests.get(f"https://ucampus.uchile.cl/m/fcfm_catalogo/?semestre={year}{semester}&depto={dcc_id}")
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

        result[curso_id] = {
            "nombre": curso_nombre,
            "malla": curso_id in malla_v5,
            "ultimoSemestre": last_sem,
            "profes": profes
        }

    print(f"Se encontraron {cursos_cnt} cursos.")
    return result


def batch_scrape(semestres: list[tuple[int, int]]) -> dict:
    """Scrapea los ramos de una lista de semestres del tipo [(año, semestre) ...]"""
    res = {}
    for i in semestres:
        scraped = scrape(i[0], i[1])
        for j in scraped:
            if j not in res:
                res[j] = scraped[j]
    return res
