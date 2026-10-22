
from django.db import migrations


DEFAULT_ORGANIZATION_NAME = "Default Organization"


def assign_existing_departments(apps, schema_editor):
    Organization = apps.get_model("common", "Organization")
    Department = apps.get_model("departments", "Department")

    database = schema_editor.connection.alias

    organization, _ = Organization.objects.using(database).get_or_create(
        name=DEFAULT_ORGANIZATION_NAME,
    )

    Department.objects.using(database).filter(
        organization__isnull=True
    ).update(organization=organization)


def reverse_assignment(apps, schema_editor):
    Organization = apps.get_model("common", "Organization")
    Department = apps.get_model("departments", "Department")

    database = schema_editor.connection.alias

    organization = Organization.objects.using(database).filter(
        name=DEFAULT_ORGANIZATION_NAME
    ).first()

    if organization is not None:
        Department.objects.using(database).filter(
            organization=organization
        ).update(organization=None)


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0001_initial"),
        ("departments", "0002_department_organization_alter_department_name_and_more"),
    ]

    operations = [
        migrations.RunPython(
            assign_existing_departments,
            reverse_assignment,
        ),
    ]
