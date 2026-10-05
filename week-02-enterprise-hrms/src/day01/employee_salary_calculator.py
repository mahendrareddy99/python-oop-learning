# Employee Salary Calculator
# Day 1 - Python Fundamentals


employee_name = input("Enter employee name: ")

basic_salary = float(input("Enter basic salary: "))
hra = float(input("Enter HRA: "))
allowance = float(input("Enter allowance: "))


if basic_salary < 0 or hra < 0 or allowance < 0:
    print("Salary values cannot be negative.")

else:
    gross_salary = basic_salary + hra + allowance

    print("\n--- Employee Salary Details ---")
    print("Employee Name:", employee_name)
    print("Basic Salary:", basic_salary)
    print("HRA:", hra)
    print("Allowance:", allowance)
    print("Gross Salary:", gross_salary)