from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Sum
from .models import (
    Pizza, Size, Topping, Drink, 
    Order, OrderItem, OrderItemTopping,
    Cart, CartItem, CartItemTopping
)
from .forms import UserRegistrationForm, PizzaSelectionForm, ToppingSelectionForm, DrinkSelectionForm

def home(request):
    """Home page view."""
    return render(request, 'pizza_app/home.html')

def about(request):
    """About page view."""
    return render(request, 'pizza_app/about.html')

def contact(request):
    """Contact page view."""
    return render(request, 'pizza_app/contact.html')

def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'pizza_app/register.html', {'form': form})

def menu(request):
    """Display the menu with pizzas and drinks."""
    pizzas = Pizza.objects.filter(available=True)
    drinks = Drink.objects.filter(available=True)
    
    # Get all sizes for the size selection
    sizes = Size.objects.all()
    
    context = {
        'pizzas': pizzas,
        'drinks': drinks,
        'sizes': sizes,
    }
    
    return render(request, 'pizza_app/menu.html', context)

@login_required
def pizza_detail(request, pizza_id):
    """Show pizza details and allow customization."""
    pizza = get_object_or_404(Pizza, id=pizza_id, available=True)
    sizes = Size.objects.all()
    
    if request.method == 'POST':
        pizza_form = PizzaSelectionForm(request.POST, initial={'pizza': pizza.id})
        topping_form = ToppingSelectionForm(
            request.POST, 
            available_toppings=pizza.available_toppings.filter(available=True)
        )
        
        if pizza_form.is_valid() and topping_form.is_valid():
            # Get or create user's cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Get form data
            size = pizza_form.cleaned_data['size']
            quantity = pizza_form.cleaned_data['quantity']
            
            # Create cart item
            cart_item = CartItem.objects.create(
                cart=cart,
                item_type='pizza',
                pizza=pizza,
                pizza_size=size,
                quantity=quantity
            )
            
            # Add selected toppings
            for field_name, value in topping_form.cleaned_data.items():
                if value and field_name.startswith('topping_'):
                    topping_id = int(field_name.split('_')[1])
                    topping = Topping.objects.get(id=topping_id)
                    CartItemTopping.objects.create(
                        cart_item=cart_item,
                        topping=topping
                    )
            
            messages.success(request, f'Added {pizza.name} to your cart!')
            # Redirect to drink suggestion page instead of cart
            return redirect('suggest_drinks', pizza_id=pizza.id)
    else:
        pizza_form = PizzaSelectionForm(initial={'pizza': pizza.id})
        topping_form = ToppingSelectionForm(
            available_toppings=pizza.available_toppings.filter(available=True)
        )
    
    context = {
        'pizza': pizza,
        'sizes': sizes,
        'pizza_form': pizza_form,
        'topping_form': topping_form,
    }
    
    return render(request, 'pizza_app/pizza_detail.html', context)

@login_required
def suggest_drinks(request, pizza_id):
    """Suggest drinks after adding a pizza to cart."""
    pizza = get_object_or_404(Pizza, id=pizza_id)
    # Get available drinks
    drinks = Drink.objects.filter(available=True)
    
    context = {
        'pizza': pizza,
        'drinks': drinks,
    }
    
    return render(request, 'pizza_app/add_drink_suggestion.html', context)

@login_required
def add_drink_to_cart(request, drink_id):
    """Add a drink to the user's cart."""
    drink = get_object_or_404(Drink, id=drink_id, available=True)
    
    if request.method == 'POST':
        form = DrinkSelectionForm(request.POST, initial={'drink': drink.id})
        
        if form.is_valid():
            # Get or create user's cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Get form data
            quantity = form.cleaned_data['quantity']
            
            # Create cart item
            CartItem.objects.create(
                cart=cart,
                item_type='drink',
                drink=drink,
                quantity=quantity
            )
            
            messages.success(request, f'Added {drink.name} to your cart!')
            return redirect('cart')
    else:
        form = DrinkSelectionForm(initial={'drink': drink.id})
    
    context = {
        'drink': drink,
        'form': form,
    }
    
    return render(request, 'pizza_app/add_drink.html', context)

@login_required
def cart(request):
    """Display the user's shopping cart."""
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        total = cart.total_price
    except Cart.DoesNotExist:
        cart_items = []
        total = 0
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    
    return render(request, 'pizza_app/cart.html', context)

@login_required
def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    item = get_object_or_404(CartItem, id=item_id)
    
    # Ensure the item belongs to the user's cart
    if item.cart.user != request.user:
        messages.error(request, "You don't have permission to remove this item.")
        return redirect('cart')
    
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required
def update_cart_item(request, item_id):
    """Update the quantity of a cart item."""
    item = get_object_or_404(CartItem, id=item_id)
    
    # Ensure the item belongs to the user's cart
    if item.cart.user != request.user:
        messages.error(request, "You don't have permission to update this item.")
        return redirect('cart')
    
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()
            messages.success(request, "Cart updated.")
        else:
            item.delete()
            messages.success(request, "Item removed from cart.")
    
    return redirect('cart')

@login_required
def checkout(request):
    """Process the checkout and create an order."""
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect('cart')
        
        # Calculate total
        total = cart.total_price
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            status='pending'
        )
        
        # Add items to order
        for cart_item in cart_items:
            if cart_item.item_type == 'pizza':
                order_item = OrderItem.objects.create(
                    order=order,
                    item_type='pizza',
                    pizza=cart_item.pizza,
                    pizza_size=cart_item.pizza_size,
                    quantity=cart_item.quantity,
                    item_price=cart_item.item_price
                )
                
                # Add toppings to order item
                for cart_topping in cart_item.toppings.all():
                    OrderItemTopping.objects.create(
                        order_item=order_item,
                        topping=cart_topping.topping,
                        topping_price=cart_topping.topping.get_price_for_size(cart_item.pizza_size)
                    )
            else:
                OrderItem.objects.create(
                    order=order,
                    item_type='drink',
                    drink=cart_item.drink,
                    quantity=cart_item.quantity,
                    item_price=cart_item.drink.price
                )
        
        # Clear the cart
        cart.items.all().delete()
        
        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_confirmation', order_id=order.id)
        
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

@login_required
def order_confirmation(request, order_id):
    """Display order confirmation."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
        'items': order.items.all(),
    }
    
    return render(request, 'pizza_app/order_confirmation.html', context)

@login_required
def order_history(request):
    """Display the user's order history."""
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'pizza_app/order_history.html', context)

@login_required
def order_detail(request, order_id):
    """Display details of a specific order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order
    }
    
    return render(request, 'pizza_app/order_detail.html', context)

@login_required
def cancel_order(request, order_id):
    """Cancel a pending order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f"Order #{order.id} has been cancelled.")
    else:
        messages.error(request, "This order cannot be cancelled.")
    
    return redirect('order_detail', order_id=order.id)
