from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class Category(models.Model):
    en_name = models.CharField(primary_key=True, max_length=255, default='')
    ru_name = models.CharField(max_length=255, default='')
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=255, default='', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)


class ProductSize(models.Model):
    value = models.CharField(primary_key=True, max_length=255, default='')
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

class ProductColor(models.Model):
    en_value = models.CharField(primary_key=True, max_length=255, default='')
    ru_value = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

class ProductGroup(models.Model):
    id = models.CharField(primary_key=True, max_length=255, default='')
    description = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255, default='')
    img_base = models.CharField(max_length=255, default='', blank=True)
    img_hover = models.CharField(max_length=255, default='', blank=True)
    img_details_1 = models.CharField(max_length=255, default='', blank=True)
    img_details_2 = models.CharField(max_length=255, default='', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color_attribute = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)
    tag = models.CharField(max_length=255, default='', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)


class ProductSKU(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size_attribute = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

class ShoppingSession(models.Model):
    id = models.AutoField(primary_key=True)
    session_key = models.CharField(blank=True, max_length=255)
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
