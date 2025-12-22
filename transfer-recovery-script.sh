#!/bin/bash

# Script to transfer recovery script to VPS
# Usage: ./transfer-recovery-script.sh

VPS_IP="91.107.172.234"
VPS_USER="root"
VPS_DEPLOY_PATH="/home/deploy/docker-deploy"

echo "📤 Transferring recovery script to VPS..."
echo "VPS: ${VPS_USER}@${VPS_IP}:${VPS_DEPLOY_PATH}"
echo ""

# Transfer recovery script
if [ -f "recover-production.sh" ]; then
    echo "Transferring recover-production.sh..."
    scp recover-production.sh "${VPS_USER}@${VPS_IP}:${VPS_DEPLOY_PATH}/"
    if [ $? -eq 0 ]; then
        echo "✅ recover-production.sh transferred successfully"
    else
        echo "❌ Failed to transfer recover-production.sh"
        exit 1
    fi
else
    echo "❌ recover-production.sh not found!"
    exit 1
fi

echo ""
echo "✅ Transfer complete!"
echo ""
echo "Next steps:"
echo "1. SSH to VPS: ssh ${VPS_USER}@${VPS_IP}"
echo "2. Navigate to: cd ${VPS_DEPLOY_PATH}"
echo "3. Make script executable: chmod +x recover-production.sh"
echo "4. Run recovery: ./recover-production.sh"

