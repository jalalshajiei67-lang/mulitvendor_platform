# 🔧 Quick Fix: Run Fake Data Script

## Problem
The file path is wrong - you're trying to read from host filesystem, but the file needs to be inside the container.

## ✅ Solution 1: Check if file exists in container

```bash
# Check if file exists
docker exec multivendor_backend find /app -name "populate_fake_data.py" -type f
```

## ✅ Solution 2: Use Python import method (RECOMMENDED)

```bash
# Method A: Direct import
docker exec -it multivendor_backend python manage.py shell -c "from multivendor_platform.populate_fake_data import main; main()"
```

Or step by step:

```bash
# Enter container shell
docker exec -it multivendor_backend bash

# Inside container, run:
cd /app/multivendor_platform
python manage.py shell
```

Then in Django shell:
```python
from multivendor_platform.populate_fake_data import main
main()
```

## ✅ Solution 3: Copy file to container first

If the file doesn't exist in container, copy it:

```bash
# From your local machine (if you have the file)
docker cp multivendor_platform/multivendor_platform/multivendor_platform/populate_fake_data.py multivendor_backend:/app/multivendor_platform/multivendor_platform/

# Then run
docker exec -it multivendor_backend python manage.py shell < /app/multivendor_platform/multivendor_platform/populate_fake_data.py
```

## ✅ Solution 4: Create file directly in container

```bash
# Enter container
docker exec -it multivendor_backend bash

# Create the file (you'll need to paste the content or use git pull)
cd /app/multivendor_platform
git pull origin staging  # If using git
# OR manually create the file
```

## 🎯 Quickest Method (Try this first):

```bash
docker exec -it multivendor_backend python manage.py shell -c "from multivendor_platform.populate_fake_data import main; main()"
```

If you get `ModuleNotFoundError`, the file doesn't exist in the container. Then use Solution 3 or 4.


