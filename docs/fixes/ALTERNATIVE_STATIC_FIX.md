# Alternative: Add Nginx to Backend Container

Since WhiteNoise causes issues, we can add Nginx to the backend container:

## Option 1: Re-enable WhiteNoise (Safer Version)

In settings_caprover.py, uncomment the WhiteNoise middleware but keep simple storage.

## Option 2: Use Django's Built-in Static Serving (Development Only)

Add to urls.py:
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your urls
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

⚠️ Only for testing! Not recommended for production.

## Option 3: CapRover Nginx Volumes

Map /app/static as a volume that CapRover's Nginx can access.

