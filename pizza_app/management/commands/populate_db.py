from django.core.management.base import BaseCommand
from pizza_app.models import Size, Topping, Pizza, Drink

class Command(BaseCommand):
    help = 'Populates the database with initial data'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')
        
        # Create sizes
        self.stdout.write('Creating sizes...')
        small, created = Size.objects.get_or_create(name='Small', price_multiplier=1.0)
        medium, created = Size.objects.get_or_create(name='Medium', price_multiplier=1.3)
        large, created = Size.objects.get_or_create(name='Large', price_multiplier=1.6)
        
        # Create toppings
        self.stdout.write('Creating toppings...')
        toppings = [
            {'name': 'Pepperoni', 'small_price': 1.5},
            {'name': 'Mushrooms', 'small_price': 1.0},
            {'name': 'Onions', 'small_price': 0.75},
            {'name': 'Sausage', 'small_price': 1.5},
            {'name': 'Bacon', 'small_price': 1.5},
            {'name': 'Extra cheese', 'small_price': 1.0},
            {'name': 'Black olives', 'small_price': 1.0},
            {'name': 'Green peppers', 'small_price': 0.75},
            {'name': 'Pineapple', 'small_price': 1.0},
            {'name': 'Spinach', 'small_price': 1.0},
        ]
        
        created_toppings = []
        for topping_data in toppings:
            topping, created = Topping.objects.get_or_create(
                name=topping_data['name'],
                defaults={'small_price': topping_data['small_price']}
            )
            created_toppings.append(topping)
        
        # Create pizzas
        self.stdout.write('Creating pizzas...')
        pizzas = [
            {
                'name': 'Margherita',
                'description': 'Classic pizza with tomato sauce, fresh mozzarella, basil, and extra virgin olive oil.',
                'base_price': 9.99,
                'available_toppings': [
                    'Extra cheese', 'Mushrooms', 'Onions', 'Black olives'
                ]
            },
            {
                'name': 'Pepperoni',
                'description': 'Classic American pizza topped with tomato sauce, mozzarella, and pepperoni slices.',
                'base_price': 10.99,
                'available_toppings': [
                    'Extra cheese', 'Mushrooms', 'Onions', 'Green peppers', 'Sausage'
                ]
            },
            {
                'name': 'Vegetarian',
                'description': 'Fresh vegetables including bell peppers, mushrooms, onions, olives, and tomatoes.',
                'base_price': 11.99,
                'available_toppings': [
                    'Extra cheese', 'Spinach', 'Pineapple', 'Black olives', 'Green peppers'
                ]
            },
            {
                'name': 'Supreme',
                'description': 'Loaded with pepperoni, sausage, bell peppers, onions, olives, and mushrooms.',
                'base_price': 12.99,
                'available_toppings': [
                    'Extra cheese', 'Bacon', 'Pineapple'
                ]
            },
        ]
        
        for pizza_data in pizzas:
            pizza, created = Pizza.objects.get_or_create(
                name=pizza_data['name'],
                defaults={
                    'description': pizza_data['description'],
                    'base_price': pizza_data['base_price']
                }
            )
            
            # Add available toppings
            for topping_name in pizza_data['available_toppings']:
                topping = Topping.objects.get(name=topping_name)
                pizza.available_toppings.add(topping)
        
        # Create drinks
        self.stdout.write('Creating drinks...')
        drinks = [
            {'name': 'Coca-Cola', 'size': 'Small', 'price': 1.99},
            {'name': 'Coca-Cola', 'size': 'Medium', 'price': 2.49},
            {'name': 'Coca-Cola', 'size': 'Large', 'price': 2.99},
            {'name': 'Sprite', 'size': 'Small', 'price': 1.99},
            {'name': 'Sprite', 'size': 'Medium', 'price': 2.49},
            {'name': 'Sprite', 'size': 'Large', 'price': 2.99},
            {'name': 'Fanta', 'size': 'Small', 'price': 1.99},
            {'name': 'Fanta', 'size': 'Medium', 'price': 2.49},
            {'name': 'Fanta', 'size': 'Large', 'price': 2.99},
            {'name': 'Water', 'size': 'Bottle', 'price': 1.49},
        ]
        
        for drink_data in drinks:
            Drink.objects.get_or_create(
                name=drink_data['name'],
                size=drink_data['size'],
                defaults={'price': drink_data['price']}
            )
        
        self.stdout.write(self.style.SUCCESS('Database successfully populated!')) 