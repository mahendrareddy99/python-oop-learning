# Day 4 — Integration and API Failure Tests

## Objective

Test the HRMS backend's API success and failure paths using automated tests and isolated test data.

## Test Execution

Run from the `week-04-django-fundamentals` directory:

```powershell
python manage.py test
```

## Test Results

- Total tests: 44
- Passed: 44
- Failures: 0
- Execution time: approximately 49.36 seconds
- Django system check: passed
- Test database: created and destroyed successfully

## Coverage Verified

### Authentication and permissions

- Anonymous users cannot access protected employee and department APIs.
- Invalid credentials do not authenticate a user.
- Users without organization membership are denied access.
- Staff users cannot perform restricted write operations.

### API validation and behavior

- Employee and department CRUD operations.
- Invalid employee data and invalid status filters.
- Missing employee and department records.
- Employee search, filtering, and pagination.
- Duplicate department names.
- Restrictions on deleting active employees and departments with employees.

### Organization-level access

- Lists exclude records from other organizations.
- Users cannot retrieve another organization's records.
- Employees cannot be created in or moved to another organization.
- Department creation uses the user's organization.

### Database behavior and performance

- Employee serialization uses `select_related`.
- Department employee relationships use `prefetch_related`.
- Multi-step transactions roll back on an integrity error.

## Execution Steps

1. Activate the virtual environment.
2. Configure the required database environment variables.
3. Run `python manage.py check`.
4. Run `python manage.py test`.
5. Review the test results and Git changes.

## Limitations

The test suite verifies the implemented automated cases; it does not establish that every possible production failure has been simulated. External service outages and deployment-specific behavior require separate testing.

## Acceptance Evidence

The Week 4 test run completed successfully with 44 tests passing and no failures.