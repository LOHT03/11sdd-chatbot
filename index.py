from controller.customer import getCustomer
from stages.findStage import getNextStage


print("Welcome to the AusBot ordering system.")
print("We hope that you enjoy your meal.")
print()
print("Before we can begin ordering, we need to check if you have ordered with us before.")

# Create a customer instance
customer = getCustomer()

# Start the ordering with the customer
getNextStage(customer)
