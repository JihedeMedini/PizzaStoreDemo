// DOM Elements
const cartCountElement = document.getElementById('cart-count');
const cartForms = document.querySelectorAll('form[action*="cart"]');

document.addEventListener('DOMContentLoaded', function() {
    // Set up event listeners for all forms that add items to cart
    cartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Don't intercept the form for now, just update the UI immediately for better UX
            updateCartCount(1); // Increment cart by the quantity in the form
        });
    });
    
    // Set up quantity change listeners
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            // This is just for a responsive feel
            const newQuantity = parseInt(input.value);
            if (!isNaN(newQuantity) && newQuantity > 0) {
                // We don't actually update the count here as the form needs to be submitted
                // This is handled by the form submit handler
            }
        });
    });
    
    // Handle quantity increase/decrease buttons if they exist
    const quantityBtns = document.querySelectorAll('.quantity-btn');
    quantityBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const action = btn.dataset.action;
            const input = btn.closest('form').querySelector('input[name="quantity"]');
            const currentValue = parseInt(input.value);
            
            if (action === 'increase') {
                input.value = Math.min(99, currentValue + 1);
            } else if (action === 'decrease' && currentValue > 1) {
                input.value = currentValue - 1;
            }
        });
    });
});

/**
 * Update the cart count in the UI
 * @param {Number} change - The amount to add to the cart count
 */
function updateCartCount(change) {
    if (!cartCountElement) return;
    
    const currentCount = parseInt(cartCountElement.textContent) || 0;
    const newCount = currentCount + change;
    
    cartCountElement.textContent = newCount;
    
    // Add animation or highlight effect
    cartCountElement.classList.add('animate-pulse', 'bg-yellow-500');
    
    // Remove animation after a short delay
    setTimeout(() => {
        cartCountElement.classList.remove('animate-pulse', 'bg-yellow-500');
        cartCountElement.classList.add('bg-pizza-red');
    }, 800);
} 