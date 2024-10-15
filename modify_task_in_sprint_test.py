import requests
# test code from sprint to backlog
if __name__ == "__main__":

    dummy_task = [
    {
        "_id": "66fbba7bbdfa356ffd44ac37",
        "taskName": "Example Task 1",
        "storyType": "Story",
        "storyPoints": 9,
        "tags": ["Frontend"],
        "priority": "Low",
        "assignee": "Alice",
        "status": "Not Started",
        "description": "Example desc for task 1",
        "progress": "Planning",
        "creationDate": "01-10-2024",
        "sprint": None
    },
    {
        "_id": "66fbba7bbdfa356ffd44ac38",
        "taskName": "Example Task 2",
        "storyType": "Bug",
        "storyPoints": 2,
        "tags": ["Backend"],
        "priority": "Medium",
        "assignee": "Bob",
        "status": "In Progress",
        "description": "Example desc for task 2",
        "progress": "Development",
        "creationDate": "05-10-2024",
        "sprint": None
     },
     {
        "_id": "66fbba7bbdfa356ffd44ac39",
        "taskName": "Example Task 3",
        "storyType": "Story",
        "storyPoints": 5,
        "tags": ["Backend"],
        "priority": "Important",
        "assignee": "Martha",
        "status": "In Progress",
        "description": "Example desc for task 3",
        "progress": "Development",
        "creationDate": "cccccc",
        "sprint": None
     },
     {
        "_id": "66fbba7bbdfa356ffd44ac3a",
        "taskName": "Example Task 4",
        "storyType": "Story",
        "storyPoints": 3,
        "tags": ["Backend"],
        "priority": "Urgent",
        "assignee": "Bob",
        "status": "Complete",
        "description": "Example desc for task 4",
        "progress": "Completed",
        "creationDate": "bbbbbb",
        "sprint": None
     },
     {
        "_id": "66fbba7bbdfa356ffd44ac3b",
        "taskName": "Example Task 5",
        "storyType": "Bug",
        "storyPoints": 6,
        "tags": ["Frontend"],
        "priority": "Urgent",
        "assignee": "Alice",
        "status": "In Progress",
        "description": "Example desc for task 5",
        "progress": "Development",
        "creationDate": "aaaaaa",
        "sprint": "66fbba7bbdfa356ffd44ac3d"
     }
]

    response = requests.patch("http://127.0.0.1:5000/api/sprints/tasks", json=dummy_task)

