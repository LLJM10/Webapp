from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'order_id', 'capture_id', 'amount', 'currency', 'status', 'raw_response',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'status', 'raw_response', 'created_at', 'updated_at']
