# Backend Integration Capstone — Database Migrations

## Purpose

Django migrations provide version-controlled changes to the database schema and help keep the database structure aligned with Django models.

## Migration Workflow

1. Update Django models when a schema change is required.
2. Run `python manage.py makemigrations` to generate migration files.
3. Review the generated migration files.
4. Run `python manage.py migrate` to apply migrations.
5. Run `python manage.py makemigrations --check --dry-run` to check for model changes that lack migrations.
6. Run `python manage.py test` to verify application behavior.

## Current Schema Areas

- **Common:** Organizations and organization memberships.
- **Departments:** Department records associated with organizations.
- **Employees:** Employee records associated with departments.

## Migration Verification

The baseline verification on 23 October 2026 reported:

- Existing migrations were applied.
- `makemigrations --check --dry-run` reported no changes.

Repeat these checks after model changes.

## Safety Notes

- Do not edit an already-applied migration casually.
- Review data migrations before applying them to important data.
- Back up important databases before risky schema changes.
- Never commit database passwords or other secrets.
