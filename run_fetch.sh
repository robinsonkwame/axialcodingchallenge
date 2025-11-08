#!/bin/bash

# NFT Description Fetcher - Simple Runner Script
# This sets up a virtual environment and runs the fetch script
# NOTE: No Hugging Face access required - uses local metadata only

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

# Ensure NFT-NET-Hub submodule is initialized
if [ ! -f "NFT-NET-Hub/.git" ] && [ ! -d "NFT-NET-Hub/.git" ]; then
    echo "📦 Initializing NFT-NET-Hub submodule..."
    git submodule update --init --recursive
    echo "✓ NFT-NET-Hub submodule initialized"
else
    echo "✓ NFT-NET-Hub submodule already initialized"
fi

# Install all requirements from unified file
echo "📦 Installing all dependencies..."
pip install -r requirements-all.txt --quiet
echo "✓ All dependencies installed"
echo ""

# Verify the import works
echo "🔍 Verifying NFT-NET-Hub installation..."
python3 -c "import sys; sys.path.insert(0, 'NFT-NET-Hub/nft_net_hub'); from utils.downloader import NFT1000; print('✓ NFT-NET-Hub successfully installed and verified')" || {
    echo "❌ Error: NFT-NET-Hub installation verification failed"
    echo "Please check the error messages above"
    exit 1
}
echo ""

# Run the fetch script using NFT-NET-Hub
echo "=================================="
echo "Running Fetch Script"
echo "=================================="
echo "Note: Using local metadata only (no downloads)"
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
    echo "Check the error messages above for details."
    echo ""
fi

# Deactivate virtual environment
deactivate

echo "Done!"
