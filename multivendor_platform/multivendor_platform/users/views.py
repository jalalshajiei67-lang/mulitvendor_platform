from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum, Avg, Prefetch
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import (
    UserProfile, VendorProfile, SellerAd, SellerAdImage, SupplierComment, UserActivity,
    SupplierPortfolioItem, SupplierTeamMember, SupplierContactMessage, VendorSubscription,
    PricingTier, SellerContact, ContactNote, ContactTask
)
from .serializers import (
    UserSerializer, UserProfileSerializer, VendorProfileSerializer, 
    SellerAdSerializer, SellerAdImageSerializer, SupplierCommentSerializer, UserActivitySerializer,
    RegisterSerializer, UserDetailSerializer, PasswordChangeSerializer,
    SupplierPortfolioItemSerializer, SupplierTeamMemberSerializer, SupplierContactMessageSerializer,
    OTPRequestSerializer, OTPVerifySerializer, PasswordResetSerializer,
    SellerContactSerializer, ContactNoteSerializer, ContactTaskSerializer
)
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from products.models import ProductComment
from products.serializers import ProductCommentSerializer
from .services.otp_service import OTPService

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
@csrf_exempt
def login_view(request):
    """
    User login endpoint
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    # DEBUG: Log incoming request
    print(f"\n{'='*60}")
    print(f"LOGIN ATTEMPT")
    print(f"Username: {username}")
    print(f"Password provided: {'Yes' if password else 'No'}")
    print(f"Request method: {request.method}")
    print(f"Content-Type: {request.META.get('CONTENT_TYPE')}")
    print(f"Origin: {request.META.get('HTTP_ORIGIN')}")
    print(f"{'='*60}\n")
    
    if not username or not password:
        print("❌ Missing username or password")
        return Response(
            {'error': 'لطفاً نام کاربری و رمز عبور را وارد کنید.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    print(f"Authentication result: {'Success' if user else 'Failed'}")
    
    if user:
        # Check if user is blocked
        try:
            if user.profile.is_blocked:
                print(f"❌ User {username} is BLOCKED")
                return Response(
                    {'error': 'حساب کاربری شما مسدود شده است. برای رفع مشکل با پشتیبانی تماس بگیرید.'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            else:
                print(f"✅ User {username} is NOT blocked")
        except UserProfile.DoesNotExist:
            print(f"⚠️  User {username} has no profile - creating one")
            # Create profile if it doesn't exist (for backward compatibility)
            UserProfile.objects.create(user=user)
        
        token, created = Token.objects.get_or_create(user=user)
        
        # Log login activity
        log_activity(user, 'login', f'User {username} logged in', request)
        
        # Get user profile info using serializer for consistent data structure
        try:
            # Use UserDetailSerializer to get complete user data including full vendor_profile
            user_serializer = UserDetailSerializer(user)
            user_data = user_serializer.data
            
            # Extract role and is_verified from profile for backward compatibility
            profile = user.profile
            user_data['role'] = profile.role
            user_data['is_verified'] = profile.is_verified
            
            return Response({
                'token': token.key,
                'user': user_data
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
            {'error': 'نام کاربری یا رمز عبور اشتباه است. لطفاً دوباره تلاش کنید.'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    User logout endpoint - optimized for speed
    """
    try:
        # Store user info before deleting token (needed for logging)
        user_id = request.user.id
        username = request.user.username
        
        # Delete token first (critical operation)
        request.user.auth_token.delete()
        
        # Log activity asynchronously after response (fire-and-forget)
        # Use threading to avoid blocking the response
        import threading
        # Extract request data before passing to thread (request object is not thread-safe)
        ip_address = get_client_ip(request) if request else None
        
        def log_logout_async():
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(id=user_id)
                # Create minimal activity data without request object
                activity_data = {
                    'user': user,
                    'action': 'logout',
                    'description': f'User {username} logged out',
                    'ip_address': ip_address
                }
                UserActivity.objects.create(**activity_data)
            except Exception:
                # Silently fail if logging fails - don't block logout
                pass
        
        # Start logging in background thread
        threading.Thread(target=log_logout_async, daemon=True).start()
        
        return Response({'message': 'Successfully logged out'})
    except Exception as e:
        # Even if token deletion fails, return success to allow frontend cleanup
        return Response({'message': 'Logged out'})

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def otp_request_view(request):
    """
    Request OTP endpoint
    """
    serializer = OTPRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    phone = serializer.validated_data.get('phone')
    username = serializer.validated_data.get('username')
    purpose = serializer.validated_data['purpose']
    
    # Get user if username provided
    user = None
    if username:
        try:
            user = User.objects.get(username=username)
            # Use phone from user profile if phone not provided
            if not phone:
                try:
                    phone = user.profile.phone or user.username
                except:
                    phone = user.username
        except User.DoesNotExist:
            return Response(
                {'error': 'کاربری با این نام کاربری یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    # Use phone or user for OTP generation
    user_or_phone = user if user else phone
    
    try:
        otp_service = OTPService()
        result = otp_service.generate_otp(user_or_phone, purpose)
        
        response_data = {
            'success': True,
            'message': 'کد تأیید با موفقیت ارسال شد. لطفاً پیامک دریافتی را بررسی کنید.'
        }
        
        # In local/dev mode, include the OTP code in response
        if 'code' in result:
            response_data['otp_code'] = result['code']
            response_data['message'] = 'کد تأیید برای شما آماده است (حالت تست)'
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except ValueError as e:
        return Response(
            {
                'error': str(e),
                'helpful_message': 'اگر مشکل ادامه داشت، لطفاً با پشتیبانی تماس بگیرید.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error generating OTP: {str(e)}", exc_info=True)
        return Response(
            {
                'error': 'متأسفانه در ارسال کد تأیید مشکلی پیش آمده است.',
                'helpful_message': 'لطفاً چند لحظه صبر کنید و دوباره تلاش کنید. اگر مشکل ادامه داشت، با پشتیبانی تماس بگیرید.'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def otp_verify_view(request):
    """
    Verify OTP endpoint
    """
    serializer = OTPVerifySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    phone = serializer.validated_data.get('phone')
    username = serializer.validated_data.get('username')
    code = serializer.validated_data['code']
    purpose = serializer.validated_data['purpose']
    first_name = serializer.validated_data.get('first_name', '').strip()
    last_name = serializer.validated_data.get('last_name', '').strip()
    
    # Get user if username provided
    user = None
    if username:
        try:
            user = User.objects.get(username=username)
            # Use phone from user profile if phone not provided
            if not phone:
                try:
                    phone = user.profile.phone or user.username
                except:
                    phone = user.username
        except User.DoesNotExist:
            # For login purpose, we'll create user if doesn't exist (after OTP verification)
            if purpose != 'login':
                return Response(
                    {
                        'error': 'شماره موبایل وارد شده در سیستم ثبت نشده است.',
                        'hint': 'لطفاً شماره موبایل خود را بررسی کنید. اگر حساب کاربری ندارید، از صفحه ثبت‌نام استفاده کنید.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
    
    # For login purpose with phone, try to find user by phone
    if purpose == 'login' and phone and not user:
        try:
            # Try to find user by phone in profile
            user = User.objects.filter(profile__phone=phone).first()
        except:
            pass
    
    # Use phone or user for OTP verification
    user_or_phone = user if user else phone
    
    try:
        otp_service = OTPService()
        # For password_reset, don't mark as used yet (will be marked when password is reset)
        mark_as_used = purpose != 'password_reset'
        result = otp_service.verify_otp(code, user_or_phone, purpose, mark_as_used=mark_as_used)
        
        response_data = {
            'success': True,
            'message': 'کد تأیید صحیح است'
        }
        
        # Include OTP code in response for password_reset flow
        if purpose == 'password_reset':
            response_data['otp_code'] = code
        
        # If login purpose, return token and user data
        if purpose == 'login':
            verified_user = None
            
            # Check if user exists in result (from OTP record)
            if 'user' in result:
                verified_user = result['user']
            elif phone:
                # OTP verified by phone, but no user in result
                # Try to find user by phone
                try:
                    verified_user = User.objects.filter(profile__phone=phone).first()
                except:
                    pass
                
                # If user doesn't exist, create new user
                if not verified_user and phone:
                    # Create new user
                    # Use phone as username (will be unique)
                    username = phone
                    # Ensure username is unique
                    base_username = username
                    counter = 1
                    while User.objects.filter(username=username).exists():
                        username = f"{base_username}_{counter}"
                        counter += 1
                    
                    # Use phone number as default name if name not provided
                    display_name = first_name or last_name or phone
                    if not first_name and not last_name:
                        first_name = display_name
                    
                    # Create user
                    verified_user = User.objects.create_user(
                        username=username,
                        email=f"{username}@temp.com",  # Temporary email
                        first_name=first_name or '',
                        last_name=last_name or '',
                    )
                    
                    # Create or update profile
                    profile, created = UserProfile.objects.get_or_create(user=verified_user)
                    profile.phone = phone
                    profile.role = 'buyer'  # Default role
                    profile.is_verified = True  # Verified via OTP
                    profile.save()
                    
                    # Log user creation
                    log_activity(verified_user, 'register', f'User {verified_user.username} registered via OTP chat', request)
            
            if verified_user:
                # Check if user is blocked
                try:
                    if verified_user.profile.is_blocked:
                        return Response(
                            {'error': 'حساب کاربری شما مسدود شده است. برای رفع مشکل با پشتیبانی تماس بگیرید.'},
                            status=status.HTTP_403_FORBIDDEN
                        )
                except:
                    pass
                
                # Update name if provided and different
                if (first_name or last_name) and verified_user.profile:
                    if first_name and verified_user.first_name != first_name:
                        verified_user.first_name = first_name
                    if last_name and verified_user.last_name != last_name:
                        verified_user.last_name = last_name
                    verified_user.save()
                
                # Create or get token
                token, created = Token.objects.get_or_create(user=verified_user)
                
                # Log login activity
                log_activity(verified_user, 'login', f'User {verified_user.username} logged in via OTP', request)
                
                # Get user profile info
                try:
                    user_serializer = UserDetailSerializer(verified_user)
                    user_data = user_serializer.data
                    
                    # Extract role and is_verified from profile
                    profile = verified_user.profile
                    user_data['role'] = profile.role
                    user_data['is_verified'] = profile.is_verified
                    
                    response_data['token'] = token.key
                    response_data['user'] = user_data
                except:
                    response_data['token'] = token.key
                    response_data['user'] = {
                        'id': verified_user.id,
                        'username': verified_user.username,
                        'email': verified_user.email,
                        'first_name': verified_user.first_name,
                        'last_name': verified_user.last_name,
                        'is_staff': verified_user.is_staff,
                    }
            else:
                # OTP verified but couldn't find or create user
                return Response(
                    {
                        'error': 'خطا در ایجاد یا یافتن حساب کاربری',
                        'helpful_message': 'لطفاً دوباره تلاش کنید یا با پشتیبانی تماس بگیرید.'
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except ValueError as e:
        return Response(
            {
                'error': str(e),
                'helpful_message': 'اگر مطمئن هستید کد را درست وارد کرده‌اید، می‌توانید کد جدیدی درخواست کنید.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error verifying OTP: {str(e)}", exc_info=True)
        return Response(
            {
                'error': 'متأسفانه در تأیید کد مشکلی پیش آمده است.',
                'helpful_message': 'لطفاً چند لحظه صبر کنید و دوباره تلاش کنید. اگر مشکل ادامه داشت، کد جدیدی درخواست کنید.'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def password_reset_view(request):
    """
    Password reset endpoint with OTP verification
    """
    serializer = PasswordResetSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    phone = serializer.validated_data.get('phone')
    username = serializer.validated_data.get('username')
    code = serializer.validated_data['code']
    new_password = serializer.validated_data['new_password']
    
    # Get user
    user = None
    if username:
        try:
            user = User.objects.get(username=username)
            if not phone:
                try:
                    phone = user.profile.phone or user.username
                except:
                    phone = user.username
        except User.DoesNotExist:
            return Response(
                {
                    'error': 'شماره موبایل وارد شده در سیستم ثبت نشده است.',
                    'hint': 'لطفاً شماره موبایل خود را بررسی کنید. اگر حساب کاربری ندارید، از صفحه ثبت‌نام استفاده کنید.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
    else:
        # Find user by phone
        try:
            # Try to find user by phone in profile
            profile = UserProfile.objects.filter(phone=phone).first()
            if profile:
                user = profile.user
            else:
                # Try to find by username (phone might be username)
                try:
                    user = User.objects.get(username=phone)
                except User.DoesNotExist:
                    return Response(
                        {
                            'error': 'شماره موبایل وارد شده در سیستم ثبت نشده است.',
                            'hint': 'لطفاً شماره موبایل خود را بررسی کنید. اگر حساب کاربری ندارید، از صفحه ثبت‌نام استفاده کنید.'
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
        except Exception:
            return Response(
                {
                    'error': 'خطا در پیدا کردن حساب کاربری.',
                    'hint': 'لطفاً شماره موبایل خود را بررسی کنید و دوباره تلاش کنید.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Verify OTP and reset password
    try:
        otp_service = OTPService()
        # Verify OTP (this will mark it as used)
        result = otp_service.verify_otp(code, phone or user, 'password_reset', mark_as_used=True)
        
        if not result.get('success'):
            return Response(
                {
                    'error': 'کد تأیید نامعتبر است.',
                    'hint': 'لطفاً کد تأیید را بررسی کنید و دوباره تلاش کنید.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Reset password
        user.set_password(new_password)
        user.save()
        
        # Log activity
        log_activity(user, 'password_reset', f'User {user.username} reset password via OTP', request)
        
        return Response(
            {
                'success': True,
                'message': 'رمز عبور شما با موفقیت تغییر یافت. اکنون می‌توانید با رمز عبور جدید وارد شوید.'
            },
            status=status.HTTP_200_OK
        )
    except ValueError as e:
        return Response(
            {
                'error': str(e),
                'helpful_message': 'لطفاً کد تأیید را بررسی کنید. اگر کد منقضی شده است، کد جدیدی درخواست کنید.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error resetting password: {str(e)}", exc_info=True)
        return Response(
            {
                'error': 'متأسفانه در تغییر رمز عبور مشکلی پیش آمده است.',
                'helpful_message': 'لطفاً چند لحظه صبر کنید و دوباره تلاش کنید. اگر مشکل ادامه داشت، با پشتیبانی تماس بگیرید.'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register_view(request):
    """
    User registration endpoint with role selection
    """
    try:
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
        
        # Format validation errors for better user experience
        formatted_errors = {}
        for field, errors in serializer.errors.items():
            if isinstance(errors, list):
                # Get the first error message
                formatted_errors[field] = errors[0] if errors else 'مقدار وارد شده معتبر نیست'
            else:
                formatted_errors[field] = str(errors)
        
        return Response({'error': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Handle unexpected errors
        return Response(
            {'error': 'مشکلی در ثبت‌نام پیش آمده است. لطفاً دوباره تلاش کنید.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """Get current logged-in user details"""
    user = request.user
    serializer = UserDetailSerializer(user)
    user_data = serializer.data
    
    # Extract role and is_verified from profile for backward compatibility
    try:
        profile = user.profile
        user_data['role'] = profile.role
        user_data['is_verified'] = profile.is_verified
    except UserProfile.DoesNotExist:
        # If profile doesn't exist, default to buyer role
        user_data['role'] = 'buyer'
        user_data['is_verified'] = False
    
    return Response(user_data)

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
    
    # Filter out vendor profile fields before validating UserProfile
    # UserProfileSerializer only accepts: role, phone, address, avatar
    user_profile_data = {}
    user_profile_fields = ['role', 'phone', 'address', 'avatar']
    for field in user_profile_fields:
        if field in request.data:
            user_profile_data[field] = request.data[field]
    
    # Update profile (only with UserProfile fields)
    serializer = UserProfileSerializer(profile, data=user_profile_data, partial=True)
    if serializer.is_valid():
        serializer.save()
        
        # Update vendor profile if user is seller
        if profile.is_seller():
            try:
                vendor_profile = user.vendor_profile
                # Handle FormData - parse JSON fields if they're strings
                vendor_data = dict(request.data)
                
                # Remove fields that don't belong to vendor profile
                user_fields = ['first_name', 'last_name', 'email']
                for field in user_fields:
                    vendor_data.pop(field, None)
                
                # Parse JSON fields if they're strings
                if 'certifications' in vendor_data and isinstance(vendor_data['certifications'], str):
                    import json
                    try:
                        vendor_data['certifications'] = json.loads(vendor_data['certifications'])
                    except (json.JSONDecodeError, TypeError):
                        vendor_data['certifications'] = []
                if 'awards' in vendor_data and isinstance(vendor_data['awards'], str):
                    import json
                    try:
                        vendor_data['awards'] = json.loads(vendor_data['awards'])
                    except (json.JSONDecodeError, TypeError):
                        vendor_data['awards'] = []
                if 'social_media' in vendor_data and isinstance(vendor_data['social_media'], str):
                    import json
                    try:
                        vendor_data['social_media'] = json.loads(vendor_data['social_media'])
                    except (json.JSONDecodeError, TypeError):
                        vendor_data['social_media'] = {}
                
                # Clean up social_media: convert empty strings to None or remove them
                if 'social_media' in vendor_data and isinstance(vendor_data['social_media'], dict):
                    cleaned_social = {}
                    for key, value in vendor_data['social_media'].items():
                        if value and value.strip():  # Only keep non-empty values
                            cleaned_social[key] = value
                    vendor_data['social_media'] = cleaned_social if cleaned_social else None
                
                # Convert empty strings to None for optional fields that allow null
                # Fields that allow null=True: contact_email, contact_phone, website, slogan, 
                # video_url, meta_title, meta_description
                # Fields that only allow blank=True (must be empty string, not None): description
                nullable_fields = ['contact_email', 'contact_phone', 'website', 
                                 'slogan', 'video_url', 'meta_title', 'meta_description']
                for field in nullable_fields:
                    if field in vendor_data and vendor_data[field] == '':
                        vendor_data[field] = None
                
                # For description, keep empty string (it doesn't allow null)
                if 'description' in vendor_data and vendor_data['description'] is None:
                    vendor_data['description'] = ''
                
                vendor_serializer = VendorProfileSerializer(vendor_profile, data=vendor_data, partial=True)
                if vendor_serializer.is_valid():
                    vendor_serializer.save()
                    # Refresh vendor_profile from database to get updated data
                    vendor_profile.refresh_from_db()
                    # Also refresh user to ensure relationships are updated
                    user.refresh_from_db()
                else:
                    # Log validation errors for debugging
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f'Vendor profile serializer validation failed: {vendor_serializer.errors}')
                    logger.error(f'Vendor data sent: {vendor_data}')
                    # Return error response if vendor profile validation fails
                    return Response({
                        'error': 'Vendor profile validation failed',
                        'vendor_profile_errors': vendor_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
            except VendorProfile.DoesNotExist:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f'VendorProfile does not exist for user {user.id}')
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Error updating vendor profile: {str(e)}', exc_info=True)
        
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
    
    # Check if user has profile and is seller
    try:
        profile = user.profile
        if not profile.is_seller():
            return Response({'error': 'Only sellers can access this endpoint'}, status=status.HTTP_403_FORBIDDEN)
    except (UserProfile.DoesNotExist, AttributeError):
            # Try to create profile if it doesn't exist (shouldn't happen, but handle gracefully)
            # This is a fallback - normally profile should be created during registration
            try:
                profile = UserProfile.objects.create(
                    user=user,
                    role='seller'  # Default to seller if accessing seller dashboard
                )
                # Signal will create VendorProfile automatically
            except Exception:
                # If creation fails, return empty dashboard data
                import logging
                logging.getLogger(__name__).warning(f"Failed to create profile for user {user.id}")
                return Response({
                    'total_products': 0,
                    'active_products': 0,
                    'total_ads': 0,
                    'total_sales': 0.0,
                    'total_orders': 0,
                    'product_views': 0,
                    'total_reviews': 0,
                    'recent_orders': [],
                })
    
    # Get products - optimized with single query
    from products.models import Product
    products_queryset = Product.objects.filter(vendor=user)
    total_products = products_queryset.count()
    active_products = products_queryset.filter(is_active=True).count()
    
    # Get orders for seller's products - optimized with select_related
    order_items = OrderItem.objects.filter(
        Q(seller=user) | Q(product__vendor=user)
    ).select_related('order', 'product', 'product__vendor')
    
    # Aggregate in single query
    order_stats = order_items.aggregate(
        total=Sum('subtotal'),
        order_count=Count('order', distinct=True)
    )
    total_sales = order_stats['total'] or 0
    total_orders = order_stats['order_count'] or 0
    
    # Get recent orders - optimized with prefetch_related
    recent_order_ids = order_items.values_list('order', flat=True).distinct()[:5]
    recent_orders = Order.objects.filter(id__in=recent_order_ids).select_related(
        'buyer', 'category'
    ).prefetch_related(
        'items__product', 'items__product__vendor', 'images', 'payments'
    ).order_by('-created_at')
    
    # Get ads count - use count() instead of loading all
    total_ads = SellerAd.objects.filter(seller=user).count()
    
    # Get reviews count - use count() instead of loading all
    total_reviews = ProductComment.objects.filter(product__vendor=user).count()
    
    # Get product views (we'll need to implement view tracking separately)
    # For now, just return 0
    product_views = 0
    
    dashboard_data = {
        'total_products': total_products,
        'active_products': active_products,
        'total_ads': total_ads,
        'total_sales': float(total_sales),
        'total_orders': total_orders,
        'product_views': product_views,
        'total_reviews': total_reviews,
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendor_subscription_view(request):
    """Expose current vendor subscription/tier and daily unlock quota state."""
    subscription = VendorSubscription.for_user(request.user)
    can_unlock, next_unlock_at = subscription.can_unlock_customer()

    remaining_unlocks = 1 if (subscription.tier.daily_customer_unlock_limit and can_unlock) else 0
    if subscription.tier.daily_customer_unlock_limit == 0:
        remaining_unlocks = None  # Unlimited

    return Response(
        {
            'tier_slug': subscription.tier.slug,
            'tier_name': subscription.tier.name,
            'pricing_type': subscription.tier.pricing_type,
            'is_commission_based': subscription.tier.is_commission_based,
            'daily_customer_unlock_limit': subscription.tier.daily_customer_unlock_limit,
            'lead_exclusivity': subscription.tier.lead_exclusivity,
            'allow_marketplace_visibility': subscription.tier.allow_marketplace_visibility,
            'is_active': subscription.is_active,
            'can_unlock_now': can_unlock,
            'remaining_unlocks': remaining_unlocks,
            'next_unlock_at': next_unlock_at,
            'last_customer_unlock_at': subscription.last_customer_unlock_at,
            'total_customer_unlocks': subscription.total_customer_unlocks,
            # Commission info
            'commission_rate_low': subscription.tier.commission_rate_low,
            'commission_rate_high': subscription.tier.commission_rate_high,
            'commission_threshold': subscription.tier.commission_threshold,
            'total_commission_charged': subscription.total_commission_charged,
            'total_sales_volume': subscription.total_sales_volume,
        }
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pricing_tiers_list(request):
    """List all available pricing tiers."""
    tiers = PricingTier.objects.all()
    data = []
    for tier in tiers:
        data.append({
            'slug': tier.slug,
            'name': tier.name,
            'pricing_type': tier.pricing_type,
            'is_commission_based': tier.is_commission_based,
            'commission_rate_low': tier.commission_rate_low,
            'commission_rate_high': tier.commission_rate_high,
            'commission_threshold': tier.commission_threshold,
            'monthly_price': tier.monthly_price,
            'daily_customer_unlock_limit': tier.daily_customer_unlock_limit,
            'allow_marketplace_visibility': tier.allow_marketplace_visibility,
            'lead_exclusivity': tier.lead_exclusivity,
        })
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def activate_commission_plan(request):
    """
    Activate commission-based plan for vendor.
    Requires: complete profile data, gold tier achievement, terms acceptance
    """
    try:
        subscription = VendorSubscription.for_user(request.user)
        
        # Check if plan is already activated and ready
        if subscription.is_commission_plan_ready():
            return Response(
                {
                    'error': 'Commission plan already activated',
                    'message': 'پلن کمیسیونی شما قبلاً فعال شده است',
                    'subscription': {
                        'tier_slug': subscription.tier.slug,
                        'tier_name': subscription.tier.name,
                        'admin_approved': subscription.admin_approved,
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already on commission tier but not fully activated
        if subscription.tier.is_commission_based and subscription.terms_accepted:
            return Response(
                {
                    'error': 'Activation already in progress',
                    'message': 'درخواست فعال‌سازی شما در حال بررسی است. لطفاً قرارداد و ضمانت‌نامه را آپلود کنید.',
                    'subscription': {
                        'tier_slug': subscription.tier.slug,
                        'contract_signed': subscription.contract_signed,
                        'bank_guarantee_submitted': subscription.bank_guarantee_submitted,
                        'admin_approved': subscription.admin_approved,
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if can activate
        can_activate, missing = subscription.can_activate_commission_plan()
        if not can_activate:
            # Generate appropriate error message
            if 'gold_tier' in missing:
                try:
                    from gamification.services import GamificationService
                    service = GamificationService.for_user(request.user)
                    current_tier = service.calculate_tier()
                    engagement = service.get_or_create_engagement()
                    
                    tier_names = {
                        'inactive': 'غیرفعال',
                        'bronze': 'برنزی',
                        'silver': 'نقره‌ای',
                        'gold': 'طلایی',
                        'diamond': 'الماس'
                    }
                    
                    current_tier_name = tier_names.get(current_tier, current_tier)
                    points = engagement.total_points if engagement else 0
                    reputation = engagement.reputation_score if engagement else 0
                    
                    message = f'برای فعال‌سازی پلن کمیسیونی، باید نشان طلایی (Gold) را دریافت کنید. وضعیت فعلی شما: {current_tier_name} (امتیاز: {points}, اعتبار: {reputation:.1f})'
                except Exception as e:
                    message = 'برای فعال‌سازی پلن کمیسیونی، باید نشان طلایی (Gold) را دریافت کنید.'
            else:
                message = 'لطفاً اطلاعات پروفایل خود را تکمیل کنید'
            
            return Response(
                {
                    'error': 'Cannot activate commission plan',
                    'missing_requirements': missing,
                    'message': message
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check terms acceptance
        terms_accepted = request.data.get('terms_accepted', False)
        if not terms_accepted:
            return Response(
                {
                    'error': 'Terms and conditions must be accepted',
                    'message': 'لطفاً شرایط و ضوابط را بپذیرید'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get commission tier
        try:
            commission_tier = PricingTier.get_commission_tier()
            if not commission_tier:
                return Response(
                    {
                        'error': 'Commission tier not found',
                        'message': 'پلن کمیسیونی در سیستم یافت نشد. لطفاً با پشتیبانی تماس بگیرید.'
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Exception as e:
            return Response(
                {
                    'error': 'Failed to get commission tier',
                    'message': 'خطا در دریافت اطلاعات پلن. لطفاً دوباره تلاش کنید.'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Update subscription
        from django.utils import timezone
        try:
            subscription.tier = commission_tier
            subscription.terms_accepted = True
            subscription.terms_accepted_at = timezone.now()
            subscription.save()
        except Exception as e:
            return Response(
                {
                    'error': 'Database error',
                    'message': 'خطا در ذخیره اطلاعات. لطفاً دوباره تلاش کنید.'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response({
            'success': True,
            'message': 'درخواست فعال‌سازی پلن کمیسیونی ثبت شد. لطفاً قرارداد و ضمانت‌نامه بانکی را آپلود کنید.',
            'subscription': {
                'tier_slug': subscription.tier.slug,
                'tier_name': subscription.tier.name,
                'contract_signed': subscription.contract_signed,
                'bank_guarantee_submitted': subscription.bank_guarantee_submitted,
                'admin_approved': subscription.admin_approved,
            }
        })
    
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error activating commission plan for user {request.user.id}: {str(e)}", exc_info=True)
        
        return Response(
            {
                'error': 'Internal server error',
                'message': 'خطای غیرمنتظره رخ داد. لطفاً دوباره تلاش کنید یا با پشتیبانی تماس بگیرید.'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_commission_contract(request):
    """Upload signed contract document for commission plan."""
    try:
        subscription = VendorSubscription.for_user(request.user)
        
        if not subscription.tier.is_commission_based:
            return Response(
                {
                    'error': 'Not commission plan',
                    'message': 'فقط برای پلن کمیسیونی قابل استفاده است'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        contract_file = request.FILES.get('contract_document')
        if not contract_file:
            return Response(
                {
                    'error': 'No file provided',
                    'message': 'فایل قرارداد ارسال نشده است'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if contract_file.size > max_size:
            return Response(
                {
                    'error': 'File too large',
                    'message': f'حجم فایل باید کمتر از ۱۰ مگابایت باشد. حجم فایل شما: {contract_file.size / (1024*1024):.2f} مگابایت'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file type
        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
        file_name = contract_file.name.lower()
        if not any(file_name.endswith(ext) for ext in allowed_extensions):
            return Response(
                {
                    'error': 'Invalid file type',
                    'message': 'فرمت فایل مجاز نیست. فرمت‌های مجاز: PDF, JPG, PNG'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.utils import timezone
        try:
            subscription.contract_document = contract_file
            subscription.contract_signed = True
            subscription.contract_signed_at = timezone.now()
            subscription.save()
        except Exception as e:
            return Response(
                {
                    'error': 'Database error',
                    'message': 'خطا در ذخیره فایل. لطفاً دوباره تلاش کنید.'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response({
            'success': True,
            'message': 'قرارداد با موفقیت آپلود شد',
            'contract_signed': True,
            'contract_signed_at': subscription.contract_signed_at
        })
    
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error uploading contract for user {request.user.id}: {str(e)}", exc_info=True)
        
        return Response(
            {
                'error': 'Internal server error',
                'message': 'خطای غیرمنتظره در آپلود فایل رخ داد. لطفاً دوباره تلاش کنید.'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_bank_guarantee(request):
    """Upload bank guarantee document for commission plan."""
    try:
        subscription = VendorSubscription.for_user(request.user)
        
        if not subscription.tier.is_commission_based:
            return Response(
                {
                    'error': 'Not commission plan',
                    'message': 'فقط برای پلن کمیسیونی قابل استفاده است'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        guarantee_file = request.FILES.get('bank_guarantee_document')
        guarantee_amount = request.data.get('bank_guarantee_amount')
        guarantee_expiry = request.data.get('bank_guarantee_expiry')
        
        if not guarantee_file:
            return Response(
                {
                    'error': 'No file provided',
                    'message': 'فایل ضمانت‌نامه ارسال نشده است'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if guarantee_file.size > max_size:
            return Response(
                {
                    'error': 'File too large',
                    'message': f'حجم فایل باید کمتر از ۱۰ مگابایت باشد. حجم فایل شما: {guarantee_file.size / (1024*1024):.2f} مگابایت'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file type
        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
        file_name = guarantee_file.name.lower()
        if not any(file_name.endswith(ext) for ext in allowed_extensions):
            return Response(
                {
                    'error': 'Invalid file type',
                    'message': 'فرمت فایل مجاز نیست. فرمت‌های مجاز: PDF, JPG, PNG'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate guarantee amount
        if guarantee_amount:
            try:
                amount = float(guarantee_amount)
                if amount <= 0:
                    return Response(
                        {
                            'error': 'Invalid amount',
                            'message': 'مبلغ ضمانت‌نامه باید بیشتر از صفر باشد'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except (ValueError, TypeError):
                return Response(
                    {
                        'error': 'Invalid amount format',
                        'message': 'مبلغ ضمانت‌نامه نامعتبر است'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Validate expiry date
        if guarantee_expiry:
            from datetime import datetime, date
            try:
                expiry_date = datetime.strptime(guarantee_expiry, '%Y-%m-%d').date()
                if expiry_date < date.today():
                    return Response(
                        {
                            'error': 'Expired guarantee',
                            'message': 'تاریخ انقضای ضمانت‌نامه نمی‌تواند در گذشته باشد'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return Response(
                    {
                        'error': 'Invalid date format',
                        'message': 'فرمت تاریخ انقضا نامعتبر است'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        try:
            subscription.bank_guarantee_document = guarantee_file
            subscription.bank_guarantee_submitted = True
            
            if guarantee_amount:
                subscription.bank_guarantee_amount = guarantee_amount
            if guarantee_expiry:
                from datetime import datetime
                expiry_date = datetime.strptime(guarantee_expiry, '%Y-%m-%d').date()
                subscription.bank_guarantee_expiry = expiry_date
            
            subscription.save()
        except Exception as e:
            return Response(
                {
                    'error': 'Database error',
                    'message': 'خطا در ذخیره اطلاعات. لطفاً دوباره تلاش کنید.'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response({
            'success': True,
            'message': 'ضمانت‌نامه بانکی با موفقیت آپلود شد',
            'bank_guarantee_submitted': True,
            'bank_guarantee_amount': subscription.bank_guarantee_amount,
            'bank_guarantee_expiry': subscription.bank_guarantee_expiry
        })
    
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error uploading bank guarantee for user {request.user.id}: {str(e)}", exc_info=True)
        
        return Response(
            {
                'error': 'Internal server error',
                'message': 'خطای غیرمنتظره در آپلود فایل رخ داد. لطفاً دوباره تلاش کنید.'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def commission_plan_status(request):
    """Get commission plan activation status."""
    subscription = VendorSubscription.for_user(request.user)
    
    can_activate, missing = subscription.can_activate_commission_plan()
    is_ready = subscription.is_commission_plan_ready()
    
    # Get gamification tier information
    from gamification.services import GamificationService
    service = GamificationService.for_user(request.user)
    current_tier = service.calculate_tier()
    engagement = service.get_or_create_engagement()
    
    tier_info = {
        'current_tier': current_tier,
        'current_points': engagement.total_points if engagement else 0,
        'current_reputation': engagement.reputation_score if engagement else 0,
        'has_gold_tier': current_tier in ['gold', 'diamond'],
    }
    
    return Response({
        'tier_slug': subscription.tier.slug,
        'tier_name': subscription.tier.name,
        'is_commission_based': subscription.tier.is_commission_based,
        'can_activate': can_activate,
        'missing_requirements': missing,
        'is_ready': is_ready,
        'gamification_tier': tier_info,
        'contract_signed': subscription.contract_signed,
        'contract_signed_at': subscription.contract_signed_at,
        'bank_guarantee_submitted': subscription.bank_guarantee_submitted,
        'bank_guarantee_amount': subscription.bank_guarantee_amount,
        'bank_guarantee_expiry': subscription.bank_guarantee_expiry,
        'terms_accepted': subscription.terms_accepted,
        'terms_accepted_at': subscription.terms_accepted_at,
        'admin_approved': subscription.admin_approved,
        'admin_approved_at': subscription.admin_approved_at,
        'rejection_reason': subscription.rejection_reason,
        'total_commission_charged': subscription.total_commission_charged,
        'total_sales_volume': subscription.total_sales_volume,
    })

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
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # Get user statistics with error handling
        try:
            total_users = User.objects.filter(is_staff=False).count()
        except Exception as e:
            logger.warning(f"Error counting total users: {str(e)}")
            total_users = 0
        
        try:
            buyers = UserProfile.objects.filter(role__in=['buyer', 'both']).count()
            sellers = UserProfile.objects.filter(role__in=['seller', 'both']).count()
            blocked_users = UserProfile.objects.filter(is_blocked=True).count()
            unverified_users = UserProfile.objects.filter(is_verified=False).count()
        except Exception as e:
            logger.warning(f"Error counting user profiles: {str(e)}")
            buyers = sellers = blocked_users = unverified_users = 0
        
        # Get product statistics with error handling
        try:
            from products.models import Product
            total_products = Product.objects.count()
            active_products = Product.objects.filter(is_active=True, is_marketplace_hidden=False).count()
            pending_products = Product.objects.filter(is_active=False, is_marketplace_hidden=False).count()
            hidden_products = Product.objects.filter(is_marketplace_hidden=True).count()
        except Exception as e:
            logger.warning(f"Error counting products: {str(e)}")
            total_products = active_products = pending_products = hidden_products = 0
        
        # Get order statistics with error handling
        try:
            total_orders = Order.objects.count()
            pending_orders = Order.objects.filter(status='pending').count()
            completed_orders = Order.objects.filter(status='delivered').count()
        except Exception as e:
            logger.warning(f"Error counting orders: {str(e)}")
            total_orders = pending_orders = completed_orders = 0
        
        # Get RFQ statistics with error handling
        try:
            total_rfqs = Order.objects.filter(is_rfq=True).count()
            pending_rfqs = Order.objects.filter(is_rfq=True, status='pending').count()
        except Exception as e:
            logger.warning(f"Error counting RFQs: {str(e)}")
            total_rfqs = pending_rfqs = 0
        
        # Get recent activities - handle potential issues with deleted users
        activities_data = []
        try:
            recent_activities = UserActivity.objects.select_related('user').all()[:20]
            activities_data = UserActivitySerializer(recent_activities, many=True).data
        except Exception as e:
            logger.warning(f"Error loading recent activities: {str(e)}")
            activities_data = []
        
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
                'pending': pending_products,
                'hidden': hidden_products
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
            'recent_activities': activities_data
        }
        
        return Response(dashboard_data)
    except Exception as e:
        logger.error(f"Error in admin_dashboard_view: {str(e)}", exc_info=True)
        return Response(
            {'error': 'Failed to load dashboard data', 'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

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

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Temporarily allow anyone for testing
@csrf_exempt
def unblock_all_users_view(request):
    """Temporary endpoint to check and unblock all blocked users"""
    try:
        # Get all profiles
        all_profiles = UserProfile.objects.all()
        blocked_profiles = UserProfile.objects.filter(is_blocked=True)
        
        # Build detailed report
        all_users = []
        for profile in all_profiles:
            all_users.append({
                'username': profile.user.username,
                'role': profile.get_role_display(),
                'is_blocked': profile.is_blocked,
                'is_verified': profile.is_verified,
                'created_at': str(profile.created_at)
            })
        
        if request.method == 'GET':
            # Just show status
            return Response({
                'total_users': all_profiles.count(),
                'blocked_users': blocked_profiles.count(),
                'users': all_users
            })
        
        # POST - Unblock all
        count = blocked_profiles.count()
        
        if count == 0:
            return Response({
                'message': 'No blocked users found',
                'count': 0,
                'total_users': all_profiles.count(),
                'users': all_users
            })
        
        # Get list of blocked users before unblocking
        blocked_users = list(blocked_profiles.values('user__username', 'created_at'))
        
        # Unblock all
        blocked_profiles.update(is_blocked=False)
        
        return Response({
            'message': f'Successfully unblocked {count} user(s)',
            'count': count,
            'blocked_users': blocked_users,
            'total_users': all_profiles.count()
        })
    except Exception as e:
        import traceback
        return Response({
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        
        old_status = order.status
        order.status = new_status
        
        # Calculate commission when order is delivered
        if new_status == 'delivered' and old_status != 'delivered':
            order.apply_commission()
        
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
def admin_product_hide_view(request, product_id):
    """Hide/unhide a product from the marketplace while keeping it visible for the seller"""
    from products.models import Product
    from products.serializers import ProductSerializer
    
    product = get_object_or_404(Product, id=product_id)
    
    hide_raw = request.data.get('hide', True)
    hide_flag = str(hide_raw).lower() not in ['false', '0', 'no', 'off']
    reason = (request.data.get('reason') or '').strip()
    
    if hide_flag and not reason:
        reason = 'تصویر یا محتوای محصول شامل واترمارک یا اطلاعات فروشنده است. لطفاً نسخه تمیز و بدون برند را بارگذاری کنید.'
    if reason:
        reason = reason[:500]
    
    product.is_marketplace_hidden = hide_flag
    product.marketplace_hide_reason = reason if hide_flag else ''
    product.save()
    
    action_desc = 'Admin hid product from marketplace' if hide_flag else 'Admin restored product to marketplace'
    log_activity(request.user, 'hide_product', f'{action_desc}: {product.name}', request, product)
    
    serializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data)

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
    Owners can view their own supplier profile even if not approved
    """
    queryset = VendorProfile.objects.filter(is_approved=True).order_by('store_name')
    serializer_class = VendorProfileSerializer
    
    def get_permissions(self):
        """All actions are public (read-only)"""
        return [AllowAny()]
    
    def get_queryset(self):
        """
        Return approved suppliers for list view with optimized queries.
        For detail view, get_object handles owner access.
        """
        return VendorProfile.objects.filter(
            is_approved=True
        ).select_related(
            'user'
        ).annotate(
            product_count=Count(
                'user__products',
                filter=Q(user__products__is_active=True),
                distinct=True
            ),
            rating_average=Avg(
                'comments__rating',
                filter=Q(comments__is_approved=True)
            )
        ).order_by('store_name')
    
    def get_object(self):
        """
        Allow owners to view their own supplier profile even if not approved.
        For public access, only return approved suppliers.
        Optimized with select_related and annotations.
        """
        import json
        log_path = '/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log'
        
        # Get the pk from URL
        pk = self.kwargs.get('pk')
        
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({'location': 'users/views.py:2214', 'message': 'SupplierViewSet.get_object entry', 'data': {'pk': pk, 'isAuthenticated': self.request.user.is_authenticated}, 'timestamp': int(__import__('time').time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'E'}) + '\n')
        except: pass
        # #endregion
        
        # Optimize query with annotations and select_related
        queryset = VendorProfile.objects.select_related(
            'user'
        ).prefetch_related(
            Prefetch(
                'comments',
                queryset=SupplierComment.objects.filter(
                    is_approved=True
                ).select_related('user').defer('is_flagged', 'flag_reason')
            )
        ).annotate(
            product_count=Count(
                'user__products',
                filter=Q(user__products__is_active=True),
                distinct=True
            ),
            rating_average=Avg(
                'comments__rating',
                filter=Q(comments__is_approved=True)
            )
        )
        
        # Try to get the object from all VendorProfiles (not just approved ones)
        try:
            obj = queryset.get(pk=pk)
            # #region agent log
            try:
                with open(log_path, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({'location': 'users/views.py:2247', 'message': 'SupplierViewSet.get_object found', 'data': {'supplierId': obj.id, 'isApproved': obj.is_approved}, 'timestamp': int(__import__('time').time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'E'}) + '\n')
            except: pass
            # #endregion
        except VendorProfile.DoesNotExist:
            # #region agent log
            try:
                with open(log_path, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({'location': 'users/views.py:2250', 'message': 'SupplierViewSet.get_object not found', 'data': {'pk': pk}, 'timestamp': int(__import__('time').time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'E'}) + '\n')
            except: pass
            # #endregion
            from rest_framework.exceptions import NotFound
            raise NotFound("Supplier not found")
        
        # Check if user is authenticated and is the owner of this supplier profile
        if self.request.user.is_authenticated:
            try:
                user_vendor_profile = self.request.user.vendor_profile
                if user_vendor_profile.id == obj.id:
                    # Owner can view their own profile even if not approved
                    # #region agent log
                    try:
                        with open(log_path, 'a', encoding='utf-8') as f:
                            f.write(json.dumps({'location': 'users/views.py:2258', 'message': 'SupplierViewSet.get_object owner access', 'data': {'supplierId': obj.id}, 'timestamp': int(__import__('time').time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'E'}) + '\n')
                    except: pass
                    # #endregion
                    return obj
            except VendorProfile.DoesNotExist:
                pass
        
        # For public access or non-owners, only return if approved
        if not obj.is_approved:
            # #region agent log
            try:
                with open(log_path, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({'location': 'users/views.py:2265', 'message': 'SupplierViewSet.get_object not approved', 'data': {'supplierId': obj.id}, 'timestamp': int(__import__('time').time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'E'}) + '\n')
            except: pass
            # #endregion
            from rest_framework.exceptions import NotFound
            raise NotFound("Supplier not found or not approved")
        
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({'location': 'users/views.py:2267', 'message': 'SupplierViewSet.get_object exit', 'data': {'supplierId': obj.id}, 'timestamp': int(__import__('time').time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'E'}) + '\n')
        except: pass
        # #endregion
        
        return obj
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get all products from a specific supplier with pagination and optimized queries"""
        import json
        import logging
        logger = logging.getLogger(__name__)
        log_path = '/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log'
        
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({'location': 'users/views.py:2270', 'message': 'SupplierViewSet.products entry', 'data': {'pk': pk, 'page': request.GET.get('page', '1')}, 'timestamp': int(__import__('time').time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'B'}) + '\n')
        except: pass
        # #endregion
        
        from products.models import Product, ProductImage, ProductFeature
        from products.serializers import ProductSerializer
        from rest_framework.pagination import PageNumberPagination
        
        try:
            supplier = self.get_object()
            # #region agent log
            try:
                with open(log_path, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({'location': 'users/views.py:2280', 'message': 'SupplierViewSet.products supplier retrieved', 'data': {'supplierId': supplier.id, 'supplierName': supplier.store_name}, 'timestamp': int(__import__('time').time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'E'}) + '\n')
            except: pass
            # #endregion
            
            # Optimize queries with select_related and prefetch_related
            products = Product.objects.filter(
                vendor=supplier.user,
                is_active=True
            ).select_related(
                'vendor',
                'vendor__vendor_profile',
                'primary_category'
            ).prefetch_related(
                'subcategories',
                Prefetch(
                    'images',
                    queryset=ProductImage.objects.order_by('-is_primary', 'sort_order', 'created_at')
                ),
                'features',
                'labels'
            ).order_by('-created_at')
            
            # #region agent log
            try:
                product_count_before_pag = products.count()
                with open(log_path, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({'location': 'users/views.py:2300', 'message': 'SupplierViewSet.products queryset ready', 'data': {'totalProducts': product_count_before_pag}, 'timestamp': int(__import__('time').time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'F'}) + '\n')
            except: pass
            # #endregion
            
            # Add pagination
            paginator = PageNumberPagination()
            paginator.page_size = 20  # 20 products per page
            paginated_products = paginator.paginate_queryset(products, request)
            
            serializer = ProductSerializer(paginated_products, many=True)
            response = paginator.get_paginated_response(serializer.data)
            
            # #region agent log
            try:
                response_data = response.data if hasattr(response, 'data') else {}
                with open(log_path, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({'location': 'users/views.py:2310', 'message': 'SupplierViewSet.products response ready', 'data': {'hasResults': 'results' in response_data, 'resultsCount': len(response_data.get('results', [])), 'hasCount': 'count' in response_data, 'hasNext': 'next' in response_data}, 'timestamp': int(__import__('time').time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'A'}) + '\n')
            except: pass
            # #endregion
            
            return response
        except Exception as e:
            # #region agent log
            try:
                with open(log_path, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({'location': 'users/views.py:2315', 'message': 'SupplierViewSet.products error', 'data': {'pk': pk, 'error': str(e), 'errorType': type(e).__name__}, 'timestamp': int(__import__('time').time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'D'}) + '\n')
            except: pass
            # #endregion
            raise
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for a specific supplier"""
        try:
            supplier = self.get_object()
            # Defer is_flagged and flag_reason fields in case they don't exist in database
            # These are handled by SerializerMethodField in the serializer
            comments = supplier.comments.filter(is_approved=True).select_related('user', 'supplier').defer('is_flagged', 'flag_reason')
            serializer = SupplierCommentSerializer(comments, many=True)
            return Response(serializer.data)
        except Exception as e:
            import traceback
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching supplier comments: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                {'error': 'Failed to fetch comments', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def portfolio(self, request, pk=None):
        """Get all portfolio items for a specific supplier"""
        supplier = self.get_object()
        # Use prefetch from get_object if available, otherwise query directly
        portfolio_items = supplier.portfolio_items.all().order_by('sort_order', '-project_date')
        serializer = SupplierPortfolioItemSerializer(portfolio_items, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def team(self, request, pk=None):
        """Get all team members for a specific supplier"""
        supplier = self.get_object()
        # Use prefetch from get_object if available, otherwise query directly
        team_members = supplier.team_members.all().order_by('sort_order', 'name')
        serializer = SupplierTeamMemberSerializer(team_members, many=True)
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


class SupplierPortfolioItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for supplier portfolio items
    - List and retrieve: Public (only approved suppliers)
    - Create/Update/Delete: Only supplier owner
    """
    serializer_class = SupplierPortfolioItemSerializer
    
    def get_queryset(self):
        """
        Return portfolio items filtered by vendor_profile
        If user is authenticated and a supplier, return their portfolio items
        Otherwise, return public portfolio items for approved suppliers
        """
        if self.request.user.is_authenticated:
            try:
                vendor_profile = self.request.user.vendor_profile
                return SupplierPortfolioItem.objects.filter(vendor_profile=vendor_profile).order_by('sort_order', '-project_date')
            except VendorProfile.DoesNotExist:
                pass
        
        # Public view: only show portfolio items for approved suppliers
        return SupplierPortfolioItem.objects.filter(vendor_profile__is_approved=True).order_by('sort_order', '-project_date')
    
    def get_permissions(self):
        """
        List and retrieve are public
        Create, update, delete require authentication
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Set the vendor_profile to the current user's vendor profile"""
        try:
            vendor_profile = self.request.user.vendor_profile
            serializer.save(vendor_profile=vendor_profile)
            log_activity(self.request.user, 'other', 'Added portfolio item', self.request)
        except VendorProfile.DoesNotExist:
            raise Response({'error': 'User does not have a vendor profile'}, status=status.HTTP_400_BAD_REQUEST)


class SupplierTeamMemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for supplier team members
    - List and retrieve: Public (only approved suppliers)
    - Create/Update/Delete: Only supplier owner
    """
    serializer_class = SupplierTeamMemberSerializer
    
    def get_queryset(self):
        """
        Return team members filtered by vendor_profile
        If user is authenticated and a supplier, return their team members
        Otherwise, return public team members for approved suppliers
        """
        if self.request.user.is_authenticated:
            try:
                vendor_profile = self.request.user.vendor_profile
                return SupplierTeamMember.objects.filter(vendor_profile=vendor_profile).order_by('sort_order', 'name')
            except VendorProfile.DoesNotExist:
                pass
        
        # Public view: only show team members for approved suppliers
        return SupplierTeamMember.objects.filter(vendor_profile__is_approved=True).order_by('sort_order', 'name')
    
    def get_permissions(self):
        """
        List and retrieve are public
        Create, update, delete require authentication
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Set the vendor_profile to the current user's vendor profile"""
        try:
            vendor_profile = self.request.user.vendor_profile
            serializer.save(vendor_profile=vendor_profile)
            log_activity(self.request.user, 'other', 'Added team member', self.request)
        except VendorProfile.DoesNotExist:
            raise Response({'error': 'User does not have a vendor profile'}, status=status.HTTP_400_BAD_REQUEST)


class SupplierContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for supplier contact messages
    - Create: Public (anyone can send a message)
    - List/Retrieve/Update/Delete: Only supplier owner (to manage their messages)
    """
    serializer_class = SupplierContactMessageSerializer
    
    def get_queryset(self):
        """
        Return messages only for the authenticated supplier
        """
        if self.request.user.is_authenticated:
            try:
                vendor_profile = self.request.user.vendor_profile
                return SupplierContactMessage.objects.filter(vendor_profile=vendor_profile).order_by('-created_at')
            except VendorProfile.DoesNotExist:
                return SupplierContactMessage.objects.none()
        return SupplierContactMessage.objects.none()
    
    def get_permissions(self):
        """
        Create is public (anyone can send a message)
        List, retrieve, update, delete require authentication
        """
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """
        When creating a message, vendor_profile should be passed in the request
        """
        # The vendor_profile will be sent from the frontend in the request data
        serializer.save()
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def mark_read(self, request, pk=None):
        """Mark a message as read"""
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response({'status': 'Message marked as read'})
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def mark_unread(self, request, pk=None):
        """Mark a message as unread"""
        message = self.get_object()
        message.is_read = False
        message.save()
        return Response({'status': 'Message marked as unread'})


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


# Admin Commission Plan Management
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_commission_requests_view(request):
    """Get all commission plan activation requests for admin review."""
    subscriptions = VendorSubscription.objects.filter(
        tier__is_commission_based=True
    ).select_related('user', 'user__profile', 'user__vendor_profile', 'tier')
    
    # Filter by status
    status_filter = request.query_params.get('status')
    if status_filter == 'pending':
        subscriptions = subscriptions.filter(
            contract_signed=True,
            bank_guarantee_submitted=True,
            admin_approved=False
        )
    elif status_filter == 'approved':
        subscriptions = subscriptions.filter(admin_approved=True)
    elif status_filter == 'incomplete':
        subscriptions = subscriptions.filter(
            Q(contract_signed=False) | Q(bank_guarantee_submitted=False)
        )
    
    data = []
    for sub in subscriptions:
        data.append({
            'id': sub.id,
            'user_id': sub.user.id,
            'username': sub.user.username,
            'store_name': sub.user.vendor_profile.store_name if hasattr(sub.user, 'vendor_profile') else '',
            'tier_name': sub.tier.name,
            'contract_signed': sub.contract_signed,
            'contract_signed_at': sub.contract_signed_at,
            'contract_document': sub.contract_document.url if sub.contract_document else None,
            'bank_guarantee_submitted': sub.bank_guarantee_submitted,
            'bank_guarantee_document': sub.bank_guarantee_document.url if sub.bank_guarantee_document else None,
            'bank_guarantee_amount': sub.bank_guarantee_amount,
            'bank_guarantee_expiry': sub.bank_guarantee_expiry,
            'terms_accepted': sub.terms_accepted,
            'terms_accepted_at': sub.terms_accepted_at,
            'admin_approved': sub.admin_approved,
            'admin_approved_at': sub.admin_approved_at,
            'rejection_reason': sub.rejection_reason,
            'total_commission_charged': sub.total_commission_charged,
            'total_sales_volume': sub.total_sales_volume,
            'started_at': sub.started_at,
        })
    
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_approve_commission_plan(request, subscription_id):
    """Approve a vendor's commission plan activation request."""
    try:
        subscription = VendorSubscription.objects.get(id=subscription_id)
        
        if not subscription.tier.is_commission_based:
            return Response(
                {'error': 'این اشتراک کمیسیونی نیست'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not subscription.contract_signed or not subscription.bank_guarantee_submitted:
            return Response(
                {'error': 'قرارداد یا ضمانت‌نامه بانکی ارسال نشده است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.utils import timezone
        subscription.admin_approved = True
        subscription.admin_approved_at = timezone.now()
        subscription.admin_approved_by = request.user
        subscription.rejection_reason = None
        subscription.save()
        
        log_activity(
            request.user,
            'other',
            f'Admin approved commission plan for {subscription.user.username}',
            request,
            subscription
        )
        
        return Response({
            'success': True,
            'message': 'پلن کمیسیونی با موفقیت تایید شد'
        })
    
    except VendorSubscription.DoesNotExist:
        return Response(
            {'error': 'اشتراک یافت نشد'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_reject_commission_plan(request, subscription_id):
    """Reject a vendor's commission plan activation request."""
    try:
        subscription = VendorSubscription.objects.get(id=subscription_id)
        
        rejection_reason = request.data.get('rejection_reason')
        if not rejection_reason:
            return Response(
                {'error': 'دلیل رد درخواست الزامی است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        subscription.admin_approved = False
        subscription.rejection_reason = rejection_reason
        subscription.save()
        
        log_activity(
            request.user,
            'other',
            f'Admin rejected commission plan for {subscription.user.username}',
            request,
            subscription
        )
        
        return Response({
            'success': True,
            'message': 'درخواست رد شد'
        })
    
    except VendorSubscription.DoesNotExist:
        return Response(
            {'error': 'اشتراک یافت نشد'},
            status=status.HTTP_404_NOT_FOUND
        )


# ===== CRM VIEWSETS =====

class SellerContactViewSet(viewsets.ModelViewSet):
    """ViewSet for CRM contacts"""
    serializer_class = SellerContactSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return contacts only for the authenticated seller"""
        user = self.request.user
        queryset = SellerContact.objects.filter(seller=user)
        
        # Search by name or phone
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone__icontains=search) |
                Q(company_name__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """Set seller automatically"""
        serializer.save(seller=self.request.user)
    
    @action(detail=True, methods=['get'])
    def notes(self, request, pk=None):
        """Get all notes for a contact"""
        contact = self.get_object()
        notes = contact.contact_notes.filter(seller=request.user).order_by('-created_at')
        serializer = ContactNoteSerializer(notes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        """Get all tasks for a contact"""
        contact = self.get_object()
        tasks = contact.tasks.filter(seller=request.user).order_by('due_date', '-priority')
        serializer = ContactTaskSerializer(tasks, many=True)
        return Response(serializer.data)


class ContactNoteViewSet(viewsets.ModelViewSet):
    """ViewSet for contact notes"""
    serializer_class = ContactNoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return notes only for the authenticated seller"""
        user = self.request.user
        queryset = ContactNote.objects.filter(seller=user)
        
        # Filter by contact if provided
        contact_id = self.request.query_params.get('contact')
        if contact_id:
            queryset = queryset.filter(contact_id=contact_id)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """Set seller automatically"""
        serializer.save(seller=self.request.user)


class ContactTaskViewSet(viewsets.ModelViewSet):
    """ViewSet for contact tasks/reminders"""
    serializer_class = ContactTaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return tasks only for the authenticated seller"""
        user = self.request.user
        queryset = ContactTask.objects.filter(seller=user)
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by contact if provided
        contact_id = self.request.query_params.get('contact')
        if contact_id:
            queryset = queryset.filter(contact_id=contact_id)
        
        # Filter by priority if provided
        priority_filter = self.request.query_params.get('priority')
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        
        return queryset.order_by('due_date', '-priority')
    
    def perform_create(self, serializer):
        """Set seller automatically"""
        serializer.save(seller=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        """Mark task as completed"""
        task = self.get_object()
        task.status = 'completed'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        """Mark task as cancelled"""
        task = self.get_object()
        task.status = 'cancelled'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
