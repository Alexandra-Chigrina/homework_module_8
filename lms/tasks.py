from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from lms.models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    """Отправляет сообщение пользователю с информацией об обновлении курса."""
    course = Course.objects.get(id=course_id)
    emails = Subscription.objects.filter(course=course).values_list("user__email", flat=True)
    for email in emails:
        send_mail(
            subject=f"Обновление курса: {course.title}",
            message=f"Курс {course.title} был обновлен. Проверьте новые материалы!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=True,
        )
