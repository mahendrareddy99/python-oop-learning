class InvalidEmployeeIDError(Exception):
    """Raised when employee ID is invalid."""
    pass


class InvalidSalaryError(Exception):
    """Raised when salary is invalid."""
    pass


class EmployeeNotFoundError(Exception):
    """Raised when employee does not exist."""
    pass


class InvalidInputError(Exception):
    """Raised when input is invalid."""
    pass


def validate_employee_id(employee_id):
    """Validate employee ID."""

    if not isinstance(employee_id, int):
        raise InvalidEmployeeIDError(
            "Employee ID must be an integer"
        )

    if employee_id <= 0:
        raise InvalidEmployeeIDError(
            "Employee ID must be greater than zero"
        )

    return True


def validate_salary(salary):
    """Validate employee salary."""

    if not isinstance(salary, (int, float)):
        raise InvalidSalaryError(
            "Salary must be a number"
        )

    if salary <= 0:
        raise InvalidSalaryError(
            "Salary must be greater than zero"
        )

    return True


def validate_employee_exists(employee):
    """Check whether employee exists."""

    if employee is None:
        raise EmployeeNotFoundError(
            "Employee not found"
        )

    return True


def divide_salary(salary, divisor):
    """Divide salary safely."""

    if divisor == 0:
        raise ZeroDivisionError(
            "Division by zero is not allowed"
        )

    return salary / divisor