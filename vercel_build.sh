#!/bin/bash

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Setting up directories..."
mkdir -p staticfiles_build

# Run Django migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Populate database with initial data
echo "Populating database with initial data..."
python manage.py populate_db

# Run Django collectstatic
echo "Running collectstatic..."
python manage.py collectstatic --noinput || {
    echo "Collectstatic failed, but continuing..."
    # Create a minimal index file in staticfiles directory
    mkdir -p staticfiles
    echo "<html><body>Static placeholder</body></html>" > staticfiles/index.html
}

# Copy files to the build directory
echo "Copying static files..."
cp -r staticfiles/* staticfiles_build/ 2>/dev/null || {
    echo "No static files to copy, creating placeholder..."
    echo "<html><body>Static placeholder</body></html>" > staticfiles_build/index.html
}

echo "Build process completed!" 