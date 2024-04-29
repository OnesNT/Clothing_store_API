from django.urls import path
from . import views

urlpatterns = [
    # GET request APIs
    #----------------------------------------------------------------------------------------
    # get products
    path('api/products/', views.get_all_product, name='get_all_product'),
    path('api/products/id/<str:id>/', views.get_product_ID, name='get_product_ID'),
    path('api/products/name_product/<str:name_product>/', views.get_product_name, name='get_product_name'),
    # path('api/products/<str:name_product>/images/', views.get_image_product, name='get_image_product'),
    path('api/products-by-category/<str:ru_category>/', views.get_products_by_category, name='get_products_by_category'),

    # get product properties
    # path('api/products/<str:name_product>/<str:size>/<str:color>/properties/', views.get_product_properties, name='get_product_size_and_color'),
    # path('api/products/<str:name_product>/<str:color>/property_color/', views.get_product_properties, name='get_product_color'),
    # path('api/products/<str:name_product>/<str:size>/property_size/', views.get_product_properties, name='get_product_size'),
    path('api/get_product_id_properties/<str:product_id>/', views.get_product_id_properties, name='get_product_id_properties'),
    path('api/get_relate_product_id/<str:product_id>/', views.get_relate_productID, name='get_relate_product_id'),
    path('api/merge-product-productSKU/<str:id>', views.merge_product_productSKU, name='merge-product-productSKU'),

    # get shopping-sessions
    path('api/shopping-sessions/', views.get_all_shopping_sessions, name='get_all_shopping_sessions'),
    path('api/shopping-sessions/<int:session_id>/', views.get_shopping_session_details, name='get_shopping_session_details'),

    # get order
    path('api/orders/', views.get_all_order_user, name='get_all_orders_user'),
    path('api/orders/<int:order_id>/', views.get_order_user_details, name='get_order_user_details'),


    path('api/view_cart/', views.view_cart, name='view_cart'),


    #----------------------------------------------------------------------------------------
    # POST request APIs
    path ('api/add_to_cart/<str:product_sku_id>', views.add_to_cart, name='add_to_cart'),
    path('api/create-shopping-session/', views.create_shopping_session, name='create_shopping_session'),
    path('api/create-cart', views.create_cart, name='create_cart'),
    path('api/create-order/<int:session_id>', views.create_order, name='create_order'),
    


    #----------------------------------------------------------------------------------------
    # Update and delete APIs
    path('api/update-order/<int:order_id>/', views.update_order, name='update_order'),
    path('api/delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('api/update-cart-item/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),
    path('api/delete-cart-item/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),

]