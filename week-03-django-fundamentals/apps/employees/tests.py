
from datetime import date

from django.test import TestCase
from rest_framework.test import APIClient

from apps.departments.models import Department
from apps.employees.models import Employee


class EmployeeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.department = Department.objects.create(
            name="Engineering",
            description="Engineering department",
        )

        self.other_department = Department.objects.create(
            name="Human Resources",
            description="HR department",
        )

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

    # --------------------------------------------------
    # Employee list, search, filtering, and pagination
    # --------------------------------------------------

    def test_employee_list_returns_paginated_response(self):
        response = self.client.get("/api/employees/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertIn("data", response.data)
        self.assertIn("pagination", response.data)
        self.assertEqual(response.data["pagination"]["count"], 1)

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
        self.assertEqual(response.data["pagination"]["count"], 2)

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
            Employee.objects.filter(employee_code="EMP003").exists()
        )

    def test_retrieve_employee_detail(self):
        employee = Employee.objects.get(employee_code="EMP001")

        response = self.client.get(
            f"/api/employees/{employee.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["data"]["employee_code"],
            "EMP001",
        )

    def test_update_employee(self):
        employee = Employee.objects.get(employee_code="EMP001")

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
        employee = Employee.objects.get(employee_code="EMP001")

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
        employee = Employee.objects.get(employee_code="EMP001")

        response = self.client.post(
            f"/api/employees/{employee.id}/",
            {"action": "deactivate"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        employee.refresh_from_db()
        self.assertFalse(employee.status)

    def test_active_employee_cannot_be_deleted(self):
        employee = Employee.objects.get(employee_code="EMP001")

        response = self.client.delete(
            f"/api/employees/{employee.id}/"
        )

        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            Employee.objects.filter(id=employee.id).exists()
        )

    def test_inactive_employee_can_be_deleted(self):
        employee = Employee.objects.get(employee_code="EMP002")

        response = self.client.delete(
            f"/api/employees/{employee.id}/"
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Employee.objects.filter(id=employee.id).exists()
        )

    def test_employee_not_found_returns_404(self):
        response = self.client.get("/api/employees/999999/")

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
            Department.objects.filter(name="Finance").exists()
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
            name="Finance",
            description="Finance department",
        )

        response = self.client.delete(
            f"/api/departments/{department.id}/"
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Department.objects.filter(id=department.id).exists()
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
        response = self.client.get("/api/departments/999999/")

        self.assertEqual(response.status_code, 404)
