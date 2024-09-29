from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from authorization.models import User
from course.models import Course


class TestCourseViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username="David",
            email="david@test.com",
            password="Q1w2e3r4t5y6_",
            role="Teacher"
        )
        self.access_token = AccessToken.for_user(self.user)

        with open("img.png", "wb+") as file:
            file.write(b"something")
            file.seek(0)
            uploaded_file = SimpleUploadedFile(file.name, file.read(), content_type="image/png")

            self.test_data = {
                "name": "Big data",
                "description": "about data",
                "certificate_blank": uploaded_file,
                "owner": self.user.pk
            }

    def test_create_course(self):

        res = self.client.post("/courses/create-course/",
                               data=self.test_data,
                               format="multipart",
                               headers={"Authorization": f"Bearer {self.access_token}"})

        self.assertEquals(res.status_code, 201)
        self.assertEquals(res.data["name"], self.test_data["name"])
        self.assertEquals(res.data["owner"], self.test_data["owner"])


    def test_course_update(self):
        res = self.client.post("/courses/create-course/",
                               data=self.test_data,
                               format="multipart",
                               headers={"Authorization": f"Bearer {self.access_token}"})

        self.assertEquals(res.status_code, 201)

        with open("imgq.png", "wb+") as file:
            file.write(b"something")
            file.seek(0)
            file = SimpleUploadedFile(file.name, file.read(), content_type="image/png")

        res = self.client.put(f"/courses/{res.data['slug']}/update/",
                              data={"name": "GameDev",
                                    "description": "new text",
                                    "certificate_blank": file,
                                    "owner": self.user.pk},
                              format="multipart",
                              headers={"Authorization": f"Bearer {self.access_token}"})

        self.assertEquals(res.status_code, 200)


    def test_course_list(self):
        res = self.client.post("/courses/create-course/",
                               data=self.test_data,
                               format="multipart",
                               headers={"Authorization": f"Bearer {self.access_token}"})

        self.assertEquals(res.status_code, 201)

        res = self.client.get("/courses/")

        self.assertEquals(res.status_code, 200)
        self.assertEquals(len(res.data), 1)


class TestModulViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username="David",
            email="david@test.com",
            password="Q1w2e3r4t5y6_",
            role="Teacher"
        )
        self.access_token = AccessToken.for_user(self.user)

        self.test_course = Course.objects.create(
            name="Big data",
            description="about data",
            certificate_blank="img.png",
            owner=self.user
        )

    def test_create_modul(self):
        with open("image.mp4", "wb+") as file:
            file.write(b"some")
            uploaded_file = SimpleUploadedFile(file.name, file.read())

        test_data = {
            "title": "about data",
            "description": ".....",
            "video": uploaded_file,
            "course": self.test_course.pk,
            "position": 1
        }

        res = self.client.post(f"/courses/{self.test_course.slug}/create-modul/",
                               data=test_data, format="multipart",
                               headers={"Authorization": f"Bearer {self.access_token}"})

        self.assertEquals(res.status_code, 201)
        self.assertEquals(res.data['title'], test_data['title'])
        self.assertEquals(res.data['description'], test_data['description'])

