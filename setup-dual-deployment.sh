#!/bin/bash
# Setup script for running Production + Staging simultaneously

set -e

echo "🚀 Setting up Dual Deployment (Production + Staging)"
echo "=================================================="
echo ""

# Check if running as root for nginx setup
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  This script needs sudo for nginx setup"
    echo "   Some commands will require sudo privileges"
    echo ""
fi

# Step 1: Check if nginx is installed
echo "📦 Step 1: Checking nginx installation..."
if ! command -v nginx &> /dev/null; then
    echo "   Installing nginx..."
    sudo apt update
    sudo apt install -y nginx certbot python3-certbot-nginx
else
    echo "   ✅ nginx is already installed"
fi

# Step 2: Get SSL certificates for staging
echo ""
echo "🔐 Step 2: Setting up SSL certificates for staging domains..."
echo "   This will request Let's Encrypt certificates for:"
echo "   - staging.indexo.ir"
echo "   - www.staging.indexo.ir"
echo "   - api.staging.indexo.ir"
echo ""
read -p "   Continue with SSL certificate setup? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo certbot certonly --standalone -d staging.indexo.ir -d www.staging.indexo.ir -d api.staging.indexo.ir
    echo "   ✅ SSL certificates obtained"
else
    echo "   ⚠️  Skipping SSL setup. You'll need to do this manually later."
fi

# Step 3: Configure nginx
echo ""
echo "⚙️  Step 3: Configuring nginx reverse proxy..."
if [ -f "nginx-staging-proxy.conf" ]; then
    sudo cp nginx-staging-proxy.conf /etc/nginx/sites-available/staging-proxy
    
    # Update SSL certificate paths if they exist
    if [ -d "/etc/letsencrypt/live/staging.indexo.ir" ]; then
        echo "   ✅ SSL certificate paths found"
    else
        echo "   ⚠️  SSL certificates not found. Update nginx config manually."
    fi
    
    # Create symlink if it doesn't exist
    if [ ! -L "/etc/nginx/sites-enabled/staging-proxy" ]; then
        sudo ln -s /etc/nginx/sites-available/staging-proxy /etc/nginx/sites-enabled/
        echo "   ✅ Nginx config enabled"
    else
        echo "   ✅ Nginx config already enabled"
    fi
    
    # Test nginx config
    echo "   Testing nginx configuration..."
    if sudo nginx -t; then
        echo "   ✅ Nginx configuration is valid"
        sudo systemctl reload nginx
        echo "   ✅ Nginx reloaded"
    else
        echo "   ❌ Nginx configuration has errors. Please fix them."
        exit 1
    fi
else
    echo "   ❌ nginx-staging-proxy.conf not found!"
    exit 1
fi

# Step 4: Start services
echo ""
echo "🐳 Step 4: Starting Docker services..."
echo "   Starting production..."
docker-compose up -d || echo "   ⚠️  Production start failed or already running"

echo "   Starting staging..."
docker-compose -f docker-compose.staging.yml up -d --build || echo "   ⚠️  Staging start failed"

# Step 5: Verify
echo ""
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "📋 Verification:"
echo ""
echo "Check production:"
echo "  docker-compose ps"
echo ""
echo "Check staging:"
echo "  docker-compose -f docker-compose.staging.yml ps"
echo ""
echo "Check nginx:"
echo "  sudo systemctl status nginx"
echo ""
echo "🌐 Test URLs:"
echo "  Production: https://indexo.ir"
echo "  Staging:    https://staging.indexo.ir"
echo ""
echo "📝 Next steps:"
echo "  1. Make sure DNS points staging.indexo.ir to your VPS IP"
echo "  2. Test both production and staging URLs"
echo "  3. Check logs if anything doesn't work:"
echo "     docker-compose logs -f"
echo "     docker-compose -f docker-compose.staging.yml logs -f"
echo ""

