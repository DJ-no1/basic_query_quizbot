#!/bin/bash

echo "================================================"
echo "QuizBot Setup Script"
echo "================================================"
echo

echo "Step 1: Activating virtual environment..."
source venv/bin/activate

echo "Step 2: Installing dependencies..."
pip install -r requirements.txt

echo
echo "Step 3: Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env file created from .env.example"
    echo
    echo "⚠️  IMPORTANT: Please edit .env file and add your Google API key!"
    echo "   Get your API key from: https://makersuite.google.com/app/apikey"
    echo
else
    echo "✅ .env file already exists"
fi

echo
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo
echo "Next steps:"
echo "1. Edit .env file and add your Google API key"
echo "2. Run: python run_server.py"
echo "3. Open frontend/index.html in your browser"
echo
