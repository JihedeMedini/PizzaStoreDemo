#!/bin/bash
# Build script for Vercel deployment

# Make script executable
chmod +x build_files.sh

# Install project dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Create the staticfiles_build directory if it doesn't exist
mkdir -p staticfiles_build

# Copy all collected static files to staticfiles_build
cp -r staticfiles/* staticfiles_build/

echo "Build completed successfully!" 