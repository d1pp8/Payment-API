from rest_framework import serializers
from apps.payments.models import Payment

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'merchant',
            'external_order_id',
            'amount',
            'currency',
        ]
        read_only_field = [
            'uuid',
            'status',
            'stripe_payment_intent_id',
            'created_at',
            'updated_at'
        ]

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentCreateResponseSerializer(serializers.Serializer):
    payment_id = serializers.UUIDField()
    external_order_id = serializers.CharField()
    amount = serializers.IntegerField()
    currency = serializers.CharField()
    client_secret = serializers.CharField()
