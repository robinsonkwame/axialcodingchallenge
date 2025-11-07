#!/bin/bash

# NFT Description Fetcher - Simple Runner Script
# This sets up a virtual environment and runs the fetch script

set -e  # Exit on error

echo "=================================="
echo "NFT Description Fetcher Setup"
echo "=================================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found. Please install Python 3."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet

# Install required packages
# Clone NFT-NET-Hub if not already present
if [ ! -d "NFT-NET-Hub" ]; then
    echo "📦 Cloning NFT-NET-Hub repository..."
    git clone https://github.com/ShuxunoO/NFT-NET-Hub.git --quiet
    echo "✓ NFT-NET-Hub cloned"
else
    echo "✓ NFT-NET-Hub already exists"
fi

# Install NFT-NET-Hub requirements (skip pywin32 on macOS)
echo "📦 Installing NFT-NET-Hub requirements..."
cd NFT-NET-Hub
# Filter out pywin32 for macOS
grep -v "pywin32" requirements.txt > requirements_filtered.txt
pip install -r requirements_filtered.txt --quiet
cd ..

echo "✓ Dependencies installed"
echo ""

# Load .env file if it exists
if [ -f ".env" ]; then
    echo "🔐 Loading credentials from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
    echo "✓ Environment variables loaded"
else
    echo "⚠️  No .env file found (this is okay if you're already logged in)"
fi
echo ""

# Check if user has dataset access
echo "🔍 Checking dataset access..."
echo "(This will fail if you haven't requested access to the dataset)"
echo ""

# Run the fetch script using NFT-NET-Hub
echo "=================================="
echo "Running Fetch Script"
echo "=================================="
echo ""

python fetch_using_nfthub.py

# Check if script succeeded
if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "✅ SUCCESS!"
    echo "=================================="
    echo ""
    echo "Files created:"
    echo "  📄 student_descriptions.txt    → Send to student"
    echo "  🔑 instructor_key.json         → Keep for reference"
    echo "  📊 collection_metadata.txt     → Documentation"
    echo ""
    echo "Next steps:"
    echo "1. Review collection_metadata.txt to see what was fetched"
    echo "2. Send student_descriptions.txt to your student"
    echo "3. Keep instructor_key.json for decoding their results"
    echo ""
else
    echo ""
    echo "=================================="
    echo "❌ ERROR"
    echo "=================================="
    echo ""
    echo "If you see 'Repository not found' or 'Access denied':"
    echo "1. Visit: https://huggingface.co/datasets/shuxunoo/NFT-Net"
    echo "2. Click 'Access repository' and accept terms"
    echo "3. Wait for approval (may take some time)"
    echo "4. Run this script again"
    echo ""
fi

# Deactivate virtual environment
deactivate

echo "Done!"
