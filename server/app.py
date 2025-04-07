# Import necessary libraries and modules
from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient

# Import custom modules for database interactions
import usersDB
import projectsDB
import hardwareDB

# Define the MongoDB connection string
MONGODB_SERVER2 = "mongodb+srv://ericshi:AmX57b9CnFTCBX9P@cluster0.bts3jlz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Initialize a new Flask web application
app = Flask(__name__)
client = MongoClient(MONGODB_SERVER2)

# Route for user login
# Tested with postman
@app.route('/login', methods=['POST'])
def login():
    # Extract data from request (e.g., username and password)
    data = request.args
    userId = data.get('userId')
    password = data.get('password')

    ## encryptedUserId = utils.encrypt(userId)
    ## encryptedPassword = utils.encrypt(password)
    
    attempt = usersDB.login(client, userId, password)

    if attempt["status"] == "success":
        return jsonify(attempt)
    else:
        return jsonify(attempt), 401


@app.route('/test', methods=['GET'])
def test():
    try:
        client.admin.command("ping")
    except Exception as e:
        return {"status": str(e)}
    return {"status": "success"}

# Route for joining a project
@app.route('/join_project', methods=['POST'])
def join_project():
    data = request.args
    projectId = data["projectId"]
    userId = data["userId"]
    
    result = usersDB.addUser(client, projectId, userId)

    return jsonify(result)


# Route for adding a new user (Signup)
# Tested with postman
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.args
    userId = data.get('userId')
    password = data.get('password')

    if not userId or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required.'}), 400
    
    result = usersDB.addUser(client, userId, password)
    
    if result:
        return jsonify({'status': 'success', 'message': 'User added successfully.'})
    else:
        return jsonify({'status': 'error', 'message': 'Signup failed. User may already exist.'}), 400

# Route for getting the list of user projects
# Tested with postman
@app.route('/get_user_projects_list', methods=['GET'])
def get_user_projects_list():
    data = request.args
    userId = data.get('userId')
    
    result = usersDB.getUserProjectsList(client, userId)
    
    return jsonify(result)
    # if result != None:
    #     return jsonify({
    #         'status' : 'success',
    #         'result' : result
    #         })
    # else:
    #     return jsonify({
    #         'status': 'error',
    #         'message': 'Getting user projects failed. User may not exist.'
    #         })

# Route for creating a new project
# Tested with postman
### TODO: Check for duplicate project IDS
@app.route('/create_project', methods=['POST', 'PUT'])
def create_project():
    data = request.args
    userId = data.get('userId')
    projectName = data.get('projectName')
    projectId = data.get('projectId')
    description = data.get('description')

    rOne = projectsDB.createProject(client, projectName, projectId, description)
    rTwo = projectsDB.addUser(client, projectId, userId)

    return jsonify({
        "createProject": rOne,
        "addUserToProject": rTwo
    })

# Route for getting project information
# Tested with postman
@app.route('/get_project_info', methods=['GET'])
def get_project_info():
    data = request.args
    projectid = data.get('projectId')
    result = projectsDB.queryProject(client, projectid)

    return jsonify(result)

# Route for getting all hardware names
@app.route('/get_all_hw_names', methods=['GET'])
def get_all_hw_names():
    return jsonify(hardwareDB.getAllHwNames(client))

    # return jsonify({})

# Route for getting hardware information
@app.route('/get_hw_info', methods=['GET'])
def get_hw_info():
    data = request.args
    hw_set_name = data.get('hwSetName')
    return jsonify(hardwareDB.queryHardwareSet(client, hw_set_name))
    # return jsonify({})

# Route for checking out hardware
@app.route('/check_out', methods=['PUT'])
def check_out():
    data = request.args
    hwSetName = data["hwSetName"]
    amount = data["amount"]
    projectId = data["projectId"]
    userId = data["userId"]

    projCheckinResult = projectsDB.checkInHW(client, projectId, hwSetName, amount, userId)
    return jsonify(projCheckinResult)

# Route for checking in hardware
@app.route('/check_in', methods=['PUT'])
def check_in():
    data = request.args
    hwSetName = data["hwSetName"]
    amount = data["amount"]
    projectId = data["projectId"]
    userId = data["userId"]

    projCheckoutResult = projectsDB.checkOutHW(client, projectId, hwSetName, amount, userId)
    return jsonify(projCheckoutResult)

# Route for creating a new hardware set
# Tested with postman
@app.route('/create_hardware_set', methods=['POST'])
def create_hardware_set():
    # Extract data from request
    data = request.args
    hwSetName = data["hwSetName"]
    initCapacity = data["capacity"]


    # Attempt to create the hardware set using the hardwareDB module
    result = hardwareDB.createHardwareSet(client, hwSetName, initCapacity)

    # Return a JSON response
    return jsonify(result)

# Route for checking the inventory of projects
@app.route('/api/inventory', methods=['GET']) # What is this used for?
def check_inventory():
    # Connect to MongoDB

    # Fetch all projects from the HardwareCheckout.Projects collection

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# @app.teardown_appcontext
# def close_db(error=None):
#     client.close()

# Main entry point for the application
if __name__ == '__main__':
    app.run()

