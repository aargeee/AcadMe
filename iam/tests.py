# Create your tests here.
from __future__ import annotations

import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


class TestSignUpView(APITestCase):
    """Signup tests."""

    def setUp(self: TestSignUpView) -> None:
        """Signup tests Setup."""
        super().setUp()
        self.url = reverse("learner-signup")
        self.client = APIClient()
        self.learner_group = Group(name="learner")
        self.learner_group.save()
        self.tutor_group = Group(name="tutor")
        self.tutor_group.save()
        self.existing_user = User.objects.create(username="existing-user")

    def tearDown(self) -> None:
        self.learner_group.delete()
        self.tutor_group.delete()
        return super().tearDown()

    def test_register_new_learner(self: TestSignUpView) -> None:
        """Test register new user."""
        payload = {
            "username": "test-learner-2",
            "first_name": "test",
            "last_name": "learner",
            "email": "test@learner.com",
            "password": "abcd123",
        }
        res = self.client.post(self.url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        resdata: list[dict[str, str]] = json.loads(res.content)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(resdata["success"])

    def test_register_new_tutor(self: TestSignUpView) -> None:
        """Test register new user."""
        payload = {
            "username": "test-tutor-2",
            "first_name": "test",
            "last_name": "tutor",
            "email": "test@tutor.com",
            "password": "abcd123",
        }
        res = self.client.post(self.url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        resdata: list[dict[str, str]] = json.loads(res.content)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(resdata["success"])
