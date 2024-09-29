from django.test import TestCase

from course.models import Course, Modul
from authorization.models import User


class TestModelCourse(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="Bob",
            email="bob@test.com",
            password="Q1w2e3r4t5y6_"
        )

        self.course = Course.objects.create(
            name="Big Data",
            description="about data",
            certificate_blank="test.png",
            owner=self.user,
        )

    def test_model_fields(self):
        self.assertEquals(self.course.owner, self.user)
        self.assertEquals(self.course.name, "Big Data")
        self.assertEquals(self.course.description, "about data")
        self.assertEquals(self.course.certificate_blank, "test.png")


class TestModelModul(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="Bob",
            email="bob@test.com",
            password="Q1w2e3r4t5y6_"
        )

        self.course = Course.objects.create(
            name="Big Data",
            description="about data",
            certificate_blank="test.png",
            owner=self.user,
        )

        self.modul = Modul.objects.create(
            title="data",
            description="about big data",
            video="test.mp4",
            course=self.course,
            position=1
        )

    def test_model_fields(self):
        self.assertEquals(self.modul.course, self.course)
        self.assertEquals(self.modul.title, "data")
        self.assertEquals(self.modul.description, "about big data")
        self.assertEquals(self.modul.video, "test.mp4")
        self.assertEquals(self.modul.position, 1)
