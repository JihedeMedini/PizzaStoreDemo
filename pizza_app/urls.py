from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='pizza_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Menu and product pages
    path('menu/', views.menu, name='menu'),
    path('pizza/<int:pizza_id>/', views.pizza_detail, name='pizza_detail'),
    path('drink/<int:drink_id>/add/', views.add_drink_to_cart, name='add_drink_to_cart'),
    path('suggest-drinks/<int:pizza_id>/', views.suggest_drinks, name='suggest_drinks'),
    
    # Cart and checkout
    path('cart/', views.cart, name='cart'),
    path('cart/remove/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<str:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Orders
    path('order/confirmation/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.order_history, name='order_history'),
    path('order/<str:order_id>/', views.order_detail, name='order_detail'),
    path('order/<str:order_id>/cancel/', views.cancel_order, name='cancel_order'),
] 