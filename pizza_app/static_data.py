# Static data for Pizza Paradise - replaces database models for Vercel deployment

# Size data with price multipliers
SIZES = {
    'Small': {'name': 'Small', 'price_multiplier': 1.0},
    'Medium': {'name': 'Medium', 'price_multiplier': 1.3},
    'Large': {'name': 'Large', 'price_multiplier': 1.6},
}

# Topping data with prices for small size
TOPPINGS = {
    'Pepperoni': {'name': 'Pepperoni', 'small_price': 1.5},
    'Mushrooms': {'name': 'Mushrooms', 'small_price': 1.0},
    'Onions': {'name': 'Onions', 'small_price': 0.75},
    'Sausage': {'name': 'Sausage', 'small_price': 1.5},
    'Bacon': {'name': 'Bacon', 'small_price': 1.5},
    'Extra cheese': {'name': 'Extra cheese', 'small_price': 1.0},
    'Black olives': {'name': 'Black olives', 'small_price': 1.0},
    'Green peppers': {'name': 'Green peppers', 'small_price': 0.75},
    'Pineapple': {'name': 'Pineapple', 'small_price': 1.0},
    'Spinach': {'name': 'Spinach', 'small_price': 1.0},
}

# Pizza data with available toppings
PIZZAS = {
    1: {
        'id': 1,
        'name': 'Margherita',
        'description': 'Classic pizza with tomato sauce, fresh mozzarella, basil, and extra virgin olive oil.',
        'base_price': 9.99,
        'image_url': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
        'available_toppings': ['Extra cheese', 'Mushrooms', 'Onions', 'Black olives']
    },
    2: {
        'id': 2,
        'name': 'Pepperoni',
        'description': 'Classic American pizza topped with tomato sauce, mozzarella, and pepperoni slices.',
        'base_price': 10.99,
        'image_url': 'https://images.unsplash.com/photo-1628840042765-356cda07504e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
        'available_toppings': ['Extra cheese', 'Mushrooms', 'Onions', 'Green peppers', 'Sausage']
    },
    3: {
        'id': 3,
        'name': 'Vegetarian',
        'description': 'Fresh vegetables including bell peppers, mushrooms, onions, olives, and tomatoes.',
        'base_price': 11.99,
        'image_url': 'https://images.unsplash.com/photo-1511689660979-10d2b1aada49?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
        'available_toppings': ['Extra cheese', 'Spinach', 'Pineapple', 'Black olives', 'Green peppers']
    },
    4: {
        'id': 4,
        'name': 'Supreme',
        'description': 'Loaded with pepperoni, sausage, bell peppers, onions, olives, and mushrooms.',
        'base_price': 12.99,
        'image_url': 'https://images.unsplash.com/photo-1571997478779-2adcbbe9ab2f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
        'available_toppings': ['Extra cheese', 'Bacon', 'Pineapple']
    },
}

# Drink data
DRINKS = [
    {'id': 1, 'name': 'Coca-Cola', 'size': 'Small', 'price': 1.99, 'description': 'Classic carbonated soft drink', 'image_url': 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'},
    {'id': 2, 'name': 'Coca-Cola', 'size': 'Medium', 'price': 2.49, 'description': 'Classic carbonated soft drink', 'image_url': 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'},
    {'id': 3, 'name': 'Coca-Cola', 'size': 'Large', 'price': 2.99, 'description': 'Classic carbonated soft drink', 'image_url': 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'},
    {'id': 4, 'name': 'Sprite', 'size': 'Small', 'price': 1.99, 'description': 'Lemon-lime flavored soda', 'image_url': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'},
    {'id': 5, 'name': 'Sprite', 'size': 'Medium', 'price': 2.49, 'description': 'Lemon-lime flavored soda', 'image_url': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'},
    {'id': 6, 'name': 'Sprite', 'size': 'Large', 'price': 2.99, 'description': 'Lemon-lime flavored soda', 'image_url': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'},
    {'id': 7, 'name': 'Fanta', 'size': 'Small', 'price': 1.99, 'description': 'Orange flavored soda', 'image_url': 'https://images.unsplash.com/photo-1624552184280-8a8585739fea?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'},
    {'id': 8, 'name': 'Fanta', 'size': 'Medium', 'price': 2.49, 'description': 'Orange flavored soda', 'image_url': 'https://images.unsplash.com/photo-1624552184280-8a8585739fea?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'},
    {'id': 9, 'name': 'Fanta', 'size': 'Large', 'price': 2.99, 'description': 'Orange flavored soda', 'image_url': 'https://images.unsplash.com/photo-1624552184280-8a8585739fea?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'},
    {'id': 10, 'name': 'Water', 'size': 'Bottle', 'price': 1.49, 'description': 'Pure spring water', 'image_url': 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'},
]

# Helper functions to mimic model behavior
def get_pizza_by_id(pizza_id):
    """Get pizza data by ID"""
    return PIZZAS.get(int(pizza_id))

def get_all_pizzas():
    """Get all pizzas"""
    return list(PIZZAS.values())

def get_drink_by_id(drink_id):
    """Get drink data by ID"""
    for drink in DRINKS:
        if drink['id'] == int(drink_id):
            return drink
    return None

def get_all_drinks():
    """Get all drinks"""
    return DRINKS

def calculate_pizza_price(pizza_id, size, toppings=None):
    """Calculate pizza price based on size and toppings"""
    pizza = get_pizza_by_id(pizza_id)
    if not pizza:
        return 0
    
    base_price = pizza['base_price']
    size_multiplier = SIZES.get(size, {}).get('price_multiplier', 1.0)
    
    price = base_price * size_multiplier
    
    if toppings:
        for topping in toppings:
            topping_data = TOPPINGS.get(topping)
            if topping_data:
                topping_price = topping_data['small_price'] * size_multiplier
                price += topping_price
    
    return round(price, 2)

def get_available_toppings_for_pizza(pizza_id):
    """Get available toppings for a specific pizza"""
    pizza = get_pizza_by_id(pizza_id)
    if not pizza:
        return []
    return pizza['available_toppings'] 