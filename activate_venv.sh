#!/bin/bash
# Quick script to activate virtual environment (Mac/Linux)

echo "Activating virtual environment..."
source venv/bin/activate
echo ""
echo "Virtual environment activated!"
echo "Python location:"
which python
echo ""
echo "Installed packages:"
pip list
echo ""
echo "To run the demo, use: streamlit run app.py"
