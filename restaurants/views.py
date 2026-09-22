from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema
from accounts.models import UserRole
from .models import Restaurant, Table
from .serializers import RestaurantSerializer, TableSerializer, TableUpdateSerializer
from .permissions import IsSuperAdminOrReadOnly, IsAdminOrStaffOrReadOnly


@extend_schema(tags=['restaurants'])
class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsSuperAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_superuser:
            return Restaurant.objects.all()
        return Restaurant.objects.filter(is_active=True)


@extend_schema(tags=['tables'])
class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    permission_classes = [IsAdminOrStaffOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['partial_update', 'update']: 
            return TableUpdateSerializer
        return TableSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Table.objects.select_related('restaurant')

        # 1. /restaurants/<restaurant_id>/tables/
        restaurant_id = self.kwargs.get('restaurant_id')
        if restaurant_id:
            if user.is_authenticated and user.role == UserRole.ADMIN:
                return queryset.filter(restaurant_id=user.restaurant)
            return queryset.filter(restaurant_id=restaurant_id, is_active=True)

        # 2. /tables/<pk>/
        table_id = self.kwargs.get('pk')
        if user.is_authenticated and user.role == UserRole.ADMIN:
            return queryset.filter(id = table_id, restaurant = user.restaurant)
        elif user.is_authenticated:
            return queryset.filter(id = table_id, is_active=True)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(restaurant=user.restaurant)