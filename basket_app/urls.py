from django.urls import path
from .views import CartDetailView, AddToCartView, RemoveFromCartView, UpdateCartItemView

urlpatterns = [
    # Путь для просмотра содержимого корзины
    path('cart/', CartDetailView.as_view(), name='cart-detail'),

    # Путь для добавления товара в корзину
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),

    # Путь для удаления товара из корзины
    path('cart/remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),

    # Путь для обновления количества товара в корзине
    path('cart/update/<int:product_id>/', UpdateCartItemView.as_view(), name='update-cart-item'),
]
