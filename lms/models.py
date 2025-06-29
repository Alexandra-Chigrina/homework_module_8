from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название курса", help_text="Укажите название курса")
    preview = models.ImageField(
        upload_to="course/course_previews", blank=True, null=True, verbose_name="Превью", help_text="Загрузите превью"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание курса", help_text="Укажите описание курса"
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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
