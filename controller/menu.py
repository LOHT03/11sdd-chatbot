from controller.types import MenuItem
from typing import Dict, List, Literal, Tuple, Union
from terminaltables import AsciiTable
from constants import menu


class Menu:
    @staticmethod
    def show(course: Union[Literal["entrees", "main", "dessert", None]] = None):
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
                        (meal[0].capitalize(), str(f"${meal[1]:5.2f}")))
                tableData.append((str(""), str("")))
            tableData.pop()

        table = AsciiTable(tableData, course.capitalize()
                           if course else "Menu")
        table.justify_columns[1] = "right"
        print()
        print(table.table)
        print()

    @staticmethod
    def displayTotals(items: List[MenuItem], tableName: str = None):
        tableData = [("Meal", "Qty", "Unit", "Price")]
        finalTotal: float = 0
        quantities: Dict[Tuple[str, float], int] = {}
        finalQty = 0
        for i in items:
            item = (i[0].lower().capitalize(), i[1])
            if item not in quantities.keys():
                quantities[item] = 1
            else:
                quantities[item] += 1
            finalTotal += item[1]
        for i in quantities.keys():
            tableData.append(
                (f"{i[0]}", f"{quantities[i]}", f"${i[1]:.2f}", f"${(i[1] * quantities[i]):.2f}"))
            finalQty += quantities[i]
        tableData.append(
            ("TOTAL", f"{finalQty}", f"---", f"${finalTotal:.2f}"))
        table = AsciiTable(tableData, tableName)
        table.justify_columns[1] = "right"
        table.justify_columns[2] = "right"
        table.justify_columns[3] = "right"
        table.inner_footing_row_border = True
        print(table.table)

    @staticmethod
    def getMeals() -> List[str]:
        menuItems: List[str] = []
        for course in menu.keys():
            for item in menu[course].items():
                menuItems.append(item[0])
        return menuItems
