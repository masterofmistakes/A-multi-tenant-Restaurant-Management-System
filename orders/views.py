from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers as drf_serializers
from accounts.models import UserRole
from .models import Order, OrderItem, OrderItemStatus
from .permissions import IsChefPermission, IsWaiterOrReadOnly
from .serializers import (
    ChefItemUpdateSerializer, KitchenOrderItemSerializer, OrderItemSerializer, OrderSerializer,
    OrderTrackingSerializer, OrderUpdateSerializer, WaiterItemUpdateSerializer,
)


class OrderViewSet(ModelViewSet):
    permission_classes = [IsWaiterOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Order.objects.none()

        queryset = Order.objects.select_related(
            'restaurant', 'client', 'waiter', 'table_number'
        ).prefetch_related('items__dish')

        if hasattr(user, 'restaurant') and user.restaurant:
            return queryset.filter(restaurant=user.restaurant)

        if user.role == UserRole.CLIENT:
            return queryset.filter(client=user)

        restaurant_id = self.kwargs.get('restaurant_id') or self.kwargs.get('pk')
        if restaurant_id:
            return queryset.filter(restaurant_id=restaurant_id)

        return queryset.none()

    def get_serializer_class(self):
        if self.action == 'add_item':
            return OrderItemSerializer
        elif self.action == 'upd_item':
            user = getattr(self.request, 'user', None)
            if user and getattr(user, 'role', None) == UserRole.WAITER:
                return WaiterItemUpdateSerializer
            return ChefItemUpdateSerializer
        elif self.action == 'partial_update':
            return OrderUpdateSerializer
        
        return OrderSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'restaurant') and user.restaurant:
            serializer.save(waiter=user, restaurant=user.restaurant)
        else:
            raise drf_serializers.ValidationError({
                "restaurant": "Paydalaniwshiga biriktirilgen restoran tabilmadi!"
            })

    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='track-order')
    def track_order(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response(
                {"detail": "Orderdin unikal kodin kiritiw shart!"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        order = get_object_or_404(
            Order.objects.select_related('restaurant', 'table_number').prefetch_related('items__dish'),
            tracking_code=code.strip().upper()
        )
        
        serializer = OrderTrackingSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='add-item')
    def add_item(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(data=request.data)     

        if serializer.is_valid():
            serializer.save(order=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], url_path=r'item-detail/(?P<item_pk>[^/.]+)')
    def upd_item(self, request, item_pk=None):
        user = request.user

        item = get_object_or_404(OrderItem, id=item_pk, order__restaurant=user.restaurant)
        
        serializer = self.get_serializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class KitchenDisplayViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsChefPermission]
    serializer_class = KitchenOrderItemSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated or not hasattr(user, 'restaurant') or not user.restaurant:
            return OrderItem.objects.none()

        return OrderItem.objects.filter(
            order__restaurant=user.restaurant,
            orderitem_status__in=[OrderItemStatus.ACCEPTED, OrderItemStatus.PREPARING]
        ).select_related('dish', 'order', 'order__table_number').order_by('created_at')

    @action(detail=True, methods=['patch'], url_path='mark-ready')
    def mark_as_ready(self, request, pk=None):
        item = self.get_object()
        item.orderitem_status = OrderItemStatus.READY
        item.save(update_fields=['orderitem_status'])
        
        serializer = self.get_serializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)