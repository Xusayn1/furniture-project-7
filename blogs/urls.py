from django.urls import path

from blogs.views import BlogDetailView, BlogListView

app_name = 'blogs'

urlpatterns = [
    path('', BlogListView.as_view(), name='list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='detail'),
]
