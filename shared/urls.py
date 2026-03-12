from django.urls import path

from shared.views import HomePageView, ContactPageView, AboutPageView

app_name = 'shared'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact')
]
