import os
from utils.database import open_connection

db = open_connection()
cursor = db.cursor()

cursor.execute("select name from Weapon")
res = cursor.fetchall()
print(os.path.exists("../../../data/img/weapons/"))
for elem in res:
    elem = elem[0]
    if not os.path.isfile(rf"../../../data/img/weapons/{elem}.png"):
        print(f"erreur avec {elem}")

cursor.execute("select name from `Character`")
res = cursor.fetchall()
print(os.path.exists("../../../data/img/persos/"))
for elem in res:
    elem = elem[0]
    if not os.path.isfile(rf"../../../data/img/persos/{elem}.png"):
        print(f"erreur avec {elem}")

cursor.close()
db.close()
