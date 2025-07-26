from unittest.mock import ANY

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription

User = get_user_model()


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@mail.com", password="1234")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Python", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Intro", course=self.course, owner=self.user, video_url="https://youtube.com/example"
        )

    def test_course_create(self):
        url = reverse("lms:course-list")
        data = {"title": "New course"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_retrieve(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_list(self):
        url = reverse("lms:course-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "lessons_count": 1,
                    "lessons": [
                        {
                            "id": self.lesson.pk,
                            "video_url": self.lesson.video_url,
                            "title": self.lesson.title,
                            "description": self.lesson.description,
                            "preview": None,
                            "course": self.course.pk,
                            "owner": self.user.pk,
                        }
                    ],
                    "is_subscribed": False,
                    "title": self.course.title,
                    "preview": None,
                    "description": self.course.description,
                    "updated_at": ANY,
                    "owner": self.user.pk,
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_course_update(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        data = {"title": "Updated course"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Updated course")

    def test_course_delete(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_other_user_cannot_update_course(self):
        other = User.objects.create(email="other2@mail.com", password="1234")
        self.client.force_authenticate(user=other)

        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.patch(url, {"title": "Hello!"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_moderator_can_view_all_courses(self):
        moderator = User.objects.create(email="mod@mail.com", password="1234")
        moderator.groups.create(name="moderator")
        moderator.groups.set(moderator.groups.all())
        self.client.force_authenticate(user=moderator)

        url = reverse("lms:course-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data["count"], 1)

    def test_anonymous_user_cannot_access_courses(self):
        self.client.logout()
        url = reverse("lms:course-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_moderator_cannot_create_course(self):
        moderator = User.objects.create(email="mod@mail.com", password="1234")
        moderator.groups.create(name="moderator")
        self.client.force_authenticate(user=moderator)
        url = reverse("lms:course-list")
        response = self.client.post(url, {"title": "Hello!"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@mail.com", password="1234")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Python", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Intro", course=self.course, owner=self.user, video_url="https://youtube.com/example"
        )

    def test_lesson_create(self):
        url = reverse("lms:lesson_create")
        data = {"title": "New lesson", "course": self.course.id, "video_url": "http://youtube.com/video"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_retrieve(self):
        url = reverse("lms:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_list(self):
        url = reverse("lms:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_url": self.lesson.video_url,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_lesson_update(self):
        url = reverse("lms:lesson_update", args=(self.lesson.pk,))
        data = {"title": "Updated lesson"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Updated lesson")

    def test_lesson_delete(self):
        url = reverse("lms:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_moderator_can_view_all_lessons(self):
        moderator = User.objects.create(email="mod@mail.com", password="1234")
        moderator.groups.create(name="moderator")
        self.client.force_authenticate(user=moderator)

        url = reverse("lms:lesson_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data["count"], 1)

    def test_other_user_cannot_update_lesson(self):
        other = User.objects.create(email="other@mail.com", password="1234")
        self.client.force_authenticate(user=other)
        url = reverse("lms:lesson_update", args=(self.lesson.pk,))
        response = self.client.patch(url, {"title": "Hack"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user@mail.com", password="1234")
        self.other_user = User.objects.create(email="other@mail.com", password="1234")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Course 1", owner=self.other_user)
        self.url = reverse("lms:subscribe")

    def test_subscribe_to_course(self):
        response = self.client.post(self.url, {"course_id": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_to_course(self):
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(self.url, {"course_id": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unauthorized_user_cannot_subscribe(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, {"course_id": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_to_nonexistent_course(self):
        response = self.client.post(self.url, {"course_id": 99999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
