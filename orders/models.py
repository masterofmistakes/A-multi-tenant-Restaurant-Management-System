from django.db import models
from restaurants.models import Restaurant, Table
from accounts.models import User
from menu.models import Dish
import random, string


def generate_tracking_code():
    """Code generate function"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=6))

class OrderItemStatus(models.TextChoices):
    ACCEPTED = 'accepted', 'Qabil etildi'
    PREPARING = 'preparing', 'Tayarlanip atir'
    READY = 'ready', 'Tayyar'
    DELIVERED = 'delivered', 'Jetkerildi'
    CANCELLED = 'cancelled', 'Biykar qilindi'

class OrderStatus(models.TextChoices):
    OPEN = 'open', 'Ashiq'
    CLOSE = 'close', 'Jabilgan'

class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Kutilmekte'
    PAID = 'paid', 'Tolendi'
    FAILED = 'failed', 'Qatelik'

class PaymentMethod(models.TextChoices):
    CASH = 'cash', 'Naq'
    CARD = 'card', 'Karta (Terminal)'
    CLICK = 'click', 'Click'

class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='client_orders')
    waiter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='waiter_orders')
    table_number = models.ForeignKey(Table, on_delete=models.SET_NULL, blank=True, null=True, related_name = 'orders')
    order_status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.OPEN)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tracking_code = models.CharField(max_length=10, unique=True, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
            if not self.tracking_code:
                code = generate_tracking_code()
                while Order.objects.filter(tracking_code=code).exists():
                    code = generate_tracking_code()
                self.tracking_code = code
            super().save(*args, **kwargs)
    def __str__(self):
        return f"Order #{self.id} - {self.table_number} : {self.order_status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    orderitem_status = models.CharField(max_length=20, choices=OrderItemStatus.choices, default=OrderItemStatus.ACCEPTED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        dish_name = self.dish.name if self.dish else "Dish bazadan oshirilgen"
        return f"{self.quantity} x {dish_name}"