from backend.services.add import add_one
from services import *
from services.sorting import get_sorted
from datetime import datetime, timedelta
from policies import tasks
from bson.objectid import ObjectId
import requests

# '''
# GET FUNCTION
# '''
# import requests
import json

# # URL for the PUT request (adjust to your actual route)
# url = 'http://127.0.0.1:5000/api/OneSprint'  # Replace with a valid sprint ID

# # Data to modify the sprint (example modifications)
# data = {
#     "_id" : "6707fc87ef1ece9d4b9bcaad",
#     "sprintName": "Updated Sprint Name 4",
#     "startDate": "15-10-2026",  # Use correct date format
#     "endDate": "27-10-2026",
#     "status": "Not Started"
# }

# # Send PUT request
# response = requests.patch(url, json=data)

# # Check the response
# print(f"Status Code: {response.status_code}")
# try:
#     print(f"Response Body: {response.json()}")
# except json.JSONDecodeError:
#     print("No valid JSON response received.")


# Define the URL for the login endpoint
# url = "http://127.0.0.1:5000/api/security_check"  # Change the URL to your API's actual host and route

# # Sample login data
# login_data = {
#     "memberName": "Nolan"  # Replace with actual test username
# }
# #"password": "john123"  # Replace with actual test password


# # Make a POST request to the login endpoint
# response = requests.patch(url, json=login_data)

# # Print the response status and content
# print(f"Status Code: {response.status_code}")

# import requests

# # API URL
# url = "http://127.0.0.1:5000/api/tasks/member?_id=67094ed048aecfd22ca75d3c"

# # Send the GET request
# response = requests.get(url)

# print(response.status_code)

# # Check for a response status before accessing JSON
# if response.status_code == 200:
#     try:
#         response_json = response.json()  # Safely try to parse JSON
#         print(f"Response JSON: {response_json}")
#     except ValueError:
#         print("Error: Received a non-JSON response.")
# else:
#     print(f"Error: Status Code {response.status_code}")

# The API URL (update the URL with your actual endpoint)


# url = 'http://127.0.0.1:5000/api/tasks?memberID=670b69d5e0c7c0785a145b68'  # Replace with actual URL and member ID

# # Payload with multiple tasks to be modified
# data = [
#     {
#         "_id": "670b69d5e0c7c0785a145b6d",  # Replace with actual task ID
#         "taskName": "Updated Task Title 4",
#         "priority": "Medium",
#         "status": "Not Started",
#         "storyPoints": 6
#     },
#     {
#         "_id": "670b69d5e0c7c0785a145b6f",  # Replace with another actual task ID
#         "taskName": "Updated Task Title 5",
#         "priority": "Important",
#         "status": "Not Started",
#         "storyPoints": 9
#     }
# ]

# # headers = {"Content-Type": "application/json"}

# response = requests.patch(url, json=data)

# print(response.status_code)
# print(response.json())

# url = 'http://127.0.0.1:5000/api/tasks?memberID=670bf8e5dbd96ff42a0aa98d'

   
# # Dummy task data
# dummy_task = {
#     "taskName": "Test 2",
#     "priority": "Urgent",
#     "status": "Not Started",
#     "storyPoints": 5,  # Ensure this is a string for the conversion test
#     "storyType": "Story",
#     "assignee": "670bf8e5dbd96ff42a0aa98a",
#     "tags": ["Backend"],
#     "description": "wqewqeq",
#     "progress": "Planning"
# }

# response = requests.post(url, json=dummy_task)

# print(response.status_code)
# print(response.json())

# import requests

# url = "http://127.0.0.1:5000/api/allMember/hours?startDate=05/10/2024&endDate=10/10/2024"
# # params = {
# #     "startDate": "05/10/2024",
# #     "endDate": "10/10/2024"
# # }

# response = requests.get(url)

# if response.status_code == 200:
#     print("Success:", response.json())
# else:
#     print("Error:", response.status_code, response.json())


# import requests

# # Make a GET request to the API
# response = requests.get("http://127.0.0.1:5000/api/security-check")

# # Check the status and print the response
# if response.status_code == 200:
#     print("Admin check successful: ", response.json())
# elif response.status_code == 400:
#     print("Admin exists: ", response.json())
# else:
#     print("Error: ", response.json())


# from datetime import timedelta

# # Store hours and minutes in a timedelta object
# time_spent = timedelta(hours=3, minutes=45)
# time_spent2 = timedelta(hours=4, minutes=14)

# time_spent += time_spent2

# print(time_spent)  # Output: 3:45:00

# total_seconds = time_spent.total_seconds()
# hours = total_seconds // 3600  # 3600 seconds in an hour
# minutes = (total_seconds % 3600) // 60  # Get remaining minutes

# print(f"{int(hours)} hours and {int(minutes)} minutes")

import requests

url = "http://127.0.0.1:5000/api/logTime"  # Replace with your actual API URL
data = {
    "taskID": "670cd583f796d8d31df82e34",  # Replace with the actual task ID
    "memberID": "670cd33423657e3796f4d44c",  # Replace with the actual member ID
    "hours": "03:14" # Optional; defaults to 0 if not provided
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Success:", response.json())
elif response.status_code == 400:
    print("Bad Request:", response.json())
elif response.status_code == 404:
    print("Not Found:", response.json())
else:
    print("Error:", response.json())
