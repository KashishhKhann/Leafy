#!/bin/bash
# Quick setup script for macOS
# Run this script with: bash setup_macos.sh

set -e  # Exit on error

echo "Leafy macOS Setup Script"
echo "=============================="
echo ""

# Check Python
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python3 not found. Installing via Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install python3
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "  Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  Virtual environment created"
else
    echo "  Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "  Activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Setup .env
echo ""
echo "Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "  Created .env file (please edit with your API keys)"
    echo "  • Get WolframAlpha key: https://developer.wolframalpha.com/"
    echo "  • Get NewsAPI key: https://newsapi.org/"
    echo "  • Edit .env: nano .env"
else
    echo "  .env file already exists"
fi

# Create data directories
echo "Creating data directories..."
mkdir -p logs
mkdir -p data/notes
echo "  Created logs/ and data/notes/ directories"

# Final instructions
echo ""
echo "=============================="
echo "Setup Complete!"
echo "=============================="
echo ""
echo "Next Steps:"
echo "1. Edit your API keys:"
echo "   nano .env"
echo ""
echo "2. Run the application:"
echo "   python Leafy.py"
echo ""
echo "3. When prompted, allow microphone access in macOS"
echo ""
echo "4. Try voice commands like:"
echo "   • 'How are you?'"
echo "   • 'Tell me a joke'"
echo "   • 'What is the time?'"
echo ""
echo "For more help, see MACOS_SETUP.md"
echo ""
