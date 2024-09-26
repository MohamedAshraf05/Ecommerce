from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    class Meta:
        model = Products
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'price',
            'image',
            'category',
            'stock',
        ]

class CategorySerializers(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'products',
        ]

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Use ProductSerializer here to get product details
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'email', 'first_name' , 'last_name' ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Use CartItemSerializer to get cart items
    total_price = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(item.get_total_price() for item in obj.items.all())