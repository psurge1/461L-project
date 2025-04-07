# Import necessary libraries and modules
from pymongo import MongoClient

import projectsDB

from dbs import dbs


"""
TO-DO

add encryption to logins

change database to mongoDB --> make database


"""


'''
Structure of User entry:
User = {
    'userId': userId,
    'password': password,
    'projects': [project1_ID, project2_ID, ...]
}
'''

# Function to add a new user
# not encrypted yet
def addUser(client, userId, password) -> dict[str, any]:
    #fix this database
    database = client[dbs.USERSDB.value]
    userCollection = database['users']

    #check already existing logins
    # if userCollection.find_one({'username': username}):
    #     return {"status": "error", "log": "already existing username"}
    if userCollection.find_one({'userId': userId}):
        return {"status": "error", "log": "already existing userId"}

    #create new user
    newUser = {
        'userId' : userId,
        'password' : password,
        'projects' : []
    }

    #add new user into database
    userCollection.insert_one(newUser)
    return {"status": "success", "log": "user added"}


# Helper function to query a user by username and userId
def __queryUser(client, userId):
    database = client[dbs.USERSDB.value]
    userCollection = database['users']

    #query user
    # users = userCollection.find_one({'username' : username, 'userId' : userId})
    users = userCollection.find_one({'userId' : userId})
    return users



# Function to log in a user
def login(client, userId, password) -> dict[str, any]:
    # users = __queryUser(client, username, userId)
    users = __queryUser(client, userId)

    #check matching login
    if users and users['password'] == password:
        return {"status": "success", "log": "login successful", "user": users['userId'], "projects": users['projects']}
    else:
        return {"status": "error", "log": "invalid login"}



# Function to add a user to a project
def joinProject(client, userId, projectId) -> dict[str, any]:
    database = client[dbs.USERSDB.value]
    userCollection = database['users']

    #find user
    users = userCollection.find_one({'userId' : userId})

    #check condition
    if not users:
        return {"status": "error", "log": "wrong user"}
    elif projectId in users['projects']:
        return {"status": "error", "log": "already existing user"}
    
    # dd a project to user's projects
    userCollection.update_one({'userId' : userId}, {'$push': {'projects': projectId}})


    return {"status": "success", "log": "added user to project"}


# inside usersDB.py
def getUserProjectsList(client, userId):
    userCollection = client[dbs.USERSDB.value]['users']
    projectCollection = client[dbs.PROJECTSDB.value]['projects']

    user = userCollection.find_one({'userId': userId})
    if not user or 'projects' not in user:
        return []

    # Now fetch full project info
    project_ids = user['projects']
    projects = list(projectCollection.find({'projectId': {'$in': project_ids}}))

    # Convert ObjectIds to strings
    for proj in projects:
        if '_id' in proj:
            proj['_id'] = str(proj['_id'])

    return projects
