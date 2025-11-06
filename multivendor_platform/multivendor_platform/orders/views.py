from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q
from .models import Order, OrderItem, OrderImage
from .serializers import OrderSerializer, CreateRFQSerializer
from products.models import Product, Category

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow anonymous submissions
def create_rfq_view(request):
    """
    Create a Request for Quotation (RFQ)
    Allows anonymous submissions
    Supports multipart/form-data for image uploads
    """
    try:
        # Handle both JSON and multipart/form-data
        data = request.data.copy()
        
        # Extract images from request.FILES
        images = []
        for key in request.FILES:
            if 'images' in key.lower() or 'image' in key.lower():
                file_obj = request.FILES[key]
                if hasattr(file_obj, 'content_type') and file_obj.content_type.startswith('image/'):
                    images.append(file_obj)
        
        # Validate image count
        if len(images) > 10:
            return Response(
                {'error': 'Maximum 10 images allowed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = CreateRFQSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            order = serializer.save()
            
            # Create order images
            for image_file in images:
                OrderImage.objects.create(
                    order=order,
                    image=image_file
                )
            
            response_serializer = OrderSerializer(order, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        import traceback
        error_detail = str(e)
        traceback_str = traceback.format_exc()
        print(f"RFQ Creation Error: {error_detail}")
        print(f"Traceback: {traceback_str}")
        return Response(
            {'error': f'Server error: {error_detail}', 'detail': traceback_str},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_rfq_list_view(request):
    """
    Get all RFQ orders for admin dashboard
    """
    rfqs = Order.objects.filter(is_rfq=True).select_related('buyer', 'category').prefetch_related('items__product', 'images')
    
    # Filter by status if provided
    status_filter = request.query_params.get('status', None)
    if status_filter:
        rfqs = rfqs.filter(status=status_filter)
    
    # Filter by category if provided
    category_id = request.query_params.get('category', None)
    if category_id:
        rfqs = rfqs.filter(category_id=category_id)
    
    # Filter by product if provided
    product_id = request.query_params.get('product', None)
    if product_id:
        rfqs = rfqs.filter(items__product_id=product_id).distinct()
    
    # Search filter
    search = request.query_params.get('search', None)
    if search:
        rfqs = rfqs.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(company_name__icontains=search) |
            Q(items__product_name__icontains=search)
        ).distinct()
    
    serializer = OrderSerializer(rfqs, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_rfq_detail_view(request, rfq_id):
    """
    Get RFQ detail for admin
    """
    try:
        rfq = Order.objects.filter(is_rfq=True, id=rfq_id).select_related('buyer', 'category').prefetch_related('items__product', 'images').first()
        if not rfq:
            return Response({'error': 'RFQ not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(rfq, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'error': 'RFQ not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendor_rfq_list_view(request):
    """
    Get RFQs for products that belong to the authenticated vendor
    """
    # Get products owned by this vendor
    vendor_products = Product.objects.filter(vendor=request.user)
    
    # Get RFQs for these products
    rfqs = Order.objects.filter(
        is_rfq=True,
        items__product__in=vendor_products
    ).select_related('buyer', 'category').prefetch_related('items__product', 'images').distinct()
    
    # Filter by status if provided
    status_filter = request.query_params.get('status', None)
    if status_filter:
        rfqs = rfqs.filter(status=status_filter)
    
    serializer = OrderSerializer(rfqs, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_update_rfq_status_view(request, rfq_id):
    """
    Update RFQ status (admin only)
    """
    try:
        rfq = Order.objects.get(is_rfq=True, id=rfq_id)
        new_status = request.data.get('status')
        
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        rfq.status = new_status
        rfq.save()
        
        serializer = OrderSerializer(rfq, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'error': 'RFQ not found'}, status=status.HTTP_404_NOT_FOUND)
