import os
import uuid

from django.db import models
from django.utils.text import slugify

from authorization.models import User


# Create your models here.

def get_upload_to(instance, filename):
    path = slugify(instance.course.slug)
    return os.path.join(f"course/{path}/modul/", filename)


class Course(models.Model):
    name = models.CharField(max_length=126, blank=False, null=False)
    slug = models.SlugField(max_length=126, unique=True, blank=True)
    description = models.TextField()
    certificate_blank = models.FileField(upload_to=f"course/certificate")
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    administrators = models.ManyToManyField(User, related_name="administrators_course")
    students = models.ManyToManyField(User, related_name="students_courses")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()

        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.owner.username} -- {self.name}'


class Modul(models.Model):
    title = models.CharField(max_length=126, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to=get_upload_to)
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.course.name[:10]} -- {self.title[:10]}'


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    joined_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} -- {self.is_completed}'


class UserCertificate(models.Model):
    certificate = models.FileField(upload_to="course/certificate/completed")
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.user.username}"
