from pymongo import MongoClient

import hardwareDB

'''
Structure of Project entry:
Project = {
    'projectName': projectName,
    'projectId': projectId,
    'description': description,
    'hwSets': {HW1: 0, HW2: 10, ...},
    'users': [user1, user2, ...]
}
'''

def queryProject(client, projectId):
    db = client['projectDB']
    project = db.projects.find_one({'projectId': projectId})
    return project

def createProject(client, projectName, projectId, description):
    db = client['projectDB']
    project = {
        'projectName': projectName,
        'projectId': projectId,
        'description': description,
        'hwSets': {},
        'users': []
    }
    db.projects.insert_one(project)
    return "Project created successfully."

def addUser(client, projectId, userId):
    db = client['projectDB']
    db.projects.update_one({'projectId': projectId}, {'$addToSet': {'users': userId}})
    return "User added successfully."

def updateUsage(client, projectId, hwSetName):
    db = client['projectDB']
    project = db.projects.find_one({'projectId': projectId})
    if project and hwSetName in project['hwSets']:
        return project['hwSets'][hwSetName]
    return "Hardware set not found in project."

def checkOutHW(client, projectId, hwSetName, qty, userId):
    db = client['projectDB']
    project = db.projects.find_one({'projectId': projectId})
    
    if not project:
        return "Project not found."
    
    if userId not in project['users']:
        return "User not part of project."
    
    available_qty = hardwareDB.getAvailableQty(hwSetName)
    if available_qty < qty:
        return "Not enough hardware available."
    
    hardwareDB.updateQty(hwSetName, -qty)
    db.projects.update_one(
        {'projectId': projectId},
        {'$inc': {f'hwSets.{hwSetName}': qty}}
    )
    return "Hardware checked out successfully."

def checkInHW(client, projectId, hwSetName, qty, userId):
    db = client['projectDB']
    project = db.projects.find_one({'projectId': projectId})
    
    if not project:
        return "Project not found."
    
    if userId not in project['users']:
        return "User not part of project."
    
    if hwSetName not in project['hwSets'] or project['hwSets'][hwSetName] < qty:
        return "Invalid hardware return quantity."
    
    hardwareDB.updateQty(hwSetName, qty)
    db.projects.update_one(
        {'projectId': projectId},
        {'$inc': {f'hwSets.{hwSetName}': -qty}}
    )
    return "Hardware checked in successfully."
