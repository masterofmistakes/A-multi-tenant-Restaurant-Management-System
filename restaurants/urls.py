from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, TableViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')

table_list_create = TableViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

table_detail = TableViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = router.urls + [
    path('restaurants/<int:restaurant_id>/tables/', table_list_create, name='restaurant-table-list'),
    path('tables/<int:pk>/', table_detail, name='table-detail'),
]