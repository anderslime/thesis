from pymongo import MongoClient
from pymongo import monitoring

class CommandLogger(monitoring.CommandListener):
    def __init__(self):
        self.commands = {}

    def started(self, event):
        # print(event.operation_id)
        # print(event.command)
        print("STARTED")
        self.commands[event.operation_id] = event.command

    def succeeded(self, event):
        print("SUCCEEDED")
        # print(event.reply)
        # print(event.command_name)
        # print(event.operation_id)
        print(event.operation_id)
        print(self.commands[event.operation_id])
        # import code; code.interact(local=locals())

    def failed(self, event):
        print("FAILED")

mongo   = MongoClient('mongodb://localhost:27017/',
                      event_listeners=[CommandLogger()])
# mongo   = MongoClient('mongodb://localhost:27017/')

order  = mongo.Northwind.orders.find_one()
print("COUNT")
print(mongo.Northwind.orders.count())
new_order = order
new_order.pop("_id", None)
print("SAVING")
saved = mongo.Northwind.orders.insert_one({"_id": "1234", "hello": "world3"})
# order  = mongo.Northwind.orders.find_one({"_id": _id})
# print(order)

## RESULT:
# succeeded still runs even though the query fails (e.g. with duplicate key)

