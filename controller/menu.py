from typing import Dict, List, Tuple, Union

from terminaltables import AsciiTable

from controller.types import MenuItem
from db.db import dbconn


class Menu:
    def __init__(self) -> None:
        data = dbconn.execute("""
        SELECT courseName,
            dishName,
            dishPrice
        FROM courses,
            dishes
        WHERE courses.courseID = dishes.courseID;
        """)

        self.menu = {}
        self.courses: List[str] = []
        self.__courselessMenu: Dict[str, float] = {}

        for row in data:
            if not row[0] in self.menu.keys():
                self.menu[row[0]] = {}
                self.courses.append(row[0])
            self.menu[row[0]][row[1]] = float(row[2])
            self.__courselessMenu[row[1]] = float(row[2])

    def show(self, course: Union[str, None] = None):
        tableData = [("Meal", "Price")]

        if course is not None:
            for meal in self.menu[course].items():
                tableData.append(
                    (meal[0].capitalize(), str(f"${meal[1]:.2f}")))
        else:
            for c in self.menu.keys():
                tableData.append((c.capitalize(), str("******")))
                for meal in self.menu[c].items():
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

    def getDish(self, dishName: str, course: str = None) -> Tuple[str, float]:
        if course is None:
            if dishName not in self.__courselessMenu:
                raise ValueError("Meal does not exist.")
            else:
                return (dishName, self.__courselessMenu[dishName])
        elif course not in self.courses:
            raise ValueError("Course does not exist.")
        else:
            if dishName not in self.menu[course].keys():
                raise ValueError("Dish does not exist within course.")
            else:
                return (dishName, self.menu[course][dishName])

    @staticmethod
    def displayTotals(items: List[MenuItem], tableName: str = None):
        tableData = [("Meal", "Qty", "Unit", "Price")]
        finalTotal: float = 0
        finalQty = 0
        for i in items:
            finalTotal += (i[1]*i[2])
            tableData.append(
                (f"{i[0].capitalize()}", f"{i[2]}", f"${i[1]:.2f}", f"${(i[1] * i[2]):.2f}"))
            finalQty += i[2]
        tableData.append(
            ("TOTAL", f"{finalQty}", f"---", f"${finalTotal:.2f}"))
        table = AsciiTable(tableData, tableName)
        table.justify_columns[1] = "right"
        table.justify_columns[2] = "right"
        table.justify_columns[3] = "right"
        table.inner_footing_row_border = True
        print(table.table)

    def getMeals(self) -> List[str]:
        menuItems: List[str] = []
        for course in self.menu.keys():
            for item in self.menu[course].items():
                menuItems.append(item[0])
        return menuItems


menuInstance = Menu()
