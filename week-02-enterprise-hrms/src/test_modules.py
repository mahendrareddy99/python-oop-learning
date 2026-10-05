from employees.employee import create_employee_name
from employees.employee import validate_employee_email

from payroll.payroll import calculate_gross_salary
from payroll.payroll import calculate_net_salary

from departments.department import create_department

from utils.helpers import format_name
from utils.helpers import is_valid_email


# Employee module
employee_name = create_employee_name("Mahendra", "Reddy")

print("Employee Name:", employee_name)

print(
    "Employee Email Valid:",
    validate_employee_email("mahendra@gmail.com")
)


# Payroll module
gross_salary = calculate_gross_salary(30000, 5000)

net_salary = calculate_net_salary(gross_salary, 2000)

print("Gross Salary:", gross_salary)
print("Net Salary:", net_salary)


# Department module
department = create_department(
    "Engineering",
    "Software development department"
)

print("Department:", department)


# Utility module
print("Formatted Name:", format_name("  mahendra reddy "))

print(
    "Email Valid:",
    is_valid_email("mahendra@gmail.com")
)