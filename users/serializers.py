from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'first_name', 'last_name']


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
