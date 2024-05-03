from django.http import HttpResponse
from rest_framework import generics # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from core.models import Category, Product, ProductSize, ProductColor, ProductSKU, ShoppingSession, Cart, CartItem, OrderDetails, OrderItem
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import api_view # type: ignore 
from django.shortcuts import get_object_or_404
from rest_framework import status # type: ignore
from myproject import settings 
from rest_framework.generics import RetrieveAPIView # type: ignore
from django.db.models import Q
from django.http import Http404
from rest_framework.views import APIView # type: ignore
from django.contrib.auth.models import User
from rest_framework.decorators import api_view # type: ignore
from rest_framework import permissions # type: ignore
from rest_framework.authentication import TokenAuthentication # type: ignore
from rest_framework.authtoken.models import Token # type: ignore
from django.http import JsonResponse

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


@api_view(['DELETE'])
def delete_productSKU_cart(request, product_sku_id):
    session_key = request.session.session_key

    shopping_session = get_object_or_404(ShoppingSession, session_key=session_key)
    cart = get_object_or_404(Cart, shopping_session=shopping_session)
    
    product_sku = get_object_or_404(ProductSKU, id=product_sku_id)
    product = product_sku.product

    cart_item = get_object_or_404(CartItem, cart=cart, product_sku=product_sku, product=product)
    cart_item.delete()

    return Response({'message': 'Product SKU deleted from cart successfully'})


@api_view(['GET'])
def view_cart(request):
    properties = []

    session_key = request.session.session_key

    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    shopping_session = get_object_or_404(ShoppingSession, session_key=session_key)
    cart = get_object_or_404(Cart, shopping_session=shopping_session)

    cartItems = CartItem.objects.filter(cart=cart)

    for cartItem in cartItems: 
        productSKU = get_object_or_404(ProductSKU, cartitem=cartItem)
        product = productSKU.product
        properties.append({
            "id" : cartItem.id,
            "imageSrc": product.img_base,
            "productName": product.name,
            "unitPrice": productSKU.price,
            "quantity": cartItem.quantity,
        })
    
    return Response(properties)

@api_view(['PUT'])
def modify_quantities_cartitem(request, product_sku_id, quantity):
    session_key = request.session.session_key

    shopping_session = get_object_or_404(ShoppingSession, session_key=session_key)
    cart = get_object_or_404(Cart, shopping_session=shopping_session)
    product_sku = ProductSKU.objects.filter(id=product_sku_id)

    cartitem = get_object_or_404(CartItem, cart=cart, product_sku=product_sku_id)
    cartitem.quantity = quantity
    cartitem.save()

    return Response({'message': "Cart item's quantities modified successfully"})

@api_view(['POST'])
def you_click_buy(request, total_price, user_name, phone, locate):
    session_key = request.session.session_key

    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    shopping_session = get_object_or_404(ShoppingSession, session_key=session_key)

    orderDetails, created = OrderDetails.objects.get_or_create(shopping_session=shopping_session)

    cart = get_object_or_404(Cart, shopping_session=shopping_session)
    cartItem = CartItem.objects.filter(cart=cart)
    productSKU = cartItem.product_skU

    productSKU.quantity -= cartItem.quantity
    orderDetails.total = int(total_price)
    orderDetails.user_name = user_name
    orderDetails.phone = phone
    orderDetails.locate = locate

    orderDetails.save()
    productSKU.save()

    return Response({'message': "Create order details successfully"})



@api_view(['GET'])
def what_you_buy(request):
    session_key = request.session.session_key
    user_information = {}

    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    shopping_session = get_object_or_404(ShoppingSession, session_key=session_key)
    order_details = get_object_or_404(OrderDetails, shopping_session=shopping_session)
    cart = get_object_or_404(Cart, shopping_session=shopping_session)
    cart_items = CartItem.objects.filter(cart=cart)

    user_information.update({ 
        "user_name": order_details.user_name, 
        "phone": order_details.phone, 
        "locate": order_details.locate,
        "total_price": order_details.total,
    })

    properties = []
    for cart_item in cart_items:
        product_sku = cart_item.product_sku
        quantity = cart_item.quantity
        properties.append({ 
            "product": product_sku.product.name, 
            "size": product_sku.size_attribute.value,
            "color": product_sku.product.color_attribute.en_value,
            "quantity": quantity,
        })

    user_information["properties"] = properties

    return Response(user_information)

