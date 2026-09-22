from .views import CategoryViewSet, DishViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path(
        'restaurants/<int:restaurant_id>/categories/',
        CategoryViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='restaurant-categories'
    ),
    
    path(
        'categories/<int:pk>/',
        CategoryViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='category-detail'
    ),
    path(
            'restaurants/<int:restaurant_id>/dishes/',
            DishViewSet.as_view({'get': 'list', 'post': 'create'}),
            name='restaurant-dishes'
        ),

    path(
            'dishes/<int:pk>/',
            DishViewSet.as_view({
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            }),
            name='dish-detail'
        ),
]
