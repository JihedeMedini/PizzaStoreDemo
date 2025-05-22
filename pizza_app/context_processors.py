import os
from .models import Cart

def cart_processor(request):
    """Add cart count to context for all templates."""
    cart_count = 0
    
    # Skip database access on Vercel environment to prevent errors
    IS_VERCEL = os.environ.get('VERCEL')
    if IS_VERCEL:
        return {'cart_count': 0}
        
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            # Calculate total items count
            cart_items = cart.items.all()
            cart_count = sum(item.quantity for item in cart_items)
        except Cart.DoesNotExist:
            # User has no cart yet
            cart_count = 0
        except Exception as e:
            # Handle any other database errors
            print(f"Error in cart_processor: {e}")
            cart_count = 0
            
    return {'cart_count': cart_count} 