from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course
from users.models import Payment

User = get_user_model()


class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="user@example.com", password="pass1234")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("users:user-detail", args=(self.user.pk,))

    def test_user_retrieve_own_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("email", response.data)

    def test_user_cannot_update_other_user(self):
        other = User.objects.create(email="other@example.com", password="pass1234")
        url = reverse("users:user-detail", args=(other.pk,))
        response = self.client.patch(url, {"email": "hacked@example.com"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_user(self):
        self.admin = User.objects.create(email="admin@example.com", password="admin1234")
        self.admin.is_staff = True
        self.admin.save()

        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_user_create(self):
        self.client.logout()
        url = reverse("users:register")
        data = {"email": "new@example.com", "password": "pass1234"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PaymentTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="payer@example.com", password="1234")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Course", owner=self.user)
        self.payment = Payment.objects.create(user=self.user, amount=1000, method="card", paid_course=self.course)

    def test_list_payments(self):
        url = reverse("users:payment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_by_course(self):
        url = reverse("users:payment-list") + f"?paid_course={self.course.pk}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data:
            self.assertEqual(item["paid_course"], self.course.pk)

    def test_ordering_by_payment_date(self):
        url = reverse("users:payment-list") + "?ordering=payment_date"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
