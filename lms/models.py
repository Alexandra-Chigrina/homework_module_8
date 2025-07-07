from django.db import models

from config import settings


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название курса", help_text="Укажите название курса")
    preview = models.ImageField(
        upload_to="lms/course_previews", blank=True, null=True, verbose_name="Превью", help_text="Загрузите превью"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание курса", help_text="Укажите описание курса"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название урока", help_text="Введите название урока")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Курс",
        help_text="Выберите курс",
        related_name="lessons",
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание курса", help_text="Укажите описание курса"
    )
    preview = models.ImageField(
        upload_to="lms/lesson_previews", blank=True, null=True, verbose_name="Превью", help_text="Загрузите превью"
    )
    video_url = models.URLField(verbose_name="Ссылка на видео", help_text="Укажите ссылку на видео")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь",related_name="subscriptions")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="subscriptions")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ('user', 'course')
