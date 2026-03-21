# Gym Management System API (FastAPI)

A Gym Management System built using FastAPI that provides APIs to manage members, trainers, and workout sessions. The system includes CRUD operations, workflow management, and advanced querying features such as search, sort, and pagination.

---

## Features

* Member management (add, update, delete, view)
* Trainer data management (predefined)
* Session booking system
* Check-in and checkout workflow
* Search, filter, sort, and pagination
* Summary and analytics endpoints
* Input validation using Pydantic

---

## Tech Stack

* Python 3
* FastAPI
* Pydantic
* Uvicorn

---

## Project Structure

```
main.py      # Contains all API endpoints
README.md    # Project documentation
```

---

## How to Run

Install dependencies:

```
pip install fastapi uvicorn
```

Run the server:

```
uvicorn main:app --reload
```

Access Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Members

* GET /members
* GET /members/{member_id}
* POST /members
* PUT /members/{member_id}
* DELETE /members/{member_id}

### Sessions

* POST /sessions
* GET /sessions
* GET /sessions/search
* GET /sessions/sort
* GET /sessions/page

### Workflow

* POST /checkin/{member_id}
* POST /checkout/{member_id}

### Advanced Features

* GET /members/search
* GET /members/sort
* GET /members/page
* GET /members/filter
* GET /members/browse

---

## Concepts Implemented

* REST API design (GET, POST, PUT, DELETE)
* Pydantic models and validation
* Helper functions for modular design
* Multi-step workflow handling
* Query parameters and filtering
* Sorting and pagination logic

---

## Submission Requirements

* main.py file
* Swagger screenshots for all endpoints (Q1–Q20)

---

## Notes

* All endpoints are tested using Swagger UI
* Fixed routes are defined before dynamic routes
* Proper error handling implemented using HTTPException

---

## Author

Yadu
