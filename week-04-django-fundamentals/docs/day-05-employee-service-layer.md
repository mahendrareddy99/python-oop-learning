
# Day 5 Ã¢â‚¬â€ Employee Service Layer and Modular Architecture

## 1. Objective

Build a modular employee management backend using Django, Django REST Framework, and PostgreSQL. Separate API handling from business logic and enforce employee business rules.

## 2. Requirements

- Create employee records.
- Retrieve employee details and list employees.
- Update employee information.
- Search employees by code, name, or email.
- Deactivate employees without deleting their records.
- Prevent deletion of active employees.
- Support retrieving inactive employees when explicitly requested.

## 3. Architecture

The application follows a layered structure:

1. URL Layer Ã¢â‚¬â€ maps incoming URLs to API views.
2. API View Layer Ã¢â‚¬â€ handles HTTP requests and responses.
3. Serializer Layer Ã¢â‚¬â€ validates and converts API data.
4. Service Layer Ã¢â‚¬â€ implements employee business rules.
5. Model Layer Ã¢â‚¬â€ defines employee and department data.
6. Database Layer Ã¢â‚¬â€ PostgreSQL stores persistent records.

## 4. Module Responsibilities

- `api_urls.py`: Defines employee API routes.
- `api_views.py`: Handles GET, POST, PUT, PATCH, and DELETE requests.
- `serializers.py`: Validates employee input and formats output.
- `services.py`: Contains employee creation, updating, searching, deactivation, and deletion logic.
- `models.py`: Defines the Employee database model.

## 5. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/employees/` | List active employees |
| POST | `/api/employees/` | Create an employee |
| GET | `/api/employees/<id>/` | Retrieve an employee |
| PUT | `/api/employees/<id>/` | Replace employee data |
| PATCH | `/api/employees/<id>/` | Partially update employee data |
| POST | `/api/employees/<id>/` | Deactivate using `{"action": "deactivate"}` |
| DELETE | `/api/employees/<id>/` | Delete an inactive employee |

### Search and filtering

- `/api/employees/?search=EMP100`
- `/api/employees/?include_inactive=true`

## 6. Database Design

### Department

- `id` Ã¢â‚¬â€ primary key
- `name` Ã¢â‚¬â€ unique department name
- `description` Ã¢â‚¬â€ optional description
- `status` Ã¢â‚¬â€ department status

### Employee

- `id` Ã¢â‚¬â€ primary key
- `employee_code` Ã¢â‚¬â€ unique employee code
- `first_name` Ã¢â‚¬â€ first name
- `last_name` Ã¢â‚¬â€ last name
- `email` Ã¢â‚¬â€ unique email address
- `phone` Ã¢â‚¬â€ phone number
- `date_of_joining` Ã¢â‚¬â€ joining date
- `status` Ã¢â‚¬â€ active or inactive
- `department_id` Ã¢â‚¬â€ foreign key to Department

Relationship: One department can have multiple employees. Each employee must belong to a department.

## 7. Business Rules

- Employee codes must be unique.
- Email addresses must be unique.
- An employee must belong to a department.
- Inactive employees are excluded from the default employee list.
- Employees can be deactivated without deleting their records.
- Active employees cannot be deleted.
- Deactivation is performed through the service layer.
- Department deletion is protected when employee records reference it.

## 8. Request Data Flow

1. A client sends an HTTP request.
2. Django resolves the URL.
3. The API view receives the request.
4. The serializer validates incoming data.
5. The service layer applies business rules.
6. The model interacts with PostgreSQL.
7. The API returns serialized data and an HTTP status code.

## 9. Error Handling

- `200 OK` Ã¢â‚¬â€ successful retrieval, update, or deactivation.
- `201 Created` Ã¢â‚¬â€ employee created.
- `204 No Content` Ã¢â‚¬â€ employee deleted successfully.
- `400 Bad Request` Ã¢â‚¬â€ invalid data or a business rule violation.
- `404 Not Found` Ã¢â‚¬â€ requested employee does not exist.

## 10. Testing Performed

- Verified PostgreSQL 18 database connectivity.
- Applied employee and department migrations.
- Created an employee using the REST API.
- Tested employee search and detail retrieval.
- Updated employee information using PATCH.
- Deactivated an employee and verified its inactive status.
- Checked the default and inactive-inclusive employee lists.
- Verified that deletion of an active employee is rejected.

## 11. Outcome

Implemented an employee service layer and integrated it with Django REST Framework API views. The design separates request handling from business logic and centralizes important employee operations and rules.
