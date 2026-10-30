"""Reports for book availability, borrowing activity, and fines."""

from collections import Counter
from datetime import date

from .book import Book, BookManager
from .issue import Issue, IssueManager
from .member import MemberManager


class ReportManager:
    """Generate catalogue, borrower, and fine reports."""

    def __init__(
        self,
        books: BookManager,
        members: MemberManager,
        issues: IssueManager,
    ) -> None:
        """Initialize report dependencies."""

        self.books = books
        self.members = members
        self.issues = issues

    def available_books(self) -> list[Book]:
        """Return books with at least one available copy."""

        return [book for book in self.books.list_books() if book.available_copies > 0]

    def borrowed_books(self) -> list[Issue]:
        """Return currently borrowed book transactions."""

        return [
            issue for issue in self.issues.list_issues() if issue.return_date is None
        ]

    def top_borrowers(
        self,
        limit: int = 5,
    ) -> list[tuple[str, int]]:
        """Return member IDs and borrowing counts in descending order."""

        if isinstance(limit, bool) or not isinstance(limit, int):
            raise TypeError("Limit must be an integer.")

        if limit < 1:
            raise ValueError("Limit must be greater than zero.")

        counts = Counter(issue.member_id for issue in self.issues.list_issues())

        return counts.most_common(limit)

    def fine_report(self) -> tuple[list[Issue], float]:
        """Return transactions with fines and the total fine amount."""

        fined_issues = [issue for issue in self.issues.list_issues() if issue.fine > 0]

        total_fine = round(
            sum(issue.fine for issue in fined_issues),
            2,
        )

        return fined_issues, total_fine

    def overdue_report(
        self,
        on_date: str | None = None,
    ) -> list[Issue]:
        """Return unreturned issues whose due dates have passed."""

        selected_date = date.fromisoformat(on_date or date.today().isoformat())

        return [
            issue
            for issue in self.issues.list_issues()
            if issue.return_date is None
            and date.fromisoformat(issue.due_date) < selected_date
        ]
