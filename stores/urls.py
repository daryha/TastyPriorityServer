# stores/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import StoreViewSet, RestaurantViewSet, CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'stores', views.StoreViewSet)
router.register(r'restaurants', views.RestaurantViewSet)
router.register(r'category', views.CategoryViewSet,  basename='category')
router.register(r'products', views.ProductViewSet, basename='product')


urlpatterns = [
    path('', include(router.urls)),
]
