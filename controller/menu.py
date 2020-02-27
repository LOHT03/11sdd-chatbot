from typing import Dict, Literal, Tuple, Union
from terminaltables import AsciiTable
from constants import menu


class Menu:
    @staticmethod
    def show(course: Union[Literal["starter", "main", "dessert", None]] = None):
        tableData = [("Meal", "Price")]
        if course is not None:
            for meal in menu[course].items():
                tableData.append(
                    (meal[0].capitalize(), str(f"${meal[1]:.2f}")))
        else:
            for c in menu.keys():
                tableData.append((c.capitalize(), str("******")))
                for meal in menu[c].items():
                    tableData.append(
                        (meal[0].capitalize(), str(f"${meal[1]:.2f}")))
                tableData.append((str(""), str("")))
            tableData.pop()

        print()
        print(AsciiTable(tableData, course.capitalize() if course else "Menu").table)
        print()
