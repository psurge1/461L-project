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
        
    
    hardware_usage = {
        hwName: {
            "total": 0,
            "byUser": {}
        } for hwName in hw_query["hwnames"]
    }

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

def updateUsage(client, projectId, hwSetName, qty, userId):
    db = client[dbs.PROJECTSDB.value]
    projectCollection = db["projects"]
    project = projectCollection.find_one({"projectId": projectId})
    
    if not project:
        return {"status": "error", "log": "Project not found"}

    hardware = project.get("hardware", {})
    usage = hardware.get(hwSetName, {"total": 0, "byUser": {}})
    new_usage_qty = usage["total"] + qty

    if new_usage_qty < 0:
        return {"status": "error", "log": "You cannot check in more than you've checked out."}
    
    usage["total"] += qty

    # Update individual user usage
    current_user_qty = usage["byUser"].get(userId, 0)
    new_user_qty = current_user_qty + qty
    usage["byUser"][userId] = new_user_qty
    hardware[hwSetName] = usage

    # Save updates
    projectCollection.update_one(
        {"projectId": projectId},
        {"$set": {f"hardware": hardware}}
    )

    return {
        "status": "success",
        "log": f"{'Checked out' if qty > 0 else 'Checked in'} {abs(qty)} units of {hwSetName}",
        "userUsage": new_user_qty
    }


def checkOutHW(client, projectId, hwSetName, qty, userId):
    project = queryProject(client, projectId)
    if not project:
        return {"status": "error", "log": "Project not found."}

    if userId not in project['users']:
        return {"status": "error", "log": "User not in project."}

    result = hardwareDB.requestSpace(client, hwSetName, qty)
    if result["status"] != "success":
        if result["log"] == "Not enough available hardware.":
            updateUsage(client, projectId, hwSetName, int(result["qty"]))
        return result

    return updateUsage(client, projectId, hwSetName, qty)


# def checkOutHW(client, projectId, hwSetName, qty, userId):
#     project = queryProject(client, projectId)
#     if not project:
#         return {"status": "error", "log": "Project not found."}

#     if userId not in project['users']:
#         return {"status": "error", "log": "User not in project."}

#     result = hardwareDB.requestSpace(client, hwSetName, qty)
#     if result["status"] != "success":
#         return result

#     return updateUsage(client, projectId, hwSetName, qty)


def removeUser(client, projectId, userId):
    if not projectId or not userId:
        return {"status": "error", "log": "missing projectId or userId"}

    projectCollection = client[dbs.PROJECTSDB.value]['projects']
    userCollection = client[dbs.USERSDB.value]['users']

    projectCollection.update_one(
        {'projectId': projectId},
        {'$pull': {'users': userId}}
    )
    userCollection.update_one(
        {'userId': userId},
        {'$pull': {'projects': projectId}}
    )

    return {"status": "success", "log": "user removed from project"}
