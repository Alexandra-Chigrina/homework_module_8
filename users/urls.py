from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    PaymentSessionCreateAPIView,
    PaymentStatusAPIView,
    PaymentViewSet,
    UserCreateAPIView,
    UserViewSet
)

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"users", UserViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("payments/checkout/", PaymentSessionCreateAPIView.as_view(), name="payments_checkout"),
    path("payments/<int:pk>/status/", PaymentStatusAPIView.as_view(), name="payment_status"),
]

urlpatterns += router.urls
