from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.templatetags.static import static

class Size(models.Model):
    name = models.CharField(max_length=50)  # Small, Medium, Large
    price_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    
    def __str__(self):
        return self.name

class Topping(models.Model):
    name = models.CharField(max_length=100)
    
    # Base price for small size - will be multiplied by size.price_multiplier
    small_price = models.DecimalField(max_digits=5, decimal_places=2)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_price_for_size(self, size):
        """Calculate topping price based on the pizza size"""
        if isinstance(size, str):
            # If we get a string (size name), find the actual size object
            try:
                size_obj = Size.objects.get(name__iexact=size)
                return self.small_price * size_obj.price_multiplier
            except Size.DoesNotExist:
                return self.small_price
        else:
            # If we already have a Size object
            return self.small_price * size.price_multiplier

class Pizza(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='pizza_images/', blank=True, null=True)
    base_price = models.DecimalField(max_digits=6, decimal_places=2)  # Base price for small size
    available = models.BooleanField(default=True)
    
    # Many-to-many relationship with toppings that can be added to this pizza
    available_toppings = models.ManyToManyField(Topping, blank=True, related_name='available_on_pizzas')
    
    def __str__(self):
        return self.name
    
    def get_price_for_size(self, size):
        """Calculate pizza price based on size"""
        if isinstance(size, str):
            try:
                size_obj = Size.objects.get(name__iexact=size)
                return self.base_price * size_obj.price_multiplier
            except Size.DoesNotExist:
                return self.base_price
        else:
            return self.base_price * size.price_multiplier
    
    @property
    def image_url(self):
        """Return the URL for the pizza image, defaulting to a placeholder if none exists"""
        default_image_urls = {
            'Margherita': 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1169&q=80',
            'Pepperoni': 'https://images.unsplash.com/photo-1628840042765-356cda07504e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1780&q=80',
            'Vegetarian': 'https://images.unsplash.com/photo-1604917877934-07d8d248d396?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1171&q=80',
            'Supreme': 'https://images.unsplash.com/photo-1590947132387-155cc02f3212?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
        }
        
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        
        # Return default image based on pizza name, or a generic pizza image
        return default_image_urls.get(self.name, 'https://images.unsplash.com/photo-1513104890138-7c749659a591?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80')

class Drink(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    size = models.CharField(max_length=50)  # Small, Medium, Large
    image = models.ImageField(upload_to='drink_images/', blank=True, null=True)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.size}"
    
    @property
    def image_url(self):
        """Return the URL for the drink image, defaulting to a placeholder if none exists"""
        default_image_urls = {
            'Coca-Cola': 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
            'Sprite': 'https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80',
            'Fanta': 'https://images.unsplash.com/photo-1624552184280-9e9631bbeee9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80',
            'Water': 'https://images.unsplash.com/photo-1615114814213-a245ffc79e9a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80',
        }
        
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        
        # Try to find a matching drink name (case insensitive)
        for drink_name, url in default_image_urls.items():
            if drink_name.lower() in self.name.lower():
                return url
        
        # Default generic drink image
        return 'https://images.unsplash.com/photo-1527281400683-1aefee6bfcbf?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('on_delivery', 'On Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.date_ordered.strftime('%Y-%m-%d %H:%M')}"

class OrderItem(models.Model):
    ITEM_TYPES = [
        ('pizza', 'Pizza'),
        ('drink', 'Drink'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)
    pizza = models.ForeignKey(Pizza, on_delete=models.SET_NULL, null=True, blank=True)
    pizza_size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    drink = models.ForeignKey(Drink, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=8, decimal_places=2)  # Price at time of order
    
    def __str__(self):
        if self.item_type == 'pizza':
            return f"{self.quantity} x {self.pizza.name} ({self.pizza_size.name})"
        else:
            return f"{self.quantity} x {self.drink.name}"

class OrderItemTopping(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='toppings')
    topping = models.ForeignKey(Topping, on_delete=models.SET_NULL, null=True)
    topping_price = models.DecimalField(max_digits=5, decimal_places=2)  # Price at time of order
    
    def __str__(self):
        return f"{self.topping.name if self.topping else 'Unknown topping'}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Cart"
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    ITEM_TYPES = [
        ('pizza', 'Pizza'),
        ('drink', 'Drink'),
    ]
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=True, blank=True)
    pizza_size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        if self.item_type == 'pizza':
            return f"{self.quantity} x {self.pizza.name} ({self.pizza_size.name})"
        else:
            return f"{self.quantity} x {self.drink.name}"
    
    @property
    def item_price(self):
        if self.item_type == 'pizza':
            base_price = self.pizza.get_price_for_size(self.pizza_size)
            topping_price = sum(item.topping.get_price_for_size(self.pizza_size) 
                               for item in self.toppings.all())
            return base_price + topping_price
        else:
            return self.drink.price
    
    @property
    def total_price(self):
        return self.item_price * self.quantity

class CartItemTopping(models.Model):
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='toppings')
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.topping.name
