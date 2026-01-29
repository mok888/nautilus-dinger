#!/bin/bash

echo "=== Paradex API Key Setup ==="
echo ""
echo "Your L2 Address: 0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8"
echo ""
echo "Steps to get API key:"
echo "1. Visit: https://testnet.paradex.trade"
echo "2. Connect wallet with the address above"
echo "3. Go to Settings > API Keys"
echo "4. Click 'Generate New Key'"
echo "5. Copy the key"
echo ""
read -p "Paste your API key here: " api_key

if [ -z "$api_key" ]; then
    echo "❌ No key provided"
    exit 1
fi

echo "PARADEX_API_KEY=$api_key" > /home/mok/projects/nautilus-dinger/memory-bank/.env
echo "✅ Saved to memory-bank/.env"
echo ""
echo "Now run: source memory-bank/.env && python3 place_order.py"
