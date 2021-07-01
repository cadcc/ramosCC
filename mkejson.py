import requests, json, sys
from bs4 import BeautifulSoup

DEPTS = ["5"]

def full_strip(st):
	return st.replace("\n", "").replace("\t", "").strip(" ")

def scrape(YEAR,SEMESTER,DESCRIPTION=False):
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
		for seccion_tag in curso_tag.find("tbody").find_all("tr"):
			seccion_data = seccion_tag.find_all("td")
			seccion_profesores = []
			for tag in seccion_data[0].find("ul", class_="profes").find_all("h1"):
				seccion_profesores.append(full_strip(tag.text))
			seccion_dict = {"profesores": seccion_profesores, "cupos": seccion_cupos, "horarios": seccion_horarios}
		if DESCRIPTION:
			result[curso_id] = {"nombre": curso_nombre, "descripcion": "lorem ipsum"}
		else:
			result[curso_id] = {"nombre": curso_nombre, "malla": "false", "tags": [], "descripcion": "none", "ultimoSemestre": lastSem, "profes": ""}
		
	print("Finished scraping, found {} cursos".format(cursos_cnt))
	return result
	
def check(semesters,description=False):
	result = scrape(semesters[0][0],semesters[0][1],description)
	semesters.pop(0)
	for i in semesters:
		temp = scrape(i[0],i[1],description)
		for j in temp:
			if j not in result:
				result[j]=temp[j]
	filename = "infoRamos.json" if description else "scrapeRamos.json"
	with open(filename,"w") as out_file:
		json.dump(result, out_file, ensure_ascii=False, sort_keys=False, indent=4)

sem = [(2021,1),(2020,2),(2020,1),(2019,2),(2019,1),(2018,2)]

descriptionMode = (len(sys.argv)>2 and eval(sys.argv[2]))

check(sem,descriptionMode)
