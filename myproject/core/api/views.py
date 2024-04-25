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

@api_view(['GET'])
def get_image_product(request, name_product):
    product = get_object_or_404(Product, name=name_product)
    images = [product.picture_1, product.picture_2, product.picture_3, product.picture_4]
    return Response(images)    

@api_view(['GET'])
def get_products_by_category(request, category_id):

    def get_products(category):
        products = Product.objects.filter(category=category)
        for product in products:
            print(product.name, ' ', product.category)
        child_categories = Category.objects.filter(parent_category=category)
        for child_category in child_categories:
            products |= get_products(child_category)
        return products

    try:
        category = Category.objects.get(id=category_id)
        products = get_products(category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response({"error": "Category does not exist"}, status=404)


# get product properties

@api_view(['GET'])
def get_product_properties(request, name_product, size=0, color=''):
    product = get_object_or_404(Product, name=name_product)
    properties = {
        'name': product.name,
        'description': product.description,
        'base_picture': product.base_picture,
        'category': product.category.name,
    }

    product_skus = product.productsku_set.all()

    if size != 0:
        product_skus = product_skus.filter(size_attribute__value=size)

    if color:
        product_skus = product_skus.filter(color_attribute__value=color)

    # Include available sizes and colors in the response data
    if not (size or color):
        available_sizes = set(product_sku.size_attribute.value for product_sku in product_skus)
        available_colors = set(product_sku.color_attribute.value for product_sku in product_skus)
        properties['available_sizes'] = list(available_sizes)
        properties['available_colors'] = list(available_colors)
    else:
        try:
            product_sku = product_skus.first()  # Get the first product SKU
            properties['price'] = product_sku.price
        except AttributeError:
            properties['price'] = None  # No product SKU found, set price to None

    return Response(properties)

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
@api_view(['POST'])
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

