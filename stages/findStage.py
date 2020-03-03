from controller.customer import Customer
from controller.menu import Menu
from fuzzywuzzy import fuzz, process

possibleOptions = ["order some food", "see a menu", "see previous orders"]


def getNextStage(customer: Customer):
    continuation = True
    while continuation:
        choiceInput = input(
            "Would you like to order some food, see a menu, or see previous orders?: ")
        if len(choiceInput) == 0:
            continuation = False
            break
        else:
            (choice, confidence) = process.extractOne(
                choiceInput, possibleOptions)
            if confidence >= 80:
                if choice == "order some food":
                    print("Going to order food.")
                elif choice == "see a menu":
                    print()
                    print("Here's the menu.")
                    Menu.show()
                elif choice == "see previous orders":
                    print()
                    customer.showPreviousOrders()
            else:
                print("Sorry, I don't understand what you would like to do.")
