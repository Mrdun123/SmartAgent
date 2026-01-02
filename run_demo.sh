#!/bin/bash
# Dubai Mall Intelligent Concierge - Quick Start Script (Mac/Linux)

echo "===================================================="
echo "  Dubai Mall Intelligent Concierge Demo"
echo "  Powered by Claude 3.5 Sonnet"
echo "===================================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[1/4] Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "[2/4] Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "[3/4] Installing dependencies..."
pip install -r requirements.txt -q
echo ""

# Check for API key
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "[WARNING] DEEPSEEK_API_KEY not set!"
    echo ""
    echo "Please set your API key:"
    echo "  1. Get API key from: https://platform.deepseek.com/"
    echo "  2. Set environment variable: export DEEPSEEK_API_KEY='sk-xxxxx'"
    echo "  3. Or enter it in the app's sidebar settings"
    echo ""
fi

# Run Streamlit app
echo "[4/4] Starting Streamlit app..."
echo ""
echo "===================================================="
echo "  App will open in your browser automatically"
echo "  Press Ctrl+C to stop the server"
echo "===================================================="
echo ""

streamlit run app.py
