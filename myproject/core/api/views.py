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
    product = product_sku.product
    products_by_group_id = Product.objects.filter(group=product.group.id)
    other_products = []
    for item in products_by_group_id:
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
        'all_product_skus': all_product_skus,
        'all_colors': all_colors
    }
    return Response(product_sku_details)




