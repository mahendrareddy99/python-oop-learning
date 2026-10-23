# Backend Integration Capstone — Runbook

## Prerequisites

- Python installed
- PostgreSQL installed and running
- Project virtual environment available
- Database and database user configured
- Required environment variables configured

## 1. Activate the Virtual Environment

From the repository root, run:

```powershell
.\venv\Scripts\Activate.ps1
```

## 2. Configure Environment Variables

Set the Django secret key in the current PowerShell session:

```powershell
$env:DJANGO_SECRET_KEY = "your-development-secret-key"
```

Set the PostgreSQL password:

```powershell
$env:DB_PASSWORD = Read-Host "Enter PostgreSQL password"
```

Use your own local development values. Do not commit secrets to Git.

## 3. Verify Configuration

```powershell
python manage.py check
python manage.py showmigrations
python manage.py makemigrations --check --dry-run
```

## 4. Apply Migrations

```powershell
python manage.py migrate
```

## 5. Run Automated Tests

```powershell
python manage.py test
```

## 6. Start the Development Server

```powershell
python manage.py runserver
```

The local development server is available at `http://127.0.0.1:8000/`.

## 7. Troubleshooting

- **Database connection failure:** Confirm PostgreSQL is running, verify the database name, user, port, and `DB_PASSWORD`.
- **Missing secret key:** Set `DJANGO_SECRET_KEY` in the current terminal session.
- **Migration differences:** Review model changes and migration files before applying changes.
- **Test failure:** Read the traceback and failing test name, then rerun the relevant test after fixing the issue.

## Known Limitations

This runbook covers local development and testing. Production deployment requires separate environment configuration, secure secret management, deployment settings, monitoring, and backup procedures.