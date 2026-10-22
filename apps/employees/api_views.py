
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import (
    get_user_organization,
    require_write_role,
)

from .models import Employee
from .pagination import EmployeePagination
from .serializers import EmployeeSerializer
from .services import (
    EmployeeBusinessRuleError,
    create_employee,
    update_employee,
    deactivate_employee,
    search_employees,
    delete_employee,
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


def business_rule_response(exc):
    return Response(
        {
            "success": False,
            "message": "The requested operation is not allowed.",
            "details": {
                "error": str(exc),
            },
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


def error_response(
    message,
    http_status=status.HTTP_400_BAD_REQUEST,
):
    return Response(
        {
            "success": False,
            "message": message,
        },
        status=http_status,
    )


class EmployeeListCreateAPIView(APIView):

    def get(self, request):
        organization = get_user_organization(request.user)

        query = request.query_params.get(
            "search", ""
        ).strip()

        include_inactive = (
            request.query_params.get(
                "include_inactive", ""
            ).lower()
            == "true"
        )

        status_param = request.query_params.get(
            "status", ""
        ).lower()

        department_param = request.query_params.get(
            "department"
        )

        if status_param and status_param not in (
            "true",
            "false",
        ):
            return error_response(
                "Status must be either 'true' or 'false'."
            )

        # Keep the existing search service and restrict its results
        # to employees in the authenticated user's organization.
        employees = search_employees(
            query=query,
            active_only=(
                not include_inactive and not status_param
            ),
        ).filter(
            department__organization=organization
        )

        if status_param:
            employees = employees.filter(
                status=(status_param == "true")
            )

        if department_param:
            try:
                department_id = int(department_param)

                if department_id <= 0:
                    raise ValueError

            except (TypeError, ValueError):
                return error_response(
                    "Department must be a positive integer ID."
                )

            employees = employees.filter(
                department_id=department_id
            )

        paginator = EmployeePagination()
        page = paginator.paginate_queryset(
            employees,
            request,
            view=self,
        )

        serializer = EmployeeSerializer(
            page,
            many=True,
            context={"request": request},
        )

        return paginator.get_paginated_response(
            serializer.data
        )

    def post(self, request):
        require_write_role(request.user)

        organization = get_user_organization(request.user)

        serializer = EmployeeSerializer(
            data=request.data,
            context={"request": request},
        )

        if not serializer.is_valid():
            return validation_error_response(
                serializer.errors
            )

        department = serializer.validated_data.get(
            "department"
        )

        # Defense in depth: never create an employee in a
        # department belonging to a different organization.
        if (
            department is None
            or department.organization_id != organization.id
        ):
            return error_response(
                "The selected department does not belong "
                "to your organization.",
                status.HTTP_400_BAD_REQUEST,
            )

        try:
            employee = create_employee(
                serializer.validated_data
            )

        except EmployeeBusinessRuleError as exc:
            return business_rule_response(exc)

        return Response(
            {
                "success": True,
                "message": "Employee created successfully.",
                "data": EmployeeSerializer(
                    employee,
                    context={"request": request},
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


class EmployeeDetailAPIView(APIView):

    def get_object(self, request, employee_id):
        organization = get_user_organization(request.user)

        # Return 404 for an employee outside the user's organization.
        return get_object_or_404(
            Employee.objects.select_related("department"),
            id=employee_id,
            department__organization=organization,
        )

    def get(self, request, employee_id):
        employee = self.get_object(
            request, employee_id
        )

        return Response(
            {
                "success": True,
                "message": "Employee retrieved successfully.",
                "data": EmployeeSerializer(
                    employee,
                    context={"request": request},
                ).data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, employee_id):
        require_write_role(request.user)

        employee = self.get_object(
            request, employee_id
        )

        serializer = EmployeeSerializer(
            employee,
            data=request.data,
            context={"request": request},
        )

        if not serializer.is_valid():
            return validation_error_response(
                serializer.errors
            )

        organization = get_user_organization(request.user)
        department = serializer.validated_data.get(
            "department", employee.department
        )

        if (
            department is None
            or department.organization_id != organization.id
        ):
            return error_response(
                "The selected department does not belong "
                "to your organization.",
                status.HTTP_400_BAD_REQUEST,
            )

        try:
            employee = update_employee(
                employee,
                serializer.validated_data,
            )

        except EmployeeBusinessRuleError as exc:
            return business_rule_response(exc)

        return Response(
            {
                "success": True,
                "message": "Employee updated successfully.",
                "data": EmployeeSerializer(
                    employee,
                    context={"request": request},
                ).data,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, employee_id):
        require_write_role(request.user)

        employee = self.get_object(
            request, employee_id
        )

        serializer = EmployeeSerializer(
            employee,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        if not serializer.is_valid():
            return validation_error_response(
                serializer.errors
            )

        organization = get_user_organization(request.user)
        department = serializer.validated_data.get(
            "department", employee.department
        )

        if (
            department is None
            or department.organization_id != organization.id
        ):
            return error_response(
                "The selected department does not belong "
                "to your organization.",
                status.HTTP_400_BAD_REQUEST,
            )

        try:
            employee = update_employee(
                employee,
                serializer.validated_data,
            )

        except EmployeeBusinessRuleError as exc:
            return business_rule_response(exc)

        return Response(
            {
                "success": True,
                "message": (
                    "Employee partially updated successfully."
                ),
                "data": EmployeeSerializer(
                    employee,
                    context={"request": request},
                ).data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, employee_id):
        require_write_role(request.user)

        employee = self.get_object(
            request, employee_id
        )

        if request.data.get("action") != "deactivate":
            return error_response(
                "Use action='deactivate' to deactivate an employee."
            )

        try:
            employee = deactivate_employee(employee)

        except EmployeeBusinessRuleError as exc:
            return business_rule_response(exc)

        return Response(
            {
                "success": True,
                "message": "Employee deactivated successfully.",
                "data": EmployeeSerializer(
                    employee,
                    context={"request": request},
                ).data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, employee_id):
        require_write_role(request.user)

        employee = self.get_object(
            request, employee_id
        )

        try:
            delete_employee(employee)

        except EmployeeBusinessRuleError as exc:
            return business_rule_response(exc)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
