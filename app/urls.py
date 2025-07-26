from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Cart functionality
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    
    # Checkout and orders
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<uuid:order_id>/', views.order_success, name='order_success'),
    path('order-history/', views.order_history, name='order_history'),
    
    # Payment
    path('payment/esewa/<uuid:order_id>/', views.esewa_payment, name='esewa_payment'),
    path('payment/esewa/success/', views.esewa_success, name='esewa_success'),
    path('payment/esewa/failure/', views.esewa_failure, name='esewa_failure'),
]