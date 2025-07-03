from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, course):
        return course.lessons.count()
