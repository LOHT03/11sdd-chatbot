from datetime import datetime
from typing import Dict, List, Tuple
from uuid import uuid4

from controller.menu import Menu
from controller.orders import Order
from controller.types import MenuItem, OrderHistory
from db.db import dbconn


class Customer:
    def __init__(self, name: str, id: str,  previousOrders: OrderHistory):
        self.name = name
        self.previousOrders = previousOrders
        self.__id = id

    def showPreviousOrders(self):
        print("Here are your previous orders with us:")
        print()
        for order in self.previousOrders.keys():
            Menu.displayTotals(self.previousOrders[order], f"Order {order}")
            print()

    def addOrder(self, order: Order):
        finalQuantity = 0
        for d in order.orders:
            finalQuantity += d[2]
        if (finalQuantity < 3):
            raise ValueError("Not enough items in the order.")
        else:
            dbconn.execute("INSERT INTO previousOrders VALUES (?,?,?)",
                           (order.id(), self.__id, str(datetime.now()),))
            for d in order.orders:
                dbconn.execute(
                    "INSERT INTO orderedDishes (orderID, dishName, dishPrice, quantity) VALUES (?,?,?,?)", (order.id(), d[0], d[1], d[2]))
            dbconn.commit()


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

    # Check db for name
    fetchedData = dbconn.execute(
        "SELECT customers.customerID FROM customers WHERE customers.customerName = ?", (name,)).fetchall()

    if len(fetchedData) == 1:
        customerID = str(fetchedData[0][0])

        # Get Previous Orders
        prevOrderData: List[Tuple[str, str, float, int]] = dbconn.execute("""
        SELECT orderedDishes.orderID,
            orderedDishes.dishName,
            orderedDishes.dishPrice,
            orderedDishes.quantity
        FROM orderedDishes
            JOIN
            previousOrders ON orderedDishes.orderID = previousOrders.orderID
            JOIN
            customers ON previousOrders.customerID = customers.customerID
        WHERE previousOrders.customerID = ?;
        """, (customerID,)).fetchall()

        previousOrders: Dict[str, List[MenuItem]] = {}

        for (orderID, dishName, dishPrice, dishQty) in prevOrderData:
            if orderID not in previousOrders.keys():
                previousOrders[orderID] = []
            previousOrders[orderID].append(
                (dishName.capitalize(), float(dishPrice), int(dishQty)))

        customer = Customer(name, customerID, previousOrders)
        print(f"Welcome back, {name.capitalize()}!")
        return customer
    else:
        print(
            f"Welcome, {name.capitalize()}. Thank you for choosing to order with us today.")
        customerID = str(uuid4())

        # Add new customer to the database
        dbconn.execute("INSERT INTO customers VALUES (?,?)",
                       (customerID, name,))
        dbconn.commit()
        return Customer(name, customerID, {})
