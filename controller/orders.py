from controller.menu import Menu
from typing import List
from controller.types import MenuItem


class Order:
    def __init__(self) -> None:
        self.__orders: List[MenuItem] = []

    def addItem(self, meal: MenuItem) -> None:
        if meal[0].lower() not in Menu.getMeals():
            print(f"\"{meal[0].capitalize()}\" is not a valid menu item.")
        else:
            self.__orders.append(meal)
            print()
            print(f"{meal[0].capitalize()} has been added to your order!")
            print(
                f"There are currently {len(self.__orders)} item(s) on your order.")
            print()

    def showTotal(self):
        print()
        print("Here's your current order.")
        print()
        Menu.displayTotals(self.__orders, "Current Order")
        print()
