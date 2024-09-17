from django.urls import path
from .views import (
    CreateCourseView,
    CreateModul,
    ListCourseView,
    DetailCourseView,
    AddNewStudentView)


urlpatterns = [
    path('create-course/', CreateCourseView.as_view(), name='create-course'),
    path('create-modul/', CreateModul.as_view(), name='create-modul'),
    path('cousers/', ListCourseView.as_view(), name='list-course'),
    path('cousers/<str:slug>/', DetailCourseView.as_view(), name='detail-course'),
    path('cousers/<str:slug>/add/', AddNewStudentView.as_view(), name="add_student")
]
