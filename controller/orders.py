from typing import List, Tuple
from uuid import uuid4

from controller.menu import Menu, menuInstance
from controller.types import MenuItem


class Order:
    def __init__(self) -> None:
        self.__orders: List[MenuItem] = []
        self.__id = str(uuid4())

    def addItem(self, meal: Tuple[str, float]) -> None:
        if meal[0].lower() not in menuInstance.getMeals():
            print(f"\"{meal[0].capitalize()}\" is not a valid menu item.")
        else:
            if any(meal[0] in x for x in self.__orders):
                self.__orders = [(x[0], x[1], x[2] + 1) if x[0] ==
                                 meal[0] else x for x in self.__orders]
            else:
                self.__orders.append((*meal, 1))
            print()
            print(f"{meal[0].capitalize()} has been added to your order!")
            print()
            print("Here's your current order.")
            print()
            Menu.displayTotals(self.__orders, "Current Order")
            print()

    def isValid(self):
        return len(self.__orders) >= 3

    def showTotal(self):
        print()
        print("Here's your current order.")
        print()
        Menu.displayTotals(self.__orders, "Current Order")
        print()

    def orders(self):
        return self.__orders

    def id(self):
        return self.__id
