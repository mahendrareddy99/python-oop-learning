from django.urls import path

from .api_views import (
    EmployeeListCreateAPIView,
    EmployeeDetailAPIView,
)


urlpatterns = [
    path(
        "employees/",
        EmployeeListCreateAPIView.as_view(),
        name="employee-list-create",
    ),

    path(
        "employees/<int:employee_id>/",
        EmployeeDetailAPIView.as_view(),
        name="employee-detail",
    ),
]