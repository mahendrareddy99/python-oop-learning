employees = {
    101: {
        "name": "Mahendra",
        "department": "IT",
        "salary": 50000
    },
    102: {
        "name": "Rahul",
        "department": "HR",
        "salary": 45000
    }
}


def create_employee(
    employee_id,
    name,
    department="IT",
    salary=30000
):
    """Create a new employee."""

    if employee_id in employees:
        raise ValueError("Employee already exists")

    employees[employee_id] = {
        "name": name,
        "department": department,
        "salary": salary
    }

    return employees[employee_id]


def get_employee(employee_id):
    """Get employee details using employee ID."""

    return employees.get(employee_id)


def update_employee(
    employee_id,
    name=None,
    department=None,
    salary=None
):
    """Update employee information."""

    employee = employees.get(employee_id)

    if employee is None:
        raise ValueError("Employee not found")

    if name is not None:
        employee["name"] = name

    if department is not None:
        employee["department"] = department

    if salary is not None:
        employee["salary"] = salary

    return employee


def delete_employee(employee_id):
    """Delete employee using employee ID."""

    if employee_id not in employees:
        raise ValueError("Employee not found")

    deleted_employee = employees.pop(employee_id)

    return deleted_employee


def calculate_salary(basic_salary, bonus=0, deduction=0):
    """Calculate final employee salary."""

    return basic_salary + bonus - deduction