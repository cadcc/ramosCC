import os

# Obtener ramos
os.system("py src/mkejson.py True")
# Obtener atributos
os.system("py src/mkejson.py False")
# Obtener datos del excel
os.system("py src/update_json.py")
# Mezclar JSONs
os.system("py src/merge_json.py")
