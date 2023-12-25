from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics

from .models import Product, Cart, CartItem
from .serializers import CartSerializer

# Представление для просмотра содержимого корзины
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Cart.objects.get_or_create(user=self.request.user)[0]

# Представление для добавления товара в корзину
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return Response({'status': 'success'}, status=status.HTTP_200_OK)

# Представление для удаления товара из корзины
class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        try:
            cart_item = CartItem.objects.get(cart__user=request.user, product_id=product_id)
            cart_item.delete()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'status': 'error', 'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

# Представление для обновления количества товара в корзине
class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, product_id):
        quantity = request.data.get('quantity', 1)
        try:
            quantity = int(quantity)
            cart_item = CartItem.objects.get(cart__user=request.user, product_id=product_id)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                cart_item.delete()
                return Response({'status': 'success', 'message': 'Item removed'}, status=status.HTTP_200_OK)
        except (CartItem.DoesNotExist, ValueError):
            return Response({'status': 'error', 'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
