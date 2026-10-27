
# Story 1: Python OOP Fundamentals

## 1. What is OOP?

Object-Oriented Programming (OOP) organizes code using objects that
combine data (attributes) and behavior (methods).

Real-world example: A book has a title and author and can display
its details.

## 2. Classes and Objects

A class is a blueprint. An object is an instance of that class.

```python
class Dog:
    def bark(self):
        print("Woof!")


dog = Dog()
dog.bark()
```

Output: `Woof!`

Diagram:

```text
       Dog (class)
       /         \
    dog1         dog2
   (object)     (object)
```

## 3. Constructor: __init__

`__init__` initializes an object when it is created.

```python
class Student:
    def __init__(self, name):
        self.name = name


student = Student("Anu")
print(student.name)
```

Output: `Anu`

## 4. The self Parameter

`self` refers to the current instance. It allows methods to access
or update that object's attributes.

```python
class Student:
    def __init__(self, name):
        self.name = name

    def introduce(self):
        print(f"My name is {self.name}")


Student("Anu").introduce()
```

## 5. Instance Variables and Class Variables

Instance variables belong to individual objects.
Class variables are defined in the class body and shared at class level.

```python
class Employee:
    company = "ABC Technologies"

    def __init__(self, name):
        self.name = name


first = Employee("Ravi")
second = Employee("Sita")

print(first.name)
print(second.name)
print(first.company)
```

Output:

```text
Ravi
Sita
ABC Technologies
```

## 6. Instance, Class, and Static Methods

- Instance method: receives `self`; works with an object's state.
- Class method: receives `cls`; works with class-level state.
- Static method: receives neither automatically; useful for related utilities.

```python
class Employee:
    count = 0

    def __init__(self, name):
        self.name = name
        Employee.count += 1

    def introduce(self):
        return f"I am {self.name}"

    @classmethod
    def get_count(cls):
        return cls.count

    @staticmethod
    def valid_name(name):
        return bool(name.strip())


employee = Employee("Ravi")
print(employee.introduce())
print(Employee.get_count())
print(Employee.valid_name("Ravi"))
```

Output:

```text
I am Ravi
1
True
```

## 7. Object Lifecycle

1. Define a class.
2. Create an object.
3. Python creates the instance and initializes it.
4. Use its attributes and methods.
5. When no longer referenced, it may become eligible for garbage collection.

`__new__` creates an instance; `__init__` initializes it.
Deleting a reference does not guarantee immediate object cleanup.

## 8. Real-World Example

A library management application can use classes such as Book,
Member, Library, and Issue.

- Book stores title, author, and availability.
- Member stores member details.
- Library manages books and members.
- Issue tracks borrowing and returns.

## 9. Important Comparisons

### Class vs Object

| Class | Object |
|---|---|
| Blueprint | Instance of a class |
| Defines behavior and attributes | Holds its own instance data |
| Example: Book | Example: Book("Python", "Ravi") |

### Instance vs Class Variables

| Instance variable | Class variable |
|---|---|
| Object-specific | Shared at class level |
| Usually uses self | Defined in class body |
| Example: self.name | Example: company |

### self vs cls

| self | cls |
|---|---|
| Current instance | Current class |
| Used in instance methods | Used in class methods |

### Method Types

| Method | First automatic argument | Purpose |
|---|---|---|
| Instance | self | Object behavior |
| Class | cls | Class-level behavior |
| Static | None | Related utility operation |

## 10. Key Takeaways

- Classes define objects; objects are instances of classes.
- `__init__` initializes instance data.
- `self` refers to an instance; `cls` refers to a class.
- Instance variables hold object-specific data.
- Class variables hold class-level data.
- Decorators `@classmethod` and `@staticmethod` declare method types.
- OOP helps make software reusable, organized, and maintainable.
