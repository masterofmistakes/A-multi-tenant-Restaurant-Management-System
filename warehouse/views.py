from .models import Ingredient
from .serializers import IngredientSerializer
from .permissions import CanManageWH
from rest_framework.viewsets import ModelViewSet

class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [CanManageWH]
    
    def perform_create(self, serializer):
        serializer.save(restaurant = self.request.user.restaurant)

    def get_queryset(self):
        return Ingredient.objects.filter(restaurant = self.request.user.restaurant)
