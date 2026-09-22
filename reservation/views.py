from .models import Reservation
from .serializers import ReservationReadSerializer, ReservationSerializer
from rest_framework.viewsets import ModelViewSet
from .permissions import WhoAreYou
from accounts.models import UserRole

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
        restaurant_id = self.request.query_params.get('restaurant_id')
        if self.request.user and self.request.user.is_authenticated and self.request.user.role == UserRole.CLIENT:
            serializer.save(restaurant=restaurant_id)
        else:
            serializer.save(restaurant=self.request.user.restaurant)

