from day04_banking_system import (
    Customer,
    SavingsAccount,
    CurrentAccount,
    Bank
)


def test_account_creation():
    customer = Customer(
        "C001",
        "Mahendra",
        "mahendra@example.com",
        "9876543210"
    )

    account = SavingsAccount("S001", customer, 10000)

    assert account.account_number == "S001"
    assert account.balance == 10000


def test_deposit():
    customer = Customer(
        "C001",
        "Mahendra",
        "mahendra@example.com",
        "9876543210"
    )

    account = SavingsAccount("S001", customer, 10000)

    account.deposit(2000)

    assert account.balance == 12000


def test_withdrawal():
    customer = Customer(
        "C001",
        "Mahendra",
        "mahendra@example.com",
        "9876543210"
    )

    account = SavingsAccount("S001", customer, 10000)

    account.withdraw(3000)

    assert account.balance == 7000


def test_insufficient_balance():
    customer = Customer(
        "C001",
        "Mahendra",
        "mahendra@example.com",
        "9876543210"
    )

    account = SavingsAccount("S001", customer, 1000)

    try:
        account.withdraw(2000)
        assert False
    except ValueError:
        assert True


def test_savings_interest():
    customer = Customer(
        "C001",
        "Mahendra",
        "mahendra@example.com",
        "9876543210"
    )

    account = SavingsAccount("S001", customer, 10000)

    interest = account.calculate_interest()

    assert interest == 400


def test_current_account_rules():
    customer = Customer(
        "C002",
        "Rahul",
        "rahul@example.com",
        "9876501234"
    )

    account = CurrentAccount("C002-A", customer, 5000)

    account.withdraw(8000)

    assert account.balance == -3000


def test_invalid_deposit():
    customer = Customer(
        "C001",
        "Mahendra",
        "mahendra@example.com",
        "9876543210"
    )

    account = SavingsAccount("S001", customer, 10000)

    try:
        account.deposit(-500)
        assert False
    except ValueError:
        assert True


def test_multiple_customers():
    bank = Bank("ABC Bank")

    customer1 = Customer(
        "C001",
        "Mahendra",
        "mahendra@example.com",
        "9876543210"
    )

    customer2 = Customer(
        "C002",
        "Rahul",
        "rahul@example.com",
        "9876501234"
    )

    bank.add_customer(customer1)
    bank.add_customer(customer2)

    assert len(bank.customers) == 2


print("All Day 4 tests passed!")