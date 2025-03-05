from pymongo import MongoClient

def get_database(client):
    return client["hardwareDB"]

def createHardwareSet(client, hwSetName, initCapacity):
    db = get_database(client)
    collection = db["hardwareSets"]
    if collection.find_one({"hwName": hwSetName}):
        print("Hardware set already exists.")
        return
    hardware_set = {
        "hwName": hwSetName,
        "capacity": initCapacity,
        "availability": initCapacity
    }
    collection.insert_one(hardware_set)
    print("Hardware set created successfully.")

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
        print("Availability updated successfully.")
    else:
        print("Hardware set not found.")

def requestSpace(client, hwSetName, amount):
    db = get_database(client)
    collection = db["hardwareSets"]
    hw_set = collection.find_one({"hwName": hwSetName})
    if not hw_set:
        print("Hardware set not found.")
        return
    if hw_set["availability"] >= amount:
        collection.update_one(
            {"hwName": hwSetName},
            {"$inc": {"availability": -amount}}
        )
        print("Space allocated successfully.")
    else:
        print("Not enough available hardware.")

def getAllHwNames(client):
    db = get_database(client)
    collection = db["hardwareSets"]
    return [hw_set["hwName"] for hw_set in collection.find({}, {"hwName": 1, "_id": 0})]


