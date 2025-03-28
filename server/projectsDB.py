from pymongo import MongoClient

import hardwareDB


def __getDatabase(client):
    return client["projectsDB"]


def queryProject(client, projectId):
    database = __getDatabase(client)
    projectCollection = database['projects']
    return projectCollection.find_one({'projectId': projectId})

def createProject(client, projectName, projectId, description):
    database = __getDatabase(client)
    projectCollection = database['projects']

    if projectCollection.find_one({'projectId': projectId}):
        return {"status": "error", "log": "project already exists"}
    
    hw_query = hardwareDB.getAllHwNames(client)
    if hw_query["status"] != "success":
        return {"status": "error", "log": "Failed to retrieve hardware sets."}
    
    hardware_usage = {hwName: 0 for hwName in hw_query["hwnames"]}

    newProject = {
        'projectId': projectId,
        'projectName': projectName,
        'description': description,
        'users': [],
        'hardware': hardware_usage,
    }

    projectCollection.insert_one(newProject)
    return {"status": "success", "log": "project created"}

def addUser(client, projectId, userId):
    database = __getDatabase(client)
    projectCollection = database['projects']

    project = queryProject(client, projectId)

    if not project:
        return {"status": "error", "log": "project not found"}
    
    if userId in project['users']:
        return {"status": "error", "log": "user already in project"}

    projectCollection.update_one(
        {'projectId': projectId},
        {'$push': {'users': userId}}
    )
    return {"status": "success", "log": "user added to project"}

def updateUsage(client, projectId, hwSetName, qty):
    database = __getDatabase(client)
    projectCollection = database['projects']
    project = queryProject(client, projectId)

    if not project:
        return {"status": "error", "log": "project not found"}

    current = project['hardware'].get(hwSetName, 0)
    new_val = current + qty

    projectCollection.update_one(
        {'projectId': projectId},
        {'$set': {f'hardware.{hwSetName}': new_val}}
    )

    action = "checked out" if qty > 0 else "checked in"
    log_message = f"{action} {abs(qty)} units of {hwSetName}"
    
    return {
        "status": "success",
        "log": log_message,
        "newUsage": new_val
    }

def checkOutHW(client, projectId, hwSetName, qty, userId):
    project = queryProject(client, projectId)
    if not project:
        return {"status": "error", "log": "Project not found."}

    if userId not in project['users']:
        return {"status": "error", "log": "User not in project."}

    result = hardwareDB.requestSpace(client, hwSetName, qty)
    if result["status"] != "success":
        return result

    return updateUsage(client, projectId, hwSetName, qty)


def checkOutHW(client, projectId, hwSetName, qty, userId):
    project = queryProject(client, projectId)
    if not project:
        return {"status": "error", "log": "Project not found."}

    if userId not in project['users']:
        return {"status": "error", "log": "User not in project."}

    result = hardwareDB.requestSpace(client, hwSetName, qty)
    if result["status"] != "success":
        return result

    return updateUsage(client, projectId, hwSetName, qty)
