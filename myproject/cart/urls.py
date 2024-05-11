from django.urls import path
from . import views

urlpatterns= [
    # GET request
    path('api/view_cart', views.view_cart, name='view_cart'),
    path('api/what_you_buy', views.what_you_buy, name='what_you_buy'),
    
    # POST request
    path('api/add_to_cart/<str:product_sku_id>', views.add_to_cart, name='add_to_cart'),
    path('api/you_click_buy/<int:total_price>/<str:user_name>/<str:phone>/<str:locate>/', views.you_click_buy, name='create_orderDetails'),

    # DELETE request
    path('api/delete_productSKU_cart/<str:product_sku_id>', views.delete_productSKU_cart, name='product_sku_id'),

    # PUT request 
    path('api/modify_quantities_cartitem/<int:cartitem_id>/<int:quantity>', views.modify_quantities_cartitem, name='modify_quantities_cartitem'),
]