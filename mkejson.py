import requests
from bs4 import BeautifulSoup
import json

DEPTS = ["5"]

def full_strip(st):
	return st.replace("\n", "").replace("\t", "").strip(" ")

def scrape(YEAR,SEMESTER):
	print("Scraping catalog...")
	result = {}
	cursos_cnt = 0

	i = 0
	for dept_id in DEPTS:
		catalogo = requests.get("https://ucampus.uchile.cl/m/fcfm_catalogo/?semestre={}{}&depto={}".format(YEAR, SEMESTER, dept_id))
		i = i + 1
		result = {}
		soup = BeautifulSoup(catalogo.content, "html.parser")

	for curso_tag in soup.find_all("div", class_="ramo"):
		cursos_cnt += 1
		curso_str = full_strip(curso_tag.find("h2").contents[0]).split(" ", 1)
		curso_id = curso_str[0]
		curso_nombre = curso_str[1]
		lastSem = str(YEAR)+"-"+str(SEMESTER)
		result[curso_id] = {"nombre": curso_nombre, "malla": "false", "tags": [], "descripcion": "none", "ultimoSemestre": lastSem, "profes": ""}
		
	print("Finished scraping, found {} cursos".format(cursos_cnt))
	return result
	
def check(semesters):
	result = scrape(semesters[0][0],semesters[0][1])
	semesters.pop(0)
	for i in semesters:
		temp = scrape(i[0],i[1])
		for j in temp:
			if j not in result:
				result[j]=temp[j]
	with open("scrapeRamos.json","w") as out_file:
		json.dump(result, out_file, ensure_ascii=False, sort_keys=False, indent=4)

sem = [(2021,1),(2020,2),(2020,1),(2019,2),(2019,1),(2018,2)]

check(sem)
