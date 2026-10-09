
from django.shortcuts import get_object_or_404, render

from .models import Employee


def employee_home(request):
    employees = Employee.objects.select_related("department").all()
    return render(
        request,
        "employees/list.html",
        {"employees": employees},
    )


def employee_list(request):
    employees = Employee.objects.select_related("department").all()
    return render(
        request,
        "employees/list.html",
        {"employees": employees},
    )


def employee_detail(request, id):
    employee = get_object_or_404(
        Employee.objects.select_related("department"),
        id=id,
    )
    return render(
        request,
        "employees/detail.html",
        {"employee": employee},
    )
