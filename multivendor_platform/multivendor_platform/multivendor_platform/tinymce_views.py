# TinyMCE image upload views
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.conf import settings
import os
from datetime import datetime
from PIL import Image
import uuid
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


@csrf_exempt
@require_http_methods(["POST"])
def tinymce_image_upload(request):
    """
    Handle image uploads from TinyMCE editor.
    Returns JSON response with image URL for TinyMCE to use.
    """
    if 'file' not in request.FILES:
        return JsonResponse({
            'error': 'No file provided'
        }, status=400)
    
    uploaded_file = request.FILES['file']
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
    if uploaded_file.content_type not in allowed_types:
        return JsonResponse({
            'error': f'Invalid file type. Allowed types: {", ".join(allowed_types)}'
        }, status=400)
    
    # Validate file size (max 5MB)
    max_size = 5 * 1024 * 1024  # 5MB
    if uploaded_file.size > max_size:
        return JsonResponse({
            'error': 'File size exceeds 5MB limit'
        }, status=400)
    
    try:
        # Generate unique filename
        file_ext = os.path.splitext(uploaded_file.name)[1]
        unique_filename = f"tinymce/{datetime.now().strftime('%Y/%m')}/{uuid.uuid4()}{file_ext}"
        
        # Optionally optimize image before saving
        file_to_save = uploaded_file
        try:
            # Open and verify image
            uploaded_file.seek(0)
            image = Image.open(uploaded_file)
            
            # Convert RGBA to RGB if necessary (for JPEG)
            if image.mode == 'RGBA' and file_ext.lower() in ['.jpg', '.jpeg']:
                rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[3])  # Use alpha channel as mask
                image = rgb_image
            
            # Resize if too large (max 2000px on longest side)
            max_dimension = 2000
            if max(image.size) > max_dimension:
                ratio = max_dimension / max(image.size)
                new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Save optimized image to temporary file
            output = BytesIO()
            # Determine format
            if file_ext.lower() in ['.jpg', '.jpeg']:
                img_format = 'JPEG'
                image.save(output, format=img_format, quality=85, optimize=True)
            elif file_ext.lower() == '.png':
                img_format = 'PNG'
                image.save(output, format=img_format, optimize=True)
            elif file_ext.lower() == '.webp':
                img_format = 'WEBP'
                image.save(output, format=img_format, quality=85, optimize=True)
            else:
                img_format = image.format or 'PNG'
                image.save(output, format=img_format, optimize=True)
            
            output.seek(0)
            # Create new file object
            file_to_save = InMemoryUploadedFile(
                output, None, unique_filename, f'image/{img_format.lower()}',
                sys.getsizeof(output), None
            )
        except Exception as e:
            # If image processing fails, use original file
            # This allows non-image files or corrupted images to still be saved
            uploaded_file.seek(0)
            file_to_save = uploaded_file
        
        # Save file (either optimized or original)
        file_path = default_storage.save(unique_filename, file_to_save)
        
        # Get full URL
        if hasattr(settings, 'MEDIA_URL'):
            media_url = settings.MEDIA_URL
        else:
            media_url = '/media/'
        
        # Ensure media_url ends with /
        if not media_url.endswith('/'):
            media_url += '/'
        
        # Build absolute URL using request.build_absolute_uri for proper URL construction
        image_url = request.build_absolute_uri(media_url + file_path)
        
        return JsonResponse({
            'location': image_url
        })
    
    except Exception as e:
        return JsonResponse({
            'error': f'Upload failed: {str(e)}'
        }, status=500)
