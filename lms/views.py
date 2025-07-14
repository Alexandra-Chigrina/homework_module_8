from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Subscription
from lms.paginators import CustomPagination
from lms.serializers import CourseSerializer, LessonSerializer
from lms.tasks import send_course_update_email
from users.permissions import IsModerator, IsOwner, NotModerator


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Получить список курсов",
        operation_description="Получает список курсов, доступных текущему пользователю (или всех, если модератор).",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Получить курс по ID",
        operation_description="Возвращает информацию о конкретном курсе, если пользователь имеет доступ.",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Создать курс",
        operation_description="Создаёт новый курс. Доступно только владельцам (не модераторам).",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_summary="Обновить курс",
        operation_description="Полностью обновляет курс. Доступно владельцу или модератору.",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_summary="Частичное обновление курса",
        operation_description="Частично обновляет курс. Доступно владельцу или модератору.",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_summary="Удалить курс",
        operation_description="Удаляет курс. Доступно только владельцу и не модератору.",
    ),
)
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Course.objects.none()
        if user.groups.filter(name="moderator").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, NotModerator]
        elif self.action in ["update", "partial_update", "retrieve", "list"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner, NotModerator]
        return [permission() for permission in self.permission_classes]

    def perform_update(self, serializer):
        instance = serializer.save()
        send_course_update_email.delay(instance.id)


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_summary="Создать урок",
        operation_description="Создаёт урок внутри курса. Доступно только владельцам, не модераторам.",
    ),
)
class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, NotModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Список уроков",
        operation_description="Возвращает список уроков. Модераторы видят все, владельцы — только свои.",
    ),
)
class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Получить урок по ID",
        operation_description="Получает подробности об уроке. Доступ зависит от ролей.",
    ),
)
class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_summary="Обновить урок", operation_description="Обновляет урок. Доступен владельцам и модераторам."
    ),
)
class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        operation_summary="Удалить урок", operation_description="Удаляет урок. Доступно владельцам (не модераторам)."
    ),
)
class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, NotModerator]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Подписка/отписка от курса",
        operation_description="""
        Добавляет или удаляет подписку на курс. Возвращает 201 при добавлении, 204 при удалении.
        """,
        responses={201: "Подписка добавлена", 204: "Подписка удалена", 401: "Не авторизован", 404: "Курс не найден"},
    )
    def post(self, request, *args, **kwargs):
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        subs = Subscription.objects.filter(user=request.user, course=course)

        if subs.exists():
            subs.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            Subscription.objects.create(user=request.user, course=course)
            return Response(status=status.HTTP_201_CREATED)
