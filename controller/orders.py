from typing import List, Tuple
from uuid import uuid4

from controller.menu import Menu, menuInstance
from controller.types import MenuItem
from functools import reduce


class Order:
    def __init__(self) -> None:

        # Create private attribute for the list of dishes for order instance
        self.__orders: List[MenuItem] = []

        # Create a new random UUID v4 for the order instance
        self.__id = str(uuid4())

    def addItem(self, dish: Tuple[str, float]) -> None:
        """Add a dish to the menu.

        Arguments:
            dish {Tuple[str, float]} -- The dish to add to the order instance.
        """

        # Destructure tuple for easier reading
        (dishName, price) = dish

        # Check if dish does not exist in the menu
        if dishName.lower() not in menuInstance.dishes:
            print(f"\"{dishName.capitalize()}\" is not a valid menu item.")

        # Dish does exist in the menu
        else:

            # Check if the dish is already in order instance
            if any(dishName in x for x in self.__orders):

                # If the dish is already in the order instance, increase qty by one
                self.__orders = [(name, price, qty + 1) if name ==
                                 dishName else (name, price, qty) for (name, price, qty) in self.__orders]

            # Dish does not exist in the order instance
            else:

                # Add the dish to the order instance
                self.__orders.append((*dish, 1))

            print()
            print(f"{dishName.capitalize()} has been added to your order!")
            print()
            print("Here's your current order.")
            print()

            # Print the current order to the console
            Menu.displayTotals(self.__orders, "Current Order")
            print()

    @property
    def isValid(self):
        """Check if the current order can be delivered."""

        # Return the result of a reducer function that reduces all items in the
        # order and returns the total quantity
        return reduce(lambda a, b: a+b, [qty for (dishName, price, qty) in self.__orders]) >= 3

    def showTotal(self):
        """Show the total for the order."""
        print()
        print("Here's your current order.")
        print()

        # Print the current order to the console
        Menu.displayTotals(self.__orders, "Current Order")
        print()

    @property
    def orders(self):
        """
        Returns:
            Items {List[Tuple[str, float, int]]} -- List of all items in the order instance
        """
        return self.__orders

    @property
    def id(self):
        """
        Returns:
            ID {str} -- ID of the order instance.
        """
        return self.__id
