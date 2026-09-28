from abc import ABC, abstractmethod


class Employee(ABC):

    company_name = "Tech Solutions"

    def __init__(self, employee_id, name, department, salary):
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.__salary = salary

    def get_salary(self):
        return self.__salary

    def set_salary(self, salary):
        if salary <= 0:
            raise ValueError("Salary must be greater than 0")

        self.__salary = salary

    @classmethod
    def change_company_name(cls, new_name):
        cls.company_name = new_name

    def display_info(self):
        print(f"ID         : {self.employee_id}")
        print(f"Name       : {self.name}")
        print(f"Department : {self.department}")
        print(f"Salary     : {self.__salary}")

    def calculate_salary(self):
        return self.get_salary()

    @abstractmethod
    def calculate_bonus(self):
        pass


class Developer(Employee):

    def calculate_bonus(self):
        return self.get_salary() * 0.10

class Manager(Employee):

    def calculate_bonus(self):
        return self.get_salary() * 0.20


class HRManager(Employee):

    def calculate_bonus(self):
        return self.get_salary() * 0.15