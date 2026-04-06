# Finance Backend API

A FastAPI-based backend for managing users, authentication, financial records, and dashboard analytics.

This backend was built as part of a finance data processing and access control assignment. The system supports role-based access control, financial record management, summary APIs, and dashboard insights.

---

# Features

* User creation and management
* Login system with password hashing
* Role-based access control
* Financial record CRUD operations
* Dashboard analytics and summaries
* Search and filtering for records
* PostgreSQL integration with SQLAlchemy ORM

---

# Project Structure

```text
finance-backend/
├── requirements.txt
└── app/
    ├── db.py
    ├── dependencies.py
    ├── main.py
    ├── models.py
    ├── schemas.py
    └── routers/
        ├── auth.py
        ├── dashboard.py
        ├── records.py
        └── users.py
```

---

# Technologies Used

* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic
* Passlib
* bcrypt
* Python-dotenv
* Uvicorn

---

# Installation

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd finance-backend
```

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

## 3. Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory:

```env
DB_URL=postgresql://username:password@localhost:5432/finance_db
```

Example:

```env
DB_URL=postgresql://postgres:password@localhost:5432/finance_db
```

---

# Running the Application

```bash
uvicorn app.main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

ReDoc Docs:

```text
http://127.0.0.1:8000/redoc
```

---

# Database Models

## User Model

| Field         | Type     | Description              |
| ------------- | -------- | ------------------------ |
| id            | UUID     | Unique user ID           |
| name          | String   | User name                |
| email         | String   | Unique email address     |
| password_hash | String   | Hashed password          |
| role          | Enum     | admin / analyst / viewer |
| is_active     | Boolean  | Active or inactive user  |
| created_at    | DateTime | User creation timestamp  |

## Record Model

| Field       | Type     | Description                    |
| ----------- | -------- | ------------------------------ |
| id          | UUID     | Unique record ID               |
| title       | String   | Record title                   |
| amount      | Float    | Record amount                  |
| type        | Enum     | income / expense               |
| category    | String   | Record category                |
| description | String   | Optional notes                 |
| date        | DateTime | Record date                    |
| created_at  | DateTime | Record creation timestamp      |
| created_by  | UUID     | User ID who created the record |

Relationship:

* One user can create multiple records
* Each record belongs to one user

---

# User Roles

The system supports three roles:

## Admin

Can:

* Create users
* View users
* Activate or deactivate users
* Delete users
* Create records
* Update records
* Delete records
* View records
* Access dashboard analytics

## Analyst

Can:

* View records
* Search records
* Access dashboard analytics

Cannot:

* Create, update, or delete records
* Manage users

## Viewer

Can:

* Limited access only

Cannot:

* Create, update, or delete records
* Access record listing APIs
* Manage users

---

# Authorization

This project uses the `x-role` request header for role-based access.

Example:

```http
x-role: admin
```

Other valid values:

```http
x-role: analyst
x-role: viewer
```

---

# API Endpoints

## Authentication

| Method | Endpoint    | Description |
| ------ | ----------- | ----------- |
| POST   | /auth/login | Login user  |

### Example Login Request

```json
{
  "email": "admin@example.com",
  "password": "password123"
}
```

### Example Login Response

```json
{
  "message": "Login successful",
  "role": "admin",
  "user_id": "uuid"
}
```

---

## Users

| Method | Endpoint                | Access | Description                   |
| ------ | ----------------------- | ------ | ----------------------------- |
| POST   | /users/                 | Admin  | Create user                   |
| GET    | /users/                 | Admin  | Get all users                 |
| GET    | /users/{user_id}        | Public | Get records created by a user |
| PATCH  | /users/{user_id}/status | Admin  | Activate/deactivate user      |
| DELETE | /users/{user_id}        | Admin  | Delete user                   |

### Example Create User Request

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "analyst"
}
```

### Example Update User Status Request

```json
true
```

---

## Records

| Method | Endpoint             | Access         | Description               |
| ------ | -------------------- | -------------- | ------------------------- |
| POST   | /records/            | Admin          | Create record             |
| GET    | /records/            | Admin, Analyst | Get all records           |
| GET    | /records/{record_id} | Admin, Analyst | Get record by ID          |
| PUT    | /records/{record_id} | Admin          | Update record             |
| DELETE | /records/{record_id} | Admin          | Delete record             |
| GET    | /records/search/     | Admin, Analyst | Search and filter records |

### Example Create Record Request

```json
{
  "title": "Office Rent",
  "amount": 15000,
  "type": "expense",
  "category": "Rent",
  "description": "Monthly office rent",
  "date": "2026-04-01T10:00:00",
  "created_by": "user-uuid"
}
```

### Example Record Search

```text
GET /records/search/?type=expense&category=rent
```

Available filters:

* type
* category
* start_date
* end_date
* search

---

## Dashboard

| Method | Endpoint                     | Access | Description                            |
| ------ | ---------------------------- | ------ | -------------------------------------- |
| GET    | /dashboard/summary           | Public | Get total income, expense, and balance |
| GET    | /dashboard/category-totals   | Public | Get totals by category                 |
| GET    | /dashboard/recent-activities | Public | Get latest 5 records                   |
| GET    | /dashboard/monthly-trends    | Public | Get monthly trends                     |

---

# Dashboard Response Examples

## Summary Response

```json
{
  "total_income": 50000,
  "total_expense": 20000,
  "net_balance": 30000
}
```

## Category Totals Response

```json
[
  {
    "category": "Rent",
    "total": 15000
  },
  {
    "category": "Salary",
    "total": 50000
  }
]
```

---

# Validation Rules

## User Validation

* Name must be between 3 and 50 characters
* Email must be valid
* Email must be unique
* Password must be between 6 and 50 characters
* Role must be one of:

  * admin
  * analyst
  * viewer

## Record Validation

* Amount is required
* Title is required
* Category is required
* Date is required
* Type must be either:

  * income
  * expense

---

# Error Handling

The API uses proper HTTP status codes.

| Status Code | Meaning                   |
| ----------- | ------------------------- |
| 400         | Bad request               |
| 401         | Invalid credentials       |
| 403         | Forbidden / Access denied |
| 404         | Resource not found        |
| 500         | Internal server error     |

Example:

```json
{
  "detail": "user not found"
}
```

---

# Assumptions Made

* PostgreSQL is used as the database
* Authentication is simplified using email/password login
* Authorization is handled through the `x-role` request header
* Only admins can create, update, or delete users and records
* Analysts can only view records and dashboard analytics
* Viewers have minimal access

---

# Known Limitations

* No JWT authentication
* No refresh tokens
* No pagination for records or users
* No unit tests
* No Docker configuration
* No audit logging
* Role-based access is header-based and not secure for production
* Viewer role has limited implementation

---

# Future Improvements

* JWT authentication
* Refresh tokens
* Pagination support
* Unit and integration tests
* Docker support
* Better role handling
* Audit logs
* Export reports to PDF or Excel
* Rate limiting
* Search optimization

---

# Author

Nandana C
