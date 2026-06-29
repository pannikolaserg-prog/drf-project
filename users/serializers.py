from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Payment, User, Status_Pay


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "city", "avatar"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "paid_course",
            "paid_lesson",
            "amount",
            "payment_date",
            "payment_method",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "phone", "first_name", "last_name", "payments"]


class Status_PaySerializer(ModelSerializer):
    class Meta:
        model = Status_Pay
        fields = "__all__"

