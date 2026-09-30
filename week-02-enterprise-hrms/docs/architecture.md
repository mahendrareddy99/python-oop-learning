# Enterprise HRMS — Basic Architecture

## 1. Overview

The Enterprise HRMS is designed as a backend system for managing employees, departments, payroll, and other HR-related operations.

The basic architecture follows:

```text
Client
   ↓
API
   ↓
Backend
   ↓
Database
```

For the HRMS project, the architecture is:

```text
Web / Mobile
      ↓
Django REST API
      ↓
Business Logic
      ↓
PostgreSQL
```

---

## 2. Client Layer

The client is the user-facing application.

Examples:

* Web application
* Mobile application

The client sends HTTP requests to the backend API.

Example:

```text
POST /api/employees/
GET /api/employees/
PUT /api/employees/101/
DELETE /api/employees/101/
```

---

## 3. Django REST API Layer

Django REST Framework provides the API layer between the client and backend.

Responsibilities:

* Receive HTTP requests
* Validate request data
* Call business logic
* Return HTTP responses
* Serialize data as JSON

Example:

```text
Client
   ↓
HTTP Request
   ↓
Django REST API
```

---

## 4. Business Logic Layer

The business logic layer contains HRMS rules and operations.

Examples:

* Create employee
* Get employee
* Update employee
* Delete employee
* Calculate salary
* Validate employee information
* Manage departments
* Process payroll

The Day 3 Python functions and OOP classes represent the type of business logic that will later be integrated into the Django backend.

---

## 5. Database Layer

PostgreSQL will be used as the persistent database.

Possible HRMS tables include:

```text
Employee
Department
Payroll
```

Example Employee fields:

```text
employee_id
name
department_id
salary
created_at
updated_at
```

The database provides persistent storage so employee information remains available after the application is restarted.

---

## 6. Request Flow

Example: creating an employee.

```text
Web / Mobile Client
        |
        | POST /api/employees/
        ↓
Django REST API
        |
        | Validate Request
        ↓
Business Logic
        |
        | Create Employee
        ↓
PostgreSQL
        |
        | Save Data
        ↓
Django REST API
        |
        | JSON Response
        ↓
Web / Mobile Client
```

---

## 7. HRMS Architecture Diagram

```text
                    ┌───────────────────┐
                    │   Web / Mobile    │
                    │      Client       │
                    └─────────┬─────────┘
                              │
                              ↓
                    ┌───────────────────┐
                    │   Django REST     │
                    │       API         │
                    └─────────┬─────────┘
                              │
                              ↓
                    ┌───────────────────┐
                    │  Business Logic   │
                    │                   │
                    │ Employee Service  │
                    │ Department Service│
                    │ Payroll Service   │
                    │ Validation        │
                    └─────────┬─────────┘
                              │
                              ↓
                    ┌───────────────────┐
                    │    PostgreSQL     │
                    │     Database      │
                    └───────────────────┘
```

---

## 8. Separation of Responsibilities

| Layer           | Responsibility                       |
| --------------- | ------------------------------------ |
| Client          | User interface and user interaction  |
| Django REST API | HTTP communication and API endpoints |
| Business Logic  | HRMS rules and processing            |
| PostgreSQL      | Persistent data storage              |

Separating these responsibilities makes the system easier to maintain, test, and extend.

---

## 9. Current Day 3 Implementation

Day 3 focuses on Python fundamentals and basic architecture.

The current implementation contains:

```text
Functions
    ↓
Employee CRUD and salary calculation

Exception Handling
    ↓
Validation and error handling

OOP
    ↓
Employee
Manager
Department
Payroll
```

The current Python implementation uses an in-memory data structure for demonstration.

PostgreSQL has not yet been integrated into this Day 3 implementation.

Django REST Framework and PostgreSQL will be integrated in later stages of the Enterprise HRMS project.

---

## 10. Future Architecture

As the HRMS develops, additional components can be introduced:

```text
Web / Mobile
      ↓
Django REST API
      ↓
Authentication / Authorization
      ↓
Business Logic
      ↓
PostgreSQL
```

Future supporting components may include:

* Redis for caching
* Background task processing
* Logging
* Monitoring
* Automated testing
* API documentation
* Authentication and authorization

---

## 11. Day 3 Learning Outcome

By completing Day 3, the following concepts were practiced:

* Python functions
* Parameters and arguments
* Return values
* Default and keyword arguments
* `*args` and `**kwargs`
* Variable scope
* Exception handling
* Custom exceptions
* `try`, `except`, `else`, and `finally`
* `raise`
* Classes and objects
* Constructors
* Attributes and methods
* Encapsulation
* Inheritance
* Polymorphism
* Basic system architecture
* Client-server communication
* API and business logic separation
* Database layer concepts
