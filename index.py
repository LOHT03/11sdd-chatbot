from controller.mSAPI import tts
from controller.customer import getCustomer
from stages.findStage import getNextStage


tts("Welcome to the OzBot ordering system.")
tts("We hope that you enjoy your meal.")
print()
tts("Before we can begin ordering, we need to check if you have ordered with us before.")

# Create a customer instance
customer = getCustomer()

# Start the ordering with the customer
getNextStage(customer)
