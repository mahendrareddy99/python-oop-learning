# Library Management System

A small, modular Python OOP project using JSON files for persistence. It uses only the Python standard library.

## Features

- Books: add, update, delete, search, unique ISBN, copy availability.
- Members: register, update, delete, active-membership validation, unique email.
- Issues: issue and return books, due dates, overdue-day calculation, configurable per-day fine.
- Reports: available books, borrowed issues, top borrowers, fine totals, overdue issues.
- Design: classes, `Person` → `Member` inheritance, composition in `LibraryApp`, type hints, docstrings, custom exceptions, validation, and JSON persistence.

## Run

From the `Day02` directory (the directory containing `library_management`):

```powershell
python -m library_management.app
```

The first run creates `library_management/data/books.json`, `members.json`, and `issues.json` if they do not exist.

## Default rules

- Loan period: 14 days.
- Fine: ₹5 per overdue day.
- Dates use `YYYY-MM-DD`.
- JSON data files are runtime data. Keep the starter files empty when committing unless your trainer specifically asks for sample data.

## Example workflow

1. Add a book and note its book ID.
2. Register a member and note their member ID.
3. Issue the book using both IDs.
4. Return it using the issue transaction ID.
5. Open Reports to review availability and fines.

## Use as Python modules

```python
from library_management.storage import JSONStorage
from library_management.book import BookManager
from library_management.member import MemberManager
from library_management.issue import IssueManager
from library_management.reports import ReportManager

storage = JSONStorage()
books = BookManager(storage)
members = MemberManager(storage)
issues = IssueManager(storage, books, members)
reports = ReportManager(books, members, issues)
```
