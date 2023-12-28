from rest_framework import serializers
from .models import Store, Restaurant, Category, Product

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  

    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'



from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'city', 'phone_num', 'postal_code', 'order_items', 'total_price']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        
        total_price = 0
        for item_data in order_items_data:
            item = OrderItem.objects.create(order=order, **item_data)
            total_price += item.price * item.quantity
        
        order.total_price = total_price
        order.save()
        return order
