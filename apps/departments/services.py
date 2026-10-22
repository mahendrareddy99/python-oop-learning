

def get_departments_with_employees():
    """Fetch departments and their employees using two database queries."""
    from django.db.models import Prefetch

    from apps.departments.models import Department
    from apps.employees.models import Employee

    return Department.objects.prefetch_related(
        Prefetch(
            "employees",
            queryset=Employee.objects.order_by("employee_code"),
        )
    ).order_by("name")
