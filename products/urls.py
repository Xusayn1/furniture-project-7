from django.urls import path

from products.views import ProductDetailView, ProductListlView

app_name = 'products'

urlpatterns = [
    path('', ProductListlView.as_view(), name='list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='detail'),
]
