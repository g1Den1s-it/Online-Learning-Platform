from django.contrib import admin

from .models import Course, Modul, UserCourse, UserCertificate
# Register your models here.

admin.site.register(Course)
admin.site.register(Modul)
admin.site.register(UserCourse)
admin.site.register(UserCertificate)
