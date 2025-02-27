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

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    # Extract data from request (e.g., username and password)
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)
    db = client.get_database()  # or specify the database name, e.g., client['your_db']
    
    # Attempt to log in the user using the usersDB module
    user = usersDB.authenticate_user(db, username, password)
    
    # Close the MongoDB connection
    client.close()
    
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
    password = data.get('password')

    # Basic validation
    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required.'}), 400
    
    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)
    print(client)
    db = client.get_database()  # or specify the database name

    # Attempt to add the user using the usersDB module
    # It is assumed that usersDB.add_user returns True if the user is added successfully
    result = usersDB.add_user(db, username, password)
    
    # Close the MongoDB connection
    client.close()
    
    if result:
        return jsonify({'status': 'success', 'message': 'User added successfully.'})
    else:
        return jsonify({'status': 'error', 'message': 'Signup failed. User may already exist.'}), 400

# Route for getting the list of user projects
@app.route('/get_user_projects_list', methods=['POST'])
def get_user_projects_list():
    # Extract data from request

    # Connect to MongoDB

    # Fetch the user's projects using the usersDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for creating a new project
@app.route('/create_project', methods=['POST'])
def create_project():
    # Extract data from request

    # Connect to MongoDB

    # Attempt to create the project using the projectsDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for getting project information
@app.route('/get_project_info', methods=['POST'])
def get_project_info():
    # Extract data from request

    # Connect to MongoDB

    # Fetch project information using the projectsDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for getting all hardware names
@app.route('/get_all_hw_names', methods=['POST'])
def get_all_hw_names():
    # Connect to MongoDB

    # Fetch all hardware names using the hardwareDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for getting hardware information
@app.route('/get_hw_info', methods=['POST'])
def get_hw_info():
    # Extract data from request

    # Connect to MongoDB

    # Fetch hardware set information using the hardwareDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for checking out hardware
@app.route('/check_out', methods=['POST'])
def check_out():
    # Extract data from request

    # Connect to MongoDB

    # Attempt to check out the hardware using the projectsDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for checking in hardware
@app.route('/check_in', methods=['POST'])
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

# Main entry point for the application
if __name__ == '__main__':
    app.run()

