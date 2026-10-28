"""Custom exceptions used by the library application."""


class LibraryError(Exception):
    """Base exception for expected library-operation errors."""


class ValidationError(LibraryError):
    """Raised when supplied data is invalid."""


class NotFoundError(LibraryError):
    """Raised when a requested book, member, or issue does not exist."""


class AvailabilityError(LibraryError):
    """Raised when a book cannot be issued or returned."""


class StorageError(LibraryError):
    """Raised when JSON data cannot be read or written."""
