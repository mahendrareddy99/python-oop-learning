# Day 2 - Python OOP
# Instance Variables, Class Variables and Instance Methods


class Student:

    # Class variable
    college = "Akshaya College"

    def __init__(self, name, age):

        # Instance variables
        self.name = name
        self.age = age

    # Instance method
    def introduce(self):
        print(f"My name is {self.name} and I am {self.age} years old.")


# Creating objects
student1 = Student("Mahendra", 21)
student2 = Student("Rahul", 22)


# Instance variables
print("Student 1:", student1.name, student1.age)
print("Student 2:", student2.name, student2.age)


# Class variable
print("College:", student1.college)
print("College:", student2.college)


# Modify class variable
Student.college = "ABC College"

print("\nAfter changing college:")
print(student1.college)
print(student2.college)


# Instance method
print("\nStudent Introductions:")
student1.introduce()
student2.introduce()

# ------------------------------------------
# TASK 6 - CLASS METHOD
# ------------------------------------------

class Employee:

    company = "ABC Technologies"

    def __init__(self, name):
        self.name = name

    @classmethod
    def change_company(cls, new_company):
        cls.company = new_company


employee1 = Employee("Mahendra")
employee2 = Employee("Rahul")

print("\nClass Method:")
print(employee1.company)

Employee.change_company("XYZ Technologies")

print(employee1.company)
print(employee2.company)

# ------------------------------------------
# TASK 7 - STATIC METHOD
# ------------------------------------------

class Calculator:

    @staticmethod
    def add(a, b):
        return a + b


print("\nStatic Method:")

result = Calculator.add(10, 20)

print("Result:", result)

# ------------------------------------------
# TASK 8 - WHEN TO USE EACH METHOD
# ------------------------------------------

class Example:

    class_data = "Python OOP"

    def __init__(self, name):
        self.name = name

    # Instance method
    def show_name(self):
        return self.name

    # Class method
    @classmethod
    def show_class_data(cls):
        return cls.class_data

    # Static method
    @staticmethod
    def multiply(a, b):
        return a * b


example = Example("Mahendra")

print("\nMethod Types:")

print("Instance Method:", example.show_name())

print("Class Method:", Example.show_class_data())

print("Static Method:", Example.multiply(5, 4))

# ------------------------------------------
# TASK 9 - PRIVATE-STYLE ATTRIBUTES
# ------------------------------------------

class BankAccount:

    def __init__(self, name, balance):
        self.name = name
        self.__balance = balance

    def show_balance(self):
        return self.__balance


account = BankAccount("Mahendra", 5000)

print("\nPrivate-Style Attribute:")
print("Account Holder:", account.name)
print("Balance:", account.show_balance())

# ------------------------------------------
# TASK 10 - GETTER AND SETTER
# ------------------------------------------

class Person:

    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    # Getter
    def get_age(self):
        return self.__age

    # Setter
    def set_age(self, age):
        self.__age = age


person = Person("Mahendra", 21)

print("\nGetter and Setter:")

print("Original age:", person.get_age())

person.set_age(22)

print("Updated age:", person.get_age())

# ------------------------------------------
# TASK 11 - VALIDATION IN SETTER
# ------------------------------------------

class Student:

    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def get_age(self):
        return self.__age

    def set_age(self, age):

        if age >= 18:
            self.__age = age
            print("Age updated successfully.")
        else:
            print("Invalid age. Age must be 18 or above.")


student = Student("Mahendra", 21)

print("\nSetter Validation:")

student.set_age(22)
print("Current age:", student.get_age())

student.set_age(15)
print("Current age:", student.get_age())

# ------------------------------------------
# TASK 12 - MEANINGFUL METHOD NAMES
# ------------------------------------------

class BankAccount:

    def __init__(self, balance):
        self.balance = balance

    def deposit_money(self, amount):
        self.balance += amount

    def withdraw_money(self, amount):

        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Insufficient balance.")

    def show_balance(self):
        print("Current balance:", self.balance)


account = BankAccount(5000)

print("\nMeaningful Method Names:")

account.deposit_money(1000)
account.show_balance()

account.withdraw_money(2000)
account.show_balance()