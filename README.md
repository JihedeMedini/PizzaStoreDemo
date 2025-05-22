# Pizza Paradise

A feature-complete pizza ordering website built with Django, featuring user authentication, cart management, and order tracking.

## Features

- **Menu Management**:
  - Pizzas with customizable sizes and toppings
  - Drinks in various sizes
  - Dynamic pricing based on size and toppings

- **User Authentication**:
  - User registration with personal information
  - Login/logout functionality
  - Protected user accounts

- **Shopping Cart**:
  - Add pizzas with customizable toppings
  - Add drinks
  - Update quantities
  - Remove items
  - Calculate total price

- **Order Management**:
  - Place orders with cart contents
  - View order history
  - Order status tracking

- **Admin Interface**:
  - Manage menu items (pizzas, toppings, drinks)
  - View and update order statuses
  - Manage user accounts

## Technical Stack

- **Backend**: Django
- **Database**: SQLite (default)
- **Frontend**: HTML, Bootstrap CSS, JavaScript
- **Image Handling**: Pillow

## Project Structure

```
pizza_paradise/
├── pizza_app/               # Main application
│   ├── management/          # Custom management commands
│   │   └── commands/        
│   │       └── populate_db.py  # Data population script
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   │   └── pizza_app/       # Application templates
│   ├── admin.py             # Admin interface configuration
│   ├── forms.py             # Form definitions
│   ├── models.py            # Database models
│   ├── urls.py              # URL routing
│   └── views.py             # View functions
├── pizza_paradise/          # Project settings
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
├── media/                   # User-uploaded media files
├── manage.py                # Django management script
└── README.md                # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pizza-paradise
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Populate the database with initial data**:
   ```bash
   python manage.py populate_db
   ```

6. **Create a superuser for admin access**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the website**:
   - Main website: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## User Guide

### For Customers

1. Register for an account
2. Browse the menu
3. Select pizzas and customize with toppings
4. Add drinks to cart
5. Review cart and checkout
6. View order history and status

### For Administrators

1. Log in to the admin interface
2. Manage menu items (add, update, delete)
3. View and update order statuses
4. Manage user accounts 