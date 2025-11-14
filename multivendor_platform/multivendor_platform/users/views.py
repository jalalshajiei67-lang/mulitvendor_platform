from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import UserProfile, VendorProfile, SellerAd, SellerAdImage, SupplierComment, UserActivity
from .serializers import (
    UserSerializer, UserProfileSerializer, VendorProfileSerializer, 
    SellerAdSerializer, SellerAdImageSerializer, SupplierCommentSerializer, UserActivitySerializer,
    RegisterSerializer, UserDetailSerializer, PasswordChangeSerializer
)
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from products.models import ProductComment
from products.serializers import ProductCommentSerializer

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_activity(user, action, description='', request=None, obj=None):
    """Helper function to log user activity"""
    activity_data = {
        'user': user,
        'action': action,
        'description': description,
    }
    if request:
        activity_data['ip_address'] = get_client_ip(request)
    if obj:
        from django.contrib.contenttypes.models import ContentType
        activity_data['content_type'] = ContentType.objects.get_for_model(obj)
        activity_data['object_id'] = obj.id
    
    UserActivity.objects.create(**activity_data)

def extract_id_list(data, key):
    """
    Normalize multi-value request parameters (supports QueryDict and JSON payloads).
    Returns a list of integers, ignoring blanks and invalid values.
    """
    values = []
    
    if hasattr(data, 'getlist'):
        values = data.getlist(key)
        if not values:
            fallback = data.get(key)
            if isinstance(fallback, (list, tuple, set)):
                values = list(fallback)
            elif fallback not in (None, '', []):
                values = [fallback]
    else:
        raw_value = data.get(key, [])
        if isinstance(raw_value, (list, tuple, set)):
            values = list(raw_value)
        elif raw_value in (None, '', []):
            values = []
        else:
            values = [raw_value]
    
    normalized = []
    for value in values:
        if isinstance(value, (list, tuple, set)):
            normalized.extend(item for item in value if item not in (None, '', []))
        elif value not in (None, '', []):
            normalized.append(value)
    
    result = []
    for item in normalized:
        if isinstance(item, str) and ',' in item:
            parts = [part.strip() for part in item.split(',') if part.strip()]
        else:
            parts = [item]
        for part in parts:
            try:
                result.append(int(part))
            except (TypeError, ValueError):
                continue
    return result

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    User login endpoint
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user:
        # Check if user is blocked
        try:
            if user.profile.is_blocked:
                return Response(
                    {'error': 'Your account has been blocked. Please contact support.'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        except UserProfile.DoesNotExist:
            # Create profile if it doesn't exist (for backward compatibility)
            UserProfile.objects.create(user=user)
        
        token, created = Token.objects.get_or_create(user=user)
        
        # Log login activity
        log_activity(user, 'login', f'User {username} logged in', request)
        
        # Get user profile info
        try:
            profile = user.profile
            vendor_profile = None
            if profile.is_seller():
                try:
                    vendor_profile = {
                        'store_name': user.vendor_profile.store_name,
                        'logo': user.vendor_profile.logo.url if user.vendor_profile.logo else None
                    }
                except VendorProfile.DoesNotExist:
                    pass
            
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                    'role': profile.role,
                    'is_verified': profile.is_verified,
                    'vendor_profile': vendor_profile
                }
            })
        except UserProfile.DoesNotExist:
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                }
            })
    else:
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    User logout endpoint
    """
    try:
        # Log logout activity
        log_activity(request.user, 'logout', f'User {request.user.username} logged out', request)
        
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'})
    except:
        return Response(
            {'error': 'Error logging out'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    User registration endpoint with role selection
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        
        # Log registration activity
        log_activity(user, 'register', f'New user {user.username} registered with role {user.profile.role}', request)
        
        # Get user profile info
        profile = user.profile
        vendor_profile = None
        if profile.is_seller():
            try:
                vendor_profile = {
                    'store_name': user.vendor_profile.store_name if user.vendor_profile.store_name else None,
                    'logo': user.vendor_profile.logo.url if user.vendor_profile.logo else None
                }
            except VendorProfile.DoesNotExist:
                vendor_profile = None
        
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email if user.email and '@placeholder.local' not in user.email else '',
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': profile.role,
                'is_verified': profile.is_verified,
                'vendor_profile': vendor_profile
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """Get current logged-in user details"""
    serializer = UserDetailSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """Update user profile"""
    user = request.user
    profile = user.profile
    
    # Update user basic info
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.email = request.data.get('email', user.email)
    user.save()
    
    # Update profile
    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        
        # Update vendor profile if user is seller
        if profile.is_seller():
            try:
                vendor_profile = user.vendor_profile
                vendor_serializer = VendorProfileSerializer(vendor_profile, data=request.data, partial=True)
                if vendor_serializer.is_valid():
                    vendor_serializer.save()
            except VendorProfile.DoesNotExist:
                pass
        
        # Log activity
        log_activity(user, 'profile_update', f'User {user.username} updated profile', request)
        
        return Response(UserDetailSerializer(user).data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Buyer Dashboard APIs
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buyer_dashboard_view(request):
    """Get buyer dashboard data"""
    user = request.user
    
    # Get orders summary (excluding RFQs)
    orders = Order.objects.filter(buyer=user, is_rfq=False)
    total_orders = orders.count()
    pending_orders = orders.filter(status='pending').count()
    completed_orders = orders.filter(status='delivered').count()
    
    # Get RFQs summary
    rfqs = Order.objects.filter(buyer=user, is_rfq=True)
    total_rfqs = rfqs.count()
    pending_rfqs = rfqs.filter(status='pending').count()
    
    # Get recent orders
    recent_orders = orders.select_related(
        'buyer', 'category'
    ).prefetch_related(
        'items__product', 'images', 'payments'
    )[:5]
    
    # Get reviews
    reviews = ProductComment.objects.filter(author=user)
    
    dashboard_data = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_reviews': reviews.count(),
        'total_rfqs': total_rfqs,
        'pending_rfqs': pending_rfqs,
        'recent_orders': OrderSerializer(recent_orders, many=True, context={'request': request}).data,
    }
    
    return Response(dashboard_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buyer_orders_view(request):
    """Get all buyer orders (including RFQs - filter on frontend)"""
    orders = Order.objects.filter(buyer=request.user).select_related(
        'buyer', 'category'
    ).prefetch_related(
        'items__product', 'images', 'payments'
    ).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buyer_reviews_view(request):
    """Get all buyer reviews"""
    reviews = ProductComment.objects.filter(author=request.user)
    serializer = ProductCommentSerializer(reviews, many=True)
    return Response(serializer.data)

# Seller Dashboard APIs
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def seller_dashboard_view(request):
    """Get seller dashboard data with analytics"""
    user = request.user
    
    # Check if user is seller
    try:
        if not user.profile.is_seller():
            return Response({'error': 'Only sellers can access this endpoint'}, status=status.HTTP_403_FORBIDDEN)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get products
    from products.models import Product
    products = Product.objects.filter(vendor=user)
    total_products = products.count()
    active_products = products.filter(is_active=True).count()
    
    # Get orders for seller's products (check both seller field and product vendor for backward compatibility)
    order_items = OrderItem.objects.filter(
        Q(seller=user) | Q(product__vendor=user)
    )
    total_sales = order_items.aggregate(total=Sum('subtotal'))['total'] or 0
    total_orders = order_items.values('order').distinct().count()
    
    # Get recent orders
    recent_order_ids = order_items.values_list('order', flat=True).distinct()[:5]
    recent_orders = Order.objects.filter(id__in=recent_order_ids).select_related(
        'buyer', 'category'
    ).prefetch_related(
        'items__product', 'images', 'payments'
    )
    
    # Get ads
    ads = SellerAd.objects.filter(seller=user)
    
    # Get reviews on seller's products
    reviews = ProductComment.objects.filter(product__vendor=user)
    
    # Get product views (we'll need to implement view tracking separately)
    # For now, just return 0
    product_views = 0
    
    dashboard_data = {
        'total_products': total_products,
        'active_products': active_products,
        'total_ads': ads.count(),
        'total_sales': float(total_sales),
        'total_orders': total_orders,
        'product_views': product_views,
        'total_reviews': reviews.count(),
        'recent_orders': OrderSerializer(recent_orders, many=True, context={'request': request}).data,
    }
    
    return Response(dashboard_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def seller_orders_view(request):
    """Get all orders for seller's products"""
    # Get order items where seller matches OR product vendor matches (for backward compatibility)
    order_items = OrderItem.objects.filter(
        Q(seller=request.user) | Q(product__vendor=request.user)
    )
    order_ids = order_items.values_list('order', flat=True).distinct()
    orders = Order.objects.filter(id__in=order_ids).select_related(
        'buyer', 'category'
    ).prefetch_related(
        'items__product', 'images', 'payments'
    ).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def seller_reviews_view(request):
    """Get all reviews on seller's products"""
    reviews = ProductComment.objects.filter(product__vendor=request.user)
    serializer = ProductCommentSerializer(reviews, many=True)
    return Response(serializer.data)

# Seller Ads ViewSet
class SellerAdViewSet(viewsets.ModelViewSet):
    serializer_class = SellerAdSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return SellerAd.objects.all()
        return SellerAd.objects.filter(seller=user)
    
    def perform_create(self, serializer):
        ad = serializer.save(seller=self.request.user)
        log_activity(self.request.user, 'create_ad', f'Created ad: {ad.title}', self.request, ad)
    
    def perform_update(self, serializer):
        ad = serializer.save()
        log_activity(self.request.user, 'update_ad', f'Updated ad: {ad.title}', self.request, ad)
    
    def perform_destroy(self, instance):
        log_activity(self.request.user, 'delete_ad', f'Deleted ad: {instance.title}', self.request)
        instance.delete()
    
    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        """Upload image to ad"""
        ad = self.get_object()
        image = request.FILES.get('image')
        alt_text = request.data.get('alt_text', '')
        sort_order = request.data.get('sort_order', 0)
        
        if not image:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        ad_image = SellerAdImage.objects.create(
            ad=ad,
            image=image,
            alt_text=alt_text,
            sort_order=sort_order
        )
        
        serializer = SellerAdImageSerializer(ad_image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Admin Dashboard APIs
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard_view(request):
    """Get admin dashboard data"""
    
    # Get user statistics
    total_users = User.objects.filter(is_staff=False).count()
    buyers = UserProfile.objects.filter(role__in=['buyer', 'both']).count()
    sellers = UserProfile.objects.filter(role__in=['seller', 'both']).count()
    blocked_users = UserProfile.objects.filter(is_blocked=True).count()
    unverified_users = UserProfile.objects.filter(is_verified=False).count()
    
    # Get product statistics
    from products.models import Product
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    pending_products = Product.objects.filter(is_active=False).count()
    
    # Get order statistics
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    completed_orders = Order.objects.filter(status='delivered').count()
    
    # Get RFQ statistics
    total_rfqs = Order.objects.filter(is_rfq=True).count()
    pending_rfqs = Order.objects.filter(is_rfq=True, status='pending').count()
    
    # Get recent activities
    recent_activities = UserActivity.objects.all()[:20]
    
    dashboard_data = {
        'users': {
            'total': total_users,
            'buyers': buyers,
            'sellers': sellers,
            'blocked': blocked_users,
            'unverified': unverified_users
        },
        'products': {
            'total': total_products,
            'active': active_products,
            'pending': pending_products
        },
        'orders': {
            'total': total_orders,
            'pending': pending_orders,
            'completed': completed_orders
        },
        'rfqs': {
            'total': total_rfqs,
            'pending': pending_rfqs
        },
        'recent_activities': UserActivitySerializer(recent_activities, many=True).data
    }
    
    return Response(dashboard_data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_users_view(request):
    """Get all users with filtering"""
    users = User.objects.filter(is_staff=False)
    
    # Filter by role
    role = request.query_params.get('role')
    if role:
        users = users.filter(profile__role=role)
    
    # Filter by blocked status
    is_blocked = request.query_params.get('is_blocked')
    if is_blocked is not None:
        users = users.filter(profile__is_blocked=is_blocked.lower() == 'true')
    
    # Filter by verified status
    is_verified = request.query_params.get('is_verified')
    if is_verified is not None:
        users = users.filter(profile__is_verified=is_verified.lower() == 'true')
    
    serializer = UserDetailSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_block_user_view(request, user_id):
    """Block or unblock a user"""
    try:
        user = User.objects.get(id=user_id)
        profile = user.profile
        
        is_blocked = request.data.get('is_blocked', True)
        profile.is_blocked = is_blocked
        profile.save()
        
        # Log activity
        action_desc = 'blocked' if is_blocked else 'unblocked'
        log_activity(request.user, 'other', f'Admin {action_desc} user {user.username}', request, user)
        
        return Response({'message': f'User {action_desc} successfully'})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_verify_user_view(request, user_id):
    """Verify or unverify a user"""
    try:
        user = User.objects.get(id=user_id)
        profile = user.profile
        
        is_verified = request.data.get('is_verified', True)
        profile.is_verified = is_verified
        profile.save()
        
        # Log activity
        action_desc = 'verified' if is_verified else 'unverified'
        log_activity(request.user, 'other', f'Admin {action_desc} user {user.username}', request, user)
        
        return Response({'message': f'User {action_desc} successfully'})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_change_password_view(request):
    """Admin can change any user's password"""
    serializer = PasswordChangeSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(id=serializer.validated_data['user_id'])
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Log activity
        log_activity(request.user, 'other', f'Admin changed password for user {user.username}', request, user)
        
        return Response({'message': 'Password changed successfully'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_activities_view(request):
    """Get all user activities"""
    activities = UserActivity.objects.all()
    
    # Filter by user
    user_id = request.query_params.get('user_id')
    if user_id:
        activities = activities.filter(user_id=user_id)
    
    # Filter by action
    action = request.query_params.get('action')
    if action:
        activities = activities.filter(action=action)
    
    serializer = UserActivitySerializer(activities[:100], many=True)  # Limit to 100
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def admin_update_order_status_view(request, order_id):
    """Admin can update order status"""
    try:
        order = Order.objects.get(id=order_id)
        new_status = request.data.get('status')
        
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        order.save()
        
        # Log activity
        log_activity(request.user, 'update_order', f'Admin updated order {order.order_number} status to {new_status}', request, order)
        
        return Response(OrderSerializer(order).data)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

# Admin Product Management APIs
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_products_view(request):
    """Get all products with filtering for admin"""
    from products.models import Product
    from products.serializers import ProductSerializer
    
    products = Product.objects.all()
    
    # Filter by category
    category = request.query_params.get('category')
    if category:
        products = products.filter(primary_category_id=category)
    
    # Filter by supplier/vendor
    supplier = request.query_params.get('supplier')
    if supplier:
        products = products.filter(vendor_id=supplier)
    
    # Filter by status
    is_active = request.query_params.get('is_active')
    if is_active is not None:
        products = products.filter(is_active=is_active.lower() == 'true')
    
    # Filter by price range
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Search by name/description
    search = request.query_params.get('search')
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_product_detail_view(request, product_id):
    """Get product detail for admin"""
    from products.models import Product
    from products.serializers import ProductDetailSerializer
    
    try:
        product = Product.objects.get(id=product_id)
        serializer = ProductDetailSerializer(product, context={'request': request})
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_product_bulk_action_view(request):
    """Bulk actions on products (activate/deactivate/delete)"""
    from products.models import Product
    
    action = request.data.get('action')
    product_ids = request.data.get('product_ids', [])
    
    if not action or not product_ids:
        return Response({'error': 'Action and product_ids are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    products = Product.objects.filter(id__in=product_ids)
    
    if action == 'activate':
        products.update(is_active=True)
        log_activity(request.user, 'other', f'Admin activated {products.count()} products', request)
        return Response({'message': f'{products.count()} products activated'})
    elif action == 'deactivate':
        products.update(is_active=False)
        log_activity(request.user, 'other', f'Admin deactivated {products.count()} products', request)
        return Response({'message': f'{products.count()} products deactivated'})
    elif action == 'delete':
        count = products.count()
        products.delete()
        log_activity(request.user, 'other', f'Admin deleted {count} products', request)
        return Response({'message': f'{count} products deleted'})
    else:
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_product_view(request, product_id):
    """Admin can delete any product"""
    from products.models import Product
    
    try:
        product = Product.objects.get(id=product_id)
        product_name = product.name
        product.delete()
        
        # Log activity
        log_activity(request.user, 'delete_product', f'Admin deleted product {product_name}', request)
        
        return Response({'message': 'Product deleted successfully'})
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

# Admin Department Management APIs
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_departments_view(request):
    """Get all departments with filtering for admin"""
    from products.models import Department
    from products.serializers import DepartmentSerializer
    
    departments = Department.objects.all()
    
    # Filter by status
    is_active = request.query_params.get('is_active')
    if is_active is not None:
        departments = departments.filter(is_active=is_active.lower() == 'true')
    
    # Search by name/description
    search = request.query_params.get('search')
    if search:
        departments = departments.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    serializer = DepartmentSerializer(departments, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_department_detail_view(request, department_id):
    """Get department detail for admin"""
    from products.models import Department
    from products.serializers import DepartmentSerializer
    
    try:
        department = Department.objects.get(id=department_id)
        serializer = DepartmentSerializer(department, context={'request': request})
        return Response(serializer.data)
    except Department.DoesNotExist:
        return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_create_department_view(request):
    """Admin can create a department"""
    from products.models import Department
    from products.serializers import DepartmentSerializer
    
    serializer = DepartmentSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        department = serializer.save()
        log_activity(request.user, 'other', f'Admin created department {department.name}', request, department)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def admin_update_department_view(request, department_id):
    """Admin can update a department"""
    from products.models import Department
    from products.serializers import DepartmentSerializer
    
    try:
        department = Department.objects.get(id=department_id)
        serializer = DepartmentSerializer(department, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            log_activity(request.user, 'other', f'Admin updated department {department.name}', request, department)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Department.DoesNotExist:
        return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_department_view(request, department_id):
    """Admin can delete a department"""
    from products.models import Department
    
    try:
        department = Department.objects.get(id=department_id)
        department_name = department.name
        department.delete()
        log_activity(request.user, 'other', f'Admin deleted department {department_name}', request)
        return Response({'message': 'Department deleted successfully'})
    except Department.DoesNotExist:
        return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

# Admin Category Management APIs
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_categories_view(request):
    """Get all categories with filtering for admin"""
    from products.models import Category
    from products.serializers import CategorySerializer
    
    categories = Category.objects.all()
    
    # Filter by department
    department = request.query_params.get('department')
    if department:
        categories = categories.filter(departments__id=department)
    
    # Filter by status
    is_active = request.query_params.get('is_active')
    if is_active is not None:
        categories = categories.filter(is_active=is_active.lower() == 'true')
    
    # Search by name/description
    search = request.query_params.get('search')
    if search:
        categories = categories.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    serializer = CategorySerializer(categories, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_category_detail_view(request, category_id):
    """Get category detail for admin"""
    from products.models import Category
    from products.serializers import CategorySerializer
    
    try:
        category = Category.objects.get(id=category_id)
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_create_category_view(request):
    """Admin can create a category"""
    from products.models import Category
    from products.serializers import CategorySerializer
    
    serializer = CategorySerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        category = serializer.save()
        # Handle departments M2M relationship
        departments = extract_id_list(request.data, 'departments')
        if departments or ('departments' in request.data):
            category.departments.set(departments)
        log_activity(request.user, 'other', f'Admin created category {category.name}', request, category)
        response_data = CategorySerializer(category, context={'request': request}).data
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def admin_update_category_view(request, category_id):
    """Admin can update a category"""
    from products.models import Category
    from products.serializers import CategorySerializer
    
    try:
        category = Category.objects.get(id=category_id)
        serializer = CategorySerializer(category, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            # Handle departments M2M relationship
            if 'departments' in request.data or (hasattr(request.data, 'getlist') and request.data.getlist('departments')):
                departments = extract_id_list(request.data, 'departments')
                category.departments.set(departments)
            log_activity(request.user, 'other', f'Admin updated category {category.name}', request, category)
            response_data = CategorySerializer(category, context={'request': request}).data
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_category_view(request, category_id):
    """Admin can delete a category"""
    from products.models import Category
    
    try:
        category = Category.objects.get(id=category_id)
        category_name = category.name
        category.delete()
        log_activity(request.user, 'other', f'Admin deleted category {category_name}', request)
        return Response({'message': 'Category deleted successfully'})
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

# Admin Subcategory Management APIs
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_subcategories_view(request):
    """Get all subcategories with filtering for admin"""
    from products.models import Subcategory
    from products.serializers import SubcategorySerializer
    
    subcategories = Subcategory.objects.all()
    
    # Filter by category
    category = request.query_params.get('category')
    if category:
        subcategories = subcategories.filter(categories__id=category)
    
    # Filter by status
    is_active = request.query_params.get('is_active')
    if is_active is not None:
        subcategories = subcategories.filter(is_active=is_active.lower() == 'true')
    
    # Search by name/description
    search = request.query_params.get('search')
    if search:
        subcategories = subcategories.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    serializer = SubcategorySerializer(subcategories, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_subcategory_detail_view(request, subcategory_id):
    """Get subcategory detail for admin"""
    from products.models import Subcategory
    from products.serializers import SubcategorySerializer
    
    try:
        subcategory = Subcategory.objects.get(id=subcategory_id)
        serializer = SubcategorySerializer(subcategory, context={'request': request})
        return Response(serializer.data)
    except Subcategory.DoesNotExist:
        return Response({'error': 'Subcategory not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_create_subcategory_view(request):
    """Admin can create a subcategory"""
    from products.models import Subcategory
    from products.serializers import SubcategorySerializer
    
    serializer = SubcategorySerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        subcategory = serializer.save()
        # Handle categories M2M relationship
        categories = extract_id_list(request.data, 'categories')
        if categories or ('categories' in request.data):
            subcategory.categories.set(categories)
        log_activity(request.user, 'other', f'Admin created subcategory {subcategory.name}', request, subcategory)
        response_data = SubcategorySerializer(subcategory, context={'request': request}).data
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def admin_update_subcategory_view(request, subcategory_id):
    """Admin can update a subcategory"""
    from products.models import Subcategory
    from products.serializers import SubcategorySerializer
    
    try:
        subcategory = Subcategory.objects.get(id=subcategory_id)
        serializer = SubcategorySerializer(subcategory, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            # Handle categories M2M relationship
            if 'categories' in request.data or (hasattr(request.data, 'getlist') and request.data.getlist('categories')):
                categories = extract_id_list(request.data, 'categories')
                subcategory.categories.set(categories)
            log_activity(request.user, 'other', f'Admin updated subcategory {subcategory.name}', request, subcategory)
            response_data = SubcategorySerializer(subcategory, context={'request': request}).data
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Subcategory.DoesNotExist:
        return Response({'error': 'Subcategory not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_subcategory_view(request, subcategory_id):
    """Admin can delete a subcategory"""
    from products.models import Subcategory
    
    try:
        subcategory = Subcategory.objects.get(id=subcategory_id)
        subcategory_name = subcategory.name
        subcategory.delete()
        log_activity(request.user, 'other', f'Admin deleted subcategory {subcategory_name}', request)
        return Response({'message': 'Subcategory deleted successfully'})
    except Subcategory.DoesNotExist:
        return Response({'error': 'Subcategory not found'}, status=status.HTTP_404_NOT_FOUND)


# ===== SUPPLIER / VENDOR VIEWSETS =====

class SupplierViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving suppliers (vendors)
    Public access - read only
    """
    queryset = VendorProfile.objects.filter(is_approved=True).order_by('store_name')
    serializer_class = VendorProfileSerializer
    
    def get_permissions(self):
        """All actions are public (read-only)"""
        return []
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get all products from a specific supplier"""
        supplier = self.get_object()
        from products.models import Product
        from products.serializers import ProductSerializer
        
        products = Product.objects.filter(vendor=supplier.user, is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for a specific supplier"""
        supplier = self.get_object()
        comments = supplier.comments.filter(is_approved=True)
        serializer = SupplierCommentSerializer(comments, many=True)
        return Response(serializer.data)


class SupplierCommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for supplier comments
    - List and retrieve: Public
    - Create: Authenticated users
    - Update/Delete: Only comment owner or admin
    """
    queryset = SupplierComment.objects.filter(is_approved=True)
    serializer_class = SupplierCommentSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Set the user to the current user when creating a comment"""
        serializer.save(user=self.request.user)
        
        # Log activity
        log_activity(self.request.user, 'other', 'User created a supplier comment', self.request)


# ===== ADMIN BLOG MANAGEMENT =====

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_blog_posts_view(request):
    """Get all blog posts with filtering for admin"""
    from blog.models import BlogPost
    from blog.serializers import BlogPostListSerializer
    
    posts = BlogPost.objects.all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.query_params.get('status')
    if status_filter:
        posts = posts.filter(status=status_filter)
    
    # Filter by category
    category = request.query_params.get('category')
    if category:
        posts = posts.filter(category__id=category)
    
    # Search by title/content
    search = request.query_params.get('search')
    if search:
        posts = posts.filter(
            Q(title__icontains=search) | 
            Q(content__icontains=search) |
            Q(excerpt__icontains=search)
        )
    
    serializer = BlogPostListSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_blog_categories_view(request):
    """Get all blog categories with filtering for admin"""
    from blog.models import BlogCategory
    from blog.serializers import BlogCategorySerializer
    
    categories = BlogCategory.objects.all()
    
    # Search by name/description
    search = request.query_params.get('search')
    if search:
        categories = categories.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    serializer = BlogCategorySerializer(categories, many=True, context={'request': request})
    return Response(serializer.data)
