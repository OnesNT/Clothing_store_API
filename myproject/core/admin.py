from django.contrib import admin
from .models import Category
from .models import Product
from .models import ProductSize
from .models import ProductColor
from .models import ProductSKU
from .models import ShoppingSession
from .models import Cart
from .models import CartItem
from .models import OrderDetails
from .models import OrderItem

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
