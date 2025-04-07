from pymongo import MongoClient

import hardwareDB

'''
Structure of Project entry:
Project = {
    'projectName': projectName,
    'projectId': projectId,
    'description': description,
    'hwSets': {HW1: 0, HW2: 10, ...},
    'users': [userId1, userId2, ...]
}
'''

def __get_database(client):
    return client["projectDB"]

def queryProject(client, projectId) -> dict[str, any]:
    db = __get_database(client)
    project = db.projects.find_one({'projectId': projectId})
    return {"status": "success", "projectName": project["projectName"], "projectId": project["projectId"], "description": project["description"], "log": ""}

def createProject(client, projectName, projectId, description) -> dict[str, any]:
    db = __get_database(client)
    project = {
        'projectName': projectName,
        'projectId': projectId,
        'description': description,
        'hwSets': {},
        'users': []
    }
    db.projects.insert_one(project)
    return {"status": "success", "log": "Project created successfully."}

### TODO: Needs to add project to user's list of projects
def addUser(client, projectId, userId) -> dict[str, any]:
    db = __get_database(client)
    db.projects.update_one({'projectId': projectId}, {'$addToSet': {'users': userId}})
    return {"status": "success", "log": "User added successfully."}


def updateUsage(client, projectId, hwSetName) -> dict[str, any]:
    db = __get_database(client)
    project = db.projects.find_one({'projectId': projectId})
    if project and hwSetName in project['hwSets']:
        return {"status": "success", "log": project['hwSets'][hwSetName]}
    return {"status": "success", "log": "Hardware set not found in project."}

def checkOutHW(client, projectId, hwSetName, qty, userId) -> dict[str, any]:
    db = __get_database(client)
    project = db.projects.find_one({'projectId': projectId})
    
    if not project:
        return {"status": "error", "log": "Project not found."}
    
    if userId not in project['users']:
        return {"status": "error", "log": "User not part of project."}
    
    # available_qty = hardwareDB.getAvailableQty(hwSetName)
    # if available_qty < qty:
    #     return {"status": "error", "log": "Not enough hardware available."}
    result = hardwareDB.requestSpace(client, hwSetName, qty)
    
    # hardwareDB.updateQty(hwSetName, -qty)
    if result["status"] == "success":
        db.projects.update_one(
            {'projectId': projectId},
            {'$inc': {f'hwSets.{hwSetName}': qty}}
        )
        return {"status": "success", "log": "Hardware checked out successfully."}
    else:
        return {"status": "error", "log": "Hardware not checked out."}

def checkInHW(client, projectId, hwSetName, qty, userId) -> dict[str, any]:
    db = __get_database(client)
    project = db.projects.find_one({'projectId': projectId})
    
    if not project:
        return {"status": "error", "log": "Project not found."}
    
    if userId not in project['users']:
        return {"status": "error", "log": "User not part of project."}
    
    if hwSetName not in project['hwSets'] or project['hwSets'][hwSetName] < qty:
        return {"status": "error", "log": "Invalid hardware return quantity."}
    
    hardwareDB.updateQty(hwSetName, qty)
    db.projects.update_one(
        {'projectId': projectId},
        {'$inc': {f'hwSets.{hwSetName}': -qty}}
    )
    return {"status": "success", "log": "Hardware checked in successfully."}
