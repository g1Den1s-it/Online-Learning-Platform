from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Course, Modul
from .serializers import CourseSerializer, ModulSerializer


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
    lookup_field = "pk"
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

