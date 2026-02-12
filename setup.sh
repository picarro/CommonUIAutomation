#!/bin/bash

# Setup script for Storybook Automation Framework

echo "Setting up Storybook Automation Framework..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please update .env with your Storybook URL and settings"
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p screenshots
mkdir -p snapshots
mkdir -p reports

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your Storybook URL"
echo "2. Start your Storybook server"
echo "3. Run tests: pytest"

