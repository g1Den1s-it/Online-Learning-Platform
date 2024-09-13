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
    certificate_blank = models.FileField(upload_to=f"course/{slug}/")
    owner = models.OneToOneField(User, on_delete=models.PROTECT)
    administrators = models.ManyToManyField(User, related_name="administrators_course")
    students = models.ManyToManyField(User, related_name="students_courses")

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = uuid.uuid4()

        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.owner.username} -- {self.name}'


class Modul(models.Model):
    title = models.CharField(max_length=126, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to=get_upload_to)
    course = models.OneToOneField(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.course.name[:10]} -- {self.title[:10]}'
