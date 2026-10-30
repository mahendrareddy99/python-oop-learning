"""Command-line interface for the Library Management System."""

from collections.abc import Callable

from .book import BookManager
from .exceptions import LibraryError
from .issue import IssueManager
from .member import MemberManager
from .reports import ReportManager
from .storage import JSONStorage


class LibraryApp:
    """Compose managers and provide a simple interactive CLI."""

    def __init__(self) -> None:
        """Initialize storage, managers, and application services."""
        self.storage = JSONStorage()
        self.books = BookManager(self.storage)
        self.members = MemberManager(self.storage)
        self.issues = IssueManager(
            self.storage,
            self.books,
            self.members,
        )
        self.reports = ReportManager(
            self.books,
            self.members,
            self.issues,
        )

    def run(self) -> None:
        """Run the main menu until the user chooses to exit."""

        actions: dict[str, Callable[[], None]] = {
            "1": self.add_book,
            "2": self.list_books,
            "3": self.search_books,
            "4": self.register_member,
            "5": self.list_members,
            "6": self.issue_book,
            "7": self.return_book,
            "8": self.show_reports,
        }

        while True:
            print("\n=== Library Management System ===")
            print("1. Add book  2. List books  3. Search books")
            print("4. Register member  5. List members")
            print("6. Issue book  7. Return book  8. Reports  0. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "0":
                print("Goodbye!")
                break

            action = actions.get(choice)

            if action is None:
                print("Please choose a valid menu option.")
                continue

            try:
                action()
            except (LibraryError, ValueError) as exc:
                print(f"Error: {exc}")

    def add_book(self) -> None:
        """Prompt for book details and add the book."""

        book = self.books.add(
            input("Title: "),
            input("Author: "),
            input("ISBN: "),
            int(input("Number of copies: ")),
        )

        print(f"Added book ID {book.id}: {book.title}")

    def list_books(self) -> None:
        """Print all books and their availability."""

        books = self.books.list_books()

        if not books:
            print("No books found.")
            return

        for book in books:
            print(
                f"ID {book.id} | {book.title} | {book.author} | "
                f"available {book.available_copies}/{book.total_copies}"
            )

    def search_books(self) -> None:
        """Search books by title, author, or ISBN."""

        results = self.books.search(input("Search text: "))

        if not results:
            print("No matching books found.")
            return

        for book in results:
            print(f"ID {book.id} | {book.title} | {book.author} | ISBN {book.isbn}")

    def register_member(self) -> None:
        """Prompt for member details and register a new member."""

        member = self.members.register(
            input("Name: "),
            input("Email: "),
            input("Phone: "),
        )

        print(f"Registered member ID {member.id}: {member.name}")

    def list_members(self) -> None:
        """Print all registered members."""

        members = self.members.list_members()

        if not members:
            print("No members found.")
            return

        for member in members:
            print(
                f"ID {member.id} | {member.name} | "
                f"{member.email} | active={member.active}"
            )

    def issue_book(self) -> None:
        """Issue a book to a registered member."""

        book_id = input("Book ID: ").strip()
        member_id = input("Member ID: ").strip()

        issue = self.issues.issue_book(book_id, member_id)

        print(f"Issued transaction {issue.id}; due date: {issue.due_date}")

    def return_book(self) -> None:
        """Return a book and display its fine."""

        issue_id = input("Issue transaction ID: ").strip()

        issue = self.issues.return_book(issue_id)

        print(f"Returned. Fine: INR {issue.fine:.2f}")

    def show_reports(self) -> None:
        """Display availability, borrowing, borrower, and fine reports."""

        print("\nAvailable books:")

        available_books = self.reports.available_books()

        if not available_books:
            print("  No available books.")

        for book in available_books:
            print(f"  {book.id}: {book.title} ({book.available_copies} available)")

        print("\nCurrently borrowed issue transactions:")

        borrowed_books = self.reports.borrowed_books()

        if not borrowed_books:
            print("  No books are currently borrowed.")

        for issue in borrowed_books:
            print(
                f"  Issue {issue.id}: book {issue.book_id}, "
                f"member {issue.member_id}, due {issue.due_date}"
            )

        print("\nTop borrowers (member ID, number of issues):")

        top_borrowers = self.reports.top_borrowers()

        if not top_borrowers:
            print("  No borrowing records found.")

        for member_id, count in top_borrowers:
            print(f"  Member {member_id}: {count} issues")

        fined_issues, total_fine = self.reports.fine_report()

        print(
            f"\nFine report: {len(fined_issues)} transactions, "
            f"total INR {total_fine:.2f}"
        )

        overdue_issues = self.reports.overdue_report()

        print(f"Overdue issues: {len(overdue_issues)}")


if __name__ == "__main__":
    LibraryApp().run()
