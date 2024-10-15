"""
sprints.py handles all communication between the frontend and the backend using api calls
and any additional logic as required for the sprints.
"""

from pymongo import MongoClient
from services import *
from services import incomplete
from controllers import *
from routes import *
from validation.sprints_validation import is_sprint_date_valid
from flask import make_response, jsonify, request
from application import app
from bson.objectid import ObjectId
from flask_cors import CORS

#Allow CORS (temporarily allow all origins)
CORS(app, origins="*")

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

# Get entire collection
@app.route(tasks_routes_public.SPRINTS, methods=['GET'])
def get_all_sprints():
    """
    get_all_sprints connects the get_all method to the api by providing the logic required to convert the collection to a json file.

    Inputs -
        None

    Returns -
        A response with either a jsonified table, or 404 if the table isn't found.
    """
    table = getter.get_all("sprints")

    # parse datetime object to only include date
    for sprint in table:
        sprint["startDate"] = sprint["startDate"].strftime("%Y-%m-%d")
        sprint["endDate"] = sprint["endDate"].strftime("%Y-%m-%d")

    # parse all task ids to string
    for sprint in table:
        for i in range(len(sprint["tasks"])):
            sprint["tasks"][i] = str(sprint["tasks"][i])

    # If no sprints are found, return 404
    if table == None:
        response = make_response(jsonify({"error": "No sprints found."}), 404)
    else:
        response = make_response(jsonify(table), 200)

    response.headers['Content-Type'] = 'application/json'
    return response

# Define the DELETE endpoint for Sprints
@app.route(tasks_routes_public.SPRINTS, methods=['DELETE'])
def sprints_delete():
    """
    sprints_delete requests a sprint in the form of a json/dict from the front end
    and runs a function to delete the matching data from the database.

    Inputs -
        None

    Returns -
        Returns a 200 response if deletion is successful, 404 if the data entry could not be found.
    """
    requestItem = request.get_json()

    # Check if the request body contains the _id
    if "_id" not in requestItem:
        return make_response(jsonify({"error": "No _id provided in the request."}), 400)

    try:
        oid = ObjectId(requestItem["_id"])  # Convert the string ID to ObjectId
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)


    result = delete.delete_sprint(oid)

    if result == 200:
        ret = make_response(jsonify({"message": f"Entry with oid: {str(oid)} in sprints table deleted."}), 200)
    else:
        ret = make_response(jsonify({"error": "Entry not found."}), 404)

    ret.status_code = result
    return ret

@app.route(tasks_routes_public.SPRINTS, methods=['POST'])
def sprints_add():
    request_data = request.json
    
    #Add the {totalSprintPoints : null} to request_data
    request_data["totalSprintPoints"] = 0

    try:

        # Call the add_sprint function if dates are valid
        status_code, result = add.add_one("sprints", request_data)

        if status_code == 200:
            result["_id"] = str(result["_id"])
            result["startDate"] = result["startDate"].strftime("%d-%m-%Y")
            result["endDate"] = result["endDate"].strftime("%d-%m-%Y")

            return make_response(jsonify({
                "message": "Sprint added successfully.",
                "sprintId": result["_id"],  # Return the ID of the added sprint
                "sprint": result
            }), 200)
        else:
            return make_response(jsonify({"error": result}), status_code)

    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)


@app.route(tasks_routes_public.SPRINTS, methods=['PATCH'])
def sprints_move_in():
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({"error": "Invalid JSON or Content-Type not set to application/json"}), 400)

    # Check if the input is a list of tasks
    if not isinstance(request_data, list):
        return make_response(jsonify({"error": "Expected a list of tasks"}), 400)

    # Validate required fields in each task
    required_fields = ["originalSprint", "assignee", "creationDate", "description", "_id", "priority", "progress", "sprint", "status", "storyPoints", "tags", "taskName"]

    for task in request_data:
        for field in required_fields:
            if field not in task:
                return make_response(jsonify({"error": f"Missing required field: {field} in task: {task.get('taskName', 'Unknown')}"}), 400)

    # Process the tasks
    status_code, result = move.into_sprint(request_data)

    if status_code == 200:
        return make_response(jsonify({"message": "All tasks processed successfully", "processed_tasks": result}), 200)
    else:
        return make_response(jsonify({"error": result}), status_code)



@app.route(tasks_routes_public.SPRINTS_START, methods=['PATCH'])
def sprint_force_start():
    try:
        # Get the sprint to be force-started
        sprintID = request.args.get("sprintID")
        if sprintID == None:
            return make_response(jsonify({"error": "Sprint ID not provided"}), 400)

        # Call the helper function to update the sprint status
        statusCode, result = force_start.force_start(sprintID)

        if statusCode != 200:
            return make_response(jsonify({"Error": result}), statusCode)
        elif statusCode == 200:
            result["_id"] = str(result["_id"])
            result["startDate"] = result["startDate"].strftime("%d/%m/%Y")
            result["endDate"] = result["endDate"].strftime("%d/%m/%Y")
            return make_response(jsonify(result), statusCode)

    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)

@app.route(tasks_routes_public.SPRINTS_TASKS, methods=['GET'])
def get_tasks():
    # Get the sprintID parameter from the request URL
    sprint_id = request.args.get('sprintID')

    # Check if sprintID is provided
    if not sprint_id:
        return jsonify({"error": "sprintID parameter is required"}), 400

    try:
        # Log the sprint ID received
        print(f"Received sprintID: {sprint_id}")

        # Query the sprints database for the sprint associated with the sprintID
        sprint = db.sprints.find_one({"_id": ObjectId(sprint_id)})

        # Check if the sprint was found
        if not sprint:
            return jsonify({"error": "Sprint not found"}), 404

        # Extract the list of task IDs from the sprint
        task_ids = sprint.get("tasks", [])
        print(f"Found task IDs for sprint: {task_ids}")

        # If no tasks are associated with the sprint
        if not task_ids:
            return jsonify([]), 200

        # Query the tasks database for the tasks using their IDs
        tasks_cursor = db.tasks.find({"_id": {"$in": [ObjectId(task_id) for task_id in task_ids]}})

        # Transform Cursor to List
        tasks_list = []
        for task in tasks_cursor:
            # Convert ObjectId to string for JSON serialization
            task["_id"] = str(task["_id"])
            task["sprint"] = str(task["sprint"])
            tasks_list.append(task)

        # Log the number of tasks found
        print(f"Found {len(tasks_list)} tasks for sprint ID {sprint_id}")

        # Return the list of tasks as JSON
        return jsonify(tasks_list), 200

    except Exception as e:
        print(f"Error retrieving tasks: {str(e)}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route(tasks_routes_public.SPRINTS_END, methods=['PATCH'])
def sprints_force_end():
    try:
        # Get the sprint to be force ended
        sprintID = request.args.get("sprintID")
        if sprintID == None:
            return make_response(jsonify({"error": "Sprint ID not provided"}), 400)

        # Call the helper function to update relevant sprints and tasks
        statusCode, result = force_end.force_end(sprintID)

        if statusCode != 200:
            return make_response(jsonify({"error": result}), statusCode)
        elif statusCode == 200:
            result["_id"] = str(result["_id"])
            result["startDate"] = result["startDate"].strftime("%d/%m/%Y")
            result["endDate"] = result["endDate"].strftime("%d/%m/%Y")
            return make_response(jsonify(result), statusCode)
    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)

@app.route(tasks_routes_public.SPRINTS_TASKS, methods=['PATCH'])
def sprint_modify_tasks():
    """
    Function that takes in a list of tasks with modifications and applies the changes to the tasks in the sprint.
    It should update the tasks in sprints table and tasks table.
    """

    request_data = request.json

    modified_tasks = []

    # modify each task in the list and append the result to a list
    for task in request_data:

        result = modify_task_in_sprint.modify_task_in_sprint(task["_id"], task)
        modified_tasks.append(result)

    return make_response(jsonify({"message": "All tasks modified successfully", "modified_tasks": modified_tasks}), 200)

@app.route(tasks_routes_public.SPRINTS_INCOMPLETE, methods=['PATCH'])
def sprints_tasks_incomplete():
    try:
        request_data = request.get_json()
        print(f"Request data: {request_data}")

        # Check if the required fields are present in the request data
        # required_fields = ["_id"]

        # if required_fields not in request_data:
        #     return make_response(jsonify({"error": f"Missing required field: {required_fields}"}), 400)

        # missing_fields = [field for field in required_fields if field not in request_data]

        # if missing_fields:
        #     return make_response(jsonify({"error": f"Missing required field(s): {', '.join(missing_fields)}"}), 400)

        status_code, result = incomplete.move_incompleted_task(request_data["_id"])
        if status_code == 200:
            return make_response(jsonify({"message": "Task moved successfully", "updated_task": result}), 200)
        else:
            ret = make_response(jsonify({"error": "Entry not found."}), 404)

        ret.status_code = result

        return ret
    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.route(tasks_routes_public.SPRINTS_DATE, methods=['GET'])
def check_sprint_dates():
    """
    Endpoint to check if the provided sprint start and end dates are valid.
    """
    start_date = request.args.get("startDate")
    end_date = request.args.get("endDate")
    force_start = request.args.get("forceStart")

    # parse force_start to boolean
    force_start = force_start.lower() == "true"

    if not start_date or not end_date:
        return make_response(jsonify({"error": "Missing required field(s): startDate, endDate", "valid": False}), 400)

    # specifically check if the dates overlap with an active sprint
    if is_sprint_date_valid(start_date, end_date, force_start):
        return make_response(jsonify({"message": "Sprint dates are valid.", "valid": True}), 200)
    else:
        return make_response(jsonify({"error": "Sprint dates overlap with an active sprint.", "valid": False}), 400)

@app.route(tasks_routes_public.ONE_SPRINT, methods=['PATCH'])
def update_sprint():
    try:
        data = request.json
        id = data.pop("_id")
        status, result = modify.modify("sprints", id, data)
        
        if status == 200:
            return jsonify(result), 200
        else:
            return jsonify({"error": result}), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500
