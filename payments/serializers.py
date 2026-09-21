from rest_framework import serializers
from .models import Payment

class PaymentListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'merchant_id',
            'external_order_id',
            'amount',
            'currency',
            'status',
            'stripe_payment_intent_id',
            'created_at',
            'updated_at'
        ]

class PaymentCreateResponseSerializer(serializers.Serializer):
    payment_id = serializers.UUIDField()
    external_order_id = serializers.CharField()
    amount = serializers.IntegerField()
    currency = serializers.CharField()
    client_secret = serializers.CharField()
