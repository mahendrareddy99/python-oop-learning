"""Book model and book catalogue operations."""

from dataclasses import asdict, dataclass
from typing import Any

from .exceptions import NotFoundError, ValidationError
from .storage import JSONStorage
from .validator import positive_int, required_text


@dataclass
class Book:
    """Represent one book in the catalogue."""

    id: str
    title: str
    author: str
    isbn: str
    total_copies: int = 1
    available_copies: int = 1

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Book":
        """Build a Book from a JSON record."""
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        """Convert the book to a JSON-compatible dictionary."""
        return asdict(self)


class BookManager:
    """Manage book creation, updates, deletion, search, and availability."""

    FILE = "books.json"

    def __init__(self, storage: JSONStorage) -> None:
        self.storage = storage

    def list_books(self) -> list[Book]:
        """Return all books."""
        return [Book.from_dict(row) for row in self.storage.read(self.FILE)]

    def get(self, book_id: str) -> Book:
        """Return a book by ID."""
        for book in self.list_books():
            if book.id == book_id:
                return book
        raise NotFoundError(f"Book '{book_id}' was not found.")

    def add(self, title: str, author: str, isbn: str, copies: int = 1) -> Book:
        """Add a book with a unique ISBN."""
        title = required_text(title, "Title")
        author = required_text(author, "Author")
        isbn = required_text(isbn, "ISBN")
        copies = positive_int(copies, "Copies")
        books = self.list_books()
        if any(book.isbn.casefold() == isbn.casefold() for book in books):
            raise ValidationError(f"ISBN '{isbn}' already exists.")
        next_id = str(max((int(b.id) for b in books if b.id.isdigit()), default=0) + 1)
        book = Book(next_id, title, author, isbn, copies, copies)
        books.append(book)
        self._save(books)
        return book

    def update(self, book_id: str, **changes: Any) -> Book:
        """Update title, author, ISBN, or total copies."""
        allowed = {"title", "author", "isbn", "total_copies"}
        unknown = set(changes) - allowed
        if unknown:
            raise ValidationError(
                f"Unsupported book fields: {', '.join(sorted(unknown))}"
            )
        books = self.list_books()
        target = next((book for book in books if book.id == book_id), None)
        if target is None:
            raise NotFoundError(f"Book '{book_id}' was not found.")
        for field in ("title", "author", "isbn"):
            if field in changes:
                changes[field] = required_text(
                    changes[field], field.replace("_", " ").title()
                )
        if "isbn" in changes and any(
            b.id != book_id and b.isbn.casefold() == changes["isbn"].casefold()
            for b in books
        ):
            raise ValidationError(f"ISBN '{changes['isbn']}' already exists.")
        if "total_copies" in changes:
            new_total = positive_int(changes["total_copies"], "Total copies")
            borrowed = target.total_copies - target.available_copies
            if new_total < borrowed:
                raise ValidationError(
                    "Total copies cannot be lower than copies currently borrowed."
                )
            target.available_copies = new_total - borrowed
        for field, value in changes.items():
            setattr(target, field, value)
        self._save(books)
        return target

    def delete(self, book_id: str) -> None:
        """Delete a book only when all copies are available."""
        books = self.list_books()
        target = next((book for book in books if book.id == book_id), None)
        if target is None:
            raise NotFoundError(f"Book '{book_id}' was not found.")
        if target.available_copies != target.total_copies:
            raise ValidationError("Cannot delete a book while copies are borrowed.")
        self._save([book for book in books if book.id != book_id])

    def search(self, query: str) -> list[Book]:
        """Search title, author, or ISBN without case sensitivity."""
        query = required_text(query, "Search query").casefold()
        return [
            book
            for book in self.list_books()
            if query in book.title.casefold()
            or query in book.author.casefold()
            or query in book.isbn.casefold()
        ]

    def change_available(self, book_id: str, delta: int) -> Book:
        """Adjust available copies after issue (+/-) or return (+)."""
        books = self.list_books()
        target = next((book for book in books if book.id == book_id), None)
        if target is None:
            raise NotFoundError(f"Book '{book_id}' was not found.")
        new_available = target.available_copies + delta
        if new_available < 0 or new_available > target.total_copies:
            raise ValidationError("Book availability would become invalid.")
        target.available_copies = new_available
        self._save(books)
        return target

    def _save(self, books: list[Book]) -> None:
        self.storage.write(self.FILE, [book.to_dict() for book in books])
