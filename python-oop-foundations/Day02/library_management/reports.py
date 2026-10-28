"""Reports for book availability, borrowing activity, and fines."""
from collections import Counter
from datetime import date
from .book import BookManager
from .issue import IssueManager
from .member import MemberManager


class ReportManager:
    """Generate catalogue, borrower, and fine reports."""

    def __init__(self, books: BookManager, members: MemberManager, issues: IssueManager) -> None:
        self.books = books
        self.members = members
        self.issues = issues

    def available_books(self):
        """List books with at least one available copy."""
        return [book for book in self.books.list_books() if book.available_copies > 0]

    def borrowed_books(self):
        """List currently borrowed copies as issue records."""
        return [issue for issue in self.issues.list_issues() if issue.return_date is None]

    def top_borrowers(self, limit: int = 5):
        """Return member IDs and number of issue transactions, highest first."""
        counts = Counter(issue.member_id for issue in self.issues.list_issues())
        return counts.most_common(max(1, limit))

    def fine_report(self):
        """Return issue records with fines and the total fine amount."""
        fined = [issue for issue in self.issues.list_issues() if issue.fine > 0]
        return fined, round(sum(issue.fine for issue in fined), 2)

    def overdue_report(self, on_date: str | None = None):
        """Return unreturned books that are overdue on the selected date."""
        selected = date.fromisoformat(on_date or date.today().isoformat())
        return [
            issue for issue in self.issues.list_issues()
            if issue.return_date is None and date.fromisoformat(issue.due_date) < selected
        ]
