# Import necessary libraries and modules
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import certifi
from dbs import dbs



# Import custom modules for database interactions
import usersDB
import projectsDB
import hardwareDB

# Define the MongoDB connection string
MONGODB_SERVER = "mongodb+srv://ericshi:AmX57b9CnFTCBX9P@cluster0.bts3jlz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

app = Flask(__name__, static_folder="build", static_url_path="")
CORS(app)  # This will allow CORS for all routes
client = MongoClient(MONGODB_SERVER,
    tls=True,
    tlsCAFile=certifi.where())

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')


@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')


def encrypt(inputText, N, D):
    if N < 1:
        raise ValueError("N must be >= 1.")
    if D not in [1, -1]:
        raise ValueError("Invalid direction.")
    re_text = inputText[::-1]
    encrypted_chars = []
    for ch in re_text:
        temp = ord(ch) - 34
        shifted_temp = (temp + (D * N)) % 93
        encrypted_ascii = shifted_temp + 34
        encrypted_chars.append(chr(encrypted_ascii))
    return "".join(encrypted_chars)

def decrypt(encryptedText, N, D):
    if N < 1:
        raise ValueError("N must be >= 1.")
    if D not in [1, -1]:
        raise ValueError("Invalid direction.")
    shifted_chars = []
    for ch in encryptedText:
        temp = ord(ch) - 34
        shifted_offset = (temp - (D * N)) % 93
        encrypted_ascii = shifted_offset + 34
        shifted_chars.append(chr(encrypted_ascii))
    return "".join(shifted_chars)[::-1]


# Tested with postman
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    userId = data.get('userId')
    password = data.get('password')

    encryptedUserId = encrypt(userId, 5, 1)
    encryptedPassword = encrypt(password, 5, 1)

    attempt = usersDB.login(client, encryptedUserId, encryptedPassword)

    if attempt["status"] == "success":
        return jsonify(attempt)
    else:
        return jsonify(attempt), 401


@app.route('/main')
def mainPage():
    data = request.args

    try:
        client.admin.command("ping")
        print("Successfully connected")
    except Exception as e:
        print(e)
    return jsonify(data)


@app.route('/join_project', methods=['POST'])
def join_project():
    data = request.args
    projectId = data.get("projectId")
    userId = data.get("userId")

    if not userId or not projectId:
        return jsonify({"status": "error", "message": "Missing userId or projectId"}), 400

    encryptedUserId = encrypt(userId, 5, 1)

    result = projectsDB.addUser(client, projectId, encryptedUserId)
    return jsonify(result)


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    userId = data.get('userId')
    password = data.get('password')

    if not userId or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required.'}), 400

    encryptedUserId = encrypt(userId, 5, 1)
    encryptedPassword = encrypt(password, 5, 1)

    result = usersDB.addUser(client, encryptedUserId, encryptedPassword)

    if result:
        return jsonify({'status': 'success', 'message': 'User added successfully.'})
    else:
        return jsonify({'status': 'error', 'message': 'Signup failed. User may already exist.'}), 400

@app.route('/get_user_projects_list', methods=['GET'])
def get_user_projects_list():
    data = request.args
    userId = data.get('userId')

    if not userId:
        return jsonify({"status": "error", "message": "Missing userId"}), 400

    encryptedUserId = encrypt(userId, 5, 1)

    result = usersDB.getUserProjectsList(client, encryptedUserId)
    return jsonify({"projects": result})


@app.route('/create_project', methods=['POST', 'PUT'])
def create_project():
    data = request.args
    userId = data.get('userId')
    projectName = data.get('projectName')
    projectId = data.get('projectId')
    description = data.get('description')

    if not userId or not projectId:
        return jsonify({"status": "error", "message": "Missing userId or projectId"}), 400

    encryptedUserId = encrypt(userId, 5, 1)

    rOne = projectsDB.createProject(client, projectName, projectId, description)
    if rOne["status"] == "error":
        return jsonify(rOne), 400

    rTwo = projectsDB.addUser(client, projectId, encryptedUserId)
    if rTwo["status"] == "error":
        return jsonify(rTwo), 400

    return jsonify({"status": "success", "log": "project created", "projectId": projectId})


@app.route('/leave_project', methods=['POST'])
def leave_project():
    data = request.args
    projectId = data.get("projectId")
    userId = data.get("userId")

    if not userId or not projectId:
        return jsonify({"status": "error", "message": "Missing userId or projectId"}), 400

    encryptedUserId = encrypt(userId, 5, 1)

    result = projectsDB.removeUser(client, projectId, encryptedUserId)
    return jsonify(result)


@app.route('/get_project_info', methods=['GET'])
def get_project_info():
    data = request.args
    projectid = data.get('projectId')
    result = projectsDB.queryProject(client, projectid)

    if result and '_id' in result:
        result['_id'] = str(result['_id'])

    return jsonify({"status": "success", "result": result})

@app.route('/get_all_hw_names', methods=['GET'])
def get_all_hw_names():
    return jsonify(hardwareDB.getAllHwNames(client))


@app.route('/get_hw_info', methods=['GET'])
def get_hw_info():
    data = request.args
    hw_set_name = data.get('hwSetName')
    return jsonify(hardwareDB.queryHardwareSet(client, hw_set_name))


@app.route('/check_out', methods=['POST'])
def checkout():
    data = request.get_json()
    hwSetName = data["setNumber"]
    amount = int(data["amount"])
    projectId = data["projectId"]
    userId = data["userId"]
    encryptedUserId = encrypt(userId, 5, 1)

    overflow = False
    # Step 1: Reserve hardware
    result = hardwareDB.requestSpace(client, hwSetName, amount)
    if result["status"] != "success":
        if result["status"] == "semierror":
            amount = result["qty"]
            overflow = True
        else:
            return jsonify(result), 400

    # Step 2: Update project usage
    usage_result = projectsDB.updateUsage(client, projectId, hwSetName, amount, encryptedUserId)
    if usage_result["status"] != "success":
        return jsonify(usage_result), 400

    if overflow:
        return jsonify({"status": "semierror", "log": usage_result["log"]})
    return jsonify(usage_result)


@app.route('/check_in', methods=['POST'])
def checkin():
    data = request.get_json()
    hwSetName = data["setNumber"]
    amount = int(data["amount"])
    projectId = data["projectId"]
    userId = data["userId"]

    encryptedUserId = encrypt(userId, 5, 1)

    result = projectsDB.updateUsage(client, projectId, hwSetName, -amount, encryptedUserId)
    if result["status"] != "success":
        return jsonify(result), 400
    
    result2 = hardwareDB.incAvailability(client, hwSetName, amount)
    return jsonify(result2)



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

