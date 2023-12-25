from django.contrib import admin
from .models import Store, Restaurant, Category, Product

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
