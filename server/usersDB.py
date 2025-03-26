# Import necessary libraries and modules
from pymongo import MongoClient

import projectsDB




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

def __getDatabase(client):
    return client["usersDB"]

# Function to add a new user
#not encrypted yet
def addUser(client, userId, password) -> dict[str, any]:
    #fix this database
    database = __getDatabase(client)
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
    database = __getDatabase(client)
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
    database = __getDatabase(client)
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

# Function to get the list of projects for a user
def getUserProjectsList(client, userId) -> dict[str, any]:
    database = __getDatabase(client)
    userCollection = database['users']

    #find user
    users = userCollection.find_one({'userId' : userId})

    if users:
        return {"status": "success", "log": "successfully retrieved projects", "projects": users['projects']}
    else:
        return {"status": "error", "log": "user doesn't exist"}
