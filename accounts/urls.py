from django.urls import path
from .views import RegisterView, UserMeView, CreateRoleView, RoleUpdateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', TokenBlacklistView.as_view(), name = 'token_logout'),
    path('auth/me/', UserMeView.as_view(), name = 'user_profile'),
    path('restaurants/<int:id>/staff/', CreateRoleView.as_view(), name = 'create_role'),
    path('staff/<int:id>/', RoleUpdateView.as_view(), name = 'update_staff')
]


