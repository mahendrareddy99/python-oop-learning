# Day 3 — ORM Efficiency and Transactions

**Date:** Wednesday, 21 October 2026  
**Project:** Enterprise HRMS Backend  
**Technology:** Python, Django, Django REST Framework, PostgreSQL

## 1. Objective

Improve database query efficiency, verify pagination boundary behavior, and demonstrate transaction rollback when one operation in a multi-step database transaction fails.

## 2. Work Completed

### 2.1 Optimized employee queries using `select_related()`

- Used the existing `select_related("department")` relationship for employee queries.
- Reviewed employee serialization, which accesses department details.
- Added a test verifying that multiple employees can be retrieved and serialized in one SQL query.

**Benefit:** Reduces unnecessary database queries when accessing a single related object through a foreign key.

### 2.2 Implemented department employee prefetching

- Added `apps/departments/services.py`.
- Implemented `get_departments_with_employees()`.
- Used `Prefetch("employees", queryset=Employee.objects.order_by("employee_code"))`.
- Added a test confirming that departments and their employees are loaded in two queries.

**Benefit:** Loads departments and their related employees efficiently without issuing an additional employee query for every department.

### 2.3 Verified pagination boundary behavior

- Tested the employee API with an out-of-range page number.
- Confirmed that requesting page 999 returns HTTP 404.

**Benefit:** Verifies the API's behavior when a client requests a page beyond the available results.

### 2.4 Tested transaction rollback

- Used `transaction.atomic()` to group two database writes.
- Created a temporary department as the first write.
- Deliberately attempted to create an employee with an existing employee code.
- Verified that the resulting `IntegrityError` caused the transaction to roll back.
- Confirmed that the temporary department was not persisted.

**Benefit:** Demonstrates that a failed operation within a transaction does not leave earlier writes from that transaction committed.

### 2.5 Expanded the test suite

Updated `apps/employees/tests.py` with four additional tests covering:

1. Employee serialization query efficiency.
2. Department employee prefetching.
3. Out-of-range pagination.
4. Transaction rollback after an integrity error.

## 3. Test Results

Command executed:

`python manage.py test`

| Check | Result |
|---|---|
| Tests discovered | 33 |
| Tests passed | 33 |
| Tests failed | 0 |
| Execution time | 34.313 seconds |
| Django system checks | No issues |

The test database was created successfully and destroyed after the tests completed.

## 4. Important Concepts Learned

- `select_related()` is suitable for single-valued relationships such as foreign keys and one-to-one relationships.
- `prefetch_related()` is suitable for reverse foreign-key and many-to-many relationships.
- `transaction.atomic()` ensures that a group of database operations commits together or rolls back together when an exception escapes the transaction block.
- Pagination boundary tests verify how an API responds to invalid page requests.
- Query-count tests provide evidence that database access remains efficient.
- Automated tests help protect existing functionality while new features are added.

## 5. Commands Practiced

```powershell
python manage.py test
git status
git diff --check
git diff
```

## 6. Known Limitations

- The new department prefetch service is available for use where departments and their employees are needed; it does not change the existing API response.
- The rollback test demonstrates Django transaction behavior using a controlled multi-write scenario. It does not establish that the current employee creation workflow itself performs multiple related writes.
- Query-count assertions verify the tested code paths, not every database operation in the application.

## 7. Conclusion

Day 3 improved the project's ORM efficiency coverage, added a department employee prefetch service, verified pagination boundary behavior, and demonstrated atomic transaction rollback. The complete test suite passed with 33 tests and no Django system-check issues.
