"""
Story 6: OOP Coding Challenges
Run: python coding_challenges.py

Ten small, runnable examples demonstrating classes, objects, encapsulation,
inheritance, polymorphism, composition, and working with collections.
"""


# 1. Student class
class Student:
    def __init__(self, name, roll_number, marks):
        self.name = name
        self.roll_number = roll_number
        self.marks = marks

    def average(self):
        return sum(self.marks) / len(self.marks) if self.marks else 0.0

    def display(self):
        print(
            f"Student: {self.name} | Roll: {self.roll_number} | "
            f"Average: {self.average():.2f}"
        )


# 2. Bank account class
class BankAccount:
    def __init__(self, account_holder, opening_balance=0.0):
        if opening_balance < 0:
            raise ValueError("Opening balance cannot be negative.")
        self.account_holder = account_holder
        self._balance = float(opening_balance)

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be greater than zero.")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be greater than zero.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount


# 3. Employee management
class Employee:
    def __init__(self, employee_id, name, role, salary):
        if salary < 0:
            raise ValueError("Salary cannot be negative.")
        self.employee_id = employee_id
        self.name = name
        self.role = role
        self.salary = float(salary)

    def __str__(self):
        return f"{self.employee_id}: {self.name} | {self.role} | ₹{self.salary:.2f}"


class EmployeeManager:
    def __init__(self):
        self._employees = {}

    def add_employee(self, employee):
        if employee.employee_id in self._employees:
            raise ValueError("Employee ID already exists.")
        self._employees[employee.employee_id] = employee

    def get_employee(self, employee_id):
        return self._employees.get(employee_id)

    def list_employees(self):
        return list(self._employees.values())


# 4. Vehicle inheritance
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def move(self):
        return f"{self.brand} vehicle is moving."


class Car(Vehicle):
    def move(self):
        return f"{self.brand} car is driving on the road."


class Bike(Vehicle):
    def move(self):
        return f"{self.brand} bike is riding on the road."


# 5. Shape area calculator
from abc import ABC, abstractmethod
from math import pi


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        if radius < 0:
            raise ValueError("Radius cannot be negative.")
        self.radius = radius

    def area(self):
        return pi * self.radius**2


class Rectangle(Shape):
    def __init__(self, width, height):
        if width < 0 or height < 0:
            raise ValueError("Dimensions cannot be negative.")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


# 6. Shopping cart
class ShoppingCart:
    def __init__(self):
        self._items = {}

    def add_item(self, name, price, quantity=1):
        if price < 0 or quantity <= 0:
            raise ValueError("Price must be non-negative and quantity positive.")
        if name in self._items:
            old_price, old_quantity = self._items[name]
            if old_price != price:
                raise ValueError("The same item cannot have two different prices.")
            self._items[name] = (price, old_quantity + quantity)
        else:
            self._items[name] = (price, quantity)

    def remove_item(self, name):
        if name not in self._items:
            raise KeyError(f"{name!r} is not in the cart.")
        del self._items[name]

    def total(self):
        return sum(price * quantity for price, quantity in self._items.values())

    def display(self):
        for name, (price, quantity) in self._items.items():
            print(f"{name}: ₹{price:.2f} x {quantity}")
        print(f"Cart total: ₹{self.total():.2f}")


# 7. Movie rating system
class Movie:
    def __init__(self, title):
        self.title = title
        self._ratings = []

    def add_rating(self, rating):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5.")
        self._ratings.append(rating)

    @property
    def average_rating(self):
        return sum(self._ratings) / len(self._ratings) if self._ratings else 0.0

    @property
    def rating_count(self):
        return len(self._ratings)


# 8. Hospital patient records
class Patient:
    def __init__(self, patient_id, name, age, diagnosis):
        if age < 0:
            raise ValueError("Age cannot be negative.")
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.diagnosis = diagnosis

    def __str__(self):
        return (
            f"Patient ID: {self.patient_id} | Name: {self.name} | "
            f"Age: {self.age} | Diagnosis: {self.diagnosis}"
        )


class PatientRegistry:
    def __init__(self):
        self._patients = {}

    def add_patient(self, patient):
        if patient.patient_id in self._patients:
            raise ValueError("Patient ID already exists.")
        self._patients[patient.patient_id] = patient

    def find_patient(self, patient_id):
        return self._patients.get(patient_id)

    def list_patients(self):
        return list(self._patients.values())


# 9. School result processing
class SchoolResult:
    def __init__(self, student_name, subject_marks):
        if any(mark < 0 or mark > 100 for mark in subject_marks.values()):
            raise ValueError("Each mark must be between 0 and 100.")
        self.student_name = student_name
        self.subject_marks = dict(subject_marks)

    @property
    def total(self):
        return sum(self.subject_marks.values())

    @property
    def percentage(self):
        if not self.subject_marks:
            return 0.0
        return self.total / len(self.subject_marks)

    @property
    def result(self):
        return (
            "Pass"
            if self.subject_marks
            and all(mark >= 35 for mark in self.subject_marks.values())
            else "Fail"
        )

    def display(self):
        print(
            f"{self.student_name}: Total={self.total}, "
            f"Percentage={self.percentage:.2f}%, Result={self.result}"
        )


# 10. Online course management
class Course:
    def __init__(self, course_id, title):
        self.course_id = course_id
        self.title = title
        self._students = set()

    def enroll(self, student_name):
        if not student_name.strip():
            raise ValueError("Student name cannot be empty.")
        self._students.add(student_name)

    def unenroll(self, student_name):
        self._students.discard(student_name)

    @property
    def enrolled_students(self):
        return sorted(self._students)

    def display(self):
        print(f"{self.title} ({self.course_id})")
        print(f"Enrolled students: {', '.join(self.enrolled_students) or 'None'}")


def main():
    print("\n1. Student class")
    student = Student("Ananya", "S101", [85, 90, 78])
    student.display()

    print("\n2. Bank account")
    account = BankAccount("Ravi", 1000)
    account.deposit(500)
    account.withdraw(200)
    print(f"{account.account_holder}'s balance: ₹{account.balance:.2f}")

    print("\n3. Employee management")
    manager = EmployeeManager()
    manager.add_employee(Employee("E101", "Priya", "Developer", 45000))
    manager.add_employee(Employee("E102", "Arjun", "Tester", 38000))
    for employee in manager.list_employees():
        print(employee)

    print("\n4. Vehicle inheritance")
    for vehicle in [Car("Toyota"), Bike("Honda")]:
        print(vehicle.move())

    print("\n5. Shape area calculator")
    shapes = [Circle(3), Rectangle(4, 5)]
    for shape in shapes:
        print(f"{type(shape).__name__} area: {shape.area():.2f}")

    print("\n6. Shopping cart")
    cart = ShoppingCart()
    cart.add_item("Notebook", 50, 2)
    cart.add_item("Pen", 10, 3)
    cart.display()

    print("\n7. Movie rating system")
    movie = Movie("The Example Movie")
    movie.add_rating(4)
    movie.add_rating(5)
    movie.add_rating(3)
    print(
        f"{movie.title}: average {movie.average_rating:.2f}/5 from {movie.rating_count} ratings"
    )

    print("\n8. Hospital patient records")
    registry = PatientRegistry()

    registry.add_patient(Patient("P101", "Kiran", 35, "Routine check-up"))

    for patient in registry.list_patients():
        print(patient)

    print("\n9. School result processing")
    result = SchoolResult("Meera", {"Maths": 88, "Science": 76, "English": 91})
    result.display()

    print("\n10. Online course management")
    course = Course("PY101", "Python OOP Fundamentals")
    course.enroll("Meera")
    course.enroll("Kiran")
    course.display()


if __name__ == "__main__":
    main()
