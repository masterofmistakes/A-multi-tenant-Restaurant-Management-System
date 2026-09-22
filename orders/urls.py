from rest_framework.urls import path
from .views import OrderViewSet, KitchenDisplayViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'kitchen-items', KitchenDisplayViewSet, basename='kitchen-item')

urlpatterns = router.urls