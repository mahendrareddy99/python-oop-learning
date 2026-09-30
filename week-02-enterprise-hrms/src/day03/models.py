class Employee:
    """Represents an employee in the HRMS."""

    def __init__(
        self,
        employee_id,
        name,
        department,
        salary
    ):
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.__salary = salary

    def get_salary(self):
        """Return employee salary."""
        return self.__salary

    def set_salary(self, salary):
        """Update employee salary."""

        if salary <= 0:
            raise ValueError(
                "Salary must be greater than zero"
            )

        self.__salary = salary

    def display_info(self):
        """Display employee information."""

        return (
            f"ID: {self.employee_id}, "
            f"Name: {self.name}, "
            f"Department: {self.department}, "
            f"Salary: {self.__salary}"
        )


class Manager(Employee):
    """Represents a manager."""

    def __init__(
        self,
        employee_id,
        name,
        department,
        salary,
        team_size
    ):
        super().__init__(
            employee_id,
            name,
            department,
            salary
        )

        self.team_size = team_size

    def display_info(self):
        """Display manager information."""

        return (
            f"Manager: {self.name}, "
            f"Department: {self.department}, "
            f"Team Size: {self.team_size}"
        )


class Department:
    """Represents a department."""

    def __init__(self, department_id, name):
        self.department_id = department_id
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        """Add employee to department."""
        self.employees.append(employee)

    def get_employee_count(self):
        """Return number of employees."""
        return len(self.employees)


class Payroll:
    """Handles employee payroll calculations."""

    def __init__(self, employee):
        self.employee = employee

    def calculate_net_salary(
        self,
        bonus=0,
        deduction=0
    ):
        """Calculate employee net salary."""

        return (
            self.employee.get_salary()
            + bonus
            - deduction
        )