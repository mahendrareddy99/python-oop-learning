from employee import Developer, Manager, HRManager
from services import EmployeeService
from report_service import ReportService


def create_employee():
    employee_id = int(input("Enter employee ID: "))
    name = input("Enter employee name: ")
    department = input("Enter department: ")
    salary = float(input("Enter salary: "))
    role = input("Enter role (developer/manager/hr): ").lower()

    if role == "developer":
        return Developer(employee_id, name, department, salary)

    elif role == "manager":
        return Manager(employee_id, name, department, salary)

    elif role == "hr":
        return HRManager(employee_id, name, department, salary)

    else:
        raise ValueError("Invalid role")


def main():
    employee_service = EmployeeService()

    # Sample employees
    employee_service.add_employee(
        Developer(101, "Mahendra Reddy", "IT", 55000)
    )

    employee_service.add_employee(
        Manager(102, "Rahul", "Management", 80000)
    )

    employee_service.add_employee(
        HRManager(103, "Priya", "HR", 60000)
    )

    while True:

        print("\n" + "=" * 50)
        print("       EMPLOYEE MANAGEMENT SYSTEM")
        print("=" * 50)

        print("1. Add Employee")
        print("2. Update Employee")
        print("3. Delete Employee")
        print("4. Search Employee")
        print("5. Display Employees")
        print("6. Search by Department")
        print("7. Generate Employee Report")
        print("8. Exit")

        choice = input("\nEnter your choice: ")

        try:

            if choice == "1":

                employee = create_employee()

                employee_service.add_employee(employee)

                print("\nEmployee added successfully.")

            elif choice == "2":

                employee_id = int(input("Enter employee ID: "))

                name = input("Enter new name (press Enter to skip): ")
                department = input(
                    "Enter new department (press Enter to skip): "
                )

                salary_input = input(
                    "Enter new salary (press Enter to skip): "
                )

                salary = (
                    float(salary_input)
                    if salary_input
                    else None
                )

                employee_service.update_employee(
                    employee_id,
                    name=name if name else None,
                    department=department if department else None,
                    salary=salary
                )

                print("\nEmployee updated successfully.")

            elif choice == "3":

                employee_id = int(input("Enter employee ID: "))

                employee_service.delete_employee(employee_id)

                print("\nEmployee deleted successfully.")

            elif choice == "4":

                employee_id = int(input("Enter employee ID: "))

                employee = employee_service.find_employee(employee_id)

                if employee:
                    employee.display_info()
                    print(
                        f"Bonus      : "
                        f"{employee.calculate_bonus()}"
                    )
                else:
                    print("\nEmployee not found.")

            elif choice == "5":

                print("\n=== EMPLOYEE LIST ===")

                employee_service.display_employees()

            elif choice == "6":

                department = input("Enter department: ")

                employees = employee_service.search_by_department(
                    department
                )

                if employees:

                    print(
                        f"\nEmployees in {department}:"
                    )

                    for employee in employees:
                        employee.display_info()
                        print(
                            f"Bonus      : "
                            f"{employee.calculate_bonus()}"
                        )
                        print("-" * 30)

                else:
                    print("\nNo employees found.")

            elif choice == "7":

                report = ReportService.generate_employee_report(
                    employee_service.employees
                )

                print("\n" + report)

            elif choice == "8":

                print("\nThank you for using Employee Management System.")
                break

            else:

                print("\nInvalid choice. Please select 1-8.")

        except ValueError as error:

            print(f"\nError: {error}")


if __name__ == "__main__":
    main()