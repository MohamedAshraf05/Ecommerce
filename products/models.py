# Models of Products applications


from django.db import models
from users.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=155)
    slug = models.SlugField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/{self.slug}/"
    


class Products(models.Model):
    category = models.ForeignKey(Category , related_name='products' ,on_delete=models.CASCADE)
    name = models.CharField(max_length=155)
    slug = models.SlugField()
    description = models.TextField(blank=True , null=True)
    price = models.DecimalField(max_digits=6 , decimal_places=2)
    image = models.ImageField(upload_to='static/images/' , blank=True , null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/{self.category.slug}/{self.slug}/"
    
    def get_image(self):
        if self.image:
            return "http://127.0.0.1:8000" + self.image.url
        return ""
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price
