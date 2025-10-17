#!/bin/bash
# Cyber Tonic Cybersecurity Compliance Hub - Quick Launch Script
# Simple shell script for easy launching

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "💡 Please install Python 3.9 or higher"
    exit 1
fi

# Run the Python launcher
python3 launch.py "$@"
