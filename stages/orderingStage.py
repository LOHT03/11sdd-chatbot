from controller.customer import Customer
from controller.menu import menuInstance
from controller.orders import Order
from fuzzywuzzy import process


def orderingStage(customer: Customer, existingOrder: Order = None):
    customerOrder: Order = existingOrder if isinstance(
        existingOrder, Order) else Order()
    isOrdering = True
    while isOrdering:
        option = input(
            f"What course would you like to order from? {menuInstance.menu.keys()}: ")
        if len(option) != 0:
            (selectedCourse, confidence) = process.extractOne(
                option, menuInstance.menu.keys())
            if confidence >= 80:
                menuLoop = True
                while menuLoop:
                    selectedDishInput = input(
                        "What meal would you like? (Or would you like to see a menu?): ")
                    if len(selectedDishInput) == 0:
                        menuLoop = False
                    else:
                        (selectedDish, selectedDishConfidence) = process.extractOne(
                            selectedDishInput, ["see a menu", *list(menuInstance.menu[selectedCourse].keys())])
                        if selectedDishConfidence >= 80:
                            if selectedDish == "see a menu":
                                menuInstance.show(selectedCourse)
                            else:
                                customerOrder.addItem(
                                    menuInstance.getDish(selectedDish))
        else:
            print()
            customerOrder.showTotal()
            goingtoConfirm = True
            while goingtoConfirm:
                if customerOrder.isValid:
                    print("You have enough items for a delivery.")
                    choice = input(
                        "Would you like to purchase this order and deliver it, add more items, or cancel the order?: ")
                    print()
                    if len(choice) != 0:
                        (selectedChoice, selectedChoiceConfidence) = process.extractOne(
                            choice, ["purchase", "add items", "cancel"])
                        if selectedChoiceConfidence >= 80:
                            if selectedChoice == "purchase":
                                print("Thanks for ordering!")
                                customer.addOrder(customerOrder)
                                print("We have saved your order to the file.")
                                goingtoConfirm = False
                            elif selectedChoice == "add items":
                                print(
                                    "Alright, let's add some more items to your order.")
                                return orderingStage(customer, customerOrder)
                            elif selectedChoice == "cancel":
                                print("Alright, we're cancelling this order.")
                                break
                else:
                    print(
                        "Unfortunately, you don't have enough items on your order, so we can't deliver this order yet.")
                    willContinue = True
                    while willContinue:
                        continuationInput = input(
                            "Would you like to continue with your order, or cancel the order?: ")
                        (continuationChoice, continuationConfidence) = process.extractOne(
                            continuationInput, ["continue with order", "cancel"])
                        if continuationConfidence >= 80:
                            if continuationChoice == "continue with order":
                                willContinue = False
                                return orderingStage(customer, customerOrder)
                            elif continuationChoice == "cancel":
                                print()
                                print()
                                print("No worries, we're cancelling this order.")
                                print()
                                willContinue = False
                    goingtoConfirm = False

            return
