// DOM Elements
const cartButton = document.getElementById('cart-button');
const cartSidebar = document.getElementById('cart-sidebar');
const closeCartButton = document.getElementById('close-cart');
const overlay = document.getElementById('overlay');
const cartItemsContainer = document.getElementById('cart-items');
const emptyCartMessage = document.getElementById('empty-cart-message');
const cartCountElement = document.getElementById('cart-count');
const cartTotalElement = document.getElementById('cart-total');
const checkoutButton = document.getElementById('checkout-btn');
const clearCartButton = document.getElementById('clear-cart');

// Cart data
let cart = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    loadCart();
    setupEventListeners();
    updateSizeLabels();
});

// Setup event listeners
function setupEventListeners() {
    // Cart toggle
    cartButton?.addEventListener('click', openCart);
    closeCartButton?.addEventListener('click', closeCart);
    overlay?.addEventListener('click', closeCart);
    
    // Size selection
    const sizeInputs = document.querySelectorAll('.pizza-size');
    sizeInputs.forEach(input => {
        input.addEventListener('change', handleSizeChange);
    });
    
    // Add to cart buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', handleAddToCart);
    });
    
    // Clear cart
    clearCartButton?.addEventListener('click', clearCart);
    
    // Checkout
    checkoutButton?.addEventListener('click', handleCheckout);
}

// Size selection handler
function handleSizeChange(event) {
    const sizeInput = event.target;
    const pizzaContainer = sizeInput.closest('div[data-pizza-id]');
    const pizzaId = pizzaContainer.dataset.pizzaId;
    const priceElement = pizzaContainer.closest('.bg-white').querySelector('.pizza-price');
    const price = sizeInput.dataset.price;
    
    // Update price display
    if (priceElement) {
        priceElement.textContent = price;
    }
    
    // Update active class for the visual selection
    const sizeLabels = pizzaContainer.querySelectorAll('.size-label');
    sizeLabels.forEach(label => {
        label.classList.remove('size-active');
    });
    
    sizeInput.nextElementSibling.classList.add('size-active');
}

// Add to cart handler
function handleAddToCart(event) {
    const button = event.target;
    const pizzaId = button.dataset.id;
    const pizzaName = button.dataset.name;
    const pizzaImage = button.dataset.image;
    
    // Get selected size and price
    const pizzaContainer = document.querySelector(`div[data-pizza-id="${pizzaId}"]`);
    const selectedSize = pizzaContainer.querySelector('input[type="radio"]:checked');
    const size = selectedSize.value;
    const price = parseFloat(selectedSize.dataset.price);
    
    // Check if this pizza is already in the cart
    const existingItemIndex = cart.findIndex(item => 
        item.id === pizzaId && item.size === size
    );
    
    if (existingItemIndex !== -1) {
        // Update quantity
        cart[existingItemIndex].quantity += 1;
    } else {
        // Add new item
        cart.push({
            id: pizzaId,
            name: pizzaName,
            size: size,
            price: price,
            quantity: 1,
            image: pizzaImage
        });
    }
    
    // Save cart to localStorage
    saveCart();
    
    // Show notification
    showAddedToCartNotification(pizzaName, size);
    
    // Update cart UI
    updateCartUI();
}

// Show notification when item is added to cart
function showAddedToCartNotification(name, size) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50 transform translate-y-10 opacity-0 transition-all duration-300';
    notification.textContent = `Added ${name} (${size}) to cart`;
    
    // Add to body
    document.body.appendChild(notification);
    
    // Trigger animation
    setTimeout(() => {
        notification.classList.remove('translate-y-10', 'opacity-0');
    }, 10);
    
    // Remove after delay
    setTimeout(() => {
        notification.classList.add('translate-y-10', 'opacity-0');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Update the cart UI
function updateCartUI() {
    // Update cart count
    const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
    cartCountElement.textContent = totalItems;
    
    // Update cart items display
    if (cart.length === 0) {
        emptyCartMessage.classList.remove('hidden');
        checkoutButton.disabled = true;
        clearCartButton.disabled = true;
    } else {
        emptyCartMessage.classList.add('hidden');
        checkoutButton.disabled = false;
        clearCartButton.disabled = false;
        
        // Clear current items
        const existingItems = cartItemsContainer.querySelectorAll('.cart-item');
        existingItems.forEach(item => item.remove());
        
        // Add items to cart
        cart.forEach(item => {
            const cartItem = createCartItemElement(item);
            cartItemsContainer.appendChild(cartItem);
        });
    }
    
    // Update total
    updateCartTotal();
}

// Create a cart item element
function createCartItemElement(item) {
    const cartItem = document.createElement('div');
    cartItem.className = 'cart-item flex items-center border-b border-gray-200 py-4';
    cartItem.dataset.id = item.id;
    cartItem.dataset.size = item.size;
    
    cartItem.innerHTML = `
        <div class="h-16 w-16 rounded overflow-hidden mr-4">
            <img src="${item.image}" alt="${item.name}" class="h-full w-full object-cover">
        </div>
        <div class="flex-grow">
            <h3 class="font-medium">${item.name}</h3>
            <p class="text-sm text-gray-600">Size: ${item.size.charAt(0).toUpperCase() + item.size.slice(1)}</p>
            <div class="flex items-center mt-1">
                <button class="decrease-quantity text-gray-500 hover:text-gray-700">
                    <i class="fas fa-minus-circle"></i>
                </button>
                <span class="quantity mx-2">${item.quantity}</span>
                <button class="increase-quantity text-gray-500 hover:text-gray-700">
                    <i class="fas fa-plus-circle"></i>
                </button>
            </div>
        </div>
        <div class="text-right">
            <p class="font-medium">$${(item.price * item.quantity).toFixed(2)}</p>
            <button class="remove-item text-sm text-pizza-red hover:underline mt-1">
                Remove
            </button>
        </div>
    `;
    
    // Add event listeners for cart item buttons
    cartItem.querySelector('.decrease-quantity').addEventListener('click', () => {
        decreaseQuantity(item.id, item.size);
    });
    
    cartItem.querySelector('.increase-quantity').addEventListener('click', () => {
        increaseQuantity(item.id, item.size);
    });
    
    cartItem.querySelector('.remove-item').addEventListener('click', () => {
        removeCartItem(item.id, item.size);
    });
    
    return cartItem;
}

// Update cart total
function updateCartTotal() {
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    cartTotalElement.textContent = total.toFixed(2);
}

// Increase item quantity
function increaseQuantity(id, size) {
    const itemIndex = cart.findIndex(item => item.id === id && item.size === size);
    if (itemIndex !== -1) {
        cart[itemIndex].quantity += 1;
        saveCart();
        updateCartUI();
    }
}

// Decrease item quantity
function decreaseQuantity(id, size) {
    const itemIndex = cart.findIndex(item => item.id === id && item.size === size);
    if (itemIndex !== -1) {
        if (cart[itemIndex].quantity > 1) {
            cart[itemIndex].quantity -= 1;
        } else {
            cart.splice(itemIndex, 1);
        }
        saveCart();
        updateCartUI();
    }
}

// Remove item from cart
function removeCartItem(id, size) {
    const itemIndex = cart.findIndex(item => item.id === id && item.size === size);
    if (itemIndex !== -1) {
        cart.splice(itemIndex, 1);
        saveCart();
        updateCartUI();
    }
}

// Clear cart
function clearCart() {
    cart = [];
    saveCart();
    updateCartUI();
    closeCart();
}

// Handle checkout
function handleCheckout() {
    alert('Thank you for your order! Your delicious pizza will be on its way soon.');
    clearCart();
}

// Save cart to localStorage
function saveCart() {
    localStorage.setItem('pizzaCart', JSON.stringify(cart));
}

// Load cart from localStorage
function loadCart() {
    const savedCart = localStorage.getItem('pizzaCart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
        updateCartUI();
    }
}

// Open cart sidebar
function openCart() {
    cartSidebar.classList.remove('translate-x-full');
    overlay.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
}

// Close cart sidebar
function closeCart() {
    cartSidebar.classList.add('translate-x-full');
    overlay.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
}

// Update the visual appearance of size labels
function updateSizeLabels() {
    const sizeLabels = document.querySelectorAll('.size-label');
    
    sizeLabels.forEach(label => {
        // Set the active style for selected size
        if (label.previousElementSibling.checked) {
            label.classList.add('bg-pizza-yellow', 'border-pizza-orange', 'text-gray-800', 'size-active');
        }
        
        // Add hover effect
        label.addEventListener('mouseenter', () => {
            if (!label.previousElementSibling.checked) {
                label.classList.add('bg-gray-100');
            }
        });
        
        label.addEventListener('mouseleave', () => {
            if (!label.previousElementSibling.checked) {
                label.classList.remove('bg-gray-100');
            }
        });
    });
} 