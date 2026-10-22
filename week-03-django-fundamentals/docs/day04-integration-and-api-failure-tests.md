
@'
# Day 4 — Integration and API Failure Tests

## Objective

Verify the HRMS backend through automated API tests covering successful requests, invalid requests, authentication, organization-level access control, query efficiency, and transaction behavior.

## Test Execution

Run the complete test suite from the Week 4 project directory:

```powershell
python manage.py test
```

## Test Results

- Total tests discovered: 44
- Passed: 44
- Failures: 0
- Execution time: approximately 49.36 seconds
- Django system check: passed
- Test database: created and destroyed successfully

## Coverage Verified by the Test Suite

### 1. Authentication and permissions

- Anonymous users cannot list employees or departments.
- Invalid credentials do not authenticate a user.
- Users without organization membership are denied access.
- Staff users cannot perform restricted employee and department write operations.
- Valid credentials and sessions allow authorized API access.

### 2. Request validation and API behavior

- Employee creation, retrieval, updates, partial updates, and deactivation.
- Invalid employee data returns HTTP 400.
- Missing employee and department records return HTTP 404.
- Invalid status filters return HTTP 400.
- Employee and department lists use paginated responses.
- Employee search and status/department filtering.
- Duplicate department names are rejected.
- Active employees cannot be deleted, and departments with employees cannot be deleted.

### 3. Organization-level access control

- Employee and department lists exclude records from other organizations.
- Users cannot retrieve records belonging to another organization.
- Employees cannot be created in another organization.
- Department creation uses the authenticated user's organization.
- Employees cannot be moved to a department in another organization.

### 4. Database behavior and query efficiency

- Employee serialization uses `select_related` efficiently.
- Department employee relationships use `prefetch_related`.
- A multi-step transaction rolls back when an integrity error occurs.

## Implementation Decisions

- Use Django REST Framework API tests to exercise endpoint behavior.
- Use isolated test data so test cases do not depend on production records.
- Enforce authentication, organization membership, and role-based permissions.
- Use database transactions to protect multi-step operations.
- Use `select_related` and `prefetch_related` to reduce unnecessary database queries.
- Verify both successful operations and relevant failure responses.

## Execution Steps

1. Activate the project's virtual environment.
2. Set the required database environment variables.
3. Change to the `week-04-django-fundamentals` directory.
4. Run `python manage.py check`.
5. Run `python manage.py test`.
6. Review the test output and Git changes before committing.

## Limitations

- The reported result verifies the automated test suite; it does not establish that every possible production failure has been simulated.
- External service outages and production deployment behavior require separate integration or environment-specific testing.
- Future API changes should include corresponding success and failure tests.

## Acceptance Evidence

The test run completed successfully with 44 tests passing and no failures. Django reported no system-check issues, and the test database was cleaned up after execution.
'@ | Set-Content -Encoding utf8 docs\day04-integration-and-api-failure-tests.md
