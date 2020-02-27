from controller.orders import Order

order = Order()

order.addItem(("fairy bread", 16))
order.addItem(("pavlova", 4))
order.addItem(("kangaroo", 12))
order.addItem(("fairy bread", 16))

order.showTotal()
