from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from django.contrib.auth.models import User
from .models import (
    Pizza, Size, Topping, Drink, 
    Order, OrderItem, OrderItemTopping,
    Cart, CartItem, CartItemTopping
)

class PizzaParadiseAdminSite(AdminSite):
    site_title = _('Pizza Paradise Admin')
    site_header = _('Pizza Paradise Administration')
    index_title = _('Pizza Paradise Management')
    
    def index(self, request, extra_context=None):
        """Customize the admin index page to include stats."""
        # Get statistics for the dashboard
        extra_context = extra_context or {}
        extra_context['pizzas_count'] = Pizza.objects.filter(available=True).count()
        extra_context['orders_count'] = Order.objects.count()
        extra_context['pending_orders_count'] = Order.objects.filter(status='pending').count()
        extra_context['users_count'] = User.objects.count()
        
        return super().index(request, extra_context)

admin_site = PizzaParadiseAdminSite(name='pizza_admin')

# Inline models
class ToppingInline(admin.TabularInline):
    model = OrderItemTopping
    extra = 0
    
class CartItemToppingInline(admin.TabularInline):
    model = CartItemTopping
    extra = 0

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('item_type', 'pizza', 'pizza_size', 'drink', 'quantity', 'item_price')
    readonly_fields = ('item_price',)
    
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

# Register your models here
@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'available')
    list_filter = ('available',)
    search_fields = ('name', 'description')
    filter_horizontal = ('available_toppings',)
    
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_multiplier')

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('name', 'small_price', 'available')
    list_filter = ('available',)
    search_fields = ('name',)

@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'price', 'available')
    list_filter = ('available', 'size')
    search_fields = ('name', 'description')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_ordered', 'status', 'total_price')
    list_filter = ('status', 'date_ordered')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('total_price',)
    inlines = [OrderItemInline]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item_type', 'get_item_name', 'quantity', 'item_price')
    list_filter = ('item_type',)
    search_fields = ('order__id', 'pizza__name', 'drink__name')
    inlines = [ToppingInline]
    
    def get_item_name(self, obj):
        if obj.item_type == 'pizza':
            return f"{obj.pizza.name} ({obj.pizza_size.name if obj.pizza_size else 'N/A'})"
        else:
            return obj.drink.name if obj.drink else 'N/A'
    get_item_name.short_description = 'Item'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'get_total_price')
    search_fields = ('user__username', 'user__email')
    inlines = [CartItemInline]
    
    def get_total_price(self, obj):
        return obj.total_price
    get_total_price.short_description = 'Total Price'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'item_type', 'get_item_name', 'quantity', 'get_total_price')
    list_filter = ('item_type',)
    search_fields = ('cart__user__username', 'pizza__name', 'drink__name')
    inlines = [CartItemToppingInline]
    
    def get_item_name(self, obj):
        if obj.item_type == 'pizza':
            return f"{obj.pizza.name} ({obj.pizza_size.name if obj.pizza_size else 'N/A'})"
        else:
            return obj.drink.name if obj.drink else 'N/A'
    get_item_name.short_description = 'Item'
    
    def get_total_price(self, obj):
        return obj.total_price
    get_total_price.short_description = 'Total Price'
