import sqlite3
from typing import Dict

dbconn = sqlite3.connect('db\\chatData.db')

cursor = dbconn.execute(
    "SELECT courseName, dishName, dishPrice FROM courses, dishes WHERE courses.courseID = dishes.courseID")

menu: Dict[str, Dict[str, float]] = {}

for row in cursor:
    if not row[0] in menu.keys():
        menu[row[0]] = {}
    menu[row[0]][row[1]] = float(row[2])

print(menu)
