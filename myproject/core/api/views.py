from django.http import HttpResponse
from .serializers import ProductSerializer, OrderSerializer, CustomerSerializer, CategorySerializer 
from rest_framework import generics # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from core.models import Product, Order, Category
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import api_view # type: ignore 
from django.shortcuts import get_object_or_404
from rest_framework import status # type: ignore
import os
from myproject import settings 

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CustomerSerializer


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class =  CategorySerializer


@api_view(['GET'])
def get_product_ID(request, id):
    product = get_object_or_404(Product, id=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def get_image_ID(request, id):
    product = get_object_or_404(Product, id)
    image = product.image
    image_path = os.path.join(settings.MEDIA_ROOT, image.image.name)
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()

        content_type = 'image/jpeg' 
        return HttpResponse(image_data, content_type=content_type)
    
    except Exception as e:
        return HttpResponse(status=404)


@api_view(['GET'])
def get_all_products_by_category(request, category, left=-1, right=-1):
    category_obj = get_object_or_404(Category, cate_name_eng=category)
    if not (left >= 0 or right >= 0 ): 
         products = Product.objects.filter(category=category_obj)
    else:
        products = Product.objects.filter(category=category_obj)[left:right]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


processed_orders = set() 

@api_view(['POST'])
def update_product_limit(request, orderID):
    if orderID in processed_orders:
        return Response({'message': 'This order has already been processed'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        order = Order.objects.get(id_order=orderID)
        quantity = order.quantity
        product = order.product
        
        if product.limit - quantity >= 0:
            product.limit -= quantity
            processed_orders.add(orderID) 
            product.save()
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
             return Response({'error': 'The quantity you ordered exceeds the quantity in stock.'}, status=status.HTTP_400_BAD_REQUEST)
    
    except Product.DoesNotExist:
        return Response({'error': 'order not found'}, status=status.HTTP_404_NOT_FOUND)
    

