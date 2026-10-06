from django.http import Http404
from django.shortcuts import render


employees = [
    {
        "id": 1,
        "name": "Mahendra Reddy",
        "email": "mahendra@example.com",
        "role": "Python Developer",
        "department": "Engineering",
    },
    {
        "id": 2,
        "name": "Sai Sarath Reddy",
        "email": "sarath@example.com",
        "role": "Software Engineer",
        "department": "Engineering",
    },
    {
        "id": 3,
        "name": "Rahul Kumar",
        "email": "rahul@example.com",
        "role": "Data Analyst",
        "department": "Analytics",
    },
]


def employee_home(request):
    return render(
        request,
        "employees/list.html",
        {"employees": employees},
    )


def employee_list(request):
    return render(
        request,
        "employees/list.html",
        {"employees": employees},
    )


def employee_detail(request, id):
    employee = next(
        (employee for employee in employees if employee["id"] == id),
        None,
    )

    if employee is None:
        raise Http404("Employee not found")

    return render(
        request,
        "employees/detail.html",
        {"employee": employee},
    )