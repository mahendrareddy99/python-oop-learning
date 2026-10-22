
from django.shortcuts import render

from .models import Department


def department_list(request):
    departments = Department.objects.all()
    return render(
        request,
        "departments/list.html",
        {"departments": departments},
    )
