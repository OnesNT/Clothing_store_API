from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='', blank=True)
    base_picture = models.CharField(max_length=255, default='', blank=True)
    picture_1 = models.CharField(max_length=255, default='', blank=True)
    picture_2 = models.CharField(max_length=255, default='', blank=True)
    picture_3 = models.CharField(max_length=255, default='', blank=True)
    picture_4 = models.CharField(max_length=255, default='', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

class ProductSize(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

class ProductColor(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

class ProductSKU(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size_attribute = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    color_attribute = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

class ShoppingSession(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    shopping_session = models.ForeignKey(ShoppingSession, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_sku = models.ForeignKey(ProductSKU, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    shopping_session = models.ForeignKey(ShoppingSession, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    user_name = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=255, default='')
    locate = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(OrderDetails, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_sku = models.ForeignKey(ProductSKU, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)
