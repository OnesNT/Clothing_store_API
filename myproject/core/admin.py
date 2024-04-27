from django.contrib import admin
from .models import Category, Product, ProductSize, ProductColor, ProductSKU, ShoppingSession, Cart, CartItem, OrderDetails, OrderItem


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductSize)
admin.site.register(ProductColor)
admin.site.register(ProductSKU)
admin.site.register(ShoppingSession)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderDetails)
admin.site.register(OrderItem)
