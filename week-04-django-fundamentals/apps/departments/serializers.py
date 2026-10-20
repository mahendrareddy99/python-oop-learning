
from rest_framework import serializers

from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "description", "status"]
        read_only_fields = ["id"]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Department name cannot be empty."
            )

        # Department names must be unique within an organization.
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            organization_id = (
                request.user.organization_membership.organization_id
            )

            queryset = Department.objects.filter(
                organization_id=organization_id,
                name__iexact=value,
            )

            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise serializers.ValidationError(
                    "A department with this name already exists."
                )

        return value
