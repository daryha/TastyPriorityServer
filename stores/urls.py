# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views
from .views import create_order_view

router = DefaultRouter()
router.register(r'stores', views.StoreViewSet)
router.register(r'restaurants', views.RestaurantViewSet)
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('cart/add/<int:product_id>/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:cart_item_id>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/', views.CartDetailView.as_view(), name='cart-detail'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('create-order/', create_order_view, name='create_order'),
    # Другие URL-конфигурации, если они есть
]
