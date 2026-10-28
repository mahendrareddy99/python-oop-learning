"""Book issue/return workflows and late-fine calculations."""
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from typing import Any
from .book import BookManager
from .exceptions import AvailabilityError, NotFoundError, ValidationError
from .member import MemberManager
from .storage import JSONStorage
from .validator import positive_int, valid_iso_date


@dataclass
class Issue:
    """Represent one issue transaction."""

    id: str
    book_id: str
    member_id: str
    issue_date: str
    due_date: str
    return_date: str | None = None
    fine: float = 0.0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Issue":
        """Build an Issue from a JSON record."""
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        """Convert the issue to a JSON-compatible dictionary."""
        return asdict(self)


class IssueManager:
    """Issue and return books, including due dates and overdue fines."""

    FILE = "issues.json"

    def __init__(
        self, storage: JSONStorage, books: BookManager, members: MemberManager,
        loan_days: int = 14, fine_per_day: float = 5.0
    ) -> None:
        self.storage = storage
        self.books = books
        self.members = members
        self.loan_days = positive_int(loan_days, "Loan days")
        if fine_per_day < 0:
            raise ValidationError("Fine per day cannot be negative.")
        self.fine_per_day = float(fine_per_day)

    def list_issues(self) -> list[Issue]:
        """Return all issue records."""
        return [Issue.from_dict(row) for row in self.storage.read(self.FILE)]

    def issue_book(self, book_id: str, member_id: str, issue_date: str | None = None) -> Issue:
        """Issue one available copy to an active member."""
        self.members.validate_active(member_id)
        book = self.books.get(book_id)
        if book.available_copies < 1:
            raise AvailabilityError(f"No available copies of '{book.title}'.")
        issued = valid_iso_date(issue_date or date.today().isoformat(), "Issue date")
        due = (date.fromisoformat(issued) + timedelta(days=self.loan_days)).isoformat()
        issues = self.list_issues()
        next_id = str(max((int(i.id) for i in issues if i.id.isdigit()), default=0) + 1)
        issue = Issue(next_id, book_id, member_id, issued, due)
        self.books.change_available(book_id, -1)
        try:
            issues.append(issue)
            self._save(issues)
        except Exception:
            self.books.change_available(book_id, 1)
            raise
        return issue

    def return_book(self, issue_id: str, return_date: str | None = None) -> Issue:
        """Return an issued book and calculate the overdue fine."""
        issues = self.list_issues()
        target = next((issue for issue in issues if issue.id == issue_id), None)
        if target is None:
            raise NotFoundError(f"Issue '{issue_id}' was not found.")
        if target.return_date is not None:
            raise AvailabilityError("This issue has already been returned.")
        returned = valid_iso_date(return_date or date.today().isoformat(), "Return date")
        if date.fromisoformat(returned) < date.fromisoformat(target.issue_date):
            raise ValidationError("Return date cannot be before issue date.")
        late_days = max(0, (date.fromisoformat(returned) - date.fromisoformat(target.due_date)).days)
        target.return_date = returned
        target.fine = round(late_days * self.fine_per_day, 2)
        self._save(issues)
        self.books.change_available(target.book_id, 1)
        return target

    def overdue_issues(self, on_date: str | None = None) -> list[Issue]:
        """List unreturned issues whose due date is before the supplied date."""
        today = date.fromisoformat(valid_iso_date(on_date or date.today().isoformat()))
        return [
            issue for issue in self.list_issues()
            if issue.return_date is None and date.fromisoformat(issue.due_date) < today
        ]

    def _save(self, issues: list[Issue]) -> None:
        self.storage.write(self.FILE, [issue.to_dict() for issue in issues])
