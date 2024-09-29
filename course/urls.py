from django.urls import path
from .views import (
    CreateCourseView,
    CreateModul,
    ListCourseView,
    DetailCourseView,
    AddNewStudentView,
    CreateCertificateView,
    ListCertificateView,
    UpdateCourseView,
    UpdateModuleView)


urlpatterns = [
    path('courses/create-course/', CreateCourseView.as_view(), name='create-course'),
    path('courses/<str:slug>/create-modul/', CreateModul.as_view(), name='create-modul'),
    path('courses/', ListCourseView.as_view(), name='list-course'),
    path('courses/<str:slug>/', DetailCourseView.as_view(), name='detail-course'),
    path('courses/<str:slug>/add/', AddNewStudentView.as_view(), name="add_student"),
    path('courses/<str:slug>/certificate/', CreateCertificateView.as_view(), name='create-certificate'),
    path('courses/user/certificate', ListCertificateView.as_view(), name="user-certificate"),
    path('courses/<str:slug>/update/', UpdateCourseView.as_view(), name='course-update'),
    path('courses/<str:slug>/modul/', UpdateModuleView.as_view(), name='modul_update'),

]
