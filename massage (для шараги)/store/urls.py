from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='store'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-multiple-from-cart/', views.remove_multiple_from_cart, name='remove_multiple_from_cart'),
]