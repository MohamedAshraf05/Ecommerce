# views of Products Application
from .utils import AuthenticateUser
from django.db.models import Q
from rest_framework.exceptions import AuthenticationFailed
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets ,status
from .models import Products , Category , Cart , CartItem
from .serializers import ProductSerializer , CategorySerializers , CartItemSerializer , CartSerializer



class ProductApiView(APIView):
    def get(self , request):
        products = Products.objects.all()
        serializer = ProductSerializer(products , many=True)
        return Response(serializer.data)
    

class LatestProductlist(APIView):
    def get(self , request , format=None):
        products = Products.objects.all()[0:5]
        serializer = ProductSerializer(products , many=True)
        return Response(serializer.data)
    

class ProductDetail(APIView):
    def get_object(self , product_slug , category_slug):
        try:
           return Products.objects.all().filter(category__slug=category_slug).get(slug=product_slug)
        except Products.DoesNotExist:
            raise Http404
        
    def get(self , request , product_slug , category_slug , format=None):
        products = self.get_object(product_slug , category_slug)
        serializer = ProductSerializer(products)
        return Response(serializer.data)
    

class CategoryDetail(APIView):
    def get_object(self , category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
        
    def get(self , request , category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializers(category)
        return Response(serializer.data)
    


class SearchView(APIView):
    def post(self , request):
        query = request.data.get('query' , '')    
        if query:
            products = Products.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__name__icontains=query)|
                Q(category__slug__icontains=query)|
                Q(price__icontains=query) |
                Q(slug__icontains=query)
            )
            serializer = ProductSerializer(products , many=True)
            return Response(serializer.data)
        else:
            return Response({'products': []})
        



class CartAPIView(APIView):
    
    def dispatch(self, *args, **kwargs):
        print(f"Request method: {self.request.method}")  # Debugging line to check if the request is coming through
        return super().dispatch(*args, **kwargs)
    

    def get_cart(self, request):
        
        user = AuthenticateUser(request)
        cart, created = Cart.objects.get_or_create(user=user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def get(self, request):
        """Retrieve the entire cart for the authenticated user."""
        return self.get_cart(request)

    def post(self, request):
        """Add an item to the cart and retrieve the entire cart."""
        # Adding an item to the cart for authenticated users only
        user = AuthenticateUser(request)
        product_slug = request.data.get('slug')
        quantity = request.data.get('quantity', 1)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                print(quantity)
                return Response({"error": "Quantity must be a positive integer"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Quantity must be an integer"}, status=status.HTTP_400_BAD_REQUEST)


        product = get_object_or_404(Products, slug=product_slug)
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = int(quantity)
        if cart_item.quantity > product.stock:
            return Response({
                "error": "Not enough stock available for this product",
            },status=status.HTTP_400_BAD_REQUEST)
        product.stock -= cart_item.quantity
        print(f"product stock after adding to the cart : {product.stock}")
        product.save()
        cart_item.save()

        return Response({
            "cart_item": CartItemSerializer(cart_item).data,
        }, status=status.HTTP_200_OK)

    def put(self, request, product_slug):
        """Edit an item in the cart and retrieve the entire cart."""

        user = AuthenticateUser(request)
        quantity = request.data.get('quantity')
        product = request.data.get('product_name')

        if not quantity:
            return Response({"error": "Quantity is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        product = get_object_or_404(Products, slug=product_slug)
        cart = get_object_or_404(Cart, user=user)

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.quantity = int(quantity)
        cart_item.save()

        # Return both the edited item and the entire cart

        return Response({
            "cart_item": CartItemSerializer(cart_item).data,
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, product_slug):

        user = AuthenticateUser(request)
        product = get_object_or_404(Products, slug=product_slug)
        cart = get_object_or_404(Cart, user=user)
        print(f"Attempting to delete product with slug: {product_slug}")
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            print(f"quantity : {cart_item.quantity} ")
            print(f"stock : {product.stock}")
            product.stock += cart_item.quantity
            product.save()
            print(f"new quantity : {cart_item.quantity} ")
            print(f"new stock : {product.stock}")
            cart_item.delete()
            return Response({
                "message": "Item removed from cart",
            },status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)