# 🔍 SSH Commands to Check Staging Deployment

## Quick Check Commands

Run these commands via SSH to check your staging deployment status:

```bash
# SSH to your VPS
ssh your-user@your-vps-ip

# Then run these commands:
```

### 1. Check if Traefik Network Exists

```bash
docker network inspect multivendor_network
```

**Expected output if network exists:**
```json
[
    {
        "Name": "multivendor_network",
        ...
    }
]
```

**If network doesn't exist, you'll see:**
```
Error: No such network: multivendor_network
```

### 2. Create Network if Missing

```bash
docker network create multivendor_network --driver bridge
```

### 3. Check Staging Containers Status

```bash
cd /path/to/your/project
docker-compose -f docker-compose.staging.yml ps
```

### 4. Check Staging Logs

```bash
cd /path/to/your/project
docker-compose -f docker-compose.staging.yml logs --tail=50
```

### 5. Check if Production is Running (creates the network)

```bash
cd /path/to/your/project
docker-compose ps
```

### 6. Check All Docker Networks

```bash
docker network ls | grep multivendor
```

### 7. Check What's Using the Network

```bash
docker network inspect multivendor_network --format '{{range .Containers}}{{.Name}} {{end}}'
```

## 🔧 Fix Network Issue

If network doesn't exist, run:

```bash
# Create the network
docker network create multivendor_network --driver bridge

# Then try staging deployment again
cd /path/to/your/project
docker-compose -f docker-compose.staging.yml up -d --build
```

## 📋 Complete Diagnostic Script

Run this to check everything:

```bash
#!/bin/bash
echo "=== Checking Traefik Network ==="
if docker network inspect multivendor_network >/dev/null 2>&1; then
    echo "✅ Network 'multivendor_network' exists"
else
    echo "❌ Network 'multivendor_network' NOT found"
    echo "Creating network..."
    docker network create multivendor_network --driver bridge
    echo "✅ Network created"
fi

echo ""
echo "=== Checking Production Status ==="
cd /path/to/your/project
if docker-compose ps | grep -q "traefik"; then
    echo "✅ Production Traefik is running"
else
    echo "⚠️  Production Traefik is NOT running"
fi

echo ""
echo "=== Checking Staging Status ==="
if docker-compose -f docker-compose.staging.yml ps | grep -q "staging"; then
    echo "✅ Staging containers exist"
    docker-compose -f docker-compose.staging.yml ps
else
    echo "❌ No staging containers found"
fi
```

## 🚀 Quick Fix Command

One-liner to fix the network issue:

```bash
docker network create multivendor_network --driver bridge || echo "Network already exists"
```

