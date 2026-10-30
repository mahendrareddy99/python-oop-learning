"""Member model and membership operations."""

from dataclasses import asdict, dataclass
from typing import Any

from .exceptions import NotFoundError, ValidationError
from .storage import JSONStorage
from .validator import required_text


@dataclass
class Person:
    """Represent a person using common personal information."""

    name: str
    email: str


@dataclass
class Member(Person):
    """Represent a registered library member."""

    id: str
    phone: str
    active: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Member":
        """Create a Member object from a JSON dictionary."""

        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        """Convert the Member object into a JSON-compatible dictionary."""

        return asdict(self)


class MemberManager:
    """Register, update, delete, and validate library members."""

    FILE = "members.json"

    def __init__(self, storage: JSONStorage) -> None:
        """Initialize member management with JSON storage."""

        self.storage = storage

    def list_members(self) -> list[Member]:
        """Return all registered members."""

        records = self.storage.read(self.FILE)

        return [Member.from_dict(record) for record in records]

    def get(self, member_id: str) -> Member:
        """Find and return a member using their ID."""

        for member in self.list_members():
            if member.id == member_id:
                return member

        raise NotFoundError(f"Member '{member_id}' was not found.")

    def register(
        self,
        name: str,
        email: str,
        phone: str,
    ) -> Member:
        """Register a member while enforcing unique email addresses."""

        name = required_text(name, "Name")
        email = required_text(email, "Email")
        phone = required_text(phone, "Phone")

        members = self.list_members()

        if any(member.email.casefold() == email.casefold() for member in members):
            raise ValidationError(f"Email '{email}' is already registered.")

        next_id = str(
            max(
                (int(member.id) for member in members if member.id.isdigit()),
                default=0,
            )
            + 1
        )

        member = Member(
            name=name,
            email=email,
            id=next_id,
            phone=phone,
        )

        members.append(member)
        self._save(members)

        return member

    def update(
        self,
        member_id: str,
        **changes: Any,
    ) -> Member:
        """Update member name, email, phone, or active status."""

        allowed_fields = {
            "name",
            "email",
            "phone",
            "active",
        }

        unknown_fields = set(changes) - allowed_fields

        if unknown_fields:
            raise ValidationError(
                f"Unsupported member fields: {', '.join(sorted(unknown_fields))}"
            )

        members = self.list_members()

        target = next(
            (member for member in members if member.id == member_id),
            None,
        )

        if target is None:
            raise NotFoundError(f"Member '{member_id}' was not found.")

        for field in ("name", "email", "phone"):
            if field in changes:
                changes[field] = required_text(
                    changes[field],
                    field.title(),
                )

        if "email" in changes:
            new_email = changes["email"]

            if any(
                member.id != member_id
                and member.email.casefold() == new_email.casefold()
                for member in members
            ):
                raise ValidationError(f"Email '{new_email}' is already registered.")

        if "active" in changes and not isinstance(changes["active"], bool):
            raise ValidationError("Active must be True or False.")

        for field, value in changes.items():
            setattr(target, field, value)

        self._save(members)

        return target

    def delete(self, member_id: str) -> None:
        """Delete a member only when they have no outstanding issues."""

        self.get(member_id)

        issues = self.storage.read("issues.json")

        has_outstanding_books = any(
            issue.get("member_id") == member_id and issue.get("return_date") is None
            for issue in issues
        )

        if has_outstanding_books:
            raise ValidationError(
                "Cannot delete a member while they have currently borrowed books."
            )

        members = self.list_members()

        remaining_members = [member for member in members if member.id != member_id]

        self._save(remaining_members)

    def validate_active(self, member_id: str) -> Member:
        """Return an active member or raise a validation error."""

        member = self.get(member_id)

        if not member.active:
            raise ValidationError(f"Member '{member_id}' is inactive.")

        return member

    def _save(self, members: list[Member]) -> None:
        """Persist member records to JSON storage."""

        records = [member.to_dict() for member in members]

        self.storage.write(self.FILE, records)
