from stages.orderingStage import orderingStage
from fuzzywuzzy import process

from controller.customer import Customer
from controller.menu import menuInstance

possibleOptions = ["order some food", "see a menu", "see previous orders"]


def getNextStage(customer: Customer):
    continuation = True
    while continuation:
        print()
        choiceInput = input(
            "Would you like to order some food, see a menu, or see previous orders?: ")
        if len(choiceInput) == 0:
            continuation = False
            print()
            print("Thank you for your patronage, and enjoy your day!")
            print()
            print()
            break
        else:
            (choice, confidence) = process.extractOne(
                choiceInput, possibleOptions)
            if confidence >= 80:
                if choice == "order some food":
                    orderingStage(customer)
                elif choice == "see a menu":
                    print()
                    courseInput = input(
                        f"What course would you like to see? {', '.join(menuInstance.menu.keys())}: ")
                    if len(courseInput) == 0:
                        print()
                        print("Here's the full menu.")
                        menuInstance.show()
                    else:
                        (courseChoice, courseConfidence) = process.extractOne(
                            courseInput, menuInstance.menu.keys())
                        if courseConfidence >= 80:
                            print()
                            print()
                            print(
                                f"Here's the {courseChoice} menu.")
                            menuInstance.show(courseChoice)
                        else:
                            print("Sorry, we don't have that course available here.")
                elif choice == "see previous orders":
                    print()
                    if len(customer.previousOrders) == 0:
                        print("Sorry, you don't have any previous orders with us.")
                    else:
                        customer.showPreviousOrders()

            else:
                print("Sorry, I don't understand what you would like to do.")
