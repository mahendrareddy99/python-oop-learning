from abc import ABC, abstractmethod


class Account(ABC):
    """Abstract base class for all bank accounts."""

    def __init__(self, account_number, customer, balance=0):
        self.account_number = account_number
        self.customer = customer
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than 0.")

        self.balance += amount
        print(f"₹{amount} deposited successfully.")

    @abstractmethod
    def withdraw(self, amount):
        """Withdraw money according to account-specific rules."""
        pass

    @abstractmethod
    def calculate_interest(self):
        """Calculate interest according to account type."""
        pass

    def display_balance(self):
        print(f"Account Balance: ₹{self.balance}")


class SavingsAccount(Account):
    """Savings account with interest calculation."""

    INTEREST_RATE = 0.04

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than 0.")

        if amount > self.balance:
            raise ValueError("Insufficient balance.")

        self.balance -= amount
        print(f"₹{amount} withdrawn successfully.")

    def calculate_interest(self):
        interest = self.balance * self.INTEREST_RATE
        return interest


class CurrentAccount(Account):
    """Current account with overdraft support."""

    OVERDRAFT_LIMIT = 5000

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than 0.")

        if amount > self.balance + self.OVERDRAFT_LIMIT:
            raise ValueError(
                "Withdrawal exceeds current account overdraft limit."
            )

        self.balance -= amount
        print(f"₹{amount} withdrawn successfully.")

    def calculate_interest(self):
        return 0


class Customer:
    """Represents a bank customer."""

    def __init__(self, customer_id, name, email, phone):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def display_customer(self):
        print(f"Customer ID: {self.customer_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Phone: {self.phone}")


class Bank:
    """Manages customers and accounts."""

    def __init__(self, name):
        self.name = name
        self.customers = []
        self.accounts = []

    def add_customer(self, customer):
        self.customers.append(customer)

    def add_account(self, account):
        self.accounts.append(account)
        account.customer.add_account(account)

    def find_customer(self, customer_id):
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer

        return None

    def find_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account

        return None

    def display_bank_details(self):
        print(f"\nBank: {self.name}")
        print(f"Total Customers: {len(self.customers)}")
        print(f"Total Accounts: {len(self.accounts)}")


def main():
    # Create bank
    bank = Bank("ABC Bank")

    # Create customers
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

    # Create accounts
    savings = SavingsAccount(
        "S001",
        customer1,
        10000
    )

    current = CurrentAccount(
        "C001-A",
        customer2,
        5000
    )

    # Add accounts to bank
    bank.add_account(savings)
    bank.add_account(current)

    # Display bank details
    bank.display_bank_details()

    # Deposit
    print("\n--- Deposit ---")
    savings.deposit(2000)
    savings.display_balance()

    # Withdrawal
    print("\n--- Savings Withdrawal ---")
    savings.withdraw(3000)
    savings.display_balance()

    # Savings interest
    print("\n--- Savings Interest ---")
    interest = savings.calculate_interest()
    print(f"Interest: ₹{interest}")

    # Current account withdrawal
    print("\n--- Current Account Withdrawal ---")
    current.withdraw(8000)
    current.display_balance()

    # Customer details
    print("\n--- Customer Details ---")
    customer1.display_customer()


if __name__ == "__main__":
    main()