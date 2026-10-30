"""Story 2: Practical examples of Python OOP concepts."""


# 1. Encapsulation
class BankAccount:
    """Manage a bank account with a private balance."""

    def __init__(self, owner: str, balance: float = 0) -> None:
        if balance < 0:
            raise ValueError("Balance cannot be negative.")
        self.owner = owner
        self.__balance = balance

    @property
    def balance(self) -> float:
        return self.__balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        self.__balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient funds.")
        self.__balance -= amount


# 2. Single inheritance: Student inherits from Person
class Person:
    def __init__(self, name: str) -> None:
        self.name = name

    def introduce(self) -> str:
        return f"My name is {self.name}."


class Student(Person):
    def __init__(self, name: str, student_id: str) -> None:
        super().__init__(name)
        self.student_id = student_id

    def introduce(self) -> str:
        return f"I am {self.name}, student ID: {self.student_id}."


# 3. Multiple inheritance
class Swimmer:
    def swim(self) -> str:
        return "Swimming"


class Flyer:
    def fly(self) -> str:
        return "Flying"


class Duck(Swimmer, Flyer):
    pass


# 4. Multilevel inheritance: Person -> Employee -> Manager
class Employee(Person):
    def __init__(self, name: str, employee_id: str) -> None:
        super().__init__(name)
        self.employee_id = employee_id


class Manager(Employee):
    def __init__(self, name: str, employee_id: str, team_size: int) -> None:
        super().__init__(name, employee_id)
        self.team_size = team_size


# 5. Hierarchical inheritance: Car and Bike inherit from Vehicle
class Vehicle:
    def move(self) -> str:
        return "The vehicle is moving."


class Car(Vehicle):
    def move(self) -> str:
        return "The car is driving."


class Bike(Vehicle):
    def move(self) -> str:
        return "The bike is riding."


# 6. Polymorphism: same method call, different behavior
def show_movement(vehicle: Vehicle) -> None:
    print(vehicle.move())


# 7. Default arguments as a method-overloading alternative
class Greeter:
    def greet(self, name: str = "Guest", greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"


# 8. Composition: Library creates and owns its Catalog in this design
class Catalog:
    def __init__(self) -> None:
        self.books: list[str] = []

    def add_book(self, title: str) -> None:
        self.books.append(title)


class Library:
    def __init__(self, name: str) -> None:
        self.name = name
        self.catalog = Catalog()

    def add_book(self, title: str) -> None:
        self.catalog.add_book(title)


# 9. Aggregation: Team uses independently created TeamMember objects
class TeamMember:
    def __init__(self, name: str) -> None:
        self.name = name


class Team:
    def __init__(self, name: str, members: list[TeamMember] | None = None) -> None:
        self.name = name
        self.members = list(members) if members is not None else []

    def add_member(self, member: TeamMember) -> None:
        self.members.append(member)


def main() -> None:
    """Demonstrate the OOP concepts."""
    print("1. Encapsulation")
    account = BankAccount("Ravi", 1000)
    account.deposit(250)
    account.withdraw(100)
    print(f"Balance: {account.balance:.2f}")

    print("\n2. Single inheritance and overriding")
    print(Student("Anu", "S101").introduce())

    print("\n3. Multiple inheritance")
    duck = Duck()
    print(duck.swim())
    print(duck.fly())

    print("\n4. Multilevel inheritance")
    manager = Manager("Kiran", "E201", 5)
    print(f"{manager.name}, {manager.employee_id}, team: {manager.team_size}")

    print("\n5. Hierarchical inheritance and polymorphism")
    show_movement(Car())
    show_movement(Bike())

    print("\n6. Default-argument method overloading alternative")
    greeter = Greeter()
    print(greeter.greet())
    print(greeter.greet("Mahendra"))
    print(greeter.greet("Mahendra", "Welcome"))

    print("\n7. Composition")
    library = Library("Central Library")
    library.add_book("Python Basics")
    print(library.catalog.books)

    print("\n8. Aggregation")
    ravi = TeamMember("Ravi")
    sita = TeamMember("Sita")
    team = Team("Development", [ravi])
    team.add_member(sita)
    print([member.name for member in team.members])


if __name__ == "__main__":
    main()
