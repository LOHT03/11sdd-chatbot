from fuzzywuzzy import fuzz, process

possibleOptions = ["order some food", "see a menu", "see previous orders"]


def getNextStage():
    isValid = False
    while isValid is False:
        choiceInput = input(
            "Would you like to order some food, see a menu, or see previous orders?: ")
        (choice, confidence) = process.extractOne(choiceInput, possibleOptions)
        print(choice)
