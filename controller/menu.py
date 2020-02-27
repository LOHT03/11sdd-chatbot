from controller.types import MenuItem
from typing import List, Literal, Union
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

    @staticmethod
    def displayTotals(items: List[MenuItem], tableName: str = None):
        tableData = [("Meal", "Price")]
        finalTotal: float = 0
        for item in items:
            tableData.append((item[0].capitalize(), f"${item[1]:.2f}"))
            finalTotal += item[1]
        tableData.append((str("------"), str("------")))
        tableData.append(("TOTAL", f"${finalTotal:.2f}"))

        print(AsciiTable(tableData, tableName).table)

    @staticmethod
    def getMeals() -> List[str]:
        menuItems: List[str] = []
        for course in menu.keys():
            for item in menu[course].items():
                menuItems.append(item[0])
        return menuItems
