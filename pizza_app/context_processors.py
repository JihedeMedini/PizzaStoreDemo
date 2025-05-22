from .models import Cart

def cart_processor(request):
    """Add cart count to context for all templates."""
    cart_count = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            # Calculate total items count
            cart_items = cart.items.all()
            cart_count = sum(item.quantity for item in cart_items)
        except Cart.DoesNotExist:
            # User has no cart yet
            cart_count = 0
            
    return {'cart_count': cart_count} 