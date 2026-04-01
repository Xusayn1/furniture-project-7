from django.urls import path

from api.views import LoginAPIView, ProductListAPIView

app_name = 'api'

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('products/', ProductListAPIView.as_view(), name='login'),
]