from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, BuyerProfile, VendorProfile, SellerAd, SellerAdImage, ProductReview, SupplierComment, UserActivity

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
    product_count = serializers.SerializerMethodField()
    rating_average = serializers.SerializerMethodField()
    
    class Meta:
        model = VendorProfile
        fields = ['id', 'user', 'store_name', 'logo', 'description', 'contact_email', 'contact_phone', 
                  'website', 'address', 'work_resume', 'successful_projects', 'history', 'about', 
                  'is_approved', 'product_count', 'rating_average', 'created_at', 'updated_at']
        read_only_fields = ['is_approved', 'product_count', 'rating_average', 'created_at', 'updated_at']
    
    def get_product_count(self, obj):
        return obj.get_product_count()
    
    def get_rating_average(self, obj):
        return obj.get_rating_average()

class SellerAdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerAdImage
        fields = ['id', 'image', 'alt_text', 'sort_order']

class SellerAdSerializer(serializers.ModelSerializer):
    images = SellerAdImageSerializer(many=True, read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    
    class Meta:
        model = SellerAd
        fields = ['id', 'seller', 'seller_username', 'title', 'description', 'contact_info', 'is_active', 'images', 'created_at', 'updated_at']
        read_only_fields = ['seller', 'created_at', 'updated_at']

class ProductReviewSerializer(serializers.ModelSerializer):
    buyer_username = serializers.CharField(source='buyer.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    rating_display = serializers.CharField(source='get_rating_display', read_only=True)
    
    class Meta:
        model = ProductReview
        fields = ['id', 'product', 'product_name', 'buyer', 'buyer_username', 'order', 'rating', 'rating_display', 
                  'title', 'comment', 'is_verified_purchase', 'is_approved', 'seller_reply', 'seller_replied_at', 
                  'created_at', 'updated_at']
        read_only_fields = ['buyer', 'is_verified_purchase', 'is_approved', 'seller_replied_at', 'created_at', 'updated_at']

class SupplierCommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    supplier_name = serializers.CharField(source='supplier.store_name', read_only=True)
    rating_display = serializers.CharField(source='get_rating_display', read_only=True)
    
    class Meta:
        model = SupplierComment
        fields = ['id', 'supplier', 'supplier_name', 'user', 'user_username', 'rating', 'rating_display', 
                  'title', 'comment', 'is_approved', 'supplier_reply', 'supplier_replied_at', 
                  'created_at', 'updated_at']
        read_only_fields = ['user', 'is_approved', 'supplier_replied_at', 'created_at', 'updated_at']

class UserActivitySerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'user_username', 'action', 'action_display', 'description', 'ip_address', 'created_at']
        read_only_fields = ['created_at']

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    
    # For sellers
    store_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    store_description = serializers.CharField(required=False, allow_blank=True)
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate(self, data):
        # If role is seller or both, store_name is required
        role = data.get('role')
        if role in ['seller', 'both'] and not data.get('store_name'):
            raise serializers.ValidationError({"store_name": "Store name is required for sellers"})
        return data
    
    def create(self, validated_data):
        # Extract user data
        user_data = {
            'username': validated_data['username'],
            'email': validated_data['email'],
            'first_name': validated_data.get('first_name', ''),
            'last_name': validated_data.get('last_name', ''),
        }
        password = validated_data['password']
        
        # Create user
        user = User.objects.create_user(**user_data, password=password)
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            role=validated_data['role'],
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', '')
        )
        
        # Create buyer profile if user is buyer
        if validated_data['role'] in ['buyer', 'both']:
            BuyerProfile.objects.create(user=user)
        
        # Create vendor profile if user is seller
        if validated_data['role'] in ['seller', 'both']:
            VendorProfile.objects.create(
                user=user,
                store_name=validated_data['store_name'],
                description=validated_data.get('store_description', '')
            )
        
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

