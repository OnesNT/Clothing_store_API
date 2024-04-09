from django.urls import path
from .views import ProductListCreateAPIView, OrderListCreateAPIView, CustomerListCreateAPIView, CategoryListCreateAPIView


urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('customers/',  CustomerListCreateAPIView.as_view(), name='customer-list-create')
]