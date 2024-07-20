import os
from utils.util import open_db_connection

db = open_db_connection()
cursor = db.cursor()

no_error = True

cursor.execute("select name from Kazooha.Weapon")
res = cursor.fetchall()
if os.path.exists("../data/img/weapons/"):
    for elem in res:
        elem = elem[0]
        if not os.path.isfile(rf"../data/img/weapons/{elem}.png"):
            no_error = False
            print(f"erreur avec {elem}")
else:
    print("Le chemin des images des armes n'existe pas.")

cursor.execute("select name from Kazooha.Character")
res = cursor.fetchall()
if os.path.exists("../data/img/persos/"):
    for elem in res:
        elem = elem[0]
        if not os.path.isfile(f"../data/img/persos/{elem}.png"):
            no_error = False
            print(f"erreur avec {elem}")
else:
    print("Le chemin des images des personnages n'existe pas.")

cursor.close()
db.close()

print("Il n'y a pas eu de problème." if no_error else "Il y a eu un problème.")
