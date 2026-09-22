from .models import Category, Dish
from .serializers import CategorySerializer, DishSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.viewsets import ModelViewSet
from accounts.models import UserRole
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['menu'])
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Category.objects.all()
        if not self.request.user.is_authenticated:
            return queryset.none()
        if self.request.user.role != UserRole.CLIENT:
            return queryset.filter(restaurant = self.request.user.restaurant)
        
        restaurant_id = self.kwargs.get('restaurant_id')
        if restaurant_id:
            return queryset.filter(restaurant=restaurant_id)
        return queryset
            
    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.restaurant)

@extend_schema(tags=['menu'])
class DishViewSet(ModelViewSet):
    serializer_class = DishSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Dish.objects.select_related('category').prefetch_related('recipe_items__ingredient')
        user = self.request.user

        if not user.is_authenticated or user.role == UserRole.CLIENT:
            queryset = queryset.filter(is_available=True)

        if user.is_authenticated and user.role != UserRole.CLIENT:
            if hasattr(user, 'restaurant') and user.restaurant:
                queryset = queryset.filter(category__restaurant=user.restaurant)
            else:
                return queryset.none()
        elif 'restaurant_id' in self.kwargs:
            queryset = queryset.filter(category__restaurant=self.kwargs['restaurant_id'])

        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

