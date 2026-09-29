employees = [
    {
        "id": 101,
        "name": "Rahul",
        "department": "IT",
        "salary": 30000,
        "status": "Active"
    }
]


def add_employee(employee):
    employees.append(employee)
    print("Employee added successfully.")


def display_employees():
    print("\nEmployee List:")

    for employee in employees:
        print(employee)


def search_employee(employee_id):
    for employee in employees:
        if employee["id"] == employee_id:
            print("Employee found:")
            print(employee)
            return

    print("Employee not found.")


def update_employee(employee_id, new_salary):
    for employee in employees:
        if employee["id"] == employee_id:
            employee["salary"] = new_salary
            print("Employee updated successfully.")
            return

    print("Employee not found.")


def delete_employee(employee_id):
    for employee in employees:
        if employee["id"] == employee_id:
            employees.remove(employee)
            print("Employee deleted successfully.")
            return

    print("Employee not found.")


# Add employee
add_employee({
    "id": 102,
    "name": "Priya",
    "department": "HR",
    "salary": 35000,
    "status": "Active"
})

# Display employees
display_employees()

# Search employee
search_employee(101)

# Update employee
update_employee(101, 40000)

# Display updated employee
search_employee(101)

# Delete employee
delete_employee(102)

# Display final employees
display_employees()