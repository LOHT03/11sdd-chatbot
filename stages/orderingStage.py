from controller.customer import Customer
from controller.menu import menuInstance
from controller.orders import Order
from fuzzywuzzy import process


def orderingStage(customer: Customer):
    customerOrder = Order()
    isOrdering = True
    while isOrdering:
        option = input(
            f"What course would you like to order from? {menuInstance.courses}: ")
        if len(option) != 0:
            (selectedCourse, confidence) = process.extractOne(
                option, menuInstance.courses)
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
            print("Here's your current order.")
            print()
            customerOrder.showTotal()
            goingtoConfirm = True
            while goingtoConfirm:
                if customerOrder.isValid():
                    print("You have enough items for a delivery.")
                    choice = input(
                        "Would you like to purchase this order and deliver it? [Y/N]: ")
                    if choice == "Y":
                        print()
                        print("Thanks for ordering!")
                        customer.addOrder(customerOrder)
                        print("We have saved your order to the file.")
                        goingtoConfirm = False
                else:
                    print(
                        "Unfortunately, you don't have enough items on your order, so we can't deliver this order yet.")
                    goingtoConfirm = False

            return
