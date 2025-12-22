#!/bin/bash
# Quick script to find the project directory on VPS

echo "Searching for docker-compose files..."
echo ""

# Search in common locations
SEARCH_PATHS=(
    "/root"
    "/opt"
    "/home"
    "/var/www"
)

FOUND=0

for path in "${SEARCH_PATHS[@]}"; do
    if [ -d "$path" ]; then
        echo "Searching in $path..."
        RESULT=$(find "$path" -maxdepth 4 -name "docker-compose*.yml" 2>/dev/null)
        if [ -n "$RESULT" ]; then
            echo "$RESULT" | while read file; do
                echo "  ✅ Found: $file"
                echo "     Directory: $(dirname "$file")"
                FOUND=1
            done
        fi
    fi
done

# Also check current directory and common project names
echo ""
echo "Checking common project directories..."
for dir in "/root/indexo-production" "/root/mulitvendor_platform" "/opt/mulitvendor_platform"; do
    if [ -d "$dir" ]; then
        echo "Checking $dir..."
        if [ -f "$dir/docker-compose.production.yml" ] || [ -f "$dir/docker-compose.yml" ]; then
            echo "  ✅ Found project in: $dir"
            FOUND=1
        fi
    fi
done

echo ""
if [ $FOUND -eq 0 ]; then
    echo "❌ No docker-compose files found!"
    echo ""
    echo "Try running manually:"
    echo "  find / -name 'docker-compose.production.yml' 2>/dev/null"
    echo "  find / -name 'docker-compose.yml' 2>/dev/null"
else
    echo "✅ Project directories found above!"
    echo ""
    echo "To run the recovery script:"
    echo "  cd <directory-from-above>"
    echo "  bash /root/crisis-recovery-production.sh"
fi

