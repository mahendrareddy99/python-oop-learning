
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Employee
from .serializers import EmployeeSerializer
from .services import (
    EmployeeBusinessRuleError,
    create_employee,
    update_employee,
    deactivate_employee,
    search_employees,
    delete_employee,
)


def business_rule_response(exc):
    return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeListCreateAPIView(APIView):
    def get(self, request):
        include_inactive = (
            request.query_params.get("include_inactive", "").lower() == "true"
        )
        employees = search_employees(
            query=request.query_params.get("search", ""),
            active_only=not include_inactive,
        )
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            employee = create_employee(serializer.validated_data)
        except EmployeeBusinessRuleError as exc:
            return business_rule_response(exc)

        return Response(
            EmployeeSerializer(employee).data,
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
            EmployeeSerializer(employee).data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, employee_id):
        employee = self.get_object(employee_id)
        serializer = EmployeeSerializer(employee, data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            employee = update_employee(employee, serializer.validated_data)
        except EmployeeBusinessRuleError as exc:
            return business_rule_response(exc)

        return Response(
            EmployeeSerializer(employee).data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request, employee_id):
        employee = self.get_object(employee_id)
        serializer = EmployeeSerializer(
            employee, data=request.data, partial=True
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            employee = update_employee(employee, serializer.validated_data)
        except EmployeeBusinessRuleError as exc:
            return business_rule_response(exc)

        return Response(
            EmployeeSerializer(employee).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request, employee_id):
        employee = self.get_object(employee_id)

        if request.data.get("action") != "deactivate":
            return Response(
                {"error": "Use action='deactivate' to deactivate an employee."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            employee = deactivate_employee(employee)
        except EmployeeBusinessRuleError as exc:
            return business_rule_response(exc)

        return Response(
            EmployeeSerializer(employee).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, employee_id):
        employee = self.get_object(employee_id)

        try:
            delete_employee(employee)
        except EmployeeBusinessRuleError as exc:
            return business_rule_response(exc)

        return Response(status=status.HTTP_204_NO_CONTENT)
