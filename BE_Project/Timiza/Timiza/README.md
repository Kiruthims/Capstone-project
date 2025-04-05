# Capstone Project: Timiza

## OVERVIEW

The Timiza API is a RESTful web service built using Django and Django REST Framework (DRF). It provides an endpoint for managing tasks, implementing authentication, permissions, and role-based access control. The API supports features such as task ownership, permissions for different user roles, and JWT-based authentication.

---

## FEATURES

- **User Authentication** (Registration & Login with JWT tokens)
- **Task Management** (Create, Update, Delete, View Tasks)
- **Permissions** (Custom permissions for task access based on user roles)
- **Task Ownership** (Allow users to access only their own tasks)
- **JWT-based Authentication** (Secure authentication with tokens)
- **Role-based Permissions** (Ensure only authorized users can perform certain actions on tasks)
- **Filtering & Sorting** (Filter tasks by user and sort by creation date)


## TECHNOLOGIES USED

- **Python** (Programming Language)
- **Django** (Web Framework)
- **Django REST Framework** (API Development)
- **SimpleJWT** (Authentication)
- **PostgreSQL** (Database)
- **Postman** (API Testing)

---

## SETUP INSTRUCTIONS

### Clone the Repository

```bash
git clone git@github.com:Kiruthims/Capstone-project.git
cd Capstone-project


Create a Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Apply Migrations
bash
Copy
Edit
python manage.py migrate
Run the Server
bash
Copy
Edit
python manage.py runserver
TESTING ENDPOINTS WITH POSTMAN
User Authentication
1. Create a User
Method: POST

URL: http://127.0.0.1:8000/api/users/register/

Body (JSON):

json
Copy
Edit
{
  "email": "joy@email.com",
  "username": "joy123",
  "password": "joypass123"
}
Expected Response: 201 Created with user details.

2. Log In to Get Token
Method: POST

URL: http://127.0.0.1:8000/api/users/login/

Body (JSON):

json
Copy
Edit
{
  "username": "joy123.com",
  "password": "joypass123"
}
Expected Response: 200 OK with the JWT token.

Task Endpoints
1. Create a Task
Method: POST

URL: http://127.0.0.1:8000/api/tasks/

Headers:

json
Copy
Edit
{
  "Authorization": "Bearer <access_token>"
}
Body (JSON):

json
Copy
Edit
{
  "title": "Task Title",
  "description": "Task description here.",
  "due_date": "2025-05-10"
}
Expected Response: 201 Created with task details.

2. View All Tasks
Method: GET

URL: http://127.0.0.1:8000/api/tasks/

Expected Response: 200 OK with a list of tasks.

3. Update a Task
Method: PUT

URL: http://127.0.0.1:8000/api/tasks/{task_id}/

Headers:

json
Copy
Edit
{
  "Authorization": "Bearer <access_token>"
}
Body (JSON):

json
Copy
Edit
{
  "title": "Updated Task Title",
  "description": "Updated task description.",
  "due_date": "2025-06-15"
}
Expected Response: 200 OK with updated task details.

4. Delete a Task
Method: DELETE

URL: http://127.0.0.1:8000/api/tasks/{task_id}/

Headers:

json
Copy
Edit
{
  "Authorization": "Bearer <access_token>"
}
Expected Response: 204 No Content (Task deleted).

Permissions Overview
IsTaskOwner: Prevents users from modifying tasks that do not belong to them. This permission applies to PUT, PATCH, and DELETE methods.

Role-Based Access: Only users with appropriate roles can modify or delete tasks. Basic users cannot perform PUT or DELETE actions unless they are the task owner.

Conclusion
This API is designed to manage tasks with role-based access, secure authentication, and efficient data management. Use the provided Postman instructions to test all the available endpoints.

Additional Resources
Django REST Framework Documentation

SimpleJWT Documentation