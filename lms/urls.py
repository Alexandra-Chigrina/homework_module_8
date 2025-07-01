from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonListAPIVew,
    LessonRetrieveAPIVew,
    LessonUpdateAPIVew,
    LessonDestroyAPIVew,
)


app_name = LmsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIVew.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIVew.as_view(), name="lesson_retrieve"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIVew.as_view(), name="lesson_delete"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIVew.as_view(), name="lesson_update"),
]

urlpatterns += router.urls
