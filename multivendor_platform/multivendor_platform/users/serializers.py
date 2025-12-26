import re
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, BuyerProfile, VendorProfile, SellerAd, SellerAdImage, 
    ProductReview, SupplierComment, UserActivity, SupplierPortfolioItem, 
    SupplierTeamMember, SupplierContactMessage, OTP,
    SellerContact, ContactNote, ContactTask
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role', 'phone', 'address', 'avatar', 'is_verified', 'is_blocked', 'created_at', 'updated_at']
        read_only_fields = ['is_verified', 'is_blocked', 'created_at', 'updated_at']

class BuyerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = BuyerProfile
        fields = ['id', 'user', 'shipping_address', 'billing_address', 'default_payment_method', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class VendorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # Use annotated fields if available, otherwise fall back to method fields
    product_count = serializers.IntegerField(read_only=True, required=False)
    rating_average = serializers.FloatField(read_only=True, required=False)
    
    class Meta:
        model = VendorProfile
        fields = [
            'id', 'user', 'store_name', 'logo', 'description', 'contact_email', 'contact_phone', 'contact_phone_landline',
            'website', 'address', 'work_resume', 'successful_projects', 'history', 'about',
            # Mini website branding fields
            'banner_image', 'brand_color_primary', 'brand_color_secondary', 'slogan',
            'year_established', 'employee_count', 'certifications', 'awards', 'social_media',
            'video_url', 'meta_title', 'meta_description',
            # Computed and status fields
            'is_approved', 'product_count', 'rating_average', 'created_at', 'updated_at'
        ]
        read_only_fields = ['is_approved', 'product_count', 'rating_average', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        """Handle both annotated and non-annotated instances"""
        data = super().to_representation(instance)
        
        # If annotations are not available, use method fields as fallback
        if 'product_count' not in data or data['product_count'] is None:
            data['product_count'] = instance.get_product_count()
        
        if 'rating_average' not in data or data['rating_average'] is None:
            rating = instance.get_rating_average()
            data['rating_average'] = round(rating, 1) if rating else 0
        elif data['rating_average'] is not None:
            # Round the annotated value
            data['rating_average'] = round(data['rating_average'], 1)
        
        return data

class SellerAdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerAdImage
        fields = ['id', 'image', 'alt_text', 'sort_order']

class SellerAdSerializer(serializers.ModelSerializer):
    images = SellerAdImageSerializer(many=True, read_only=True)
    seller_display_name = serializers.SerializerMethodField()
    
    class Meta:
        model = SellerAd
        fields = ['id', 'seller', 'seller_display_name', 'title', 'description', 'contact_info', 'is_active', 'images', 'created_at', 'updated_at']
        read_only_fields = ['seller', 'created_at', 'updated_at']
    
    def get_seller_display_name(self, obj):
        """Get display name: vendor.store_name if seller, otherwise first_name last_name"""
        if hasattr(obj.seller, 'vendor_profile') and obj.seller.vendor_profile:
            return obj.seller.vendor_profile.store_name
        name_parts = [obj.seller.first_name, obj.seller.last_name]
        return ' '.join(filter(None, name_parts)) or obj.seller.username

class ProductReviewSerializer(serializers.ModelSerializer):
    buyer_display_name = serializers.SerializerMethodField()
    product_name = serializers.CharField(source='product.name', read_only=True)
    rating_display = serializers.CharField(source='get_rating_display', read_only=True)
    
    class Meta:
        model = ProductReview
        fields = ['id', 'product', 'product_name', 'buyer', 'buyer_display_name', 'order', 'rating', 'rating_display', 
                  'title', 'comment', 'is_verified_purchase', 'is_approved', 'is_flagged', 'flag_reason',
                  'seller_reply', 'seller_replied_at', 
                  'created_at', 'updated_at']
        read_only_fields = ['buyer', 'is_verified_purchase', 'is_approved', 'is_flagged', 'flag_reason', 'seller_replied_at', 'created_at', 'updated_at']
    
    def get_buyer_display_name(self, obj):
        """Get display name: first_name last_name"""
        name_parts = [obj.buyer.first_name, obj.buyer.last_name]
        return ' '.join(filter(None, name_parts)) or obj.buyer.username

class SupplierCommentSerializer(serializers.ModelSerializer):
    user_display_name = serializers.SerializerMethodField()
    user_username = serializers.SerializerMethodField()
    supplier_name = serializers.SerializerMethodField()
    rating_display = serializers.SerializerMethodField()
    is_flagged = serializers.SerializerMethodField()
    flag_reason = serializers.SerializerMethodField()
    
    class Meta:
        model = SupplierComment
        fields = ['id', 'supplier', 'supplier_name', 'user', 'user_username', 'user_display_name', 'rating', 'rating_display', 
                  'title', 'comment', 'is_approved', 'is_flagged', 'flag_reason', 'supplier_reply', 'supplier_replied_at', 
                  'created_at', 'updated_at']
        read_only_fields = ['user', 'is_approved', 'supplier_replied_at', 'created_at', 'updated_at']
    
    def get_user_username(self, obj):
        """Get username, handling deleted users"""
        try:
            if not obj.user:
                return 'Deleted User'
            return obj.user.username
        except (AttributeError, Exception):
            return 'Deleted User'
    
    def get_user_display_name(self, obj):
        """Get display name: first_name last_name"""
        try:
            if not obj.user:
                return 'Deleted User'
            name_parts = [obj.user.first_name, obj.user.last_name]
            return ' '.join(filter(None, name_parts)) or obj.user.username
        except (AttributeError, Exception):
            return 'Deleted User'
    
    def get_supplier_name(self, obj):
        """Get supplier store name, handling deleted suppliers"""
        try:
            if not obj.supplier:
                return 'Deleted Supplier'
            return obj.supplier.store_name
        except (AttributeError, Exception):
            return 'Deleted Supplier'
    
    def get_rating_display(self, obj):
        """Get rating display value"""
        try:
            return obj.get_rating_display()
        except (AttributeError, Exception):
            return str(obj.rating) if hasattr(obj, 'rating') and obj.rating else ''
    
    def get_is_flagged(self, obj):
        """Get is_flagged value, handling missing database column"""
        try:
            return getattr(obj, 'is_flagged', False)
        except (AttributeError, Exception):
            return False
    
    def get_flag_reason(self, obj):
        """Get flag_reason value, handling missing database column"""
        try:
            return getattr(obj, 'flag_reason', None)
        except (AttributeError, Exception):
            return None

class UserActivitySerializer(serializers.ModelSerializer):
    user_username = serializers.SerializerMethodField()
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'user_username', 'action', 'action_display', 'description', 'ip_address', 'created_at']
        read_only_fields = ['created_at']
    
    def get_user_username(self, obj):
        """Safely get username, handling deleted users"""
        try:
            return obj.user.username if obj.user else 'Deleted User'
        except Exception:
            return 'Unknown User'

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, help_text="Mobile number used as username")
    password = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    
    # Optional fields (can be added later in profile)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    
    # For sellers (optional during registration)
    store_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    store_description = serializers.CharField(required=False, allow_blank=True)
    
    # Referral code (from ?ref=CODE query parameter)
    referral_code = serializers.CharField(max_length=50, required=False, allow_blank=True)
    
    def validate_username(self, value):
        # Validate and normalize mobile number format (Iranian format: 09XXXXXXXXX or +98XXXXXXXXXX)
        # Remove spaces, dashes, parentheses
        cleaned = re.sub(r'[\s\-()]', '', value.strip())
        
        # Normalize to Iranian format (09XXXXXXXXX)
        if cleaned.startswith('+98'):
            cleaned = '0' + cleaned[3:]
        elif cleaned.startswith('0098'):
            cleaned = '0' + cleaned[4:]
        elif cleaned.startswith('98'):
            cleaned = '0' + cleaned[2:]
        elif not cleaned.startswith('0'):
            cleaned = '0' + cleaned
        
        # Check if it's a valid Iranian mobile number (09XXXXXXXXX - 11 digits)
        if not re.match(r'^09\d{9}$', cleaned):
            raise serializers.ValidationError("شماره موبایل معتبر نیست. لطفاً شماره را به صورت صحیح وارد کنید (مثال: 09123456789)")
        
        # Check uniqueness
        if User.objects.filter(username=cleaned).exists():
            raise serializers.ValidationError("این شماره موبایل قبلاً ثبت شده است")
        
        return cleaned
    
    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("این ایمیل قبلاً ثبت شده است")
        return value
    
    def validate(self, data):
        # Store name is no longer required during registration
        # It can be added later in profile completion
        return data
    
    def create(self, validated_data):
        # Extract user data - mobile number is username
        mobile = validated_data['username']  # username field contains mobile number
        email = validated_data.get('email', '')
        
        # If no email provided, create a placeholder email using mobile number
        # Django User model requires email, but we can use a placeholder
        if not email:
            email = f"{mobile}@placeholder.local"
            # Keep trying until we find a unique email
            counter = 1
            while User.objects.filter(email=email).exists():
                email = f"{mobile}{counter}@placeholder.local"
                counter += 1
        
        user_data = {
            'username': mobile,  # Explicitly set username to mobile number
            'email': email,
            'first_name': validated_data.get('first_name', ''),
            'last_name': validated_data.get('last_name', ''),
        }
        password = validated_data['password']
        
        # Create user
        user = User.objects.create_user(**user_data, password=password)
        
        # Create user profile - do not populate phone with username
        # BuyerProfile and VendorProfile will be created automatically by signals
        phone = validated_data.get('phone', '')  # Only use provided phone, not username
        user_profile = UserProfile.objects.create(
            user=user,
            role=validated_data['role'],
            phone=phone,
            address=validated_data.get('address', '')
        )
        
        # Ensure VendorProfile is created for sellers (signal should handle this, but ensure it exists)
        # Signal runs synchronously, so VendorProfile should exist now
        if validated_data['role'] in ['seller', 'both']:
            from users.models import VendorProfile
            import uuid
            
            # Get or create vendor profile (signal should have created it, but ensure it exists)
            vendor_profile, created = VendorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'store_name': f"فروشگاه_{user.username}_{uuid.uuid4().hex[:6]}",
                    'description': ''
                }
            )
            
            # Update store_name and description if provided during registration
            store_name = validated_data.get('store_name', '').strip()
            store_description = validated_data.get('store_description', '').strip()
            
            if store_name:
                vendor_profile.store_name = store_name
            if store_description:
                vendor_profile.description = store_description
            
            # Save if we updated anything or if it was just created
            if store_name or store_description or created:
                vendor_profile.save()
        
        # Handle referral code (invitation system)
        referral_code = validated_data.get('referral_code', '').strip()
        if referral_code:
            try:
                from gamification.models import Invitation
                from gamification.services import GamificationService
                from django.utils import timezone
                
                # Find the invitation
                invitation = Invitation.objects.filter(
                    invite_code=referral_code,
                    status='pending'
                ).first()
                
                if invitation:
                    # Mark invitation as accepted
                    invitation.status = 'accepted'
                    invitation.accepted_at = timezone.now()
                    
                    # Link invitee if user is a seller
                    if validated_data['role'] in ['seller', 'both']:
                        try:
                            new_vendor_profile = VendorProfile.objects.get(user=user)
                            invitation.invitee = new_vendor_profile
                        except VendorProfile.DoesNotExist:
                            pass  # VendorProfile will be created by signal
                    
                    invitation.save()
                    
                    # Award points to inviter (100 points per Phase 5 spec)
                    inviter_service = GamificationService(invitation.inviter)
                    inviter_service.add_points('peer_invitation', 100, metadata={
                        'invitee_username': user.username,
                        'invitation_id': invitation.id
                    })
            except Exception as e:
                # Don't fail registration if invitation processing fails
                # Just log the error
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to process referral code {referral_code}: {str(e)}")
        
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    buyer_profile = BuyerProfileSerializer(read_only=True)
    vendor_profile = VendorProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'profile', 'buyer_profile', 'vendor_profile']

class PasswordChangeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True, min_length=6)
    
    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist")
        return value

class SupplierPortfolioItemSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor_profile.store_name', read_only=True)
    
    class Meta:
        model = SupplierPortfolioItem
        fields = [
            'id', 'vendor_profile', 'vendor_name', 'title', 'description', 'image',
            'project_date', 'client_name', 'category', 'sort_order', 'is_featured',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['vendor_profile', 'created_at', 'updated_at']

class SupplierTeamMemberSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor_profile.store_name', read_only=True)
    
    class Meta:
        model = SupplierTeamMember
        fields = [
            'id', 'vendor_profile', 'vendor_name', 'name', 'position', 'photo',
            'bio', 'sort_order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['vendor_profile', 'created_at', 'updated_at']

class SupplierContactMessageSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor_profile.store_name', read_only=True)
    
    class Meta:
        model = SupplierContactMessage
        fields = [
            'id', 'vendor_profile', 'vendor_name', 'sender_name', 'sender_email',
            'sender_phone', 'subject', 'message', 'is_read', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class OTPRequestSerializer(serializers.Serializer):
    """Serializer for OTP request"""
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    username = serializers.CharField(max_length=150, required=False, allow_blank=True)
    purpose = serializers.ChoiceField(choices=OTP.PURPOSE_CHOICES)

    def validate(self, data):
        phone = data.get('phone')
        username = data.get('username')

        if not phone and not username:
            raise serializers.ValidationError("شماره موبایل یا نام کاربری الزامی است.")

        if phone:
            cleaned = re.sub(r'[\s\-()]', '', phone.strip())
            if cleaned.startswith('+98'):
                cleaned = '0' + cleaned[3:]
            elif cleaned.startswith('0098'):
                cleaned = '0' + cleaned[4:]
            elif cleaned.startswith('98'):
                cleaned = '0' + cleaned[2:]
            elif not cleaned.startswith('0'):
                cleaned = '0' + cleaned
            
            if not re.match(r'^09\d{9}$', cleaned):
                raise serializers.ValidationError("فرمت شماره موبایل معتبر نیست. لطفاً شماره را به صورت صحیح وارد کنید (مثال: 09123456789).")
            data['phone'] = cleaned
        
        return data

class OTPVerifySerializer(serializers.Serializer):
    """Serializer for OTP verification"""
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    username = serializers.CharField(max_length=150, required=False, allow_blank=True)
    code = serializers.CharField(max_length=6, min_length=6)
    purpose = serializers.ChoiceField(choices=OTP.PURPOSE_CHOICES)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

    def validate(self, data):
        phone = data.get('phone')
        username = data.get('username')

        if not phone and not username:
            raise serializers.ValidationError("شماره موبایل یا نام کاربری الزامی است.")
        
        if phone:
            cleaned = re.sub(r'[\s\-()]', '', phone.strip())
            if cleaned.startswith('+98'):
                cleaned = '0' + cleaned[3:]
            elif cleaned.startswith('0098'):
                cleaned = '0' + cleaned[4:]
            elif cleaned.startswith('98'):
                cleaned = '0' + cleaned[2:]
            elif not cleaned.startswith('0'):
                cleaned = '0' + cleaned
            
            if not re.match(r'^09\d{9}$', cleaned):
                raise serializers.ValidationError("فرمت شماره موبایل معتبر نیست. لطفاً شماره را به صورت صحیح وارد کنید (مثال: 09123456789).")
            data['phone'] = cleaned

        return data

class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset with OTP"""
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    username = serializers.CharField(max_length=150, required=False, allow_blank=True)
    code = serializers.CharField(max_length=6, min_length=6)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, data):
        phone = data.get('phone')
        username = data.get('username')

        if not phone and not username:
            raise serializers.ValidationError("شماره موبایل یا نام کاربری الزامی است.")
        
        if phone:
            cleaned = re.sub(r'[\s\-()]', '', phone.strip())
            if cleaned.startswith('+98'):
                cleaned = '0' + cleaned[3:]
            elif cleaned.startswith('0098'):
                cleaned = '0' + cleaned[4:]
            elif cleaned.startswith('98'):
                cleaned = '0' + cleaned[2:]
            elif not cleaned.startswith('0'):
                cleaned = '0' + cleaned
            
            if not re.match(r'^09\d{9}$', cleaned):
                raise serializers.ValidationError("فرمت شماره موبایل معتبر نیست. لطفاً شماره را به صورت صحیح وارد کنید (مثال: 09123456789).")
            data['phone'] = cleaned

        return data


class SellerContactSerializer(serializers.ModelSerializer):
    """Serializer for CRM contacts"""
    notes_count = serializers.SerializerMethodField()
    tasks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SellerContact
        fields = [
            'id', 'seller', 'first_name', 'last_name', 'company_name', 
            'phone', 'email', 'address', 'notes', 'source_order',
            'notes_count', 'tasks_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['seller', 'created_at', 'updated_at']
    
    def get_notes_count(self, obj):
        return obj.contact_notes.count()
    
    def get_tasks_count(self, obj):
        return obj.tasks.count()


class ContactNoteSerializer(serializers.ModelSerializer):
    """Serializer for contact notes"""
    contact_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ContactNote
        fields = ['id', 'contact', 'contact_name', 'seller', 'content', 'created_at', 'updated_at']
        read_only_fields = ['seller', 'created_at', 'updated_at']
    
    def get_contact_name(self, obj):
        return str(obj.contact)


class ContactTaskSerializer(serializers.ModelSerializer):
    """Serializer for contact tasks/reminders"""
    contact_name = serializers.SerializerMethodField()
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = ContactTask
        fields = [
            'id', 'contact', 'contact_name', 'seller', 'title', 'description',
            'due_date', 'priority', 'priority_display', 'status', 'status_display',
            'is_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['seller', 'created_at', 'updated_at']
    
    def get_contact_name(self, obj):
        return str(obj.contact) if obj.contact else None
    
    def get_is_overdue(self, obj):
        from django.utils import timezone
        return obj.status == 'pending' and obj.due_date < timezone.now()
