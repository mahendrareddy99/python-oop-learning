
from django.urls import path

from .api_views import (
    DepartmentListCreateAPIView,
    DepartmentDetailAPIView,
)

urlpatterns = [
    path(
        "departments/",
        DepartmentListCreateAPIView.as_view(),
        name="department-api-list-create",
    ),
    path(
        "departments/<int:department_id>/",
        DepartmentDetailAPIView.as_view(),
        name="department-api-detail",
    ),
]
