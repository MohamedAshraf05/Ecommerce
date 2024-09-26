from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import LatestProductlist , ProductDetail , CategoryDetail , SearchView , CartAPIView , ProductApiView

urlpatterns = [
    path('products/' ,ProductApiView.as_view() , name='products'),
    path('latest-products/' , LatestProductlist.as_view() , name='latest-product'),
    path('products/<slug:category_slug>/<slug:product_slug>/' , ProductDetail.as_view() , name="product_detail_test"),
    path('products/<slug:category_slug>/' , CategoryDetail.as_view() ,name='category-detail'),
    path('product/search/' , SearchView.as_view() , name='search'),
    path('cart/' , CartAPIView.as_view() , name='cart_list'),
    path('cart/edit/<slug:product_slug>/' , CartAPIView.as_view() , name='cart_edit'),
    path('cart/delete/<slug:product_slug>/' , CartAPIView.as_view() , name='cart_delete'),  
]   