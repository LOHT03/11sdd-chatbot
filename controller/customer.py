from db.db import dbconn
from controller.types import MenuItem, OrderHistory
from controller.orders import Order
from controller.menu import Menu
from datetime import datetime
from typing import Dict, List, Tuple
from uuid import uuid4

import en_core_web_sm
tokenize = en_core_web_sm.load()


class Customer:
    def __init__(self, name: str, id: str,  previousOrders: OrderHistory):

        # Customer instance name
        self.name = name

        # Previous orders of the customer instance
        self.previousOrders = previousOrders

        # ID of the customer instance
        self.__id = id

    def showPreviousOrders(self):
        """Display tables showing all previous orders of this customer, if any."""
        print("Here are your previous orders with us:")
        print()

        # Iterate over all previous orders of the customer instance
        for order in self.previousOrders:

            # Show table for the current previous customer order
            Menu.displayTotals(self.previousOrders[order], f"Order {order}")
            print()

    def addOrder(self, order: Order):
        """Adds a complete order under the customers name to file.

        Arguments:
            order {Order} -- The order to add.
        """

        # No need to check if order has enough items as that is not part of the
        # customers responsibility

        # Create a new order in the database
        dbconn.execute("INSERT INTO previousOrders VALUES (?,?,?)",
                       (order.id, self.__id, str(datetime.now()),))

        # Add each of the dishes in the order to the orderedDishes table in the
        # database
        for (dishName, price, qty) in order.orders:
            dbconn.execute(
                """INSERT INTO orderedDishes (orderID, dishName, dishPrice, quantity)
                VALUES (?,?,?,?)""", (order.id, dishName, price, qty))

        # Commit changes to the database
        dbconn.commit()

# TODO: Fix name input system


def tokenizeInputAndGetName() -> str:
    inputName = input("Please enter your name: ").lower() + " and."
    nlpMatches = [(x.text, x.label_) for x in tokenize(inputName).ents]
    while len(nlpMatches) == 0:
        inputName = input("Please enter your name: ").lower() + " and."
        nlpMatches = [(x.text, x.label_) for x in tokenize(inputName).ents]
    if nlpMatches[0][1] == "PERSON":
        return nlpMatches[0][0]
    else:
        return ""


def confirmCustomerName() -> str:
    # Implement the sentence input structure
    inputName = tokenizeInputAndGetName()
    nameConfirmed = "N"
    while nameConfirmed != "Y":
        nameConfirmed = input(
            f"You entered \"{inputName}\". Is that correct? [Y/N]: ").upper()
        if nameConfirmed.upper().startswith("N"):
            inputName = tokenizeInputAndGetName()
    return inputName


def getCustomer() -> Customer:
    """
    Return a customer based on a provided name, from the database.
    Creates a new customer if provided name does not exist in the database.

    Returns:
        Customer -- The customer instance from the database.
    """

    # Get customer name
    name = confirmCustomerName()
    print()

    # Check db for name
    # Uses sql templating to prevent SQL injection attacks
    fetchedData: List[str] = dbconn.execute(
        """
        SELECT customers.customerID 
        FROM customers 
        WHERE customers.customerName = ?
        """, (name,)).fetchall()

    # Check to see if the returned data has a customer
    if len(fetchedData) == 1:

        # The fetched data is a List of strings, so get the first element and
        # save it to a variable as customerID
        customerID = str(fetchedData[0])

        # Get previous orders from the database
        # Returns in the format (courseName, dishName, dishPrice, Qty)
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

        # Create a variable to hold the previous orders for the customer
        previousOrders: Dict[str, List[MenuItem]] = {}

        # Parse the database information to the dictionary
        for (orderID, dishName, dishPrice, dishQty) in prevOrderData:

            # If the ID does not exist in the dictionary
            if orderID not in previousOrders:

                # Initialise the ID in the dictionary to an empty list
                previousOrders[orderID] = []

            # Add each dish in the order to the corresponding ID in the
            # dictionary
            previousOrders[orderID].append(
                (dishName.capitalize(), float(dishPrice), int(dishQty)))

        # Instantiate a new customer instance using the collected data
        customer = Customer(name, customerID, previousOrders)

        # Welcome the customer back in the console
        print(f"Welcome back, {name.capitalize()}!")

        # Return the customer instance
        return customer

    # If this is a new customer (not in the database)
    else:

        # Welcome the customer
        print(
            f"Welcome, {name.capitalize()}. Thank you for choosing to order with us today.")

        # Create a new ID for the customer
        customerID = str(uuid4())

        # Add the new customer's details to the database
        dbconn.execute("INSERT INTO customers VALUES (?,?)",
                       (customerID, name,))

        # Commit database changes
        dbconn.commit()

        # Return the a created instace of the customer with an empty dictionary
        # for the customer's previous orders
        return Customer(name, customerID, {})
