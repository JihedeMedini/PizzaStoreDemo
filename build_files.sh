#!/bin/bash
# Build script for Vercel deployment

echo "Starting build process..."

# Make script executable
chmod +x build_files.sh

# Create the staticfiles_build directory
mkdir -p staticfiles_build

# Create a simple index.html file to satisfy Vercel's requirement
echo '<html><head><meta http-equiv="refresh" content="0; URL=/"></head></html>' > staticfiles_build/index.html

echo "Static files directory created successfully!"
echo "Build completed successfully!" 