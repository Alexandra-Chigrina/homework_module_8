from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "paid_course", "paid_lesson", "amount", "method", "payment_date"]


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentShortSerializer(source="payments.all", many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar", "first_name", "last_name", "payments"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'phone', 'city', 'avatar', 'first_name', 'last_name']
