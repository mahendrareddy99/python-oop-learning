from functions import (
    create_employee,
    get_employee,
    update_employee,
    delete_employee,
    calculate_salary
)

from exceptions import (
    InvalidEmployeeIDError,
    InvalidSalaryError,
    EmployeeNotFoundError,
    validate_employee_id,
    validate_salary,
    validate_employee_exists,
    divide_salary
)

from models import (
    Employee,
    Manager,
    Department,
    Payroll
)


def main():

    print("=" * 50)
    print("ENTERPRISE HRMS - DAY 3 DEMO")
    print("=" * 50)

    # ==========================================
    # 1. PYTHON FUNCTIONS
    # ==========================================

    print("\n--- 1. PYTHON FUNCTIONS ---")

    employee_data = create_employee(
        103,
        "Suresh",
        "Finance",
        40000
    )

    print("Created Employee:")
    print(employee_data)

    employee_data = get_employee(103)

    print("\nFetched Employee:")
    print(employee_data)

    employee_data = update_employee(
        103,
        salary=45000
    )

    print("\nUpdated Employee:")
    print(employee_data)

    salary = calculate_salary(
        45000,
        bonus=5000,
        deduction=2000
    )

    print("\nCalculated Salary:", salary)

    # ==========================================
    # 2. EXCEPTION HANDLING
    # ==========================================

    print("\n--- 2. EXCEPTION HANDLING ---")

    try:
        validate_employee_id(-10)

    except InvalidEmployeeIDError as error:
        print("Invalid Employee ID:", error)

    try:
        validate_salary(-5000)

    except InvalidSalaryError as error:
        print("Invalid Salary:", error)

    try:
        validate_employee_exists(None)

    except EmployeeNotFoundError as error:
        print("Missing Employee:", error)

    try:
        divide_salary(50000, 0)

    except ZeroDivisionError as error:
        print("Division Error:", error)

    # Demonstrate try/except/else/finally

    print("\nSalary Validation:")

    try:
        salary = 50000
        validate_salary(salary)

    except InvalidSalaryError as error:
        print("Handled Error:", error)

    else:
        print("Salary is valid")

    finally:
        print("Salary validation completed")

    # ==========================================
    # 3. OOP - EMPLOYEE
    # ==========================================

    print("\n--- 3. OOP ---")

    employee = Employee(
        101,
        "Mahendra",
        "IT",
        50000
    )

    print("\nEmployee:")
    print(employee.display_info())

    # Encapsulation

    print("\nOriginal Salary:")
    print(employee.get_salary())

    employee.set_salary(55000)

    print("Updated Salary:")
    print(employee.get_salary())

    # ==========================================
    # 4. INHERITANCE
    # ==========================================

    manager = Manager(
        102,
        "Rahul",
        "Engineering",
        70000,
        8
    )

    print("\nManager:")
    print(manager.display_info())

    print("Manager Salary:")
    print(manager.get_salary())

    # ==========================================
    # 5. POLYMORPHISM
    # ==========================================

    print("\n--- POLYMORPHISM ---")

    employees = [
        employee,
        manager
    ]

    for emp in employees:
        print(emp.display_info())

    # ==========================================
    # 6. DEPARTMENT
    # ==========================================

    print("\n--- DEPARTMENT ---")

    department = Department(
        1,
        "Engineering"
    )

    department.add_employee(employee)
    department.add_employee(manager)

    print("Department:", department.name)
    print(
        "Employee Count:",
        department.get_employee_count()
    )

    # ==========================================
    # 7. PAYROLL
    # ==========================================

    print("\n--- PAYROLL ---")

    payroll = Payroll(employee)

    net_salary = payroll.calculate_net_salary(
        bonus=5000,
        deduction=2000
    )

    print("Employee:", employee.name)
    print("Net Salary:", net_salary)

    # ==========================================
    # COMPLETION
    # ==========================================

    print("\n" + "=" * 50)
    print("DAY 3 HRMS DEMO COMPLETED SUCCESSFULLY")
    print("=" * 50)


if __name__ == "__main__":
    main()