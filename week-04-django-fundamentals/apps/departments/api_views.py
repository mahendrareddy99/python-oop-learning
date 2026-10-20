
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import (
    get_user_organization,
    require_write_role,
)

from .models import Department
from .serializers import DepartmentSerializer


class DepartmentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "success": True,
                "message": "Departments retrieved successfully.",
                "data": data,
                "pagination": {
                    "count": self.page.paginator.count,
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
            }
        )


def validation_error_response(errors):
    return Response(
        {
            "success": False,
            "message": "Validation failed.",
            "details": errors,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


class DepartmentListCreateAPIView(APIView):

    def get(self, request):
        organization = get_user_organization(request.user)

        # Only return departments belonging to the user's organization.
        departments = Department.objects.filter(
            organization=organization
        ).order_by("name")

        # Search departments by name.
        search = request.query_params.get("search", "").strip()

        if search:
            departments = departments.filter(
                name__icontains=search
            )

        # Filter by active/inactive status.
        status_param = request.query_params.get(
            "status", ""
        ).lower()

        if status_param:
            if status_param not in ("true", "false"):
                return Response(
                    {
                        "success": False,
                        "message": (
                            "Status must be either 'true' or 'false'."
                        ),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            departments = departments.filter(
                status=(status_param == "true")
            )

        # Apply pagination.
        paginator = DepartmentPagination()
        page = paginator.paginate_queryset(
            departments,
            request,
            view=self,
        )

        serializer = DepartmentSerializer(
            page,
            many=True,
            context={"request": request},
        )

        return paginator.get_paginated_response(
            serializer.data
        )

    def post(self, request):
        # Only administrators and HR staff may create departments.
        require_write_role(request.user)

        serializer = DepartmentSerializer(
            data=request.data,
            context={"request": request},
        )

        if not serializer.is_valid():
            return validation_error_response(
                serializer.errors
            )

        # Never trust an organization ID supplied by the client.
        organization = get_user_organization(request.user)

        department = serializer.save(
            organization=organization
        )

        return Response(
            {
                "success": True,
                "message": "Department created successfully.",
                "data": DepartmentSerializer(
                    department,
                    context={"request": request},
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


class DepartmentDetailAPIView(APIView):

    def get_object(self, request, department_id):
        organization = get_user_organization(request.user)

        # A department in another organization returns 404.
        return get_object_or_404(
            Department,
            id=department_id,
            organization=organization,
        )

    def get(self, request, department_id):
        department = self.get_object(
            request, department_id
        )

        return Response(
            {
                "success": True,
                "message": "Department retrieved successfully.",
                "data": DepartmentSerializer(
                    department,
                    context={"request": request},
                ).data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, department_id):
        require_write_role(request.user)

        department = self.get_object(
            request, department_id
        )

        serializer = DepartmentSerializer(
            department,
            data=request.data,
            context={"request": request},
        )

        if not serializer.is_valid():
            return validation_error_response(
                serializer.errors
            )

        # Preserve the department's existing organization.
        department = serializer.save(
            organization=department.organization
        )

        return Response(
            {
                "success": True,
                "message": "Department updated successfully.",
                "data": DepartmentSerializer(
                    department,
                    context={"request": request},
                ).data,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, department_id):
        require_write_role(request.user)

        department = self.get_object(
            request, department_id
        )

        serializer = DepartmentSerializer(
            department,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        if not serializer.is_valid():
            return validation_error_response(
                serializer.errors
            )

        # Prevent reassignment to another organization.
        department = serializer.save(
            organization=department.organization
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Department partially updated successfully."
                ),
                "data": DepartmentSerializer(
                    department,
                    context={"request": request},
                ).data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, department_id):
        require_write_role(request.user)

        department = self.get_object(
            request, department_id
        )

        try:
            department.delete()
        except ProtectedError:
            return Response(
                {
                    "success": False,
                    "message": (
                        "This department cannot be deleted "
                        "because employees are assigned to it."
                    ),
                },
                status=status.HTTP_409_CONFLICT,
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
