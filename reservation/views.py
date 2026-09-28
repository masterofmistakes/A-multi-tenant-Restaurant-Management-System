from .models import Reservation
from .serializers import ReservationReadSerializer, ReservationSerializer
from rest_framework.viewsets import ModelViewSet
from .permissions import WhoAreYou
from accounts.models import UserRole
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from restaurants.models import Restaurant

class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    permission_classes = [WhoAreYou]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReservationReadSerializer
        return ReservationSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.role in {UserRole.ADMIN, UserRole.WAITER}:
            return Reservation.objects.filter(restaurant = self.request.user.restaurant)
        elif self.request.user and self.request.user.is_authenticated:
            return Reservation.objects.filter(client = self.request.user)
        return super().get_queryset()


    def perform_create(self, serializer):
        user = self.request.user

        if user.role == UserRole.CLIENT:
            restaurant_id = self.request.query_params.get('restaurant_id')

            if not restaurant_id:
                raise ValidationError({
                    'restaurant_id': 'restaurant_id  parametiri kiritiliw shart!!!.'
                })

            restaurant = get_object_or_404(
                Restaurant, pk=restaurant_id, is_active=True
            )
            serializer.save(restaurant=restaurant)
        else:
            if not user.restaurant:
                raise ValidationError({
                    'detail': (
                        'Sizge hesh qanday restoran biriktirilmegen.'
                    )
                })

            serializer.save(restaurant=user.restaurant)

