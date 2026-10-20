
from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.common.models import Organization, OrganizationMembership
from apps.departments.models import Department
from apps.employees.models import Employee


class EmployeeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        User = get_user_model()
        self.user = User.objects.create_user(
            username="hrms_test_user",
            password="TestPassword123!",
        )

        # Create the organization for the authenticated user.
        self.organization = Organization.objects.create(
            name="Test Organization",
        )

        OrganizationMembership.objects.create(
            user=self.user,
            organization=self.organization,
            role=OrganizationMembership.Role.ADMIN,
        )

        self.client.force_authenticate(user=self.user)

        # Both departments belong to the user's organization.
        self.department = Department.objects.create(
            organization=self.organization,
            name="Engineering",
            description="Engineering department",
        )

        self.other_department = Department.objects.create(
            organization=self.organization,
            name="Human Resources",
            description="HR department",
        )

        # Create an active employee.
        Employee.objects.create(
            employee_code="EMP001",
            first_name="Ravi",
            last_name="Kumar",
            email="ravi.test@example.com",
            phone="9876543210",
            date_of_joining=date(2026, 1, 1),
            department=self.department,
            status=True,
        )

        # Create an inactive employee.
        Employee.objects.create(
            employee_code="EMP002",
            first_name="Priya",
            last_name="Sharma",
            email="priya.test@example.com",
            phone="9876543211",
            date_of_joining=date(2026, 2, 1),
            department=self.other_department,
            status=False,
        )

    def create_other_organization_data(self):
        """Create a second organization, department, and employee."""
        organization = Organization.objects.create(
            name="Another Organization",
        )

        department = Department.objects.create(
            organization=organization,
            name="Engineering",
            description="Other organization's engineering team",
        )

        employee = Employee.objects.create(
            employee_code="OTHER001",
            first_name="Other",
            last_name="Employee",
            email="other.employee@example.com",
            phone="9876543299",
            date_of_joining=date(2026, 4, 1),
            department=department,
            status=True,
        )

        return organization, department, employee

    def create_staff_user(self):
        """Create a user with read-only staff permissions."""
        User = get_user_model()
        staff_user = User.objects.create_user(
            username="hrms_staff_user",
            password="StaffPassword123!",
        )

        OrganizationMembership.objects.create(
            user=staff_user,
            organization=self.organization,
            role=OrganizationMembership.Role.STAFF,
        )

        return staff_user

    # --------------------------------------------------
    # Authentication and permissions
    # --------------------------------------------------

    def test_unauthenticated_user_cannot_list_employees(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/employees/")

        self.assertIn(response.status_code, [401, 403])

    def test_unauthenticated_user_cannot_list_departments(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/departments/")

        self.assertIn(response.status_code, [401, 403])

    def test_user_without_membership_cannot_list_employees(self):
        User = get_user_model()
        user_without_membership = User.objects.create_user(
            username="no_membership_user",
            password="TestPassword123!",
        )

        self.client.force_authenticate(
            user=user_without_membership
        )

        response = self.client.get("/api/employees/")

        self.assertEqual(response.status_code, 403)

    def test_staff_cannot_create_employee(self):
        staff_user = self.create_staff_user()
        self.client.force_authenticate(user=staff_user)

        payload = {
            "employee_code": "EMP003",
            "first_name": "Arun",
            "last_name": "Reddy",
            "email": "arun.test@example.com",
            "phone": "9876543212",
            "date_of_joining": "2026-03-01",
            "department": self.department.id,
        }

        response = self.client.post(
            "/api/employees/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(
            Employee.objects.filter(
                employee_code="EMP003"
            ).exists()
        )

    def test_staff_cannot_create_department(self):
        staff_user = self.create_staff_user()
        self.client.force_authenticate(user=staff_user)

        response = self.client.post(
            "/api/departments/",
            {
                "name": "Finance",
                "description": "Finance department",
                "status": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(
            Department.objects.filter(
                organization=self.organization,
                name="Finance",
            ).exists()
        )

    def test_staff_cannot_update_department(self):
        staff_user = self.create_staff_user()
        self.client.force_authenticate(user=staff_user)

        response = self.client.patch(
            f"/api/departments/{self.department.id}/",
            {"name": "Unauthorized Update"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

        self.department.refresh_from_db()
        self.assertEqual(self.department.name, "Engineering")

    def test_staff_cannot_update_employee(self):
        staff_user = self.create_staff_user()
        self.client.force_authenticate(user=staff_user)

        employee = Employee.objects.get(
            employee_code="EMP001"
        )

        response = self.client.patch(
            f"/api/employees/{employee.id}/",
            {"first_name": "Unauthorized Update"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

        employee.refresh_from_db()
        self.assertEqual(employee.first_name, "Ravi")

    # --------------------------------------------------
    # Employee list, search, filtering, and pagination
    # --------------------------------------------------

    def test_employee_list_returns_paginated_response(self):
        response = self.client.get("/api/employees/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertIn("data", response.data)
        self.assertIn("pagination", response.data)
        self.assertEqual(
            response.data["pagination"]["count"], 1
        )

    def test_search_employees(self):
        response = self.client.get(
            "/api/employees/",
            {"search": "Ravi"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(
            response.data["data"][0]["employee_code"],
            "EMP001",
        )

    def test_filter_employees_by_status(self):
        response = self.client.get(
            "/api/employees/",
            {"status": "false"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(
            response.data["data"][0]["employee_code"],
            "EMP002",
        )

    def test_filter_employees_by_department(self):
        response = self.client.get(
            "/api/employees/",
            {
                "department": str(self.other_department.id),
                "include_inactive": "true",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(
            response.data["data"][0]["employee_code"],
            "EMP002",
        )

    def test_invalid_status_returns_400(self):
        response = self.client.get(
            "/api/employees/",
            {"status": "unknown"},
        )

        self.assertEqual(response.status_code, 400)

    # --------------------------------------------------
    # Department list and detail
    # --------------------------------------------------

    def test_department_list_returns_paginated_response(self):
        response = self.client.get("/api/departments/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertIn("data", response.data)
        self.assertIn("pagination", response.data)
        self.assertEqual(
            response.data["pagination"]["count"], 2
        )

    def test_department_detail_returns_department(self):
        response = self.client.get(
            f"/api/departments/{self.department.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["data"]["name"],
            "Engineering",
        )

    # --------------------------------------------------
    # Employee CRUD operations
    # --------------------------------------------------

    def test_create_employee(self):
        payload = {
            "employee_code": "EMP003",
            "first_name": "Arun",
            "last_name": "Reddy",
            "email": "arun.test@example.com",
            "phone": "9876543212",
            "date_of_joining": "2026-03-01",
            "department": self.department.id,
        }

        response = self.client.post(
            "/api/employees/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["data"]["employee_code"],
            "EMP003",
        )
        self.assertTrue(
            Employee.objects.filter(
                employee_code="EMP003",
                department__organization=self.organization,
            ).exists()
        )

    def test_retrieve_employee_detail(self):
        employee = Employee.objects.get(
            employee_code="EMP001"
        )

        response = self.client.get(
            f"/api/employees/{employee.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["data"]["employee_code"],
            "EMP001",
        )

    def test_update_employee(self):
        employee = Employee.objects.get(
            employee_code="EMP001"
        )

        payload = {
            "employee_code": "EMP001",
            "first_name": "Ravi Updated",
            "last_name": "Kumar",
            "email": "ravi.test@example.com",
            "phone": "9876543210",
            "date_of_joining": "2026-01-01",
            "department": self.department.id,
        }

        response = self.client.put(
            f"/api/employees/{employee.id}/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["data"]["first_name"],
            "Ravi Updated",
        )

    def test_partial_update_employee(self):
        employee = Employee.objects.get(
            employee_code="EMP001"
        )

        response = self.client.patch(
            f"/api/employees/{employee.id}/",
            {"first_name": "Ravi Patched"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["data"]["first_name"],
            "Ravi Patched",
        )

    def test_deactivate_employee(self):
        employee = Employee.objects.get(
            employee_code="EMP001"
        )

        response = self.client.post(
            f"/api/employees/{employee.id}/",
            {"action": "deactivate"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        employee.refresh_from_db()
        self.assertFalse(employee.status)

    def test_active_employee_cannot_be_deleted(self):
        employee = Employee.objects.get(
            employee_code="EMP001"
        )

        response = self.client.delete(
            f"/api/employees/{employee.id}/"
        )

        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            Employee.objects.filter(id=employee.id).exists()
        )

    def test_inactive_employee_can_be_deleted(self):
        employee = Employee.objects.get(
            employee_code="EMP002"
        )

        response = self.client.delete(
            f"/api/employees/{employee.id}/"
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Employee.objects.filter(id=employee.id).exists()
        )

    def test_employee_not_found_returns_404(self):
        response = self.client.get(
            "/api/employees/999999/"
        )

        self.assertEqual(response.status_code, 404)

    def test_invalid_employee_data_returns_400(self):
        payload = {
            "employee_code": "EMP003",
            "first_name": "",
            "last_name": "Reddy",
            "email": "invalid-email",
            "date_of_joining": "2026-03-01",
            "department": self.department.id,
        }

        response = self.client.post(
            "/api/employees/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("details", response.data)

    # --------------------------------------------------
    # Department CRUD and validation tests
    # --------------------------------------------------

    def test_create_department(self):
        payload = {
            "name": "Finance",
            "description": "Finance department",
            "status": True,
        }

        response = self.client.post(
            "/api/departments/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["success"])
        self.assertEqual(
            response.data["data"]["name"],
            "Finance",
        )
        self.assertTrue(
            Department.objects.filter(
                organization=self.organization,
                name="Finance",
            ).exists()
        )

    def test_create_department_with_duplicate_name_returns_400(self):
        payload = {
            "name": "Engineering",
            "description": "Duplicate department",
            "status": True,
        }

        response = self.client.post(
            "/api/departments/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data["success"])

    def test_update_department(self):
        payload = {
            "name": "Engineering Updated",
            "description": "Updated engineering department",
            "status": True,
        }

        response = self.client.put(
            f"/api/departments/{self.department.id}/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["data"]["name"],
            "Engineering Updated",
        )

        self.department.refresh_from_db()
        self.assertEqual(
            self.department.name,
            "Engineering Updated",
        )

    def test_partial_update_department(self):
        response = self.client.patch(
            f"/api/departments/{self.department.id}/",
            {"description": "Updated description"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["data"]["description"],
            "Updated description",
        )

    def test_delete_department_without_employees(self):
        department = Department.objects.create(
            organization=self.organization,
            name="Finance",
            description="Finance department",
        )

        response = self.client.delete(
            f"/api/departments/{department.id}/"
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Department.objects.filter(
                id=department.id
            ).exists()
        )

    def test_department_with_employees_cannot_be_deleted(self):
        response = self.client.delete(
            f"/api/departments/{self.department.id}/"
        )

        self.assertEqual(response.status_code, 409)
        self.assertTrue(
            Department.objects.filter(
                id=self.department.id
            ).exists()
        )

    def test_department_not_found_returns_404(self):
        response = self.client.get(
            "/api/departments/999999/"
        )

        self.assertEqual(response.status_code, 404)

    # --------------------------------------------------
    # Organization isolation tests
    # --------------------------------------------------

    def test_employee_list_excludes_other_organization(self):
        _, _, other_employee = (
            self.create_other_organization_data()
        )

        response = self.client.get("/api/employees/")

        self.assertEqual(response.status_code, 200)

        employee_ids = [
            item["id"] for item in response.data["data"]
        ]

        self.assertNotIn(other_employee.id, employee_ids)

    def test_cannot_retrieve_employee_from_other_organization(self):
        _, _, other_employee = (
            self.create_other_organization_data()
        )

        response = self.client.get(
            f"/api/employees/{other_employee.id}/"
        )

        self.assertEqual(response.status_code, 404)

    def test_department_list_excludes_other_organization(self):
        _, other_department, _ = (
            self.create_other_organization_data()
        )

        response = self.client.get("/api/departments/")

        self.assertEqual(response.status_code, 200)

        department_ids = [
            item["id"] for item in response.data["data"]
        ]

        self.assertNotIn(
            other_department.id,
            department_ids,
        )

    def test_cannot_retrieve_department_from_other_organization(self):
        _, other_department, _ = (
            self.create_other_organization_data()
        )

        response = self.client.get(
            f"/api/departments/{other_department.id}/"
        )

        self.assertEqual(response.status_code, 404)

    def test_cannot_create_employee_in_other_organization(self):
        _, other_department, _ = (
            self.create_other_organization_data()
        )

        payload = {
            "employee_code": "EMP003",
            "first_name": "Arun",
            "last_name": "Reddy",
            "email": "arun.test@example.com",
            "phone": "9876543212",
            "date_of_joining": "2026-03-01",
            "department": other_department.id,
        }

        response = self.client.post(
            "/api/employees/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            Employee.objects.filter(
                employee_code="EMP003"
            ).exists()
        )

    def test_department_creation_uses_users_organization(self):
        other_organization, _, _ = (
            self.create_other_organization_data()
        )

        response = self.client.post(
            "/api/departments/",
            {
                "name": "Finance",
                "description": "Finance department",
                "status": True,
                "organization": other_organization.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        department = Department.objects.get(
            name="Finance",
            organization=self.organization,
        )

        self.assertEqual(
            department.organization_id,
            self.organization.id,
        )
        self.assertFalse(
            Department.objects.filter(
                name="Finance",
                organization=other_organization,
            ).exists()
        )

    def test_cannot_move_employee_to_other_organization(self):
        _, other_department, _ = (
            self.create_other_organization_data()
        )

        employee = Employee.objects.get(
            employee_code="EMP001"
        )

        response = self.client.patch(
            f"/api/employees/{employee.id}/",
            {"department": other_department.id},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

        employee.refresh_from_db()
        self.assertEqual(
            employee.department_id,
            self.department.id,
        )
