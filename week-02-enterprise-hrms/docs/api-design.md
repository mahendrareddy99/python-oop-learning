# HRMS API Design

## 1. Introduction

The Enterprise HRMS exposes REST APIs for managing employees and departments.

The APIs follow REST principles and use HTTP methods to perform CRUD operations.

Base URL:

```text
/api/
```

Data format:

```text
JSON
```

---

# 2. Employee APIs

## 2.1 Create Employee

### Endpoint

```http
POST /api/employees/
```

### Purpose

Creates a new employee.

### Request

```json
{
    "employee_code": "EMP001",
    "name": "Rahul",
    "email": "rahul@example.com",
    "department_id": 1
}
```

### Response

```json
{
    "id": 1,
    "employee_code": "EMP001",
    "name": "Rahul",
    "email": "rahul@example.com",
    "department_id": 1,
    "status": "Active"
}
```

### Status Codes

```text
201 Created
400 Bad Request
409 Conflict
```

### Validation Rules

- employee_code is required.
- employee_code must be unique.
- name is required.
- email is required.
- email must have a valid format.
- department_id must refer to an existing department.
- status defaults to Active.

---

## 2.2 Get Employees

### Endpoint

```http
GET /api/employees/
```

### Purpose

Returns a list of employees.

### Response

```json
[
    {
        "id": 1,
        "employee_code": "EMP001",
        "name": "Rahul",
        "email": "rahul@example.com",
        "department_id": 1,
        "status": "Active"
    }
]
```

### Status Codes

```text
200 OK
```

---

## 2.3 Get Employee by ID

### Endpoint

```http
GET /api/employees/{id}/
```

### Example

```http
GET /api/employees/1/
```

### Purpose

Returns details of a specific employee.

### Status Codes

```text
200 OK
404 Not Found
```

---

## 2.4 Update Employee

### Endpoint

```http
PUT /api/employees/{id}/
```

### Example

```http
PUT /api/employees/1/
```

### Purpose

Completely updates an employee resource.

### Request

```json
{
    "employee_code": "EMP001",
    "name": "Rahul Kumar",
    "email": "rahulkumar@example.com",
    "department_id": 2,
    "status": "Active"
}
```

### Status Codes

```text
200 OK
400 Bad Request
404 Not Found
```

---

## 2.5 Partially Update Employee

### Endpoint

```http
PATCH /api/employees/{id}/
```

### Example

```http
PATCH /api/employees/1/
```

### Request

```json
{
    "email": "newemail@example.com"
}
```

### Purpose

Updates only selected employee fields.

### Status Codes

```text
200 OK
400 Bad Request
404 Not Found
```

---

## 2.6 Delete Employee

### Endpoint

```http
DELETE /api/employees/{id}/
```

### Example

```http
DELETE /api/employees/1/
```

### Purpose

Deletes an employee.

### Status Codes

```text
204 No Content
404 Not Found
```

---

# 3. Department APIs

## 3.1 Create Department

### Endpoint

```http
POST /api/departments/
```

### Request

```json
{
    "name": "Engineering",
    "description": "Software development department"
}
```

### Response

```json
{
    "id": 1,
    "name": "Engineering",
    "description": "Software development department"
}
```

### Status Codes

```text
201 Created
400 Bad Request
409 Conflict
```

---

## 3.2 Get Departments

### Endpoint

```http
GET /api/departments/
```

### Purpose

Returns all departments.

### Status Codes

```text
200 OK
```

---

## 3.3 Get Department by ID

### Endpoint

```http
GET /api/departments/{id}/
```

### Example

```http
GET /api/departments/1/
```

### Status Codes

```text
200 OK
404 Not Found
```

---

## 3.4 Update Department

### Endpoint

```http
PUT /api/departments/{id}/
```

### Request

```json
{
    "name": "Human Resources",
    "description": "Human resources department"
}
```

### Status Codes

```text
200 OK
400 Bad Request
404 Not Found
```

---

## 3.5 Delete Department

### Endpoint

```http
DELETE /api/departments/{id}/
```

### Example

```http
DELETE /api/departments/1/
```

### Status Codes

```text
204 No Content
404 Not Found
```

---

# 4. HTTP Status Codes

| Status Code | Meaning |
|---|---|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 500 | Internal Server Error |

---

# 5. Common Validation Rules

### Employee

- Employee code must be unique.
- Name is required.
- Email is required.
- Email must be valid.
- Department must exist.
- Employee status must contain a valid value.

### Department

- Department name is required.
- Department name should be unique.
- Description is optional.

---

# 6. API Summary

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/employees/ | Create employee |
| GET | /api/employees/ | List employees |
| GET | /api/employees/{id}/ | Get employee |
| PUT | /api/employees/{id}/ | Replace employee |
| PATCH | /api/employees/{id}/ | Partially update employee |
| DELETE | /api/employees/{id}/ | Delete employee |
| POST | /api/departments/ | Create department |
| GET | /api/departments/ | List departments |
| GET | /api/departments/{id}/ | Get department |
| PUT | /api/departments/{id}/ | Update department |
| DELETE | /api/departments/{id}/ | Delete department |