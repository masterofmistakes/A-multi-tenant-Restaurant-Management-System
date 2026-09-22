import datetime
from django.db import models
from restaurants.models import Table, Restaurant
from accounts.models import User

class ReservationStatus(models.TextChoices):
    PENDING = 'pending', 'Kutilmekte'
    BOOKED = 'booked', 'Bronlangan'
    CANCELLED = 'cancelled', 'Biykarlandi'
    COMPLETED = 'completed', 'Orinlandi'

class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    guests_count = models.PositiveIntegerField(default=1)
    start_time = models.DateTimeField(verbose_name='Baslaniw waqti')
    duration = models.DurationField(
        verbose_name="Dawamliligi", 
        help_text="Format: HH:MM:SS", 
        default=datetime.timedelta(hours=2)
    )
    end_time = models.DateTimeField(verbose_name='Tamamlaniw waqti', null=True, blank=True, editable=False)
    status = models.CharField(max_length=20, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.start_time and self.duration:
            self.end_time = self.start_time + self.duration
        super().save(*args, **kwargs)

    def __str__(self):
        client_name = getattr(self.client, 'fullname', 'Guest')
        table_num = self.table.number 
        return f"Bron #{self.id} - {client_name} (Stol #{table_num})"