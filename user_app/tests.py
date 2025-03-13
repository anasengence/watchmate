from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            "username": "testcase",
            "email": "test@localhost",
            "password": "some_strong_psw",
            "password3": "some_strong_psw",
        }
        response = self.client.post(reverse("Register"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testcase", password="some_strong_psw"
        )
        self.token = Token.objects.create(user=self.user)

    def test_login(self):
        data = {"username": "testcase", "password": "some_strong_psw"}
        response = self.client.post(reverse("Login"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete(reverse("Logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
