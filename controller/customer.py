from constants import previousOrders
from controller.menu import Menu
from controller.types import OrderHistory


class Customer:
    def __init__(self, name: str, previousOrders: OrderHistory) -> None:
        self.name = name
        self.previousOrders = previousOrders

    def showPreviousOrders(self):
        print("Here are your previous orders with us:")
        print()
        for order in self.previousOrders.keys():
            Menu.displayTotals(self.previousOrders[order], f"Order {order}")
            print()


def getCustomer() -> Customer:
    # Implement the sentence input structure
    name = input("Please enter your name: ").lower()
    nameConfirmed = "N"
    while nameConfirmed != "Y":
        nameConfirmed = input(
            f"You entered \"{name}\". Is that correct? [Y/N]: ").upper()
        if nameConfirmed.upper() == "N":
            name = input("Please enter your name: ").lower()

    print()
    if name in previousOrders.keys():
        customer = Customer(name, previousOrders[name])
        print(f"Welcome back, {name.capitalize()}!")
        return customer
    else:
        print(
            f"Welcome, {name.capitalize()}. Thank you for choosing to order with us today.")
        return Customer(name, {})
