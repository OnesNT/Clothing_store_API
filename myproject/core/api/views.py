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
from django.http import JsonResponse

# GET request API 
# ------------------------------------------------------------------------------------------------------------------------------


# get product 
@api_view(['GET'])
def get_all_product(request):
    products = Product.objects.all() 
    all_products = []
    for product in products:
        relate_products = Product.objects.filter(group=product.group).exclude(id=product.id)
        list_color = []
        data = []
        queryset = [product] + list(relate_products)
        for relate_product in queryset: 
            id = relate_product.id
            relate_product_sku = ProductSKU.objects.filter(product=relate_product).first()
            color = relate_product.color_attribute
            
            list_color.append({'id': relate_product_sku.id, 'color': color.en_value, 'colorName': color.ru_value})
            productSKU = ProductSKU.objects.filter(product=relate_product).first()
            data.append({
                "id": id,
                "color": str(color.en_value), 
                "id_sku": productSKU.id,
            })
        properties = { 
            "id": product.id,
            "id_sku" : ProductSKU.objects.filter(product=product).first().id,
            "name": product.name,
            "price": str(productSKU.price), 
            "img_base": product.img_base,
            "img_hover": product.img_hover,
            "product_relate": data,
            "color": list_color,
            "category": product.category.en_name,
            "tag": product.tag,
        }
        all_products.append(properties)

    return Response(all_products)

@api_view(['GET'])
def get_product_ID(request, id):
    product = get_object_or_404(Product, id=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def get_product_sku_ID(request, id):
    product = get_object_or_404(ProductSKU, id=id)
    serializer = ProductSKUSerializer(product)
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
def get_products_by_category(request, en_category):
    def get_products(category):
        products = Product.objects.filter(category=category)
        child_categories = Category.objects.filter(parent_category=category)
        for child_category in child_categories:
            products |= get_products(child_category)
        return products

    try:
        category = Category.objects.get(en_name=en_category)
        products = get_products(category)
        all_products = []
        for product in products:
            relate_products = Product.objects.filter(group=product.group).exclude(id=product.id)
            list_color = []
            data = []
            queryset = [product] + list(relate_products)
            for relate_product in queryset: 
                id = relate_product.id
                relate_product_sku = ProductSKU.objects.filter(product=relate_product).first()
                color = relate_product.color_attribute
                
                list_color.append({'id': relate_product_sku.id, 'color': color.en_value, 'colorName': color.ru_value})
                productSKU = ProductSKU.objects.filter(product=relate_product).first()
                data.append({
                    "id": id,
                    "color": str(color.en_value), 
                    "id_sku": productSKU.id,
                })
            properties = { 
                "id": product.id,
                "id_sku" : ProductSKU.objects.filter(product=product).first().id,
                "name": product.name,
                "price": str(productSKU.price), 
                "img_base": product.img_base,
                "img_hover": product.img_hover,
                "product_relate": data,
                "color": list_color,
                "category": product.category.en_name,
                "tag": product.tag,
            }
            all_products.append(properties)

        return Response(all_products)  
        # serializer = ProductSerializer(products, many=True)
        # return Response(serializer.data)
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

# get product sku detail
@api_view(['GET'])
def get_product_sku_details(request, id):
    product_sku = get_object_or_404(ProductSKU, id=id)
    # serializer = ProductSKUSerializer(product_sku)
    product = product_sku.product
    products_by_group_id = Product.objects.filter(group=product.group.id)
    other_products = []
    for item in products_by_group_id:
        # if item.id != product.id:
        new_product = {
            'id': item.id,
            'ru_color': item.color_attribute.ru_value,
            'en_color': item.color_attribute.en_value
        }
        other_products.append(new_product)

    
    all_product_skus = []
    all_colors = []
    for product_item in products_by_group_id:
        product_skus_by_product_id = ProductSKU.objects.filter(product=product_item)
        product_color_ru = product_item.color_attribute.ru_value
        product_color_en = product_item.color_attribute.en_value
        color_item = {'en_color': product_color_en, 'ru_color': product_color_ru}
        if color_item not in all_colors:
            all_colors.append(color_item)
        for item in product_skus_by_product_id:
            found_product_sku = {
                "id": item.id,
                "ru_color": product_item.color_attribute.ru_value,
                "color": product_item.color_attribute.en_value,
                "size": item.size_attribute.value,
                "status": "ok"
            }
            all_product_skus.append(found_product_sku)

    product_sku_details = {
        'id': product_sku.id,
        'price': product_sku.price,
        'size': product_sku.size_attribute.value,
        'quantity': product_sku.quantity,
        'product_id': product.id,
        'name': product.name,
        'img_base': product.img_base,
        'img_hover': product.img_hover,
        'img_details_1': product.img_details_1,
        'img_details_2': product.img_details_2,
        'ru_category': product.category.ru_name,
        'en_category': product.category.en_name,
        'ru_color': product.color_attribute.ru_value,
        'en_color': product.color_attribute.en_value,
        'status': "ok",
        'group_id': product.group.id,
        'description': product.group.description,
        # 'other_products': other_products,
        'all_product_skus': all_product_skus,
        'all_colors': all_colors
    }
    return Response(product_sku_details)
    # return Response(serializer.data)

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
def view_cart_from_db(request):
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
            "quantity": productSKU.quantity,
        })
    
    return Response(properties)

@api_view(['PUT'])
def modify_quantities_cartitem(request, cartitem_id, quantity):
    quantity = int(quantity)
    session_key = request.session.session_key

    shopping_session = get_object_or_404(ShoppingSession, session_key=session_key)
    cart = get_object_or_404(Cart, shopping_session=shopping_session)

    cartitem = get_object_or_404(CartItem, cart=cart, id=cartitem_id)
    cartitem.quantity = quantity

    cartitem.save()

    return Response({'message': "Cart item's quantities modified successfully"})

