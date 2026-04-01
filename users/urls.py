from django.urls import path

from users.views import RegisterFormView, LoginFormView, LogoutView, ResetPasswordFormView, verify_email_view, \
    AccountUpdateView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterFormView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', AccountUpdateView.as_view(), name='account'),
    path('reset-password/', ResetPasswordFormView.as_view(), name='reset-password'),
    path('verify-email/<uidb64>/<token>/', verify_email_view, name='verify-email'),
]