from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem, Store, Restaurant, Category, Product 
from rest_framework.views import APIView


from .serializers import StoreSerializer, RestaurantSerializer, CategorySerializer, ProductSerializer

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
    def post(self, request, id):
        if request.user.is_authenticated:
            try:
                cart = request.user.cart  # Получите объект корзины, связанный с текущим пользователем

                # Проверьте, существует ли товар с указанным 'id'
                try:
                    product = Product.objects.get(id=id)
                except Product.DoesNotExist:
                    return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

                # Проверьте, существует ли уже такой товар в корзине пользователя
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

                # Увеличьте количество товара в корзине, если он уже существует
                if not created:
                    cart_item.quantity += 1
                    cart_item.save()

                return Response({'message': 'Товар успешно добавлен в корзину'}, status=status.HTTP_200_OK)
            except Cart.DoesNotExist:
                # Корзина не существует для данного пользователя, создайте ее
                cart = Cart(user=request.user)
                cart.save()

                # Теперь, когда у вас есть корзина, добавьте в нее товар
                try:
                    product = Product.objects.get(id=id)
                except Product.DoesNotExist:
                    return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

                # Увеличьте количество товара в корзине, если он уже существует
                if not created:
                    cart_item.quantity += 1
                    cart_item.save()

                return Response({'message': 'Товар успешно добавлен в корзину'}, status=status.HTTP_200_OK)
        else:
            # Пользователь не аутентифицирован
            return Response({'error': 'Вы не авторизованы'}, status=status.HTTP_401_UNAUTHORIZED)
