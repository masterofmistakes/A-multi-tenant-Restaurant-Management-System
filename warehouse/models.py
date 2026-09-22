from django.db import models
from restaurants.models import Restaurant

class UnitType(models.TextChoices):
    KG = 'kg', 'Kilogramm'
    GRAM = 'g', 'Gramm'
    LITER = 'l', 'Litr'
    MILLILITER = 'ml', 'Millilitr'
    PIECE = 'piece', 'dana'


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10, choices=UnitType.choices, default=UnitType.KG)
    current_stock = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='ingredients')

    class Meta:
            unique_together = ('restaurant', 'name')

    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.unit})"


