from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
import os
import json
from .static_data import (
    get_all_pizzas, get_all_drinks, get_pizza_by_id, get_drink_by_id,
    calculate_pizza_price, get_available_toppings_for_pizza,
    SIZES, TOPPINGS
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
    """Display the menu with pizzas and drinks using static data."""
    pizzas = get_all_pizzas()
    drinks = get_all_drinks()
    
    context = {
        'pizzas': pizzas,
        'drinks': drinks,
    }
    return render(request, 'pizza_app/menu.html', context)

def pizza_detail(request, pizza_id):
    """Show pizza details and allow customization."""
    pizza = get_pizza_by_id(pizza_id)
    if not pizza:
        messages.error(request, "Pizza not found.")
        return redirect('menu')
    
    if request.method == 'POST':
        size = request.POST.get('size', 'Medium')
        quantity = int(request.POST.get('quantity', 1))
        selected_toppings = request.POST.getlist('toppings')
        
        # Validate size
        if size not in SIZES:
            size = 'Medium'
        
        # Validate toppings against available toppings for this pizza
        available_toppings = get_available_toppings_for_pizza(pizza_id)
        valid_toppings = [t for t in selected_toppings if t in available_toppings]
        
        # Calculate price
        price = calculate_pizza_price(pizza_id, size, valid_toppings)
        
        # Add to session cart
        if 'cart' not in request.session:
            request.session['cart'] = []
        
        cart_item = {
            'id': f"pizza_{pizza_id}_{len(request.session['cart'])}",
            'type': 'pizza',
            'pizza_id': pizza_id,
            'pizza_name': pizza['name'],
            'size': size,
            'toppings': valid_toppings,
            'quantity': quantity,
            'price': price,
            'total_price': price * quantity
        }
        
        request.session['cart'].append(cart_item)
        request.session.modified = True
        
        messages.success(request, f'Added {pizza["name"]} to your cart!')
        return redirect('suggest_drinks', pizza_id=pizza_id)
    
    context = {
        'pizza': pizza,
        'sizes': SIZES,
        'available_toppings': get_available_toppings_for_pizza(pizza_id),
        'toppings_data': TOPPINGS,
    }
    
    return render(request, 'pizza_app/pizza_detail.html', context)

def suggest_drinks(request, pizza_id):
    """Suggest drinks after adding a pizza to cart."""
    pizza = get_pizza_by_id(pizza_id)
    if not pizza:
        messages.error(request, "Pizza not found.")
        return redirect('menu')
    
    # Get available drinks
    drinks = get_all_drinks()
    
    context = {
        'pizza': pizza,
        'drinks': drinks,
    }
    
    return render(request, 'pizza_app/add_drink_suggestion.html', context)

def add_drink_to_cart(request, drink_id):
    """Add a drink to the user's cart."""
    drink = get_drink_by_id(drink_id)
    if not drink:
        messages.error(request, "Drink not found.")
        return redirect('menu')
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        # Add to session cart
        if 'cart' not in request.session:
            request.session['cart'] = []
        
        cart_item = {
            'id': f"drink_{drink_id}_{len(request.session['cart'])}",
            'type': 'drink',
            'drink_id': drink_id,
            'drink_name': drink['name'],
            'drink_size': drink['size'],
            'quantity': quantity,
            'price': drink['price'],
            'total_price': drink['price'] * quantity
        }
        
        request.session['cart'].append(cart_item)
        request.session.modified = True
        
        messages.success(request, f'Added {drink["name"]} to your cart!')
        return redirect('cart')
    
    context = {
        'drink': drink,
    }
    
    return render(request, 'pizza_app/add_drink.html', context)

def cart(request):
    """Display the user's shopping cart."""
    cart_items = request.session.get('cart', [])
    total = sum(item['total_price'] for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    
    return render(request, 'pizza_app/cart.html', context)

def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    cart_items = request.session.get('cart', [])
    
    # Find and remove the item
    updated_cart = [item for item in cart_items if item['id'] != item_id]
    
    if len(updated_cart) < len(cart_items):
        request.session['cart'] = updated_cart
        request.session.modified = True
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Item not found in cart.")
    
    return redirect('cart')

def update_cart_item(request, item_id):
    """Update the quantity of a cart item."""
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        cart_items = request.session.get('cart', [])
        
        for item in cart_items:
            if item['id'] == item_id:
                if new_quantity > 0:
                    item['quantity'] = new_quantity
                    item['total_price'] = item['price'] * new_quantity
                    messages.success(request, "Cart updated.")
                else:
                    # Remove item if quantity is 0
                    cart_items = [i for i in cart_items if i['id'] != item_id]
                    messages.success(request, "Item removed from cart.")
                break
        
        request.session['cart'] = cart_items
        request.session.modified = True
    
    return redirect('cart')

def checkout(request):
    """Process the checkout and create an order."""
    cart_items = request.session.get('cart', [])
    
    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')
    
    # Calculate total
    total = sum(item['total_price'] for item in cart_items)
    
    # Create a simple order ID using timestamp
    import time
    order_id = f"ORD{int(time.time())}"
    
    # Store order in session for confirmation
    order_data = {
        'id': order_id,
        'items': cart_items.copy(),
        'total': total,
        'status': 'confirmed',
        'user': 'Guest User' if not request.user.is_authenticated else request.user.username,
        'timestamp': time.time()
    }
    
    # Store in session for order confirmation
    request.session['last_order'] = order_data
    
    # Clear the cart
    request.session['cart'] = []
    request.session.modified = True
    
    messages.success(request, "Your order has been placed successfully!")
    return redirect('order_confirmation')

def order_confirmation(request):
    """Display order confirmation."""
    order = request.session.get('last_order')
    
    if not order:
        messages.error(request, "No recent order found.")
        return redirect('menu')
    
    context = {
        'order': order,
    }
    
    return render(request, 'pizza_app/order_confirmation.html', context)

def order_history(request):
    """Display the user's order history."""
    # For demo purposes, show only the last order if it exists
    last_order = request.session.get('last_order')
    orders = [last_order] if last_order else []
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'pizza_app/order_history.html', context)

def order_detail(request, order_id):
    """Display details of a specific order."""
    last_order = request.session.get('last_order')
    
    if not last_order or last_order['id'] != order_id:
        messages.error(request, "Order not found.")
        return redirect('order_history')
    
    context = {
        'order': last_order
    }
    
    return render(request, 'pizza_app/order_detail.html', context)

def cancel_order(request, order_id):
    """Cancel a pending order."""
    last_order = request.session.get('last_order')
    
    if not last_order or last_order['id'] != order_id:
        messages.error(request, "Order not found.")
        return redirect('order_history')
    
    if last_order['status'] == 'confirmed':
        last_order['status'] = 'cancelled'
        request.session['last_order'] = last_order
        request.session.modified = True
        messages.success(request, f"Order #{order_id} has been cancelled.")
    else:
        messages.error(request, "This order cannot be cancelled.")
    
    return redirect('order_detail', order_id=order_id)
