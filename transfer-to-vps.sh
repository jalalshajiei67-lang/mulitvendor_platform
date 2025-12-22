#!/bin/bash

# Script to transfer diagnostic files to VPS
# Usage: ./transfer-to-vps.sh

VPS_IP="91.107.172.234"
VPS_USER="root"
VPS_PATH="/root/indexo-production"  # Adjust if your project is elsewhere

echo "📤 Transferring files to VPS..."
echo "VPS: ${VPS_USER}@${VPS_IP}:${VPS_PATH}"
echo ""

# Files to transfer
FILES=(
    "diagnose-api-404.sh"
    "FIX_API_404_DOCKER_COMPOSE.md"
)

# Transfer each file
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Transferring $file..."
        scp "$file" "${VPS_USER}@${VPS_IP}:${VPS_PATH}/"
        if [ $? -eq 0 ]; then
            echo "✅ $file transferred successfully"
        else
            echo "❌ Failed to transfer $file"
        fi
    else
        echo "⚠️  $file not found, skipping..."
    fi
done

echo ""
echo "✅ Transfer complete!"
echo ""
echo "Next steps:"
echo "1. SSH to VPS: ssh ${VPS_USER}@${VPS_IP}"
echo "2. Navigate to: cd ${VPS_PATH}"
echo "3. Make script executable: chmod +x diagnose-api-404.sh"
echo "4. Run diagnostic: ./diagnose-api-404.sh"

