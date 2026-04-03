from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import (
    LoginAPIView,
    LogoutAPIView,
    MeAPIView,
    ProductListAPIView,
    RegisterAPIView,
)

app_name = 'api'

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='auth-register'),
    path('auth/login/', LoginAPIView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='auth-logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/me/', MeAPIView.as_view(), name='auth-me'),

    path('products/', ProductListAPIView.as_view(), name='products'),
]
