from controller.mSAPI import tts
from controller.customer import Customer
from controller.menu import menuInstance
from controller.orders import Order
from fuzzywuzzy import process


def orderingStage(customer: Customer, existingOrder: Order = None):
    """
    The ordering stage of the program. Takes a customer and an optional 
    existing order for recursion.
    """

    # Check if an order was provided as a paramater by checking if the order
    # is an instance of an order
    customerOrder: Order = existingOrder if isinstance(
        existingOrder, Order) else Order()

    while True:
        # Ask the customer what course they would like to order from
        tts("What course would you like to order from?")
        option = input(
            f"{', '.join(menuInstance.menu.keys())}: ")

        # Check if the customer provided an input
        if len(option) != 0:

            # Fuzzy process user input for a valid course from the menu
            (selectedCourse, confidence) = process.extractOne(
                option, menuInstance.menu.keys())

            # Check if the package is more than 80% confident
            if confidence >= 80:

                while True:

                    # Ask the user if they would like to see a menu or to enter
                    # a meal they would like to order
                    tts("What meal would you like to order, or would you like to see a menu?")
                    selectedDishInput = input(
                        "> ")

                    # Exit loop if they don't enter anything
                    if len(selectedDishInput) == 0:
                        break

                    # If the customer did enter something
                    else:

                        # Fuzzy process user input for a meal valid meal or to see a menu
                        (selectedDish, selectedDishConfidence) = process.extractOne(
                            selectedDishInput, ["see a menu", *list(menuInstance.menu[selectedCourse].keys())])

                        # If fuzzy is more than 80% confident
                        if selectedDishConfidence >= 80:

                            # If user wishes to see a menu
                            if selectedDish == "see a menu":

                                # Show the menu for the specified course
                                menuInstance.show(selectedCourse)
                            else:

                                # Add the item that the customer entered to the
                                # order
                                customerOrder.addItem(
                                    menuInstance.getDish(selectedDish))

        # No input was entered
        else:
            print()

            # Show the current order to the customer
            customerOrder.showTotal()

            while True:

                # If the order is valid
                if customerOrder.isValid:
                    tts("You have enough items for a delivery.")

                    # Ask the customer if they would like to add more items,
                    # deliver the order or cancel the order
                    tts("Would you like to purchase this order and deliver it, add more items, or cancel the order?")
                    choice = input(
                        "> ")
                    print()

                    # If the user entered input
                    if len(choice) != 0:

                        # Process fuzzy logic on the acceptable options
                        (selectedChoice, selectedChoiceConfidence) = process.extractOne(
                            choice, ["deliver", "add items", "cancel"])

                        # If fuzzy logic is more than 80% confident
                        if selectedChoiceConfidence >= 80:

                            # User wants to deliver the order
                            if selectedChoice == "deliver":
                                tts("Thanks for ordering!")

                                # Add the order for the customer on file
                                customer.addOrder(customerOrder)
                                tts("We have saved your order to the file.")

                                # Exit the loop
                                break

                            # Customer chooses to add more items to the order
                            elif selectedChoice == "add items":
                                tts(
                                    "Alright, let's add some more items to your order.")

                                # Recurse back to the ordering stage with the
                                # current order
                                return orderingStage(customer, customerOrder)

                            # CUstomer wishes to cancel the order
                            elif selectedChoice == "cancel":
                                tts("Alright, we're cancelling this order.")

                                # Exit the loop
                                break

                # Not enough items in the order to complete a delivery
                else:
                    tts(
                        "Unfortunately, you don't have enough items on your order, so we can't deliver this order yet.")
                    while True:

                        # User input to continue adding items or to cancel
                        # the current order
                        tts("Would you like to continue with your order, or cancel the order?")
                        continuationInput = input(
                            "> ")

                        # Fuzzy process the user input to continue with the
                        # order or to cancel the order
                        (continuationChoice, continuationConfidence) = process.extractOne(
                            continuationInput, ["continue with order", "cancel"])

                        if continuationConfidence >= 80:

                            # Customer chooses to continue with the order
                            if continuationChoice == "continue with order":
                                # Recurse back to the ordering stage
                                return orderingStage(customer, customerOrder)

                            # Customer chooses to cancel the order
                            elif continuationChoice == "cancel":
                                print()
                                print()
                                tts("No worries, we're cancelling this order.")
                                print()

                                # Exit out of the loop
                                break

            return
