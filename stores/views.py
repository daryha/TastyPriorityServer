from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Store, Restaurant, Category, Product
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

