from .serializers import RegisterSerializer, UserSerializer, CreateRoleSerializer, UpdateRoleSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAdmin
from .models import User, UserRole
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

class UserMeView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  

    def get_object(self):
        return self.request.user

@extend_schema(tags=['staff'])
class CreateRoleView(ListCreateAPIView):
    serializer_class = CreateRoleSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        user_restaurant = getattr(self.request.user, 'restaurant', None)
        
        if user_restaurant is None:
            raise ValidationError({"detail": "You do not have permission for this action!!!"})
        
        serializer.save(restaurant=user_restaurant)
    def get_queryset(self):
        user_restaurant = getattr(self.request.user, 'restaurant', None)
        if user_restaurant is None:
            return User.objects.none()
        return User.objects.filter(restaurant = self.request.user.restaurant)
    
@extend_schema(tags=['staff'])
class RoleUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = UpdateRoleSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'id' 
    lookup_url_kwarg = 'id'

    def perform_destroy(self, instance):
        if instance.role == UserRole.ADMIN:
            raise PermissionDenied("You cant delete admin profile")
            
        instance.delete()

    def get_queryset(self):
        return User.objects.filter(restaurant = self.request.user.restaurant)


