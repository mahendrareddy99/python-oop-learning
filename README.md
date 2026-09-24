# Python OOP Learning

This repository contains my 5-day Python Object-Oriented Programming (OOP) learning journey.

## Epic Details

- **Duration:** 21-Sep-2026 to 25-Sep-2026
- **Working Days:** 5
- **Daily Effort:** 8 Hours
- **Total Effort:** 40 Hours

## Epic Objective

The objective of this Epic is to move from procedural Python programming to Object-Oriented Programming.

By the end of the Epic, I will understand and implement:

- Classes
- Objects
- Constructors
- Instance Variables
- Instance Methods
- Inheritance
- Encapsulation
- Polymorphism
- Abstraction

## Daily Progress

| Day | Topic | Status |
|---|---|---|
| Day 1 | Classes, Objects & Constructors | Completed |
| Day 2 | TBD | Pending |
| Day 3 | TBD | Pending |
| Day 4 | TBD | Pending |
| Day 5 | TBD | Pending |

## Day 1 — Classes, Objects & Constructors

### Topics Covered

- Understanding why OOP is used
- Creating classes
- Creating objects
- Understanding attributes
- Instance variables
- Instance methods
- Understanding `self`
- Using `__init__()` constructors
- Passing values through constructors
- Creating multiple objects
- Displaying object information
- Modifying object attributes
- Adding validation inside methods

### Practical Assignment

Created an `Employee` class with:

- Employee ID
- Name
- Department
- Salary
- Experience

Implemented:

- `display_details()`
- `calculate_bonus()`
- `calculate_annual_salary()`
- `update_salary()`

Created five Employee objects and tested their methods.

### Additional Practice Classes

- Student
- BankAccount
- Product
- Car
- Book

## Repository Structure

```text
python-oop-learning/
│
├── README.md
│
└── day01_oop_basics.py

## Day 2 - Attributes and Methods

### Topics Learned

- Instance variables
- Class variables
- Creating class variables
- Modifying class-level information
- Instance methods
- Class methods using `@classmethod`
- Static methods using `@staticmethod`
- Difference between instance, class, and static methods
- Private-style attributes
- Getter and setter methods
- Validation in setters
- Meaningful method names

### Tasks Completed

- [x] Understand instance variables
- [x] Understand class variables
- [x] Create a class variable
- [x] Modify class-level information
- [x] Understand instance methods
- [x] Create `@classmethod`
- [x] Create `@staticmethod`
- [x] Understand when to use each method type
- [x] Use private-style attributes
- [x] Create getter/setter methods
- [x] Add validation to setters
- [x] Use meaningful method names

### Practical Implementation

Implemented all Day 2 concepts in `day02_attributes_and_methods.py` and tested the program successfully using Python.

### Day 3 — Encapsulation, Inheritance & Polymorphism

### Objective

Learn how to build related classes, reuse common functionality, protect data, and implement different behaviors using inheritance and polymorphism.

### Concepts Learned

* Inheritance
* Parent and child classes
* Method overriding
* `super()`
* Encapsulation
* Private-style attributes
* Getters and setters
* Polymorphism

### Employee Hierarchy

```text
Employee
├── Developer
├── Manager
└── HRManager
```

The `Employee` class contains common attributes such as ID, name, salary, and department.

The child classes inherit these common attributes and add their own specific attributes.

### Inheritance

`Developer`, `Manager`, and `HRManager` inherit from the `Employee` parent class. The `super()` function is used to call the parent constructor and reuse parent functionality.

### Method Overriding

Each child class provides its own implementation of `calculate_bonus()`.

* Developer — 10% of salary
* Manager — 15% of salary + management bonus
* HRManager — 8% of salary

### Encapsulation

The employee salary is stored using the private-style attribute `__salary`. Getter and setter methods are used to access and modify the salary.

The setter validates the salary and rejects negative values.

### Polymorphism

Different employee objects are stored in the same list:

```python
employees = [
    developer,
    manager,
    hr_manager
]

for employee in employees:
    employee.calculate_bonus()
```

The same `calculate_bonus()` method call automatically executes the implementation belonging to each object's class.

### Testing

Created `tests/test_day03.py` using pytest.

Tested:

* Developer bonus calculation
* Manager bonus calculation
* HRManager bonus calculation
* Getter and setter functionality
* Polymorphism

### Test Result

```text
5 passed in 0.15s
```

### Day 3 Outcome

Successfully implemented an employee hierarchy using inheritance, encapsulation, method overriding, `super()`, getters/setters, and polymorphism. All five automated test cases passed successfully.
