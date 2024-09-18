from rest_framework import serializers

from .models import Course, Modul, UserCourse


class CourseSerializer(serializers.ModelSerializer):
    amount_students = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id',
                  'name',
                  'slug',
                  'certificate_blank',
                  'owner',
                  'amount_students')


    def get_amount_students(self, obj):
        return obj.students.count()


class ModulSerializer(serializers.ModelSerializer):

    class Meta:
        model = Modul
        fields = ('id',
                  'title',
                  'description',
                  'video')


class UserCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCourse
        fields = ('id',
                  'user',
                  'course',
                  'joined_at',
                  'is_completed',
                  'completed_at')
