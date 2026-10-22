
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.common.models import Organization, OrganizationMembership


class AuthenticationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            username="auth_test_user",
            password="TestPassword123!",
        )

        # Create an organization for the authenticated user.
        self.organization = Organization.objects.create(
            name="Authentication Test Organization",
        )

        # The APIs require every authenticated user to have membership.
        OrganizationMembership.objects.create(
            user=self.user,
            organization=self.organization,
            role=OrganizationMembership.Role.ADMIN,
        )

    def test_anonymous_user_cannot_access_employee_api(self):
        response = self.client.get("/api/employees/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_valid_credentials_allow_employee_api_access(self):
        logged_in = self.client.login(
            username="auth_test_user",
            password="TestPassword123!",
        )

        self.assertTrue(logged_in)

        response = self.client.get("/api/employees/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_invalid_credentials_do_not_authenticate_user(self):
        logged_in = self.client.login(
            username="auth_test_user",
            password="WrongPassword123!",
        )

        self.assertFalse(logged_in)

        response = self.client.get("/api/employees/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_valid_session_can_access_department_api(self):
        logged_in = self.client.login(
            username="auth_test_user",
            password="TestPassword123!",
        )

        self.assertTrue(logged_in)

        response = self.client.get("/api/departments/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
