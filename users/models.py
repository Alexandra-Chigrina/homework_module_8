from django.contrib.auth.models import AbstractUser
from django.db import models


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


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [("cash", "Наличные"), ("transfer", "Перевод")]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, совершивший оплату",
        related_name="payments",
    )
    payment_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата оплаты", help_text="Дата и время совершения оплаты"
    )
    paid_course = models.ForeignKey(
        "lms.Course",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Оплаченный курс",
        related_name="payments",
        help_text="Ссылка на курс, если он оплачен",
    )
    paid_lesson = models.ForeignKey(
        "lms.Lesson",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Оплаченный урок",
        related_name="payments",
        help_text="Ссылка на урок, если он оплачен",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты", help_text="Сумма, уплаченная за курс или урок"
    )
    method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты: наличные или перевод",
    )
    stripe_session_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="ID сессии", help_text="Укажите ID сессии"
    )
    payment_url = models.URLField(
        max_length=400, blank=True, null=True, verbose_name="Ссылка на оплату", help_text="Укажите ссылку на оплату"
    )

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user.email} - {self.amount} ₽ ({self.payment_date.date()}) "
