from django.urls import path
from .views import register, LoginView, user_profile
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # ... другие пути
    path('api/accounts/register/', register, name='register'),
    path('api/accounts/login/', LoginView.as_view(), name='login'),
    path('api/user/profile/', user_profile, name='user_profile'),
]

