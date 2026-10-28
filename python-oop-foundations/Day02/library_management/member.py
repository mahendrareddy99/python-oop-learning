"""Member model and membership operations."""
from dataclasses import asdict, dataclass
from typing import Any
from .exceptions import NotFoundError, ValidationError
from .storage import JSONStorage
from .validator import required_text


@dataclass
class Person:
    """Base class demonstrating inheritance for people in the system."""

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
        """Build a Member from a JSON record."""
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        """Convert the member to a JSON-compatible dictionary."""
        return asdict(self)


class MemberManager:
    """Register, update, delete, and validate members."""

    FILE = "members.json"

    def __init__(self, storage: JSONStorage) -> None:
        self.storage = storage

    def list_members(self) -> list[Member]:
        """Return all registered members."""
        return [Member.from_dict(row) for row in self.storage.read(self.FILE)]

    def get(self, member_id: str) -> Member:
        """Find a member by ID."""
        for member in self.list_members():
            if member.id == member_id:
                return member
        raise NotFoundError(f"Member '{member_id}' was not found.")

    def register(self, name: str, email: str, phone: str) -> Member:
        """Register a member; email must be unique."""
        name = required_text(name, "Name")
        email = required_text(email, "Email")
        phone = required_text(phone, "Phone")
        members = self.list_members()
        if any(m.email.casefold() == email.casefold() for m in members):
            raise ValidationError(f"Email '{email}' is already registered.")
        next_id = str(max((int(m.id) for m in members if m.id.isdigit()), default=0) + 1)
        member = Member(name=name, email=email, id=next_id, phone=phone)
        members.append(member)
        self._save(members)
        return member

    def update(self, member_id: str, **changes: Any) -> Member:
        """Update member name, email, phone, or active status."""
        allowed = {"name", "email", "phone", "active"}
        unknown = set(changes) - allowed
        if unknown:
            raise ValidationError(f"Unsupported member fields: {', '.join(sorted(unknown))}")
        members = self.list_members()
        target = next((m for m in members if m.id == member_id), None)
        if target is None:
            raise NotFoundError(f"Member '{member_id}' was not found.")
        for field in ("name", "email", "phone"):
            if field in changes:
                changes[field] = required_text(changes[field], field.title())
        if "email" in changes and any(
            m.id != member_id and m.email.casefold() == changes["email"].casefold()
            for m in members
        ):
            raise ValidationError(f"Email '{changes['email']}' is already registered.")
        if "active" in changes and not isinstance(changes["active"], bool):
            raise ValidationError("Active must be True or False.")
        for field, value in changes.items():
            setattr(target, field, value)
        self._save(members)
        return target

    def delete(self, member_id: str) -> None:
        """Delete a member only if they have no currently borrowed books."""
        member = self.get(member_id)
        members = self.list_members()
        self._save([m for m in members if m.id != member_id])

    def validate_active(self, member_id: str) -> Member:
        """Return the member if registered and active; otherwise raise an error."""
        member = self.get(member_id)
        if not member.active:
            raise ValidationError(f"Member '{member_id}' is inactive.")
        return member

    def _save(self, members: list[Member]) -> None:
        self.storage.write(self.FILE, [member.to_dict() for member in members])
