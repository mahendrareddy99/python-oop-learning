"""
Story 3: Magic methods and operator overloading.

Run:
    python magic_methods.py

Expected output is printed by the example section at the bottom.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Product:
    """Represent stock for one product/SKU."""

    sku: str
    name: str
    unit_price: float
    quantity: int = 0

    def __post_init__(self) -> None:
        if not self.sku.strip():
            raise ValueError("SKU cannot be empty.")
        if not self.name.strip():
            raise ValueError("Product name cannot be empty.")
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative.")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative.")

    @property
    def total_value(self) -> float:
        """Return the total monetary value of this stock."""
        return self.unit_price * self.quantity

    def __str__(self) -> str:
        """Return a user-friendly representation."""
        return f"{self.name} (SKU: {self.sku}) — {self.quantity} units"

    def __repr__(self) -> str:
        """Return an unambiguous developer-oriented representation."""
        return (
            f"Product(sku={self.sku!r}, name={self.name!r}, "
            f"unit_price={self.unit_price!r}, quantity={self.quantity!r})"
        )

    def __len__(self) -> int:
        """Allow len(product) to return the stock quantity."""
        return self.quantity

    def __eq__(self, other: object) -> bool:
        """Products are equal when their SKUs match."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.sku == other.sku

    def __lt__(self, other: object) -> bool:
        """Compare products by total stock value."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.total_value < other.total_value

    def __gt__(self, other: object) -> bool:
        """Compare products by total stock value."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.total_value > other.total_value

    def __add__(self, other: object) -> Product:
        """Combine quantities for the same SKU."""
        if not isinstance(other, Product):
            return NotImplemented
        if self.sku != other.sku:
            raise ValueError("Only products with the same SKU can be added.")
        if self.unit_price != other.unit_price:
            raise ValueError("Products with the same SKU must have the same price.")
        return Product(self.sku, self.name, self.unit_price, self.quantity + other.quantity)

    def __sub__(self, other: object) -> Product:
        """Subtract quantities for the same SKU without allowing negative stock."""
        if not isinstance(other, Product):
            return NotImplemented
        if self.sku != other.sku:
            raise ValueError("Only products with the same SKU can be subtracted.")
        if other.quantity > self.quantity:
            raise ValueError("Cannot subtract more stock than is available.")
        return Product(self.sku, self.name, self.unit_price, self.quantity - other.quantity)


if __name__ == "__main__":
    laptop_a = Product("LAP-01", "Laptop", 50000.0, 5)
    laptop_b = Product("LAP-01", "Laptop", 50000.0, 3)
    mouse = Product("MOU-01", "Mouse", 500.0, 10)

    print("1. __str__:", str(laptop_a))
    print("2. __repr__:", repr(laptop_a))
    print("3. __len__:", len(laptop_a))
    print("4. __eq__:", laptop_a == laptop_b)
    print("5. __lt__:", mouse < laptop_a)
    print("6. __gt__:", laptop_a > mouse)
    print("7. __add__:", laptop_a + laptop_b)
    print("8. __sub__:", laptop_a - laptop_b)
    print("9. combined quantity:", len(laptop_a + laptop_b))
