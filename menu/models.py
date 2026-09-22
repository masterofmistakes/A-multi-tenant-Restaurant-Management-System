from django.db import models
from restaurants.models import Restaurant
from django.core.exceptions import ValidationError
from warehouse.models import Ingredient

class Category(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.parent:
            if self.parent.restaurant != self.restaurant:
                raise ValidationError({'parent': "Subkategoriya ham parent kategoriya restorani bir boliwi kerek!"})

            if self.parent_id == self.pk:
                raise ValidationError({'parent': "Kategoriya oz-ozine subkategoriya bola almaydi!"})
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    photo = models.ImageField(upload_to='dishes/', null=True, blank=True)
    is_available = models.BooleanField(db_default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes')

    def __str__(self):
        return self.name

class RecipeItem(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='recipe_items')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipe_items')
    quantity_per_serving = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        unique_together = ('dish', 'ingredient')

    def __str__(self):
        return f"{self.dish.name} -> {self.ingredient.name}: {self.quantity_per_serving}"