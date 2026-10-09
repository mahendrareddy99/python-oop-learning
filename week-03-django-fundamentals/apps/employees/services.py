
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Q

from .models import Employee


class EmployeeBusinessRuleError(Exception):
    """Raised when an employee business rule is violated."""


def create_employee(validated_data):
    """Create an employee after checking business rules."""
    if not validated_data.get("department"):
        raise EmployeeBusinessRuleError(
            "An employee must belong to a department."
        )

    try:
        with transaction.atomic():
            employee = Employee(**validated_data)
            employee.full_clean()
            employee.save()
            return employee
    except (IntegrityError, ValidationError) as exc:
        raise EmployeeBusinessRuleError(
            "Employee could not be created. Check the submitted data."
        ) from exc


def update_employee(employee, validated_data):
    """Update an existing employee."""
    if (
        "department" in validated_data
        and validated_data["department"] is None
    ):
        raise EmployeeBusinessRuleError(
            "An employee must belong to a department."
        )

    try:
        with transaction.atomic():
            for field, value in validated_data.items():
                setattr(employee, field, value)

            employee.full_clean()
            employee.save()
            return employee
    except (IntegrityError, ValidationError) as exc:
        raise EmployeeBusinessRuleError(
            "Employee could not be updated. Check the submitted data."
        ) from exc


def deactivate_employee(employee):
    """Mark an employee as inactive without deleting the record."""
    if not employee.status:
        raise EmployeeBusinessRuleError(
            "Employee is already inactive."
        )

    employee.status = False
    employee.save(update_fields=["status"])
    return employee


def search_employees(query="", active_only=True):
    """Search employees by code, name, or email."""
    employees = Employee.objects.select_related("department")

    if active_only:
        employees = employees.filter(status=True)

    query = query.strip()

    if query:
        employees = employees.filter(
            Q(employee_code__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
        )

    return employees.order_by("employee_code")


def delete_employee(employee):
    """Allow deletion only after an employee is inactive."""
    if employee.status:
        raise EmployeeBusinessRuleError(
            "Active employees cannot be deleted. Deactivate them first."
        )

    employee.delete()
