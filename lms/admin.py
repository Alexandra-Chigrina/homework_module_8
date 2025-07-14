from django.contrib import admin

from lms.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "updated_at")
    list_filter = ("owner",)
    search_fields = ("title",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "course", "owner")
    list_filter = ("owner",)
    search_fields = ("title",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course")
    list_filter = ("user",)
    search_fields = ("course",)
