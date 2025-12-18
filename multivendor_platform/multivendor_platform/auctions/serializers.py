from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    AuctionRequest, AuctionPhoto, AuctionDocument, Bid,
    AuctionDepositPayment, AuctionReport, AuctionNotification
)
from products.models import Product, Subcategory
from products.utils import build_absolute_uri

User = get_user_model()


class AuctionPhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = AuctionPhoto
        fields = ['id', 'image', 'image_url', 'uploaded_at']
        read_only_fields = ['uploaded_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return build_absolute_uri(request, obj.image.url)
        return None


class AuctionDocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = AuctionDocument
        fields = ['id', 'file', 'file_url', 'file_name', 'uploaded_at']
        read_only_fields = ['uploaded_at']
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            return build_absolute_uri(request, obj.file.url)
        return None


class BidSerializer(serializers.ModelSerializer):
    """Bid serializer with identity masking logic"""
    seller_name = serializers.SerializerMethodField()
    seller_id = serializers.SerializerMethodField()
    bidder_number = serializers.SerializerMethodField()
    
    class Meta:
        model = Bid
        fields = ['id', 'auction', 'seller', 'seller_name', 'seller_id', 'bidder_number',
                 'price', 'technical_compliance', 'additional_notes', 'is_winner', 
                 'rank', 'created_at', 'updated_at']
        read_only_fields = ['seller', 'created_at', 'updated_at', 'is_winner', 'rank']
    
    def get_seller_name(self, obj):
        """Return seller name only for buyer or bid owner"""
        request = self.context.get('request')
        if not request or not request.user:
            return None
        
        user = request.user
        auction = obj.auction
        
        # Buyer sees real seller name
        if user == auction.buyer:
            return obj.seller.get_full_name() or obj.seller.username
        
        # Seller sees their own bid with real name
        if user == obj.seller:
            return obj.seller.get_full_name() or obj.seller.username
        
        # Other sellers see masked identity
        return None
    
    def get_seller_id(self, obj):
        """Return seller ID only for buyer or bid owner"""
        request = self.context.get('request')
        if not request or not request.user:
            return None
        
        user = request.user
        auction = obj.auction
        
        # Buyer sees real seller ID
        if user == auction.buyer:
            return obj.seller.id
        
        # Seller sees their own bid with real ID
        if user == obj.seller:
            return obj.seller.id
        
        # Other sellers see None
        return None
    
    def get_bidder_number(self, obj):
        """Return bidder number for identity masking"""
        request = self.context.get('request')
        if not request or not request.user:
            return None
        
        user = request.user
        auction = obj.auction
        
        # Buyer sees None (they see real names)
        if user == auction.buyer:
            return None
        
        # Seller sees their own bid as "You"
        if user == obj.seller:
            return "You"
        
        # Other sellers see "Bidder #X"
        # Get all bids for this auction, ordered by creation time
        # Use a consistent ordering based on creation time and ID
        all_bids = list(Bid.objects.filter(auction=auction).order_by('created_at', 'id').values_list('id', flat=True))
        try:
            bidder_index = all_bids.index(obj.id) + 1
            return f"Bidder #{bidder_index}"
        except ValueError:
            return "Bidder #?"


class AuctionDepositPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionDepositPayment
        fields = ['id', 'auction', 'user', 'amount', 'status', 'track_id', 'order_id',
                 'ref_number', 'card_number', 'payment_method', 'created_at', 
                 'paid_at', 'verified_at']
        read_only_fields = ['user', 'track_id', 'order_id', 'created_at', 
                          'paid_at', 'verified_at', 'ref_number', 'card_number']


class AuctionReportSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(source='admin.get_full_name', read_only=True)
    
    class Meta:
        model = AuctionReport
        fields = ['id', 'auction', 'admin', 'admin_name', 'report_text', 
                 'created_at', 'updated_at']
        read_only_fields = ['admin', 'created_at', 'updated_at']


class AuctionNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionNotification
        fields = ['id', 'auction', 'user', 'notification_type', 'message', 
                 'is_read', 'created_at']
        read_only_fields = ['user', 'created_at']


class AuctionRequestSerializer(serializers.ModelSerializer):
    """Main auction request serializer"""
    photos = AuctionPhotoSerializer(many=True, read_only=True)
    documents = AuctionDocumentSerializer(many=True, read_only=True)
    bids = BidSerializer(many=True, read_only=True)
    buyer_name = serializers.CharField(source='buyer.get_full_name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True, allow_null=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True, allow_null=True)
    deposit_payment_detail = AuctionDepositPaymentSerializer(read_only=True)
    report = AuctionReportSerializer(read_only=True)
    bid_count = serializers.SerializerMethodField()
    can_close_early = serializers.SerializerMethodField()
    time_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = AuctionRequest
        fields = ['id', 'buyer', 'buyer_name', 'product', 'product_name', 
                 'subcategory', 'subcategory_name', 'status', 'request_type',
                 'deposit_amount', 'deposit_status', 'deposit_payment', 
                 'deposit_payment_detail', 'auction_style', 'start_time', 
                 'end_time', 'description', 'technical_specs', 'admin_notes',
                 'reviewed_by', 'reviewed_at', 'winner', 'closed_at',
                 'photos', 'documents', 'bids', 'bid_count', 'report',
                 'can_close_early', 'time_remaining', 'created_at', 'updated_at']
        read_only_fields = ['buyer', 'created_at', 'updated_at', 'reviewed_by', 
                          'reviewed_at', 'closed_at', 'winner']
    
    def get_bid_count(self, obj):
        return obj.bids.count()
    
    def get_can_close_early(self, obj):
        return obj.can_close_early()
    
    def get_time_remaining(self, obj):
        if obj.end_time:
            from django.utils import timezone
            remaining = obj.end_time - timezone.now()
            if remaining.total_seconds() > 0:
                return int(remaining.total_seconds())
        return None


class AuctionRequestCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating auction requests"""
    photo_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    document_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = AuctionRequest
        fields = ['product', 'subcategory', 'request_type', 'auction_style',
                 'start_time', 'end_time', 'description', 'technical_specs',
                 'photo_ids', 'document_ids']
    
    def validate(self, data):
        """Validate auction request data"""
        # Validate that subcategory is provided
        if not data.get('subcategory'):
            raise serializers.ValidationError("Subcategory is required")
        
        # Validate time range
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        if start_time and end_time:
            if end_time <= start_time:
                raise serializers.ValidationError("End time must be after start time")
        
        # Validate technical_specs if subcategory has feature templates
        subcategory = data.get('subcategory')
        if subcategory:
            from products.models import SubcategoryFeatureTemplate
            templates = SubcategoryFeatureTemplate.objects.filter(
                subcategory=subcategory
            )
            required_templates = templates.filter(is_required=True)
            technical_specs = data.get('technical_specs', {})
            
            for template in required_templates:
                if template.feature_name not in technical_specs or not technical_specs[template.feature_name]:
                    raise serializers.ValidationError(
                        f"Required field '{template.feature_name}' is missing in technical_specs"
                    )
        
        return data
    
    def create(self, validated_data):
        """Create auction request with photos and documents"""
        photo_ids = validated_data.pop('photo_ids', [])
        document_ids = validated_data.pop('document_ids', [])
        
        # Set buyer from request user
        validated_data['buyer'] = self.context['request'].user
        validated_data['status'] = 'pending_review'
        
        # Create auction request
        auction = AuctionRequest.objects.create(**validated_data)
        
        # Associate photos
        if photo_ids:
            AuctionPhoto.objects.filter(id__in=photo_ids).update(auction=auction)
        
        # Associate documents (only if deposit is paid)
        if document_ids:
            if auction.deposit_status in ['paid', 'held_in_escrow']:
                AuctionDocument.objects.filter(id__in=document_ids).update(auction=auction)
            else:
                # Documents should not be uploaded without deposit
                raise serializers.ValidationError(
                    "Documents can only be uploaded for verified requests with paid deposit"
                )
        
        return auction


class BidCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bids"""
    
    class Meta:
        model = Bid
        fields = ['auction', 'price', 'technical_compliance', 'additional_notes']
    
    def validate(self, data):
        """Validate bid data"""
        auction = data.get('auction')
        user = self.context['request'].user
        
        # Check if auction is active
        if auction.status != 'active':
            raise serializers.ValidationError("Can only bid on active auctions")
        
        # Check if user is a seller
        if not hasattr(user, 'profile') or not user.profile.is_seller():
            raise serializers.ValidationError("Only sellers can submit bids")
        
        # Check if seller already has a bid
        if Bid.objects.filter(auction=auction, seller=user).exists():
            raise serializers.ValidationError("You have already submitted a bid for this auction")
        
        # Validate technical_compliance if auction has feature templates
        if auction.subcategory:
            from products.models import SubcategoryFeatureTemplate
            templates = SubcategoryFeatureTemplate.objects.filter(
                subcategory=auction.subcategory
            )
            required_templates = templates.filter(is_required=True)
            technical_compliance = data.get('technical_compliance', {})
            
            for template in required_templates:
                if template.feature_name not in technical_compliance or not technical_compliance[template.feature_name]:
                    raise serializers.ValidationError(
                        f"Required field '{template.feature_name}' is missing in technical_compliance"
                    )
        
        return data
    
    def create(self, validated_data):
        """Create bid with seller from request user"""
        validated_data['seller'] = self.context['request'].user
        return Bid.objects.create(**validated_data)
