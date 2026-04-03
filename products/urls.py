
from django.urls import path

from products.views import ProductListView, ProductDetailView, add_or_remove_from_cart, add_or_remove_from_wishlist, \
    CartListView, WishlistListView

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('<int:pk>/cart/', add_or_remove_from_cart, name='cart'),
    path('<int:pk>/wishlist/', add_or_remove_from_wishlist, name='wishlist'),
    # Full-page views
    path('wishlist/', WishlistListView.as_view(), name='wishlist_page'),
    path('cart/', CartListView.as_view(), name='cart_page'),
]
