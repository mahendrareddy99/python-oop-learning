from day03_oop_inheritance import Developer, Manager, HRManager


def test_developer_bonus():
    developer = Developer(
        101,
        "Rahul",
        60000,
        "IT",
        "Python",
        3
    )

    assert developer.calculate_bonus() == 6000


def test_manager_bonus():
    manager = Manager(
        102,
        "Priya",
        90000,
        "Management",
        10,
        5000
    )

    assert manager.calculate_bonus() == 18500


def test_hr_manager_bonus():
    hr_manager = HRManager(
        103,
        "Anita",
        70000,
        "Human Resources",
        50
    )

    assert hr_manager.calculate_bonus() == 5600


def test_salary_getter_and_setter():
    developer = Developer(
        101,
        "Rahul",
        60000,
        "IT",
        "Python",
        3
    )

    assert developer.get_salary() == 60000

    developer.set_salary(65000)

    assert developer.get_salary() == 65000


def test_polymorphism():
    employees = [
        Developer(101, "Rahul", 60000, "IT", "Python", 3),
        Manager(102, "Priya", 90000, "Management", 10, 5000),
        HRManager(103, "Anita", 70000, "Human Resources", 50)
    ]

    bonuses = [
        employee.calculate_bonus()
        for employee in employees
    ]

    assert bonuses == [6000, 18500, 5600]