from controller.mSAPI import tts
from stages.orderingStage import orderingStage
from fuzzywuzzy import process

from controller.customer import Customer
from controller.menu import menuInstance

possibleOptions = ["order some food", "see a menu", "see previous orders"]


def getNextStage(customer: Customer):
    """Runs a given customer through all of the different stages in the ordering stages."""

    # Loop through all of the options constantly asking for input
    while True:
        print()

        # Ask the customer what they would like to do
        tts("Would you like to order some food, see a menu, or see your previous orders?")
        print("(Leave empty to exit)")
        choiceInput = input(
            "> ")

        # Check if customer didn't enter anything
        if len(choiceInput) == 0:
            print()
            tts("Thank you for your patronage, and enjoy your day!")
            print()
            print()

            # Exit the loop
            break

        # Customer did enter a choice
        else:

            # Process the user's input for a potential choice using fuzzy
            (choice, confidence) = process.extractOne(
                choiceInput, possibleOptions)

            # Case where confidence is greater than 80%
            if confidence >= 80:

                if choice == "order some food":

                    # Send the customer to the ordering stage
                    orderingStage(customer)

                elif choice == "see a menu":
                    print()

                    # Ask the customer which course they would like to see a menu

                    tts("What course would you like to see?")
                    courseInput = input(
                        f"{', '.join(menuInstance.menu.keys())}: ")

                    # Customer does not provide a course
                    if len(courseInput) == 0:
                        print()
                        tts("Here's the full menu.")

                        # Show the entire entire menu (all courses)
                        menuInstance.show()

                    # User provides a course
                    else:

                        # Process user input for potential choice of course
                        # using fuzzy logic
                        (courseChoice, courseConfidence) = process.extractOne(
                            courseInput, menuInstance.menu.keys())

                        # If the fuzzy logic is more than 80% confidence of a
                        # choice
                        if courseConfidence >= 80:
                            print()
                            print()
                            tts(
                                f"Here's the {courseChoice} menu.")

                            # Show the menu for the provided course
                            menuInstance.show(courseChoice)
                        else:

                            # Course doesn't exist in the menu if fuzzy logic
                            # is unable to determine the course inputted
                            tts("Sorry, we don't have that course available here.")

                elif choice == "see previous orders":
                    print()

                    # Check if the customer has any previous orders
                    if len(customer.previousOrders) == 0:
                        tts("Sorry, you don't have any previous orders with us.")
                    else:

                        # Show the customers' previous orders in a table,
                        # printed to the console
                        customer.showPreviousOrders()

            else:

                # Unable to determine the input provided
                tts("Sorry, I don't understand what you would like to do.")
