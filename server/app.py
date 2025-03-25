# Import necessary libraries and modules
from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient

# Import custom modules for database interactions
import usersDB
import projectsDB
import hardwareDB

# Define the MongoDB connection string
MONGODB_SERVER = "mongodb+srv://ericshi:AmX57b9CnFTCBX9P@users.h6xkw.mongodb.net/"

# Initialize a new Flask web application
app = Flask(__name__)
client = MongoClient(MONGODB_SERVER)
db = client.get_database()

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    # Extract data from request (e.g., username and password)
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = usersDB.authenticate_user(db, username, password)
    
    # Check if user exists and return a JSON response
    if user:
        return jsonify({'status': 'success', 'user': user})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401


# Route for the main page (Work in progress)
@app.route('/main')
def mainPage():
    # Extract data from request

    # Connect to MongoDB

    # Fetch user projects using the usersDB module
    projects = usersDB.getUserProjectsList()

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for joining a project
@app.route('/join_project', methods=['POST'])
def join_project():
    # Extract data from request

    # Connect to MongoDB

    # Attempt to join the project using the usersDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})


# Route for adding a new user (Signup)
@app.route('/add_user', methods=['POST'])
def add_user():
    # Extract data from request
    data = request.get_json()
    username = data.get('username')
    userID = data.get('userid')
    password = data.get('password')

    # Basic validation
    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required.'}), 400
    
    # Connect to MongoDB
    # print(client)

    # Attempt to add the user using the usersDB module
    # It is assumed that usersDB.add_user returns True if the user is added successfully
    result = usersDB.addUser(db, username, userID, password)
    
    if result:
        return jsonify({'status': 'success', 'message': 'User added successfully.'})
    else:
        return jsonify({'status': 'error', 'message': 'Signup failed. User may already exist.'}), 400

# Route for getting the list of user projects
@app.route('/get_user_projects_list', methods=['GET'])
def get_user_projects_list():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    userid = data.get('userid')
    
    result = get_user_projects_list(client, userid)
    
    if result != None:
        return jsonify({
            'status' : 'success',
            'result' : result
            })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Getting user projects failed. User may not exist.'
            })

# Route for creating a new project
@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.get_json()
    userid = data.get('userid')
    project_name = data.get('projectname')
    projectid = data.get('projectid')
    description = data.get('description')

    projectsDB.createProject(client, project_name, projectid, description)
    projectsDB.addUser(client, projectid, userid)

    return jsonify({})

# Route for getting project information
@app.route('/get_project_info', methods=['GET'])
def get_project_info():
    data = request.get_json()
    projectid = data.get('projectid')
    projectsDB.queryProject(client, projectid)

    return jsonify({})

# Route for getting all hardware names
@app.route('/get_all_hw_names', methods=['GET'])
def get_all_hw_names():
    return hardwareDB.getAllHwNames(client)

    # return jsonify({})

# Route for getting hardware information
@app.route('/get_hw_info', methods=['GET'])
def get_hw_info():
    data = request.get_json()
    hw_set_name = data.get('hw-set-name')
    return hardwareDB.queryHardwareSet(client, hw_set_name)
    # return jsonify({})

# Route for checking out hardware
@app.route('/check_out', methods=['PUT'])
def check_out():
    # Extract data from request

    # Connect to MongoDB

    # Attempt to check out the hardware using the projectsDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for checking in hardware
@app.route('/check_in', methods=['PUT'])
def check_in():
    # Extract data from request

    # Connect to MongoDB

    # Attempt to check in the hardware using the projectsDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for creating a new hardware set
@app.route('/create_hardware_set', methods=['POST'])
def create_hardware_set():
    # Extract data from request

    # Connect to MongoDB

    # Attempt to create the hardware set using the hardwareDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for checking the inventory of projects
@app.route('/api/inventory', methods=['GET'])
def check_inventory():
    # Connect to MongoDB

    # Fetch all projects from the HardwareCheckout.Projects collection

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

@app.teardown_appcontext
def close_db():
    client.close()

# Main entry point for the application
if __name__ == '__main__':
    app.run()

