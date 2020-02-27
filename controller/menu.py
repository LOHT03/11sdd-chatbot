from typing import Dict, Literal, Union
from terminaltables import AsciiTable
from constants import menu

menuType = Dict[str, Dict[str, float]]

# menu: menuType = {
#     "starters": {
#         "snails": 1.20,
#         "prawns": 3.00
#     },
#     "main": {
#         "steak": 16.00,
#         "lasagna": 15.00
#     },
#     "dessert": {
#         "cake": 6.00,
#         "jelly": 4.00
#     }
# }


class Menu:
    @staticmethod
    def showAll():
        tableData = [("Meal", "Price")]
        for course in menu.keys():
            tableData.append((course.capitalize(), str("******")))
            for meal in menu[course].items():
                tableData.append(
                    (meal[0].capitalize(), str(f"${meal[1]:.2f}")))
            tableData.append((str(""), str("")))
        tableData.pop()

        print()
        print(AsciiTable(tableData, "Restaurant Menu").table)
        print()

    @staticmethod
    def show(course: Literal["starter", "main", "dessert"]):
        tableData = [("Meal", "Price")]
        for meal in menu[course].items():
            tableData.append((meal[0].capitalize(), str(f"${meal[1]:.2f}")))

        print()
        print(AsciiTable(tableData, course.capitalize()).table)
        print()
