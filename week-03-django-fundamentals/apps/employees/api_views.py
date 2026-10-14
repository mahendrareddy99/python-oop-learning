
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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


def error_response(message, http_status=status.HTTP_400_BAD_REQUEST):
    return Response(
        {
            "success": False,
            "message": message,
        },
        status=http_status,
    )


class EmployeeListCreateAPIView(APIView):
    def get(self, request):
        query = request.query_params.get("search", "").strip()

        include_inactive = (
            request.query_params.get("include_inactive", "").lower()
            == "true"
        )

        status_param = request.query_params.get("status", "").lower()
        department_param = request.query_params.get("department")

        # Validate the status filter.
        if status_param and status_param not in ("true", "false"):
            return error_response(
                "Status must be either 'true' or 'false'."
            )

        # Retrieve employees using the existing search service.
        employees = search_employees(
            query=query,
            active_only=not include_inactive and not status_param,
        )

        # Apply an explicit status filter.
        if status_param:
            employees = employees.filter(
                status=(status_param == "true")
            )

        # Filter by department ID.
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

        # Apply pagination.
        paginator = EmployeePagination()
        page = paginator.paginate_queryset(
            employees,
            request,
            view=self,
        )

        serializer = EmployeeSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)

        if not serializer.is_valid():
            return validation_error_response(serializer.errors)

        try:
            employee = create_employee(serializer.validated_data)

        except EmployeeBusinessRuleError as exc:
            return business_rule_response(exc)

        return Response(
            {
                "success": True,
                "message": "Employee created successfully.",
                "data": EmployeeSerializer(employee).data,
            },
            status=status.HTTP_201_CREATED,
        )


class EmployeeDetailAPIView(APIView):
    def get_object(self, employee_id):
        return get_object_or_404(
            Employee.objects.select_related("department"),
            id=employee_id,
        )

    def get(self, request, employee_id):
        employee = self.get_object(employee_id)

        return Response(
            {
                "success": True,
                "message": "Employee retrieved successfully.",
                "data": EmployeeSerializer(employee).data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, employee_id):
        employee = self.get_object(employee_id)

        serializer = EmployeeSerializer(
            employee,
            data=request.data,
        )

        if not serializer.is_valid():
            return validation_error_response(serializer.errors)

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
                "data": EmployeeSerializer(employee).data,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, employee_id):
        employee = self.get_object(employee_id)

        serializer = EmployeeSerializer(
            employee,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return validation_error_response(serializer.errors)

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
                "message": "Employee partially updated successfully.",
                "data": EmployeeSerializer(employee).data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, employee_id):
        employee = self.get_object(employee_id)

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
                "data": EmployeeSerializer(employee).data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, employee_id):
        employee = self.get_object(employee_id)

        try:
            delete_employee(employee)

        except EmployeeBusinessRuleError as exc:
            return business_rule_response(exc)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
