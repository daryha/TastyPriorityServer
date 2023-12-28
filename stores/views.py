from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializers import CartSerializer
from rest_framework.response import Response
from .models import Cart, CartItem, Store, Restaurant, Category, Product
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import JsonResponse
from .models import Cart, Order, OrderItem
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem, Product
from django.conf import settings
from django.shortcuts import get_object_or_404
from .serializers import OrderSerializer



from .serializers import StoreSerializer, RestaurantSerializer, CategorySerializer, ProductSerializer, OrderItemSerializer

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    lookup_field = 'slug'

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        store_slug = self.request.query_params.get('store_slug', None)
        if store_slug is not None:
            queryset = queryset.filter(store__slug=store_slug)
        return queryset

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        store_slug = self.request.query_params.get('store_slug', None)
        if store_slug is not None:
            queryset = queryset.filter(store__slug=store_slug)
        return queryset


class AddToCartView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):  # Ensure this matches the URL parameter
        # No need to check if user is authenticated again since you're using the IsAuthenticated permission
        try:
            cart = request.user.cart  # Get the cart associated with the current user

            # Check if the product with the given 'product_id' exists
            product = Product.objects.get(pk=product_id)  # Use pk or id, but ensure it's product_id from the method's parameter

            # Check if the product is already in the user's cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            # Increase the quantity of the product in the cart if it already exists
            if not created:
                cart_item.quantity += 1
                cart_item.save()

            return Response({'message': 'Product successfully added to cart'}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            # Cart does not exist for this user, create it
            cart = Cart.objects.create(user=request.user)

            # Now that you have a cart, add the product to it
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if not created:
                cart_item.quantity += 1
                cart_item.save()

            return Response({'message': 'Product successfully added to cart'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            # Product does not exist
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, product_id):
        try:
            cart = request.user.cart
            product = Product.objects.get(pk=product_id)
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
            return Response({'message': 'Product removed from cart'}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Product not in cart'}, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)




class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({'error': 'Корзина не найдена'}, status=status.HTTP_404_NOT_FOUND)





class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, cart_item_id):
        try:
            # Убедитесь, что используете правильное имя поля для пользователя
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Элемент корзины не найден'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order_view(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save(user=request.user)
        return Response({'status': 'success', 'order_id': order.id}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)