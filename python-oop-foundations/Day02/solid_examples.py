"""
Story 5: SOLID Principles
Run: python solid_examples.py

SOLID is a set of five design principles that help make software easier
to understand, test, extend, and maintain.
"""

from abc import ABC, abstractmethod


# 1. Single Responsibility Principle (SRP)
# A class should have one main responsibility and one reason to change.
class Invoice:
    def __init__(self, items):
        self.items = items

    def total(self):
        return sum(price for _, price in self.items)


class InvoicePrinter:
    """Responsible only for displaying an invoice."""

    @staticmethod
    def print_invoice(invoice):
        print("Invoice")
        for name, price in invoice.items:
            print(f"- {name}: ₹{price:.2f}")
        print(f"Total: ₹{invoice.total():.2f}")


# 2. Open/Closed Principle (OCP)
# Software should be open for extension but closed for modification.
class Discount(ABC):
    @abstractmethod
    def calculate(self, amount):
        pass


class NoDiscount(Discount):
    def calculate(self, amount):
        return amount


class TenPercentDiscount(Discount):
    def calculate(self, amount):
        return amount * 0.90


def final_price(amount, discount: Discount):
    """New discount rules can be added without changing this function."""
    return discount.calculate(amount)


# 3. Liskov Substitution Principle (LSP)
# A subtype should be usable wherever its base type is expected.
class Bird(ABC):
    @abstractmethod
    def move(self):
        pass


class Sparrow(Bird):
    def move(self):
        return "Sparrow flies."


class Penguin(Bird):
    def move(self):
        return "Penguin swims."


def describe_movement(bird: Bird):
    """Works with any Bird subtype without making assumptions about flying."""
    print(bird.move())


# 4. Interface Segregation Principle (ISP)
# Prefer small, focused interfaces instead of forcing classes to implement
# methods they do not need.
class Printable(ABC):
    @abstractmethod
    def print_document(self):
        pass


class Scannable(ABC):
    @abstractmethod
    def scan_document(self):
        pass


class BasicPrinter(Printable):
    def print_document(self):
        return "Printing document."


class MultiFunctionPrinter(Printable, Scannable):
    def print_document(self):
        return "Printing document."

    def scan_document(self):
        return "Scanning document."


# 5. Dependency Inversion Principle (DIP)
# High-level code should depend on an abstraction, not a specific implementation.
class MessageSender(ABC):
    @abstractmethod
    def send(self, message):
        pass


class EmailSender(MessageSender):
    def send(self, message):
        return f"Email sent: {message}"


class SMSSender(MessageSender):
    def send(self, message):
        return f"SMS sent: {message}"


class NotificationService:
    def __init__(self, sender: MessageSender):
        self.sender = sender

    def notify(self, message):
        return self.sender.send(message)


def main():
    print("\n1. Single Responsibility Principle")
    invoice = Invoice([("Book", 250), ("Pen", 20)])
    InvoicePrinter.print_invoice(invoice)

    print("\n2. Open/Closed Principle")
    amount = 1000
    print(f"No discount: ₹{final_price(amount, NoDiscount()):.2f}")
    print(f"10% discount: ₹{final_price(amount, TenPercentDiscount()):.2f}")

    print("\n3. Liskov Substitution Principle")
    describe_movement(Sparrow())
    describe_movement(Penguin())

    print("\n4. Interface Segregation Principle")
    print(BasicPrinter().print_document())
    printer = MultiFunctionPrinter()
    print(printer.print_document())
    print(printer.scan_document())

    print("\n5. Dependency Inversion Principle")
    email_service = NotificationService(EmailSender())
    sms_service = NotificationService(SMSSender())
    print(email_service.notify("Your order is confirmed."))
    print(sms_service.notify("Your OTP is 123456."))


if __name__ == "__main__":
    main()
