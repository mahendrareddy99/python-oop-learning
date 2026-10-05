class Employee:
    def __init__(self, id, name, salary, department):
        self.id = id
        self.name = name
        self.__salary = salary
        self.department = department

    def display_details(self):
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Salary: {self.__salary}")
        print(f"Department: {self.department}")

    def calculate_bonus(self):
        return self.__salary * 0.05

    # Getter
    def get_salary(self):
        return self.__salary

    # Setter
    def set_salary(self, salary):
        if salary > 0:
            self.__salary = salary
        else:
            print("Salary must be positive")


class Developer(Employee):
    def __init__(
        self,
        id,
        name,
        salary,
        department,
        programming_language,
        projects
    ):
        super().__init__(id, name, salary, department)
        self.programming_language = programming_language
        self.projects = projects

    def display_details(self):
        super().display_details()
        print(f"Programming Language: {self.programming_language}")
        print(f"Projects: {self.projects}")

    def calculate_bonus(self):
        return self.get_salary() * 0.10


class Manager(Employee):
    def __init__(
        self,
        id,
        name,
        salary,
        department,
        team_size,
        management_bonus
    ):
        super().__init__(id, name, salary, department)
        self.team_size = team_size
        self.management_bonus = management_bonus

    def display_details(self):
        super().display_details()
        print(f"Team Size: {self.team_size}")
        print(f"Management Bonus: {self.management_bonus}")

    def calculate_bonus(self):
        return self.get_salary() * 0.15 + self.management_bonus


class HRManager(Employee):
    def __init__(
        self,
        id,
        name,
        salary,
        department,
        employees_handled
    ):
        super().__init__(id, name, salary, department)
        self.employees_handled = employees_handled

    def display_details(self):
        super().display_details()
        print(f"Employees Handled: {self.employees_handled}")

    def calculate_bonus(self):
        return self.get_salary() * 0.08


# Creating objects

developer = Developer(
    101,
    "Rahul",
    60000,
    "IT",
    "Python",
    3
)

manager = Manager(
    102,
    "Priya",
    90000,
    "Management",
    10,
    5000
)

hr_manager = HRManager(
    103,
    "Anita",
    70000,
    "Human Resources",
    50
)


# Display Developer details

print("----- Developer -----")
developer.display_details()
print("Bonus:", developer.calculate_bonus())


# Display Manager details

print("\n----- Manager -----")
manager.display_details()
print("Bonus:", manager.calculate_bonus())


# Display HR Manager details

print("\n----- HR Manager -----")
hr_manager.display_details()
print("Bonus:", hr_manager.calculate_bonus())


# Polymorphism

print("\n----- Polymorphism -----")

employees = [
    developer,
    manager,
    hr_manager
]

for employee in employees:
    print(
        f"{employee.name} bonus: "
        f"{employee.calculate_bonus()}"
    )


# Encapsulation Test

print("\n----- Encapsulation Test -----")

print("Developer salary:", developer.get_salary())

developer.set_salary(65000)

print("Updated Developer salary:", developer.get_salary())

developer.set_salary(-5000)