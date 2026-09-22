from rest_framework import serializers
from .models import Restaurant, Table


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            'id', 'name', 'logo', 'phone', 'is_active', 
            'address', 'opening_time', 'closing_time'
        )


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = (
            'id', 'restaurant', 'number', 'capacity', 
            'is_active', 'table_type', 'status'
        )
        read_only_fields = ['restaurant']


class TableUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('number', 'capacity', 'is_active', 'table_type', 'status')