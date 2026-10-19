# Day 2 Ã¢â‚¬â€ Django REST Framework Serializers

**Project:** Enterprise HRMS Backend
**Date:** 13 October 2026
**Technology:** Python, Django, Django REST Framework, PostgreSQL

## 1. Objective

Implement DRF serializers for employees and departments, validate incoming API data, handle related department data, and return clear validation errors.

## 2. What I Implemented

### EmployeeSerializer

File: `apps/employees/serializers.py`

- Created and configured an employee ModelSerializer.
- Defined the employee fields returned by the API.
- Added employee-code uniqueness validation.
- Added email uniqueness validation and normalized email to lowercase.
- Validated employee names and phone numbers.
- Validated department assignment.
- Rejected inactive departments.
- Added department details to employee API responses.
- Supported partial updates using `partial=True`.

### DepartmentSerializer

File: `apps/departments/serializers.py`

- Created a department ModelSerializer.
- Configured department fields.
- Removed surrounding whitespace from department names.
- Rejected empty department names.
- Checked for duplicate department names, ignoring letter case.
- Excluded the current department during update validation.

## 3. Related Data Handling

The employee serializer uses `PrimaryKeyRelatedField` for the department field.

The client submits a department ID, for example:

`"department": 1`

The serializer validates that the department exists and then resolves its ID to a Department model instance.

The response also contains related department details:

```json
{
  "department": 1,
  "department_details": {
    "id": 1,
    "name": "Engineering",
    "status": true
  }
}
```

The `department_details` field is read-only and is generated using `SerializerMethodField`.

## 4. Validation Concepts

- `validate_employee_code()` validates the employee code.
- `validate_email()` validates and normalizes email.
- `validate_department()` rejects inactive departments.
- `validate()` performs object-level validation.
- `is_valid()` runs serializer validation.
- `validated_data` contains the validated values.
- `errors` contains validation errors.
- `PrimaryKeyRelatedField` validates related object IDs.
- `read_only_fields` prevents clients from writing selected response fields.

## 5. API Testing

| Test case | Expected result | Actual result |
|---|---|---|
| GET employee API | Return employee data | HTTP 200 |
| Missing department | Return required-field error | HTTP 400 |
| Nonexistent department ID | Return clear error | HTTP 400 |
| Duplicate employee code | Reject duplicate | HTTP 400 |
| Duplicate email | Reject duplicate | HTTP 400 |
| Partial serializer validation | Accept valid supplied field | Passed |

Invalid POST requests were rejected during validation. No successful employee creation was intended in these negative tests.

## 6. Commands Used

```powershell
python manage.py check
python manage.py shell
git status
```

API tests were run using DRF's `APIClient`.

## 7. Key Learnings

1. A serializer converts model instances into API-friendly data and validates incoming data.
2. ModelSerializer automatically derives fields and some validators from a model.
3. Field-level validation checks individual fields.
4. Object-level validation checks relationships or rules involving multiple fields.
5. Related fields connect API input to existing database objects.
6. HTTP 400 indicates that a request was rejected because its submitted data was invalid.
7. API responses can include related information without requiring the client to submit an entire related object.

## 8. Final Verification

- Django system check passed.
- Employee API returned HTTP 200.
- Missing and invalid department tests returned HTTP 400.
- Duplicate employee-code and email tests returned HTTP 400.
- Git changes were reviewed before committing.
