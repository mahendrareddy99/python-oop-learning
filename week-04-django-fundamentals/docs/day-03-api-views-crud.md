
# Day 3 Ã¢â‚¬â€ API Views, CRUD, Filtering, and Pagination

## 1. Objective

Implement Django REST Framework API endpoints for employees and departments. Support CRUD operations, filtering, pagination, validation, and consistent response formats.

## 2. API Base Path

All API endpoints use the `/api/` prefix.

## 3. Employee Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/employees/` | List employees with pagination |
| POST | `/api/employees/` | Create an employee |
| GET | `/api/employees/<id>/` | Retrieve an employee |
| PUT | `/api/employees/<id>/` | Replace/update an employee |
| PATCH | `/api/employees/<id>/` | Partially update an employee |
| POST | `/api/employees/<id>/` | Deactivate an employee using an action |
| DELETE | `/api/employees/<id>/` | Delete an inactive employee |

### Employee List Query Parameters

| Parameter | Purpose | Example |
|---|---|---|
| `search` | Search employee details | `?search=Ravi` |
| `status` | Filter by active/inactive status | `?status=true` |
| `department` | Filter by department ID | `?department=1` |
| `include_inactive` | Include inactive employees | `?include_inactive=true` |
| `page` | Select a page | `?page=1` |
| `page_size` | Choose the page size | `?page_size=5` |

The default page size is 10, and the maximum page size is 100.

## 4. Department Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/departments/` | List departments with pagination |
| POST | `/api/departments/` | Create a department |
| GET | `/api/departments/<id>/` | Retrieve a department |
| PUT | `/api/departments/<id>/` | Update a department |
| PATCH | `/api/departments/<id>/` | Partially update a department |
| DELETE | `/api/departments/<id>/` | Delete a department |

### Department List Query Parameters

| Parameter | Purpose | Example |
|---|---|---|
| `search` | Search department names | `?search=Engineering` |
| `status` | Filter by active/inactive status | `?status=true` |
| `page` | Select a page | `?page=1` |
| `page_size` | Choose the page size | `?page_size=5` |

## 5. Response Contracts

### Successful resource response

```json
{
  "success": true,
  "message": "Resource retrieved successfully.",
  "data": {}
}
```

### Paginated response

```json
{
  "success": true,
  "message": "Resources retrieved successfully.",
  "data": [],
  "pagination": {
    "count": 0,
    "next": null,
    "previous": null
  }
}
```

### Validation error

```json
{
  "success": false,
  "message": "Validation failed.",
  "details": {}
}
```

A successful DELETE operation returns HTTP 204 No Content with an empty body.

## 6. HTTP Status Codes

| Status | Meaning |
|---|---|
| 200 | Successful retrieval or update |
| 201 | Resource created |
| 204 | Resource deleted successfully |
| 400 | Invalid input or business-rule violation |
| 404 | Resource not found |
| 409 | Department deletion blocked by assigned employees |

The exact response structure depends on the endpoint implementation and should be verified against the current source code.

## 7. Employee Business Rules

- Employees belong to departments.
- Employee creation and updates are validated by serializers and service-layer logic.
- Active employees cannot be deleted; deactivate them first.
- Search and filtering are applied before pagination.
- Inactive employees are excluded from the default employee list unless requested through supported filters.

## 8. Department Business Rules

- Department names must be unique.
- Department creation and updates use serializer validation.
- A department cannot be deleted while employees are assigned to it.

## 9. Automated Testing

Run the complete test suite:

```powershell
python manage.py test
```

Run Django system checks:

```powershell
python manage.py check
```

Check for whitespace errors:

```powershell
git diff --check
```

## 10. Current Verification Record

The Day 3 test suite has reported 23 passing tests.

Django's system check has reported no issues, and the Git whitespace check has passed.

Re-run these checks after any further changes.
