
from django.db.models import Prefetch

from apps.employees.models import Employee
from .models import Department


def get_departments_with_employees():
    """Fetch departments and their employees efficiently."""
    return Department.objects.prefetch_related(
        Prefetch(
            "employees",
            queryset=Employee.objects.order_by("employee_code"),
        )
    ).order_by("name")
