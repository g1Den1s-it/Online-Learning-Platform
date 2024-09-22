from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from authorization.models import User
from .models import Course, Modul, UserCourse, UserCertificate
from .permissions import IsTeacher, IsStudent, IsCourseOwner
from .serializers import CourseSerializer, ModulSerializer, UserCourseSerializer, UserCertificateSerializer
from .task import create_certificate


class CreateCourseView(CreateAPIView):
    queryset = Course.objects.all()
    permission_classes = (IsTeacher, )
    serializer_class = CourseSerializer


class CreateModul(CreateAPIView):
    queryset = Modul.objects.all()
    permission_classes = (IsCourseOwner, )
    serializer_class = ModulSerializer

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        file = request.FILES.get('video')
        course_slug = kwargs.get('slug')

        if not course_slug:
            return Response(
                {"message": "Slug does not exist"},
                status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, slug=course_slug)

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
    permission_classes = (IsStudent, )

    def update(self, request, *args, **kwargs):
        student_id = request.data.get('student_id')

        if not student_id:
            return Response({"message": "wrong data"},
                            status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, **{self.lookup_field: self.kwargs[self.lookup_field]})
        student = get_object_or_404(User, id=student_id)

        course.students.add(student)
        course.save()

        serializer = UserCourseSerializer(data={
            "user": student.id,
            "course": course.id,
        })

        if serializer.is_valid():
            serializer.save()

        return Response(status=status.HTTP_200_OK)


class CreateCertificateView(CreateAPIView):
    permission_classes = (IsStudent, )

    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        slug = kwargs.get("slug")

        user = get_object_or_404(User, id=user_id)
        course = get_object_or_404(Course, slug=slug)
        user_course = get_object_or_404(UserCourse, user=user_id, course=course.id)

        if UserCertificate.objects.filter(user=user, course=course).exists():
            return Response({'message': 'You already have certificate for this course!'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not user_course.is_completed:
            return Response({'message': "you didn't finish course yet, to get certificate"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not user.first_name and not user.last_name:
            return Response({'message': "To get certificate, you must fill 'first_name' and 'last_name'!"},
                            status=status.HTTP_400_BAD_REQUEST)

        user_certificate = UserCertificate.objects.create(user=user, course=course)

        user_certificate.save()

        create_certificate.delay(
            f'{user.first_name} {user.last_name}',
            course.name,
            user_course.completed_at,
            course.certificate_blank.path,
            user_certificate.pk
        )

        return Response({'message': 'Thanks, your certificate will be created in several minutes.'},
                        status=status.HTTP_201_CREATED)
