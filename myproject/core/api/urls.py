from django.urls import path
from .views import  (ProductListCreateAPIView,
                    OrderListCreateAPIView,
                    CustomerListCreateAPIView,
                    CategoryListCreateAPIView,
                    get_product_ID,
                    get_all_products_by_category,
                    update_product_limit,
                    get_image_ID)

urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:id>/', get_product_ID, name='get-products-by-ID'), 
    path('products/category/<str:category>/', get_all_products_by_category, name='get-products-by-category'),
    path('products/categoryIndex/<str:category>/<int:left>/<int:right>/', get_all_products_by_category, name='get-products-by-category-index'),
    path('products/image/<int:id>',get_image_ID, name='get-image'),
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('customers/', CustomerListCreateAPIView.as_view(), name='customer-list-create'), 
    path('products/update_limit/<int:orderID>/', update_product_limit,name='update-limit')
]
