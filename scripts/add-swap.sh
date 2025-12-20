#!/bin/bash
# Script to add swap space on VPS for low-memory builds
# Run this on your VPS: bash scripts/add-swap.sh

set -e

SWAP_SIZE=${1:-2G}
SWAP_FILE="/swapfile"

echo "🔧 Adding ${SWAP_SIZE} swap space to VPS..."

# Check if swap already exists
if swapon --show | grep -q "${SWAP_FILE}"; then
    echo "✅ Swap file already exists and is active"
    swapon --show
    exit 0
fi

# Check if swap file exists but is not active
if [ -f "${SWAP_FILE}" ]; then
    echo "⚠️  Swap file exists but is not active. Activating..."
    sudo chmod 600 "${SWAP_FILE}"
    sudo swapon "${SWAP_FILE}"
    echo "✅ Swap activated"
    swapon --show
    exit 0
fi

# Create swap file
echo "📦 Creating ${SWAP_SIZE} swap file..."
if command -v fallocate &> /dev/null; then
    sudo fallocate -l "${SWAP_SIZE}" "${SWAP_FILE}"
else
    echo "⚠️  fallocate not available, using dd (this may take longer)..."
    sudo dd if=/dev/zero of="${SWAP_FILE}" bs=1024 count=$((2 * 1024 * 1024)) 2>/dev/null
fi

# Set permissions
echo "🔒 Setting permissions..."
sudo chmod 600 "${SWAP_FILE}"

# Format as swap
echo "💾 Formatting as swap..."
sudo mkswap "${SWAP_FILE}"

# Enable swap
echo "🚀 Enabling swap..."
sudo swapon "${SWAP_FILE}"

# Make it permanent
echo "💾 Making swap permanent..."
if ! grep -q "${SWAP_FILE}" /etc/fstab; then
    echo "${SWAP_FILE} none swap sw 0 0" | sudo tee -a /etc/fstab
    echo "✅ Added to /etc/fstab"
else
    echo "✅ Already in /etc/fstab"
fi

# Adjust swappiness (optional - less aggressive swap usage)
echo "⚙️  Adjusting swappiness..."
if ! grep -q "vm.swappiness" /etc/sysctl.conf; then
    echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
    sudo sysctl vm.swappiness=10
    echo "✅ Swappiness set to 10"
else
    echo "✅ Swappiness already configured"
fi

# Verify
echo ""
echo "✅ Swap space added successfully!"
echo ""
echo "📊 Current memory status:"
free -h
echo ""
echo "📊 Active swap:"
swapon --show

