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
    'username': username,
    'userId': userId,
    'password': password,
    'projects': [project1_ID, project2_ID, ...]
}
'''

# Function to add a new user
#not encrypted yet
def addUser(client, username, userId, password):
    #fix this database
    database = client['database']
    userCollection = database['users']

    #check already existing logins
    if userCollection.find_one({'username': username}):
        return {"error": "already existing username"}
    if userCollection.find_one({'userId': userId}):
        return {"error": "already existing userId"}

    #create new user
    newUser = {
        'username' : username,
        'userId' : userId,
        'password' : password,
        'projects' : []
    }

    #add new user into database
    userCollection.insert_one(newUser)
    return {"log": "user added"}


# Helper function to query a user by username and userId
def __queryUser(client, username, userId):
    database = client['database']
    userCollection = database['users']

    #query user
    users = userCollection.find_one({'username' : username, 'userId' : userId})
    return users



# Function to log in a user
def login(client, username, userId, password):
    users = __queryUser(client, username, userId)

    #check matching login
    if users and users['password'] == password:
        return {"log": "login successful", "user": users}
    else:
        return {"error": "unvalid login"}


# Function to add a user to a project
def joinProject(client, userId, projectId):
    database = client['database']
    userCollection = database['users']

    #find user
    users = userCollection.find_one({'userId' : userId})

    #check condition
    if not users:
        return {"error": "wrong user"}
    elif projectId in users['projects']:
        return {"error": "already existing user"}
    
    # dd a project to user's projects
    userCollection.update_one({'userId' : userId}, {'$push': {'projects': projectId}})


    return {"log": "added user to project"}

# Function to get the list of projects for a user
def getUserProjectsList(client, userId):
    database = client['database']
    userCollection = database['users']

    #find user
    users = userCollection.find_one({'userId' : userId})

    if users:
            return{"projects": users['projects']}
    else:
            return{"error": "user doesn't exist"}
