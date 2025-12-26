from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from .models import Order, OrderItem, OrderImage, OrderVendorView
from .serializers import OrderSerializer, CreateRFQSerializer, AdminCreateRFQSerializer
from products.models import Product, Category
from gamification.services import GamificationService
from users.models import Supplier, VendorSubscription

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
    rfqs = Order.objects.filter(is_rfq=True).select_related('buyer', 'category').prefetch_related('items__product', 'images', 'suppliers').order_by('-created_at')
    
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
        rfq = Order.objects.filter(is_rfq=True, id=rfq_id).select_related('buyer', 'category').prefetch_related('items__product', 'images', 'suppliers').first()
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
    Also includes RFQs where the vendor's suppliers are selected
    """
    # Get products owned by this vendor
    vendor_products = Product.objects.filter(vendor=request.user, is_active=True)
    vendor_category_ids = vendor_products.values_list('primary_category_id', flat=True)
    
    # Get suppliers managed by this vendor
    vendor_suppliers = Supplier.objects.filter(vendor=request.user, is_active=True)
    
    # Get RFQs for:
    # - free leads (is_free=True)
    # - product owned by vendor
    # - category matches vendor products
    # - explicitly assigned suppliers
    # Exclude RFQs already revealed by this vendor
    viewed_ids = OrderVendorView.objects.filter(vendor=request.user).values_list('order_id', flat=True)

    rfqs = Order.objects.filter(is_rfq=True).exclude(id__in=viewed_ids).filter(
        Q(is_free=True)
        | Q(items__product__in=vendor_products)
        | (Q(items__product__isnull=True) & Q(category_id__in=vendor_category_ids))
        | Q(suppliers__in=vendor_suppliers)
    ).select_related('buyer', 'category').prefetch_related('items__product', 'images', 'suppliers').distinct()
    
    # Filter by status if provided
    status_filter = request.query_params.get('status', None)
    if status_filter:
        rfqs = rfqs.filter(status=status_filter)
    
    serializer = OrderSerializer(
        rfqs,
        many=True,
        context={
            'request': request,
            'show_full_contact': False,
            'contact_revealed': False,
            'viewed_order_ids': set(viewed_ids)
        }
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendor_rfq_my_list_view(request):
    """
    Get RFQs that the vendor has already revealed (My Customers)
    """
    viewed_ids = OrderVendorView.objects.filter(vendor=request.user).values_list('order_id', flat=True)

    vendor_products = Product.objects.filter(vendor=request.user, is_active=True)
    vendor_category_ids = vendor_products.values_list('primary_category_id', flat=True)
    vendor_suppliers = Supplier.objects.filter(vendor=request.user, is_active=True)

    rfqs = Order.objects.filter(is_rfq=True, id__in=viewed_ids).filter(
        Q(is_free=True)
        | Q(items__product__in=vendor_products)
        | (Q(items__product__isnull=True) & Q(category_id__in=vendor_category_ids))
        | Q(suppliers__in=vendor_suppliers)
    ).select_related('buyer', 'category').prefetch_related('items__product', 'images', 'suppliers').distinct()

    serializer = OrderSerializer(
        rfqs,
        many=True,
        context={
            'request': request,
            'show_full_contact': True,
            'contact_revealed': True,
            'viewed_order_ids': set(viewed_ids)
        }
    )
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_create_rfq_view(request):
    """
    Admin endpoint to create manual RFQ/lead
    Supports multipart/form-data for image uploads
    Auto-matches suppliers based on category/product if supplier_ids not provided
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
        
        # Handle supplier_ids from FormData (can be multiple values with same key)
        supplier_ids = []
        if 'supplier_ids' in data:
            supplier_ids_raw = data.getlist('supplier_ids') if hasattr(data, 'getlist') else data.get('supplier_ids', [])
            if isinstance(supplier_ids_raw, list):
                supplier_ids = [int(id) for id in supplier_ids_raw if id]
            elif supplier_ids_raw:
                supplier_ids = [int(supplier_ids_raw)]
        
        # Remove supplier_ids from data before validation
        if 'supplier_ids' in data:
            if hasattr(data, 'getlist'):
                # FormData - remove all occurrences
                data = data.copy()
                data.pop('supplier_ids', None)
            else:
                data.pop('supplier_ids', None)
        
        serializer = AdminCreateRFQSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            validated_data = serializer.validated_data.copy()
            category_id = validated_data.pop('category_id')
            product_id = validated_data.pop('product_id', None)
            is_free = validated_data.pop('is_free', False)
            
            # Get category
            category = None
            if category_id:
                category = Category.objects.get(id=category_id)
            elif not is_free:
                return Response({'error': 'Category is required for non-free leads'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Get product if provided
            product = None
            if product_id:
                product = Product.objects.get(id=product_id)
                is_free = False  # product-specific leads are not free
            
            # Auto-match suppliers if not provided
            matched_suppliers = []
            if not supplier_ids and not is_free:
                # Find suppliers that have products in this category
                if product:
                    # If product is provided, get supplier from product
                    if product.supplier and product.supplier.is_active:
                        matched_suppliers.append(product.supplier)
                else:
                    # Find all suppliers with products in this category
                    products_in_category = Product.objects.filter(
                        primary_category=category,
                        is_active=True,
                        supplier__is_active=True
                    ).select_related('supplier')
                    matched_suppliers = list(set([p.supplier for p in products_in_category if p.supplier]))
            else:
                # Use provided supplier IDs
                matched_suppliers = list(Supplier.objects.filter(id__in=supplier_ids, is_active=True))
            
            # Create RFQ order
            order = Order.objects.create(
                buyer=None,  # Manual leads don't have a buyer user
                is_rfq=True,
                is_free=is_free,
                status='pending',
                category=category,
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                company_name=validated_data['company_name'],
                phone_number=validated_data['phone_number'],
                email=validated_data.get('email'),
                unique_needs=validated_data.get('unique_needs', ''),
                lead_source=validated_data['lead_source']
            )
            
            # Add suppliers to the order
            if matched_suppliers:
                order.suppliers.set(matched_suppliers)
            
            # Create order item if product is provided
            if product:
                from decimal import Decimal
                product_price = Decimal(str(product.price)) if product.price else Decimal('0')
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=1,
                    price=product_price
                )
            
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
        print(f"Admin RFQ Creation Error: {error_detail}")
        print(f"Traceback: {traceback_str}")
        return Response(
            {'error': f'Server error: {error_detail}', 'detail': traceback_str},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vendor_rfq_reveal_view(request, rfq_id):
    """
    Reveal full contact info for an RFQ if the vendor is eligible to view it.
    Eligibility:
      - Free lead (is_free=True)
      - Vendor owns the product linked to the RFQ
      - Vendor has a product in the RFQ category
      - Vendor is explicitly selected as supplier
    """
    # #region agent log
    import json
    try:
        with open('/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({
                'sessionId': 'debug-session',
                'runId': 'run1',
                'hypothesisId': 'A',
                'location': 'orders/views.py:360',
                'message': 'vendor_rfq_reveal_view entry',
                'data': {'rfq_id': rfq_id, 'user_id': request.user.id if request.user.is_authenticated else None},
                'timestamp': int(__import__('time').time() * 1000)
            }) + '\n')
    except: pass
    # #endregion
    rfq = Order.objects.filter(is_rfq=True, id=rfq_id).select_related('buyer', 'category').prefetch_related('items__product', 'images', 'suppliers').first()
    if not rfq:
        return Response({'detail': 'RFQ not found'}, status=status.HTTP_404_NOT_FOUND)

    vendor_products = Product.objects.filter(vendor=request.user, is_active=True)
    vendor_category_ids = set(vendor_products.values_list('primary_category_id', flat=True))
    vendor_suppliers = Supplier.objects.filter(vendor=request.user, is_active=True)

    owns_product = rfq.items.filter(product__vendor=request.user).exists()
    has_product = rfq.items.filter(product__isnull=False).exists()
    matches_category = not has_product and rfq.category_id in vendor_category_ids if rfq.category_id else False
    is_selected_supplier = rfq.suppliers.filter(id__in=vendor_suppliers).exists()

    if not (rfq.is_free or owns_product or matches_category or is_selected_supplier):
        return Response({'detail': 'You are not allowed to view this lead'}, status=status.HTTP_403_FORBIDDEN)

    # #region agent log
    try:
        with open('/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({
                'sessionId': 'debug-session',
                'runId': 'run1',
                'hypothesisId': 'A',
                'location': 'orders/views.py:385',
                'message': 'Before VendorSubscription.for_user call',
                'data': {'user_id': request.user.id},
                'timestamp': int(__import__('time').time() * 1000)
            }) + '\n')
    except: pass
    # #endregion
    subscription = VendorSubscription.for_user(request.user)
    existing_view = OrderVendorView.objects.filter(order=rfq, vendor=request.user).first()
    can_unlock, next_unlock_at = subscription.can_unlock_customer()

    # Enforce daily unlock limit only for new reveals
    if not existing_view and not can_unlock:
        return Response(
            {
                'detail': 'حداکثر یک مشتری جدید در هر ۲۴ ساعت برای پلن رایگان مجاز است.',
                'next_unlock_at': next_unlock_at,
                'tier': subscription.tier.slug,
            },
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    if not rfq.first_viewed_at:
        rfq.first_viewed_at = timezone.now()
        rfq.save(update_fields=['first_viewed_at'])

    if not existing_view:
        OrderVendorView.objects.create(order=rfq, vendor=request.user)
        subscription.register_customer_unlock()
        # After registering, compute the next window for client display
        can_unlock, next_unlock_at = subscription.can_unlock_customer()

    serializer = OrderSerializer(
        rfq,
        context={
            'request': request,
            'show_full_contact': True,
            'contact_revealed': True
        }
    )
    data = serializer.data
    data['subscription'] = {
        'tier_slug': subscription.tier.slug,
        'tier_name': subscription.tier.name,
        'daily_customer_unlock_limit': subscription.tier.daily_customer_unlock_limit,
        'can_unlock_now': can_unlock,
        'next_unlock_at': next_unlock_at,
        'last_customer_unlock_at': subscription.last_customer_unlock_at,
    }
    data['lead_shared'] = subscription.tier.lead_exclusivity == 'shared'
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def track_order_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    service = GamificationService.for_user(request.user)
    service.register_order_view(order)
    return Response({'first_viewed_at': order.first_viewed_at})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def track_order_response(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    service = GamificationService.for_user(request.user)
    service.register_order_response(order)
    return Response({
        'first_responded_at': order.first_responded_at,
        'response_points_awarded': order.response_points_awarded,
        'response_speed_bucket': order.response_speed_bucket,
    })
