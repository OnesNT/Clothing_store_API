from django.http import HttpResponse
from .serializers import ProductSerializer, ProductSizeerializer, ProductColorSerializer, CategorySerializer, ProductSKUSerializer, ShoppingSessionSerializer, CartSerializer, CartItemSerializer, OrderDetailsSerializer, OrderItemSerializer
from rest_framework import generics # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from core.models import Category, Product, ProductSize, ProductColor, ProductSKU, ShoppingSession, Cart, CartItem, OrderDetails, OrderItem
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import api_view # type: ignore 
from django.shortcuts import get_object_or_404
from rest_framework import status # type: ignore
import os
from myproject import settings 
from rest_framework.generics import RetrieveAPIView # type: ignore
from django.db.models import Q
from django.http import Http404
from rest_framework.views import APIView # type: ignore
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes # type: ignore
from rest_framework import permissions # type: ignore
from rest_framework.authentication import TokenAuthentication # type: ignore
from rest_framework.authtoken.models import Token # type: ignore
from django.contrib.sessions.backends.db import SessionStore

# GET request API 
# ------------------------------------------------------------------------------------------------------------------------------


# get product 
@api_view(['GET'])
def get_all_product(request):
    product = Product.objects.all() 
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_product_ID(request, id):
    product = get_object_or_404(Product, id=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def get_product_name(request, name_product):
    product = get_object_or_404(Product, name=name_product)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

# @api_view(['GET'])
# def get_image_product(request, name_product):
#     product = get_object_or_404(Product, name=name_product)
#     images = [product.picture_1, product.picture_2, product.picture_3, product.picture_4]
#     return Response(images)    

@api_view(['GET'])
def get_products_by_category(request, ru_category):

    def get_products(category):
        products = Product.objects.filter(category=category)
        child_categories = Category.objects.filter(parent_category=category)
        for child_category in child_categories:
            products |= get_products(child_category)
        return products

    try:
        category = Category.objects.get(ru_name=ru_category)
        products = get_products(category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response({"error": "Category does not exist"}, status=404)


# get product properties
@api_view(['GET'])
def get_product_id_properties(request, product_id):

    product = Product.objects.filter(id=product_id).first()
    productSKU = ProductSKU.objects.filter(product=product).first()

    relate_products = Product.objects.filter(group=product.group)
    
    list_color = []
    data = []
    for  relate_product in relate_products: 
        id = relate_product.id
        color = relate_product.color_attribute
        list_color.append(color.en_value)
        product = Product.objects.filter(id=id).first()
        productSKU = ProductSKU.objects.filter(product=product).first()
        data.append({
            "id": id,
            "color": str(color.en_value), 
            "id_sku": productSKU.id,
        })

    properties = { 
        "id_ski" : str(productSKU.id), 
        "name": product.name,
        "price": str(productSKU.price), 
        "image_1": product.img_base,
        "image_2": product.img_hover,
        "product_relate": data,
        "color": list_color,
    }
    return Response(properties)



# @api_view(['GET'])
# def get_product_properties(request, name_product, size=0, color=''):
#     product = get_object_or_404(Product, name=name_product)
#     properties = {
#         'name': product.name,
#         'description': product.description,
#         'base_picture': product.base_picture,
#         'category': product.category.name,
#     }

#     product_skus = product.productsku_set.all()

#     if size != 0:
#         product_skus = product_skus.filter(size_attribute__value=size)

#     if color:
#         product_skus = product_skus.filter(color_attribute__value=color)

#     # Include available sizes and colors in the response data
#     if not (size or color):
#         available_sizes = set(product_sku.size_attribute.value for product_sku in product_skus)
#         available_colors = set(product_sku.color_attribute.value for product_sku in product_skus)
#         properties['available_sizes'] = list(available_sizes)
#         properties['available_colors'] = list(available_colors)
#     else:
#         try:
#             product_sku = product_skus.first()  # Get the first product SKU
#             properties['price'] = product_sku.price
#         except AttributeError:
#             properties['price'] = None  # No product SKU found, set price to None

#     return Response(properties)

@api_view(['GET'])
def get_relate_productID(request, product_id):
    if product_id:
        if product_id[-1].isdigit():
            # If the last character is a digit, retrieve the product by its ID
            product = get_object_or_404(Product, id=product_id)
            return Response({product_id: str(product.color_attribute)})
        else:
            # If the last character is not a digit, assume it's a group ID and retrieve related products
            products = Product.objects.filter(group=product_id[0:-1])
            print([product.id for product in products])
            data = {str(product.id): str(product.color_attribute) for product in products}
            return Response(data)
    else:
        return Response({"error": "Product ID is missing"})


@api_view(['GET'])
def merge_product_productSKU(request, id): 
    productSKU = get_object_or_404(ProductSKU, id=id)
    product = productSKU.product

    properties = { 
        "name" : product.name, 
        "color": str(product.color_attribute),
        "size": str(productSKU.size_attribute), 
        "image_base": product.img_base,
        "image_hover": product.img_hover, 
        "image_detail_1": product.img_details_1,
        "image_detail_2":product.img_details_2,
        "category": str(product.category),
        "group": str(product.group),
        "price": str(productSKU.price),
        "quantity": str(productSKU.quantity),  
    }
   
    return Response(properties)


@api_view(['GET'])
def view_cart(request):
    # Retrieve the cart associated with the current session
    session_key = request.session.session_key
    shopping_session = get_object_or_404(ShoppingSession, session_key=session_key)
    cart = get_object_or_404(Cart, shopping_session=shopping_session )

    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)
    else:
        return Response({'message': 'Cart is empty'})
    

# get shopping sessions

@api_view(['GET'])
def get_all_shopping_sessions(request):
    shopping_session = ShoppingSession.objects.all()
    serializer = ShoppingSessionSerializer(shopping_session, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_shopping_session_details(request, session_id):
    shopping_session = get_object_or_404(ShoppingSession, pk=session_id)
    serializer = ShoppingSessionSerializer(shopping_session)
    return Response(serializer.data)

# get order
@api_view(['GET'])
def get_all_order_user(request):
    order = OrderDetails.objects.all()
    serializer = OrderDetailsSerializer(order, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_order_user_details(request, order_id):
    order = get_object_or_404(OrderDetails, pk=order_id)
    serializer = OrderDetailsSerializer(order)
    return Response(serializer.data)


# POST request API
# ------------------------------------------------------------------------------------------------------------------------------

# post shopping sessions
# @api_view(['POST'])
def create_shopping_session(request):
    serializer = ShoppingSessionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_cart(request):
    serializer = CartSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_order(request):
    serializer = OrderDetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# DELETE request API
# ------------------------------------------------------------------------------------------------------------------------------

@api_view(['DELETE'])
def delete_order(request, order_id):
    order = get_object_or_404(OrderDetails, pk=order_id)
    order.delete()
    return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return Response({"message": "Cart item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_shopping_session(request, session_id):
    shoping_session = get_object_or_404(ShoppingSession, pk=session_id)
    shoping_session.delete()
    return Response({"message": "Shoping session item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# others request API

@api_view(['PUT', 'PATCH'])
def update_order(request, order_id):
    order = get_object_or_404(OrderDetails, pk=order_id)
    serializer = OrderDetailsSerializer(order, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'PATCH'])
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def add_to_cart(request, product_id):
#     # Retrieve or create the cart associated with the current session
#     session_key = request.session.session_key
#     cart, _ = Cart.objects.get_or_create(shopping_session=session_key)

#     # Add the product to the cart (create a new cart item)
#     cart_item, _ = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
#     cart_item.quantity += 1
#     cart_item.save()

#     return Response({'message': 'Item added to cart successfully'})



@api_view(['POST'])
def add_to_cart(request, product_sku_id):
    session_key = request.session.session_key

    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    shopping_session, _ = ShoppingSession.objects.get_or_create(session_key=session_key)
    cart, _ = Cart.objects.get_or_create(shopping_session=shopping_session)

    product_sku = get_object_or_404(ProductSKU, id=product_sku_id)
    product = product_sku.product
    
    cart_item, _ = CartItem.objects.get_or_create(cart=cart, product_sku=product_sku, product=product)
    cart_item.quantity += 1
    cart_item.save()

    return Response({'message': 'Item added to cart successfully'})


