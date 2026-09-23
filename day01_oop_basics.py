# Day 1 - Python OOP Basics
# Topics: Classes, Objects, Constructors, Attributes, Methods and Validation


# ---------------------------------------------------------
# 1. Employee Class
# ---------------------------------------------------------

class Employee:

    def __init__(self, employee_id, name, department, salary, experience):
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.salary = salary
        self.experience = experience

    def display_details(self):
        print(f"Employee ID : {self.employee_id}")
        print(f"Name        : {self.name}")
        print(f"Department  : {self.department}")
        print(f"Salary      : ₹{self.salary}")
        print(f"Experience  : {self.experience} years")

    def calculate_bonus(self):
        if self.experience >= 5:
            bonus = self.salary * 0.10
        elif self.experience >= 2:
            bonus = self.salary * 0.05
        else:
            bonus = self.salary * 0.02

        return bonus

    def calculate_annual_salary(self):
        return self.salary * 12

    def update_salary(self, new_salary):
        if new_salary <= 0:
            print("Invalid salary. Salary must be greater than 0.")
            return

        self.salary = new_salary
        print(f"Salary updated successfully for {self.name}.")


# ---------------------------------------------------------
# 2. Creating 5 Employee Objects
# ---------------------------------------------------------

employee1 = Employee(101, "Rahul", "IT", 50000, 3)
employee2 = Employee(102, "Priya", "HR", 45000, 2)
employee3 = Employee(103, "Arjun", "Finance", 60000, 6)
employee4 = Employee(104, "Sneha", "Marketing", 40000, 1)
employee5 = Employee(105, "Kiran", "Development", 70000, 8)


employees = [
    employee1,
    employee2,
    employee3,
    employee4,
    employee5
]


# ---------------------------------------------------------
# 3. Display Employee Information
# ---------------------------------------------------------

print("\n========== EMPLOYEE DETAILS ==========\n")

for employee in employees:
    employee.display_details()

    print(f"Bonus         : ₹{employee.calculate_bonus()}")
    print(f"Annual Salary : ₹{employee.calculate_annual_salary()}")
    print("-" * 40)


# ---------------------------------------------------------
# 4. Modify Employee Attribute
# ---------------------------------------------------------

print("\n========== UPDATING SALARY ==========\n")

employee1.update_salary(55000)

print(f"Updated Salary: ₹{employee1.salary}")


# Test validation
employee2.update_salary(-5000)


# ---------------------------------------------------------
# 5. Student Class
# ---------------------------------------------------------

class Student:

    def __init__(self, name, roll_number, course, marks):
        self.name = name
        self.roll_number = roll_number
        self.course = course
        self.marks = marks

    def display_details(self):
        print(f"Name        : {self.name}")
        print(f"Roll Number : {self.roll_number}")
        print(f"Course      : {self.course}")
        print(f"Marks       : {self.marks}")

    def is_passed(self):
        return self.marks >= 40


student1 = Student(
    "Mahendra",
    101,
    "AI & Data Science",
    82
)

print("\n========== STUDENT ==========\n")
student1.display_details()
print(f"Passed      : {student1.is_passed()}")


# ---------------------------------------------------------
# 6. BankAccount Class
# ---------------------------------------------------------

class BankAccount:

    def __init__(self, account_number, holder_name, balance):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be greater than 0.")
            return

        self.balance += amount
        print(f"₹{amount} deposited successfully.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be greater than 0.")
            return

        if amount > self.balance:
            print("Insufficient balance.")
            return

        self.balance -= amount
        print(f"₹{amount} withdrawn successfully.")

    def display_balance(self):
        print(f"Account Holder : {self.holder_name}")
        print(f"Balance        : ₹{self.balance}")


account1 = BankAccount("ACC101", "Mahendra", 10000)

print("\n========== BANK ACCOUNT ==========\n")

account1.display_balance()
account1.deposit(5000)
account1.withdraw(3000)
account1.display_balance()


# ---------------------------------------------------------
# 7. Product Class
# ---------------------------------------------------------

class Product:

    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def calculate_total_value(self):
        return self.price * self.quantity

    def display_details(self):
        print(f"Product ID : {self.product_id}")
        print(f"Name       : {self.name}")
        print(f"Price      : ₹{self.price}")
        print(f"Quantity   : {self.quantity}")
        print(f"Total      : ₹{self.calculate_total_value()}")


product1 = Product(1, "Laptop", 60000, 2)

print("\n========== PRODUCT ==========\n")
product1.display_details()


# ---------------------------------------------------------
# 8. Car Class
# ---------------------------------------------------------

class Car:

    def __init__(self, brand, model, year, price):
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price

    def display_details(self):
        print(f"Brand : {self.brand}")
        print(f"Model : {self.model}")
        print(f"Year  : {self.year}")
        print(f"Price : ₹{self.price}")

    def apply_discount(self, percentage):
        if percentage < 0 or percentage > 100:
            print("Invalid discount percentage.")
            return

        discount = self.price * percentage / 100
        self.price -= discount


car1 = Car("Toyota", "Fortuner", 2025, 4000000)

print("\n========== CAR ==========\n")
car1.display_details()

car1.apply_discount(10)

print("\nAfter Discount:")
car1.display_details()


# ---------------------------------------------------------
# 9. Book Class
# ---------------------------------------------------------

class Book:

    def __init__(self, title, author, price, pages):
        self.title = title
        self.author = author
        self.price = price
        self.pages = pages

    def display_details(self):
        print(f"Title  : {self.title}")
        print(f"Author : {self.author}")
        print(f"Price  : ₹{self.price}")
        print(f"Pages  : {self.pages}")


book1 = Book(
    "Python Programming",
    "John Smith",
    599,
    450
)

print("\n========== BOOK ==========\n")
book1.display_details()