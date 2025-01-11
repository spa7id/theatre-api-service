from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from user.serializers import UserSerializer

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email="test@example.com", password="password123")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password123"))

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email="admin@example.com", password="admin123")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class UserSerializerTests(TestCase):
    def test_user_serializer(self):
        user = User.objects.create_user(email="test@example.com", password="password123")
        serializer = UserSerializer(user)
        data = serializer.data
        self.assertEqual(data["email"], "test@example.com")
        self.assertNotIn("password", data)

    def test_user_serializer_create(self):
        data = {"email": "test@example.com", "password": "password123"}
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password123"))


class UserViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="test@example.com",
                                             password="password123")

    def test_create_user_view(self):
        payload = {
            "email": "newuser@example.com",
            "password": "password123",
        }
        response = self.client.post("/api/users/register/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_login_user(self):
        payload = {
            "email": "test@example.com",
            "password": "password123",
        }
        response = self.client.post("/api/users/token/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_manage_user_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/users/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_update_user_view(self):
        self.client.force_authenticate(user=self.user)
        payload = {"password": "newpassword123"}
        response = self.client.patch("/api/users/me/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))
