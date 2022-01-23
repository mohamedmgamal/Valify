from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import  views
urlpatterns = [
    path('signUp/', views.signUp, name='Registration'),
    path('login/', views.ObtainAuthToken.as_view(), name='api_token_auth'),
    path('refreshToken/', views.RefreshToken.as_view(), name='api_refresh_token_auth'),
    path('activeAccount/', views.ActiveAccount.as_view(), name='api_active_account'),
]
