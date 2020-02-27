from controller.orders import Order
from controller.menu import Menu

order = Order()
order.addItem(("Steak", 12))
order.addItem(("snails", 9.10))
order.showTotal()
