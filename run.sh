#!/usr/bin/env bash
# Nutrition Chatbot — Linux/macOS launcher
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install/upgrade dependencies silently
pip install -q -r requirements.txt

# Copy .env.example to .env if .env doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "⚠️  First run: edit .env and set your OPENAI_API_KEY, then run this script again."
    echo "   nano .env"
    echo ""
    deactivate
    exit 1
fi

# Run the chatbot
python chat.py
