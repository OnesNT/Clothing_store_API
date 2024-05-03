from django.urls import path
from . import views

urlpatterns = [
    # GET request APIs
    #----------------------------------------------------------------------------------------
    # get products
    path('api/products/', views.get_all_product, name='get_all_product'),
    path('api/products/id/<str:id>/', views.get_product_ID, name='get_product_ID'),
    path('api/products_sku/<str:id>/', views.get_product_sku_ID, name='get_product_sku_ID'),
    path('api/products_by_category/<str:en_category>/', views.get_products_by_category, name='get_products_by_category'),
    path('api/product_sku_details/<str:id>/', views.get_product_sku_details, name='get_product_sku_details'),
    
    # get product properties
    path('api/products/<str:name_product>/<str:size>/<str:color>/properties/', views.get_product_properties, name='get_product_size_and_color'),
    path('api/products/<str:name_product>/<str:color>/property_color/', views.get_product_properties, name='get_product_color'),
    path('api/products/<str:name_product>/<str:size>/property_size/', views.get_product_properties, name='get_product_size'),
    path('api/products/<str:name_product>/properties/', views.get_product_properties, name='get_product_properties'),




]
