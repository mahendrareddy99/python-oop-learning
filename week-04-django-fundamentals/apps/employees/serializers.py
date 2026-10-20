
from rest_framework import serializers

from apps.departments.models import Department
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        error_messages={
            "required": "An employee must belong to a department.",
            "does_not_exist": "The selected department does not exist.",
            "incorrect_type": "Provide a valid department ID.",
        },
    )

    department_details = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_code",
            "first_name",
            "last_name",
            "email",
            "phone",
            "date_of_joining",
            "status",
            "department",
            "department_details",
        ]
        read_only_fields = [
            "id",
            "status",
            "department_details",
        ]

    def validate_employee_code(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Employee code cannot be empty."
            )

        queryset = Employee.objects.filter(
            employee_code__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "An employee with this code already exists."
            )

        return value

    def validate_first_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "First name cannot be empty."
            )

        return value

    def validate_last_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Last name cannot be empty."
            )

        return value

    def validate_email(self, value):
        value = value.strip().lower()

        queryset = Employee.objects.filter(
            email__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "An employee with this email already exists."
            )

        return value

    def validate_phone(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Phone number cannot be empty."
            )

        if len(value) > 15:
            raise serializers.ValidationError(
                "Phone number cannot exceed 15 characters."
            )

        return value

    def validate_department(self, value):
        if not value.status:
            raise serializers.ValidationError(
                "Employees cannot be assigned to an inactive department."
            )

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            try:
                membership = (
                    request.user.organization_membership
                )
            except Exception:
                raise serializers.ValidationError(
                    "You must belong to an organization "
                    "to assign a department."
                )

            if not membership.organization.status:
                raise serializers.ValidationError(
                    "Your organization is inactive."
                )

            if (
                value.organization_id
                != membership.organization_id
            ):
                raise serializers.ValidationError(
                    "The selected department does not belong "
                    "to your organization."
                )

        return value

    def validate(self, attrs):
        department = attrs.get(
            "department",
            getattr(self.instance, "department", None),
        )

        if department is None:
            raise serializers.ValidationError({
                "department": (
                    "An employee must belong to a department."
                )
            })

        return attrs

    def get_department_details(self, obj):
        return {
            "id": obj.department.id,
            "name": obj.department.name,
            "status": obj.department.status,
        }
