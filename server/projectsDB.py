from pymongo import MongoClient

import hardwareDB
from dbs import dbs



def queryProject(client, projectId):
    database = client[dbs.PROJECTSDB.value]
    projectCollection = database['projects']
    return projectCollection.find_one({'projectId': projectId})

def createProject(client, projectName, projectId, description):
    if projectId == "" or projectName == "":
        return {"status": "error", "log": "empty projectId or projectName"}
    
    database = client[dbs.PROJECTSDB.value]
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
    if projectId == "" or userId == "":
        return {"status": "error", "log": "empty projectId or userId"}
    
    projectsDatabase = client[dbs.PROJECTSDB.value]
    projectCollection = projectsDatabase['projects']
    usersDatabase = client[dbs.USERSDB.value]
    userCollection = usersDatabase['users']

    users = userCollection.find_one({'userId' : userId})

    if not users:
        return {"status": "error", "log": "wrong user"}
    # print(projectId, userId)
    project = queryProject(client, projectId)
    # print(project)

    if not project:
        return {"status": "error", "log": "project not found"}
    
    if userId in project['users']:
        return {"status": "error", "log": "user already in project"}
    
    userCollection.update_one({'userId' : userId}, {'$push': {'projects': projectId}})

    projectCollection.update_one(
        {'projectId': projectId},
        {'$push': {'users': userId}}
    )
    return {"status": "success", "log": "user added to project"}

def updateUsage(client, projectId, hwSetName, qty):
    database = client[dbs.PROJECTSDB.value]
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
