from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.permissions import IsSelfUser
from users.serializers import PaymentSerializer, UserPublicSerializer, UserRegisterSerializer, UserSerializer


@method_decorator(name="list", decorator=swagger_auto_schema(
    operation_summary="Получить список пользователей",
    operation_description="Доступен авторизованным пользователям. Возвращает публичные данные пользователей."
),)
@method_decorator(name="retrieve", decorator=swagger_auto_schema(
    operation_summary="Получить пользователя по ID",
    operation_description="Возвращает полный профиль, если пользователь - владелец профиля, иначе — публичные данные."
),)
@method_decorator(name="update", decorator=swagger_auto_schema(
    operation_summary="Обновить пользователя",
    operation_description="Позволяет обновить профиль, если пользователь - владелец профиля."
),)
@method_decorator(name="partial_update", decorator=swagger_auto_schema(
    operation_summary="Частичное обновление пользователя",
    operation_description="Позволяет частично обновить профиль, если пользователь - владелец профиля."
),)
@method_decorator(name="destroy", decorator=swagger_auto_schema(
    operation_summary="Удалить пользователя",
    operation_description="Удаление доступно администраторам."
),)
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["retrieve", "update", "partial_update"]:
            obj = self.get_object()
            if obj == self.request.user:
                return UserSerializer  # Полный
        return UserPublicSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsSelfUser]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


@method_decorator(name="post", decorator=swagger_auto_schema(
    operation_summary="Регистрация нового пользователя",
    operation_description="Создание нового пользователя. Доступно без авторизации."
),)
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


@method_decorator(name="list", decorator=swagger_auto_schema(
    operation_summary="Список платежей",
    operation_description="Возвращает список всех платежей с возможностью фильтрации по курсам, урокам и методу оплаты."
),)
@method_decorator(name="retrieve", decorator=swagger_auto_schema(
    operation_summary="Получить информацию о платеже",
    operation_description="Возвращает подробную информацию о конкретном платеже по ID."
),)
@method_decorator(name="create", decorator=swagger_auto_schema(
    operation_summary="Создать платёж",
    operation_description="Добавляет новый платёж. Только для авторизованных пользователей."
),)
@method_decorator(name="update", decorator=swagger_auto_schema(
    operation_summary="Обновить платёж",
    operation_description="Обновляет платёж полностью."
),)
@method_decorator(name="partial_update", decorator=swagger_auto_schema(
    operation_summary="Частично обновить платёж",
    operation_description="Частично обновляет поля платежа."
),)
@method_decorator(name="destroy", decorator=swagger_auto_schema(
    operation_summary="Удалить платёж",
    operation_description="Удаляет платёж по ID."
),)
class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["paid_course", "paid_lesson", "method"]
    ordering_fields = ["payment_date"]
    permission_classes = [IsAuthenticated]
