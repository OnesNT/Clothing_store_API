from .serializers import ProductSerializer, OrderSerializer, CustomerSerializer, CategorySerializer 
from rest_framework import generics # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from core.models import Product, Order 

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