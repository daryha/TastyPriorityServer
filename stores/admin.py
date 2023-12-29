from django.contrib import admin
from .models import Store, Restaurant, Category, Product, Order,  OrderItem

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'store', 'restaurant']
    search_fields = ['name']
    list_filter = ['store', 'restaurant']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'store', 'restaurant']
    search_fields = ['name']
    list_filter = ['category', 'store', 'restaurant']



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'address', 'city', 'phone_num', 'postal_code', 'created_at', 'updated_at', 'total_price']
    search_fields = ['user__username', 'first_name', 'last_name', 'address', 'city', 'phone_num']
    list_filter = ['created_at', 'updated_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity']
    search_fields = ['order__user__username', 'product__name']