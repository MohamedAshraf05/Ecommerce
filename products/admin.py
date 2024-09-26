from django.contrib import admin
from .models import Products , Category , Cart , CartItem
# Register your models here.

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'category' , 'stock' , 'id')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name' , 'slug' , 'id')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user' , 'created_at' , 'id')
    

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart' , 'product' , 'quantity' , 'id')