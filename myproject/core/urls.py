from django.urls import path
from core import views 


app_name = "core"

urlpatterns = [
    path('core/', views.index, name='core'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.product_list, name='products'),
    # path('logout/', views.as_view(), name='logout'),
    # path('product/<int:pk>/', views.product_detail, name='product_detail'),
    # path('api/products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    # path('api/orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
]