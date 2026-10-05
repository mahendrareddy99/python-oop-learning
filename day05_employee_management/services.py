class ValidationService:

    @staticmethod
    def validate_employee_id(employee_id):
        if not isinstance(employee_id, int):
            raise ValueError("Employee ID must be an integer")

        if employee_id <= 0:
            raise ValueError("Employee ID must be greater than 0")

        return True

    @staticmethod
    def validate_name(name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")

        if not name.strip():
            raise ValueError("Name cannot be empty")

        return True

    @staticmethod
    def validate_department(department):
        if not isinstance(department, str):
            raise ValueError("Department must be a string")

        if not department.strip():
            raise ValueError("Department cannot be empty")

        return True

    @staticmethod
    def validate_salary(salary):
        if not isinstance(salary, (int, float)):
            raise ValueError("Salary must be a number")

        if salary <= 0:
            raise ValueError("Salary must be greater than 0")

        return True


class EmployeeService:

    def __init__(self):
        self.employees = []

    def add_employee(self, employee):
        ValidationService.validate_employee_id(employee.employee_id)
        ValidationService.validate_name(employee.name)
        ValidationService.validate_department(employee.department)
        ValidationService.validate_salary(employee.get_salary())

        if self.find_employee(employee.employee_id):
            raise ValueError("Employee ID already exists")

        self.employees.append(employee)

    def find_employee(self, employee_id):
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee

        return None

    def update_employee(self, employee_id, name=None, department=None, salary=None):
        employee = self.find_employee(employee_id)

        if employee is None:
            raise ValueError("Employee not found")

        if name is not None:
            ValidationService.validate_name(name)
            employee.name = name

        if department is not None:
            ValidationService.validate_department(department)
            employee.department = department

        if salary is not None:
            ValidationService.validate_salary(salary)
            employee.set_salary(salary)

    def delete_employee(self, employee_id):
        employee = self.find_employee(employee_id)

        if employee is None:
            raise ValueError("Employee not found")

        self.employees.remove(employee)

    def display_employees(self):
        if not self.employees:
            print("No employees found.")
            return

        for employee in self.employees:
            employee.display_info()
            print(f"Bonus      : {employee.calculate_bonus()}")
            print("-" * 30)

    def search_by_department(self, department):
        matching_employees = []

        for employee in self.employees:
            if employee.department.lower() == department.lower():
                matching_employees.append(employee)

        return matching_employees