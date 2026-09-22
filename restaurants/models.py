from django.db import models
import datetime

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='restaurants/', null=True, blank=True)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    opening_time = models.TimeField(default=datetime.time(8, 0))
    closing_time = models.TimeField(default=datetime.time(23, 59))

    def __str__(self):
        return self.name

class TableStatus(models.TextChoices):
    FREE = 'free', 'Bos'
    RESERVED = 'reserved', 'Bron qilingan'
    BUSY = 'busy', 'Bant'

class TableType(models.TextChoices):
    COMMON = 'common', 'Uliwmaliq'
    CABIN = 'cabin', 'Kabina'

class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables')
    number = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField(default=2)
    is_active = models.BooleanField(default=True)
    table_type = models.CharField(max_length=20, choices=TableType.choices, default=TableType.COMMON)
    status = models.CharField(max_length=20, choices=TableStatus.choices, default=TableStatus.FREE)

    class Meta:
        unique_together = ('restaurant', 'number')

    def __str__(self):
        return f"Stol #{self.number} ({self.capacity} adamliq)"