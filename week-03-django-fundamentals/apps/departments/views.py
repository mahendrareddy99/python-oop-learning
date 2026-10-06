from django.shortcuts import render


departments = [
    {
        "id": 1,
        "name": "Engineering",
        "description": "Software development and technology team.",
    },
    {
        "id": 2,
        "name": "Human Resources",
        "description": "Employee management and organizational support.",
    },
    {
        "id": 3,
        "name": "Finance",
        "description": "Financial planning, payroll and accounting.",
    },
    {
        "id": 4,
        "name": "Analytics",
        "description": "Data analysis and business intelligence.",
    },
]


def department_list(request):
    return render(
        request,
        "departments/list.html",
        {"departments": departments},
    )