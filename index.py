from stages.findStage import getNextStage
from controller.customer import getCustomer


print("Welcome to the AusBot ordering system.")
print("We hope that you enjoy your meal.")
print()
print("Before we can begin ordering, we need to check if you have ordered with us before.")

customer = getCustomer()
getNextStage(customer)
