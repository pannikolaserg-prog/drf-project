from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from materials.models import Lesson, Course

User = get_user_model()


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin@sky.pro",
            phone="+79991234567"
        )
        self.course = Course.objects.create(
            name="Python",
            description="Курс основы программирования",
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Введение",
            course=self.course,
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], "Python")

    def test_course_create(self):
        url = reverse("course-list")
        data = {
            "name": "Java",
            "description": "Курс по Java"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        url = reverse("course-detail", args=(self.course.pk,))
        data = {
            "name": "Basic"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data["name"], "Basic"
        )

    def test_course_delete(self):
        url = reverse("course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        url = reverse("course-list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["name"], "Python")
        self.assertEqual(data["results"][0]["id"], self.course.pk)


