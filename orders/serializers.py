from decimal import Decimal
from django.db import transaction
from django.db.models import F
from rest_framework import serializers
from .models import Order, OrderItem, OrderItemStatus


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'dish', 'quantity', 'price', 'orderitem_status')
        read_only_fields = ['price', 'order']

    @transaction.atomic 
    def create(self, validated_data):
        order = validated_data.get('order')
        dish = validated_data.get('dish')
        quantity = validated_data.get('quantity', 1)

        for recipe_item in dish.recipe_items.select_related('ingredient'):
            total_amount = recipe_item.quantity_per_serving * quantity
            ingredient = recipe_item.ingredient

            if ingredient.current_stock < total_amount:
                raise serializers.ValidationError({
                    "ingredient": f"'{ingredient.name} jeterli emes. Talap etiletugin mugdari: {total_amount}, Skladdagi mugdari: {ingredient.current_stock}"
                })
            
            ingredient.current_stock = F('current_stock') - total_amount
            ingredient.save(update_fields=['current_stock'])

        item_price = dish.price * quantity
        validated_data['price'] = item_price

        order.total_price = F('total_price') + item_price
        order.save(update_fields=['total_price'])

        return OrderItem.objects.create(**validated_data)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['restaurant', 'client', 'waiter', 'tracking_code', 'total_price', 'items']  

class OrderTrackingSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    table_number = serializers.CharField(source='table_number.number', read_only=True, default="Stol bazadan oshirilgen")
    items = OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ('tracking_code', 'restaurant_name', 'table_number', 'order_status', 
                  'total_price', 'payment_status', 'items', 'created_at'
        )

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'order_status', 'payment_status', 'payment_method')


class ChefItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'dish', 'quantity', 'orderitem_status']
        read_only_fields = ('dish', 'quantity')


class WaiterItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'dish', 'quantity', 'orderitem_status']
        read_only_fields = ('dish',)

    def update(self, instance, validated_data):
        old_quantity = instance.quantity
        new_quantity = validated_data.get('quantity', old_quantity)
        dish = instance.dish

        if new_quantity != old_quantity:
            if new_quantity > old_quantity:
                raise serializers.ValidationError(
                    {"quantity": "Buyirtpada item sanin asirip bolmaydi."}
                )
            if instance.orderitem_status != OrderItemStatus.ACCEPTED:
                raise serializers.ValidationError(
                    {"quantity": "Tek gana accepted statusindagi awqatlardi ozgertiw mumkin"}
                )   
            if not dish:
                raise serializers.ValidationError(
                    {"dish": "Bul dish menudan oshirilgeni sebepli oni ozgertip bolmaydi."}
                )

            quantity_diff = old_quantity - new_quantity

            with transaction.atomic():
                for recipe_item in dish.recipe_items.select_related('ingredient'):
                    returned_amount = recipe_item.quantity_per_serving * quantity_diff
                    ingredient = recipe_item.ingredient
                    ingredient.current_stock = F('current_stock') + returned_amount
                    ingredient.save(update_fields=['current_stock'])

                price_reduce = dish.price * quantity_diff

                instance.price = F('price') - price_reduce
                instance.quantity = new_quantity
                instance.orderitem_status = validated_data.get('orderitem_status', instance.orderitem_status)
                instance.save()

                order = instance.order
                order.total_price = F('total_price') - price_reduce
                order.save(update_fields=['total_price'])

                instance.refresh_from_db()
                return instance

        return super().update(instance, validated_data)


class KitchenOrderItemSerializer(serializers.ModelSerializer):
    dish = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ['order', 'dish', 'quantity', 'price']

    def get_dish(self, obj):
        return obj.dish.name if obj.dish else "Deleted dish"