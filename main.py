import os

# Obtener ramos
os.system("py mkejson.py True")
# Obtener atributos
os.system("py mkejson.py False")
# Obtener datos del excel
os.system("py update_json.py")
# Mezclar JSONs
os.system("py merge_json.py")
