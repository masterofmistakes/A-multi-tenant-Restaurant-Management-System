from .views import IngredientViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredient')

urlpatterns = router.urls

