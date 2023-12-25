from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import register, LoginView, user_profile, password_reset_request
from . import views

urlpatterns = [
    # ... другие пути
    path('api/accounts/register/', register, name='register'),
    path('api/accounts/login/', LoginView.as_view(), name='login'),
    path('api/user/profile/', user_profile, name='user_profile'),
    path('api/accounts/password-reset-request/', views.password_reset_request, name='password-reset-request'),
    path('api/accounts/reset-password-confirm/', views.reset_password_confirm, name='reset-password-confirm'),
]
