from .models import Category, Dish, RecipeItem
from rest_framework import serializers
from django.db import transaction

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['restaurant']
    
    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []

class RecipeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeItem
        fields = "__all__"
        read_only_fields = ('dish',)

class DishSerializer(serializers.ModelSerializer):
    recipe = RecipeItemSerializer(many=True, source='recipe_items', required=False)

    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'photo', 'is_available', 'category', 'recipe']

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('recipe_items', [])
        dish = Dish.objects.create(**validated_data)
        
        if items_data:
            recipe_items = [
                RecipeItem(dish=dish, **item_data) for item_data in items_data
            ]
            RecipeItem.objects.bulk_create(recipe_items)
            
        return dish

    @transaction.atomic
    def update(self, instance, validated_data):
        items_data = validated_data.pop('recipe_items', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.recipe_items.all().delete()
            recipe_items = [
                RecipeItem(dish=instance, **item_data) for item_data in items_data
            ]
            RecipeItem.objects.bulk_create(recipe_items)

        return instance
