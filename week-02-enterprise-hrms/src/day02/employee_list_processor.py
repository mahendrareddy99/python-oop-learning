employees = [
    "Rahul",
    "Priya",
    "Anusha",
    "Lokesh"
]


def display_employees():
    print("\nEmployee List:")

    for employee in employees:
        print(employee)


def search_employee(name):
    for employee in employees:
        if employee.lower() == name.lower():
            print(f"Employee found: {employee}")
            return

    print("Employee not found")


def count_employees():
    print(f"\nTotal employees: {len(employees)}")


def display_employee_numbers():
    print("\nEmployee Numbers:")

    for number, employee in enumerate(employees, start=1):
        print(f"{number}. {employee}")


display_employees()
count_employees()
display_employee_numbers()

search_employee("Anusha")
search_employee("Kiran")