from datetime import timedelta
from rest_framework import serializers
from .models import Reservation, ReservationStatus
from restaurants.serializers import TableSerializer


class ReservationReadSerializer(serializers.ModelSerializer):
    table = TableSerializer(read_only=True)
    client_name = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = (
            'id', 'restaurant', 'table', 'client', 'client_name',
            'guests_count', 'start_time', 'duration', 'end_time',
            'status', 'notes', 'created_at'
        )

    def get_client_name(self, obj):
        if obj.client:
            return getattr(obj.client, 'first_name', None) or obj.client.username
        return "Guest"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            'id', 'restaurant', 'table', 'client',
            'guests_count', 'start_time', 'duration',
            'status', 'notes'
        )
        read_only_fields = ['client', 'restaurant']

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)

        table = attrs.get('table', getattr(instance, 'table', None))
        start_time = attrs.get('start_time', getattr(instance, 'start_time', None))
        duration = attrs.get('duration', getattr(instance, 'duration', None))
        restaurant = attrs.get('restaurant', getattr(instance, 'restaurant', None))

        if not duration:
            duration = timedelta(hours=2)

        if start_time and table:
            end_time = start_time + duration

            if restaurant and table.restaurant_id != restaurant.id:
                raise serializers.ValidationError({
                    "table": "Tanlangan stol restoranga tiyisli emes!"
                })

            overlapping = Reservation.objects.filter(
                table=table,
                status__in=[ReservationStatus.PENDING, ReservationStatus.BOOKED],
                start_time__lt=end_time,
                end_time__gt=start_time
            )

            if instance:
                overlapping = overlapping.exclude(pk=instance.pk)

            if overlapping.exists():
                raise serializers.ValidationError({
                    "table": "Bul stol korsetilgen waqit ishinde bos emes!"
                })

        return attrs