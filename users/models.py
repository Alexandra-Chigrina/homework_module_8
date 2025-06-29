from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Укажите почту")
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Номер телефона", help_text="Укажите номер телефона"
    )
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город", help_text="Укажите город")
    avatar = models.ImageField(
        upload_to="user/avatars", blank=True, null=True, verbose_name="Аватар", help_text="Загрузите аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
