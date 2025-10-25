from rest_framework import serializers
from .models import Customer
import math

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['approved_limit']

    def create(self, validated_data):
        income = validated_data.get('monthly_income')
        # Formula: approved_limit = 36 * monthly_income
        limit = 36 * income
        limit = int(round(limit, -5))  # Round to nearest lakh (100000)
        validated_data['approved_limit'] = limit
        return super().create(validated_data)
