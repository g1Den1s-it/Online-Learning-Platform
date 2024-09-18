from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from authorization.models import User
from .models import Course, Modul, UserCourse
from .serializers import CourseSerializer, ModulSerializer, UserCourseSerializer


class CreateCourseView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CreateModul(CreateAPIView):
    queryset = Modul.objects.all()
    serializer_class = ModulSerializer

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        file = request.FILES.get('video')

        if not data.get('course'):
            return Response(
                {"message": "must be course key"},
                status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=data.get('course'))

        modul = Modul.objects.create(
            title=data.get('title'),
            description=data.get('description'),
            video=file,
            course=course)

        modul.save()

        modul_serializer = ModulSerializer(modul, many=False)
        return Response(modul_serializer.data, status=status.HTTP_201_CREATED)


class ListCourseView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class DetailCourseView(RetrieveAPIView):
    lookup_field = "slug"
    queryset = Course.objects.all()
    serializer_class = CourseSerializer



class AddNewStudentView(UpdateAPIView):
    lookup_field = "slug"
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, )

    def update(self, request, *args, **kwargs):
        student_id = request.data.get('student_id')

        if not student_id:
            return Response({"message": "wrong data"},
                            status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, **{self.lookup_field: self.kwargs[self.lookup_field]})
        student = get_object_or_404(User, id=student_id)

        if student.role != 'Student':
            return Response({"message": "User is not student"})

        course.students.add(student)
        course.save()

        serializer = UserCourseSerializer(data={
            "user": student.id,
            "course": course.id,
        })

        if serializer.is_valid():
            serializer.save()

        return Response(status=status.HTTP_200_OK)


