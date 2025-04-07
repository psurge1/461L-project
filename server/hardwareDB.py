from pymongo import MongoClient

from dbs import dbs


def createHardwareSet(client, hwSetName, initCapacity) -> dict[str, any]:
    db = client[dbs.HARDWAREDB.value]
    collection = db["hardwareSets"]
    if collection.find_one({"hwName": hwSetName}):
        return {"status": "error", "log": "Hardware set already exists."}
    hardware_set = {
        "hwName": hwSetName,
        "capacity": initCapacity,
        "availability": initCapacity
    }
    collection.insert_one(hardware_set)
    return {"status": "success", "log": "Hardware set created successfully."}

def queryHardwareSet(client, hwSetName) -> dict[str, any]:
    db = client[dbs.HARDWAREDB.value]
    collection = db["hardwareSets"]
    hwSet = collection.find_one({"hwName": hwSetName})
    if hwSet != None:
        return {"status": "success", "log": "successfully retrieved hardware set", "hwset": hwSet}
    else:
        return {"status": "error", "log": "Hardware set doesn't exist"}

def updateAvailability(client, hwSetName, newAvailability) -> dict[str, any]:
    db = client[dbs.HARDWAREDB.value]
    collection = db["hardwareSets"]
    result = collection.update_one(
        {"hwName": hwSetName},
        {"$set": {"availability": newAvailability}}
    )
    if result.matched_count:
        return {"status": "success", "log": "Availability updated successfully."}
    else:
        return {"status": "error", "log": "Hardware set not found."}

def incAvailability(client, hwSetName, amount) -> dict[str, any]:
    db = client[dbs.HARDWAREDB.value]
    collection = db["hardwareSets"]
    hw_set = collection.find_one({"hwName": hwSetName})
    if not hw_set:
        return {"status": "error", "log": "Hardware set not found."}
    if hw_set["availability"] + amount <= hw_set["capacity"]:
        collection.update_one(
            {"hwName": hwSetName},
            {"$inc": {"availability": amount}}
        )
        return {"status": "success", "log": "Hardware Availability Incremented."}
    else:
        return {"status": "error", "log": "Too much hardware."}

def requestSpace(client, hwSetName, amount) -> dict[str, any]:
    db = client[dbs.HARDWAREDB.value]
    collection = db["hardwareSets"]
    hw_set = collection.find_one({"hwName": hwSetName})
    if not hw_set:
        return {"status": "error", "log": "Hardware set not found."}
    if hw_set["availability"] >= amount:
        collection.update_one(
            {"hwName": hwSetName},
            {"$inc": {"availability": -amount}}
        )
        return {"status": "success", "log": "Space allocated successfully."}
    else:
        return {"status": "error", "log": "Not enough available hardware."}

def getAllHwNames(client) -> dict[str, any]:
    db = client[dbs.HARDWAREDB.value]
    collection = db["hardwareSets"]
    return {
        "status": "success", 
        "log": "Retrieved all hardware names.", 
        "hwnames": [hw_set["hwName"] for hw_set in collection.find({}, {"hwName": 1, "_id": 0})]
        }