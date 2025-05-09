from pymongo import MongoClient


def __get_database(client):
    return client["hardwareDB"]

def createHardwareSet(client, hwSetName, initCapacity) -> dict[str, any]:
    db = __get_database(client)
    collection = db["hardwareSets"]
    initCapacity = int(initCapacity)
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
    db = __get_database(client)
    collection = db["hardwareSets"]
    hwSet = collection.find_one({"hwName": hwSetName})
    if hwSet is not None:
        hwSet.pop("_id", None)
        return {"status": "success", "log": "successfully retrieved hardware set", "hwset": hwSet}
    else:
        return {"status": "error", "log": "Hardware set doesn't exist"}

def updateAvailability(client, hwSetName, newAvailability) -> dict[str, any]:
    db = __get_database(client)
    collection = db["hardwareSets"]
    result = collection.update_one(
        {"hwName": hwSetName},
        {"$set": {"availability": int(newAvailability)}}
    )
    if result.matched_count:
        return {"status": "success", "log": "Availability updated successfully."}
    else:
        return {"status": "error", "log": "Hardware set not found."}

def incAvailability(client, hwSetName, amount) -> dict[str, any]:
    db = __get_database(client)
    collection = db["hardwareSets"]
    hw_set = collection.find_one({"hwName": hwSetName})
    if not hw_set:
        return {"status": "error", "log": "Hardware set not found."}
    if int(hw_set["availability"]) + int(amount) <= int(hw_set["capacity"]):
        collection.update_one(
            {"hwName": hwSetName},
            {"$inc": {"availability": int(amount)}}
        )
        return {"status": "success", "log": "Hardware Availability Incremented."}
    else:
        return {"status": "error", "log": "Too much hardware."}

def requestSpace(client, hwSetName, amount) -> dict[str, any]:
    db = __get_database(client)
    collection = db["hardwareSets"]
    hw_set = collection.find_one({"hwName": hwSetName})
    if not hw_set:
        return {"status": "error", "log": "Hardware set not found."}
    if int(hw_set["availability"]) >= int(amount):
        collection.update_one(
            {"hwName": hwSetName},
            {"$inc": {"availability": -int(amount)}}
        )
        return {"status": "success", "log": "Space allocated successfully."}
    else:
        collection.update_one(
            {"hwName": hwSetName},
            {"$set": {"availability": 0}}
        )
        return {"status": "semierror", "log": "Not enough available hardware.", "qty": int(hw_set["availability"])}

def getAllHwNames(client) -> dict[str, any]:
    db = __get_database(client)
    collection = db["hardwareSets"]
    return {
        "status": "success",
        "log": "Retrieved all hardware names.",
        "hwnames": [hw_set["hwName"] for hw_set in collection.find({}, {"hwName": 1, "_id": 0})]
    }
