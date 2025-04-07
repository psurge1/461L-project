from pymongo import MongoClient


'''
Structure of Hardware Set entry:
HardwareSet = {
   'hwName': hwSetName,
   'capacity': initCapacity,
   'availability': initCapacity
}
'''


def get_database(client):
   return client["hardwareDB"]


def createHardwareSet(client, hwSetName, initCapacity):
   db = get_database(client)
   collection = db["hardwareSets"]
   if collection.find_one({"hwName": hwSetName}):
       # print("Hardware set already exists.")
       return
   hardware_set = {
       "hwName": hwSetName,
       "capacity": initCapacity,
       "availability": initCapacity
   }
   collection.insert_one(hardware_set)
   # print("Hardware set created successfully.")


def queryHardwareSet(client, hwSetName):
   db = get_database(client)
   collection = db["hardwareSets"]
   return collection.find_one({"hwName": hwSetName})


def updateAvailability(client, hwSetName, newAvailability):
   db = get_database(client)
   collection = db["hardwareSets"]
   result = collection.update_one(
       {"hwName": hwSetName},
       {"$set": {"availability": newAvailability}}
   )
   if result.matched_count:
       return 1
   else:
       return -1


def requestSpace(client, hwSetName, amount):
   db = get_database(client)
   collection = db["hardwareSets"]
   hw_set = collection.find_one({"hwName": hwSetName})
   if not hw_set:
       return {"checked_out":-1, "status":"error"}
   if hw_set["availability"] >= amount:
       collection.update_one(
           {"hwName": hwSetName},
           {"$inc": {"availability": -amount}}
       )
       return {"checked_out": amount,"status" : "success"}
   else:
       z = hw_set["availability"]
       collection.update_one(
           {"hwName": hwSetName},
           {"$inc": {"availability": 0}}
       )
       return {"checked_out": z, "status": "error"}


def getAllHwNames(client):
   db = get_database(client)
   collection = db["hardwareSets"]
   return [hw_set["hwName"] for hw_set in collection.find({}, {"hwName": 1, "_id": 0})]







