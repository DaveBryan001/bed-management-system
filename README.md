# Bed Management System API

## Overview
The Bed Management System API allows multiple hospitals to manage bed availability, allocation, and patient assignments efficiently.
This documentation provides detailed information on setting up and using the API, including endpoint descriptions, required parameters, and response formats.

## Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Running the Application](#running-the-application)
4. [API Endpoints](#api-endpoints)
5. [Authentication](#authentication)
6. [Usage](#usage)

## Installation

### Prerequisites
- Python 3.x
- Flask
- Flask-RESTful
- Flask-JWT-Extended
- SQLAlchemy
- Flask-Bcrypt
- PostgreSQL (or SQLite for local development)

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/bed-management-system.git
    cd bed-management-system
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and set the necessary environment variables:
    ```bash
    SECRET_KEY=your_secret_key
    DATABASE_URL=your_database_url
    JWT_SECRET_KEY=your_jwt_secret_key
    ```

## Configuration
Configure your environment variables as per the example in the `.env` file.
The 'config.py' file manages the environment variables and sets up the flask application and configuration.

## Running the Application

Run the Flask application:
```bash
flask run
```
The application should now be running at `http://127.0.0.1:5000` or at `http://localhost:5000`.

## API EndPoints

### Authentication

#### User Registration
Endpoint: /register

Method: POST

Description: Register a new user.

Request Body:
```json
{
    "username": "user",
    "password": "password"
}
```
Response:

```json
201 Created: User created successfully.
409 Conflict: User already exists.
```

User Login
Endpoint: /login

Method: POST

Description: Authenticate a user and generate a JWT token.

Request Body:

```json
{
    "username": "testuser",
    "password": "testpassword"
}
```
Response:
```
200 OK: Returns the JWT token.
401 Unauthorized: Invalid credentials.
```
#### Hospital Management
Add a Hospital
Endpoint: /hospitals

Method: POST

Description: Add a new hospital.

Request Body:

```json
{
    "name": "Hospital A",
    "location": "123 Main St"
}
```
Response:
```
201 Created: Hospital created successfully.

```
#### Get All Hospitals
Endpoint: /hospitals

Method: GET

Description: Retrieve a list of all hospitals.

Response:
```
200 OK: Returns a list of hospitals.
```
Example:
```
curl -X GET http://127.0.0.1:5000/hospitals -H "Authorization: Bearer <your_token>"
```

#### Get Hospital by ID
Endpoint: /hospitals/<int:hospital_id>

Method: GET

Description: Retrieve details of a specific hospital.

Response:
```
200 OK: Returns hospital details.
404 Not Found: Hospital not found.
```
Example:
```
curl -X GET http://127.0.0.1:5000/hospitals/1 -H "Authorization: Bearer <your_token>"
```
#### Update Hospital
Endpoint: /hospitals/<int:hospital_id>

Method: PUT

Description: Update details of a specific hospital.

Request Body:

```json
{
    "name": "Updated Hospital Name",
    "location": "456 New Address"
}
```
Response:
```
200 OK: Hospital updated successfully.
404 Not Found: Hospital not found.
```
Example:
```
curl -X PUT http://127.0.0.1:5000/hospitals/1 -H "Content-Type: application/json" -H "Authorization: Bearer <your_token>" -d '{"name": "Updated Hospital Name", "location": "456 New Address"}'
```
#### Delete Hospital
Endpoint: /hospitals/<int:hospital_id>

Method: DELETE

Description: Delete a specific hospital.

Response:
```
200 OK: Hospital deleted successfully.
404 Not Found: Hospital not found.
```
Example:
```
curl -X DELETE http://127.0.0.1:5000/hospitals/1 -H "Authorization: Bearer <your_token>"
```
#### Department Management
Add a Department
Endpoint: /departments

Method: POST

Description: Add a new department.

Request Body:
```json
{
    "name": "Cardiology",
    "hospital_id": 1
}
```
Response:
```
201 Created: Department created successfully.
```
Example:
```
curl -X POST http://127.0.0.1:5000/departments -H "Content-Type: application/json" -H "Authorization: Bearer <your_token>" -d '{"name": "Cardiology", "hospital_id": 1}'
```
### Get All Departments
Endpoint: /departments

Method: GET

Description: Retrieve a list of all departments.

Response:
```
200 OK: Returns a list of departments.
```
Example:
```
curl -X GET http://127.0.0.1:5000/departments -H "Authorization: Bearer <your_token>"
```
#### Get Department by ID
Endpoint: /departments/<int:department_id>

Method: GET

Description: Retrieve details of a specific department.

Response:
```
200 OK: Returns department details.
404 Not Found: Department not found.
```
Example:
```
curl -X GET http://127.0.0.1:5000/departments/1 -H "Authorization: Bearer <your_token>"
```
#### Update Department
Endpoint: /departments/<int:department_id>

Method: PUT

Description: Update details of a specific department.

Request Body:
```json
{
    "name": "Updated Department Name",
    "hospital_id": 1
}
```
Response:
```
200 OK: Department updated successfully.
404 Not Found: Department not found.
```
Example:
```
curl -X PUT http://127.0.0.1:5000/departments/1 -H "Content-Type: application/json" -H "Authorization: Bearer <your_token>" -d '{"name": "Updated Department Name", "hospital_id": 1}'
```
#### Delete Department
Endpoint: /departments/<int:department_id>

Method: DELETE

Description: Delete a specific department.

Response:
```
200 OK: Department deleted successfully.
404 Not Found: Department not found.
```
Example:
```
curl -X DELETE http://127.0.0.1:5000/departments/1 -H "Authorization: Bearer <your_token>"
```
#### Bed Management
Add a Bed
Endpoint: /beds

Method: POST

Description: Add a new bed.

Request Body:
```json
{
    "bed_number": 101,
    "status": "available",
    "department_id": 1
}
````
Response:
```
201 Created: Bed created successfully.
```
Example:
```
curl -X POST http://127.0.0.1:5000/beds -H "Content-Type: application/json" -H "Authorization: Bearer <your_token>" -d '{"bed_number": 101, "status": "available", "department_id": 1}'
```
#### Get All Beds
Endpoint: /beds

Method: GET

Description: Retrieve a list of all beds.

Response:
```
200 OK: Returns a list of beds.
```
Example:
```
curl -X GET http://127.0.0.1:5000/beds -H "Authorization: Bearer <your_token>"
```
#### Get Bed by ID
Endpoint: /beds/<int:bed_id>

Method: GET

Description: Retrieve details of a specific bed.

Response:
```
200 OK: Returns bed details.
404 Not Found: Bed not found.
```
Example:
```
curl -X GET http://127.0.0.1:5000/beds/1 -H "Authorization: Bearer <your_token>"
```
#### Update Bed
Endpoint: /beds/<int:bed_id>

Method: PUT

Description: Update details of a specific bed.

Request Body:
```json
{
    "bed_number": 102,
    "status": "occupied",
    "department_id": 1
}
```
Response:
```
200 OK: Bed updated successfully.
404 Not Found: Bed not found.
```
Example:
```
curl -X PUT http://127.0.0.1:5000/beds/1 -H "Content-Type: application/json" -H "Authorization: Bearer <your_token>" -d '{"bed_number": 102, "status": "occupied", "department_id": 1}'
```
#### Delete Bed
Endpoint: /beds/<int:bed_id>

Method: DELETE

Description: Delete a specific bed.

Response:
```
200 OK: Bed deleted successfully.
404 Not Found: Bed not found.
```
Example:
```
curl -X DELETE http://127.0.0.1:5000/beds/1 -H "Authorization: Bearer <your_token>"
```
#### Patient Management
Add a Patient
Endpoint: /patients

Method: POST

Description: Add a new patient

Request body:
```json
{
    "name": "John Doe",
    "age": 45,
    "bed_id": 1
}
```
Response:
```
{
    "id": 1,
    "name": "John Doe",
    "age": 45,
    "bed_id": 1
}
```

GET /patients/<int:patient_id>

Retrieve a specific patient by ID.

Response:
```
{
    "id": 1,
    "name": "John Doe",
    "age": 45,
    "bed_id": 1
}
```
#### Update Patient 
PUT /patients/<int:patient_id>

Update a specific patient by ID.

Request:
```
{
    "name": "John Doe",
    "age": 46,
    "bed_id": 2
}
```

Response:
```
{
    "id": 1,
    "name": "John Doe",
    "age": 46,
    "bed_id": 2
}
```

#### DELETE PATIENT

Endpoint /patients/<int:patient_id>

Delete a specific patient by ID.

Response:
```
{
    "message": "Patient deleted"
}
```

## Authentication
Each request to secured endpoints requires a JWT token in the 'Authorization' header:

```
Authorization: Bearer your_jwt_token
```

## Usage
Register a new user using the '/register' endpoint.
Log in with the '/login' endpoint to obtain a JWT token.
Use the token to access other endpoints.




