from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from lms.models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)
    for sub in subscribers:
        send_mail(
            subject=f"Обновление курса: {course.title}",
            message=f"Курс {course.title} был обновлен. Проверьте новые материалы!",
            from_email=EMAIL_HOST_USER,
            recipient_list=[sub.user.email],
            fail_silently=True
        )
