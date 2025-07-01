from rest_framework.serializers import ModelSerializer, SerializerMethodField

from users.models import User, Payment

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentShortSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'paid_course', 'paid_lesson', 'amount', 'method', 'payment_date']


class UserSerializer(ModelSerializer):
    payments = PaymentShortSerializer(source="payments.all", many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'first_name', 'last_name', 'payments']
