from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import StoreViewSet, RestaurantViewSet, CategoryViewSet, ProductViewSet
from .views import AddToCartView  # Импортируйте ваше представление AddToCartView

router = DefaultRouter()
router.register(r'stores', views.StoreViewSet)
router.register(r'restaurants', views.RestaurantViewSet)
router.register(r'category', views.CategoryViewSet,  basename='category')
router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    
    # Добавьте URL для вашего представления AddToCartView
    path('api/cart/add/<int:id>/', AddToCartView.as_view(), name='add-to-cart'),

    # Другие URL, если есть
]
