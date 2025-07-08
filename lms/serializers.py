from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, course):
        return course.lessons.count()

    def get_is_subscribed(self, course):
        user = self.context.get("request").user
        if user.is_authenticated:
            return course.subscriptions.filter(user=user).exists()
        return False
