#!/bin/bash
# Quick start script for LinkedIn Age Classifier Agent

echo "========================================"
echo "LinkedIn Age Classifier Agent"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please create one with: python -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if API key is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  GEMINI_API_KEY not set!"
    echo ""
    echo "Please set your API key:"
    echo "  export GEMINI_API_KEY='your_api_key_here'"
    echo ""
    echo "Get your key from: https://makersuite.google.com/app/apikey"
    echo ""
    exit 1
fi

echo "✓ Virtual environment activated"
echo "✓ API key found"
echo ""

# Run the agent
if [ $# -eq 0 ]; then
    echo "Running with default sample file..."
    python age_classifier_agent.py
elif [ $# -eq 1 ]; then
    echo "Running with input file: $1"
    python age_classifier_agent.py "$1"
else
    echo "Running with input: $1, output: $2"
    python age_classifier_agent.py "$1" "$2"
fi

