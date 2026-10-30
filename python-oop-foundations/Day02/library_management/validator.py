"""Input validation helpers."""

from datetime import date

from .exceptions import ValidationError


def required_text(value: str, field_name: str) -> str:
    """Return trimmed non-empty text or raise ValidationError."""
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} is required.")
    return value.strip()


def positive_int(value: int, field_name: str, *, allow_zero: bool = False) -> int:
    """Validate an integer as positive, or non-negative when allow_zero is true."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{field_name} must be an integer.")
    minimum = 0 if allow_zero else 1
    if value < minimum:
        adjective = "non-negative" if allow_zero else "positive"
        raise ValidationError(f"{field_name} must be {adjective}.")
    return value


def valid_iso_date(value: str, field_name: str = "date") -> str:
    """Validate a date formatted as YYYY-MM-DD and return it unchanged."""
    try:
        date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} must use YYYY-MM-DD format.") from None
    return value
