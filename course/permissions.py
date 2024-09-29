from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Course


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        jwt_auth = JWTAuthentication()
        user_data = jwt_auth.authenticate(request)[0]
        if not user_data:
            raise PermissionDenied("Authentication failed.")

        if user_data.role != "Teacher":
            raise PermissionDenied(f"Access denied. User role is '{user_data.role}', not 'Teacher'.")

        return True


class IsCourseOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        jwt_auth = JWTAuthentication()
        user_data = jwt_auth.authenticate(request)[0]
        course_slug = view.kwargs.get("slug")

        if not user_data:
            raise PermissionDenied("Authentication failed.")

        course = get_object_or_404(Course, slug=course_slug)

        if course.owner != user_data:
            raise PermissionDenied(f"{user_data.username} is not owner of {course.name}")

        return True


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        jwt_auth = JWTAuthentication()
        user_data = jwt_auth.authenticate(request)[0]

        if not user_data:
            raise PermissionDenied("Authentication failed.")

        if user_data.role != "Student":
            raise PermissionDenied(f"Access denied. User role is '{user_data.role}', not 'Student'.")

        return True
