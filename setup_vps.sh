#!/bin/bash
# Quick VPS Setup Script for Domain Claimer
# Run: bash setup_vps.sh

set -e  # Exit on error

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 JAGOAN HOSTING DOMAIN CLAIMER - VPS SETUP"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "⚠️  Please don't run as root. Create a user first:"
    echo "   sudo adduser domainbot"
    echo "   sudo usermod -aG sudo domainbot"
    echo "   su - domainbot"
    exit 1
fi

echo "📦 Step 1: Updating system..."
sudo apt update && sudo apt upgrade -y

echo ""
echo "🐍 Step 2: Installing Python..."
sudo apt install python3 python3-pip python3-venv -y

echo ""
echo "📚 Step 3: Installing Playwright dependencies..."
sudo apt install -y \
    libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
    libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 \
    libasound2 libatspi2.0-0 libxshmfence1 libglib2.0-0

echo ""
echo "🛠️  Step 4: Installing utilities..."
sudo apt install screen tmux htop -y

echo ""
echo "🔧 Step 5: Creating virtual environment..."
python3 -m venv venv

echo ""
echo "📥 Step 6: Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "🌐 Step 7: Installing Playwright browsers..."
python -m playwright install chromium
python -m playwright install-deps chromium

echo ""
echo "⚙️  Step 8: Setting up config..."
if [ ! -f config.env ]; then
    cp config.env.example config.env
    
    # Auto-set HEADLESS=True for VPS
    sed -i 's/HEADLESS=False/HEADLESS=True/g' config.env
    
    echo "✅ Config file created: config.env"
    echo "⚠️  HEADLESS mode automatically set to True (VPS mode)"
    echo ""
    echo "You can edit other settings:"
    read -p "Do you want to edit config.env now? (y/n): " edit_config
    if [ "$edit_config" = "y" ] || [ "$edit_config" = "Y" ]; then
        nano config.env
    fi
else
    echo "✅ Config file already exists"
fi

echo ""
echo "🔒 Step 9: Setting permissions..."
chmod 600 config.env
chmod +x domain_claimer.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SETUP COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎯 Quick Start:"
echo ""
echo "1. Test run (foreground):"
echo "   source venv/bin/activate"
echo "   python domain_claimer.py"
echo ""
echo "2. Run in background with screen:"
echo "   screen -S domain-claimer"
echo "   source venv/bin/activate"
echo "   python domain_claimer.py"
echo "   # Press Ctrl+A then D to detach"
echo ""
echo "3. Re-attach to screen:"
echo "   screen -r domain-claimer"
echo ""
echo "4. Monitor logs:"
echo "   tail -f domain_claimer.log"
echo ""
echo "5. View results:"
echo "   cat results.txt"
echo ""
echo "📖 Full documentation: VPS_DEPLOYMENT.md"
echo ""
echo "Happy claiming! 🚀"
