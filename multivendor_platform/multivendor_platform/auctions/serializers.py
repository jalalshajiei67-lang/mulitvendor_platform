from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ReverseAuction, AuctionInvitation, Bid
from .services import AuctionService


class BidSerializer(serializers.ModelSerializer):
    """Serializer for bid representation"""
    supplier_username = serializers.CharField(source='supplier.username', read_only=True)
    supplier_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Bid
        fields = ['id', 'supplier', 'supplier_username', 'supplier_name', 'amount', 'rank', 'is_winning', 'created_at']
        read_only_fields = ['rank', 'is_winning', 'created_at']
    
    def get_supplier_name(self, obj):
        """Get supplier's display name"""
        try:
            if hasattr(obj.supplier, 'vendor_profile') and obj.supplier.vendor_profile:
                return obj.supplier.vendor_profile.store_name
            return obj.supplier.get_full_name() or obj.supplier.username
        except:
            return obj.supplier.username


class BidCreateSerializer(serializers.Serializer):
    """Serializer for creating a bid"""
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
    
    def validate_amount(self, value):
        """Validate amount is positive"""
        if value <= 0:
            raise serializers.ValidationError("Bid amount must be greater than zero")
        return value


class AuctionAwardSerializer(serializers.Serializer):
    """Serializer for awarding an auction"""
    bid_id = serializers.IntegerField()


class ReverseAuctionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for auction lists"""
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    bid_count = serializers.SerializerMethodField()
    time_remaining = serializers.SerializerMethodField()
    my_bid = serializers.SerializerMethodField()
    my_rank = serializers.SerializerMethodField()
    is_invited = serializers.SerializerMethodField()
    
    class Meta:
        model = ReverseAuction
        fields = [
            'id', 'title', 'category', 'category_name', 'starting_price', 
            'deadline', 'status', 'bid_count', 'time_remaining', 
            'created_at', 'my_bid', 'my_rank', 'is_invited'
        ]
        read_only_fields = ['created_at']
    
    def get_bid_count(self, obj):
        """Get number of bids"""
        return obj.bids.count()
    
    def get_time_remaining(self, obj):
        """Get time remaining until deadline"""
        time_remaining = obj.time_remaining()
        if time_remaining:
            total_seconds = int(time_remaining.total_seconds())
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60
            return {
                'days': days,
                'hours': hours,
                'minutes': minutes,
                'total_seconds': total_seconds
            }
        return None
    
    def get_my_bid(self, obj):
        """Get current user's bid if they are a supplier"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                bid = obj.bids.get(supplier=request.user)
                return {
                    'id': bid.id,
                    'amount': bid.amount,
                    'rank': bid.rank,
                    'is_winning': bid.is_winning
                }
            except Bid.DoesNotExist:
                return None
        return None
    
    def get_my_rank(self, obj):
        """Get current user's rank if they have bid"""
        my_bid = self.get_my_bid(obj)
        return my_bid['rank'] if my_bid and my_bid.get('rank') else None
    
    def get_is_invited(self, obj):
        """Check if current user is invited"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return AuctionInvitation.objects.filter(
                auction=obj,
                supplier=request.user
            ).exists()
        return False


class ReverseAuctionDetailSerializer(serializers.ModelSerializer):
    """Full detail serializer with role-based field visibility"""
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    buyer_username = serializers.CharField(source='buyer.username', read_only=True)
    bid_count = serializers.SerializerMethodField()
    time_remaining = serializers.SerializerMethodField()
    my_bid = serializers.SerializerMethodField()
    my_rank = serializers.SerializerMethodField()
    is_invited = serializers.SerializerMethodField()
    can_bid = serializers.SerializerMethodField()
    all_bids = serializers.SerializerMethodField()  # Only visible to buyer after deadline
    winner_info = serializers.SerializerMethodField()
    
    class Meta:
        model = ReverseAuction
        fields = [
            'id', 'title', 'description', 'category', 'category_name',
            'starting_price', 'reserve_price', 'deadline', 'minimum_decrement',
            'status', 'buyer', 'buyer_username', 'bid_count', 'time_remaining',
            'created_at', 'updated_at', 'extended_count',
            'my_bid', 'my_rank', 'is_invited', 'can_bid',
            'all_bids', 'winner_info'
        ]
        read_only_fields = ['created_at', 'updated_at', 'extended_count']
    
    def get_bid_count(self, obj):
        """Get number of bids"""
        return obj.bids.count()
    
    def get_time_remaining(self, obj):
        """Get time remaining until deadline"""
        time_remaining = obj.time_remaining()
        if time_remaining:
            total_seconds = int(time_remaining.total_seconds())
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60
            return {
                'days': days,
                'hours': hours,
                'minutes': minutes,
                'total_seconds': total_seconds
            }
        return None
    
    def get_my_bid(self, obj):
        """Get current user's bid if they are a supplier"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                bid = obj.bids.get(supplier=request.user)
                return {
                    'id': bid.id,
                    'amount': bid.amount,
                    'rank': bid.rank,
                    'is_winning': bid.is_winning,
                    'created_at': bid.created_at
                }
            except Bid.DoesNotExist:
                return None
        return None
    
    def get_my_rank(self, obj):
        """Get current user's rank if they have bid"""
        my_bid = self.get_my_bid(obj)
        return my_bid['rank'] if my_bid and my_bid.get('rank') else None
    
    def get_is_invited(self, obj):
        """Check if current user is invited"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return AuctionInvitation.objects.filter(
                auction=obj,
                supplier=request.user
            ).exists()
        return False
    
    def get_can_bid(self, obj):
        """Check if current user can place a bid"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        
        # Check if user is invited
        if not self.get_is_invited(obj):
            return False
        
        # Check if auction is active
        if obj.status != 'active':
            return False
        
        # Check deadline
        from django.utils import timezone
        if timezone.now() >= obj.deadline:
            return False
        
        return True
    
    def get_all_bids(self, obj):
        """
        Get all bids - only visible to buyer after deadline.
        Suppliers never see competitor bids.
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return []
        
        # Only buyer can see all bids, and only after deadline
        if request.user != obj.buyer:
            return []
        
        from django.utils import timezone
        if timezone.now() < obj.deadline and obj.status == 'active':
            return []  # Don't show bids until deadline passes
        
        # Return all bids sorted by amount (lowest first)
        bids = obj.bids.all().order_by('amount', 'created_at')
        return BidSerializer(bids, many=True, context=self.context).data
    
    def get_winner_info(self, obj):
        """Get winner information if auction is awarded"""
        if obj.status == 'awarded' and obj.winner:
            return {
                'bid_id': obj.winner.id,
                'supplier_username': obj.winner.supplier.username,
                'supplier_name': self._get_supplier_name(obj.winner.supplier),
                'amount': obj.winner.amount
            }
        return None
    
    def _get_supplier_name(self, supplier):
        """Helper to get supplier display name"""
        try:
            if hasattr(supplier, 'vendor_profile') and supplier.vendor_profile:
                return supplier.vendor_profile.store_name
            return supplier.get_full_name() or supplier.username
        except:
            return supplier.username
    
    def to_representation(self, instance):
        """Customize representation based on user role"""
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        if request and request.user.is_authenticated:
            # If user is not the buyer, hide reserve_price
            if request.user != instance.buyer:
                data.pop('reserve_price', None)
        
        return data


class ReverseAuctionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating an auction"""
    
    class Meta:
        model = ReverseAuction
        fields = [
            'title', 'description', 'category', 'starting_price', 
            'reserve_price', 'deadline', 'minimum_decrement'
        ]
    
    def validate_deadline(self, value):
        """Validate deadline is in the future"""
        from django.utils import timezone
        if value <= timezone.now():
            raise serializers.ValidationError("Deadline must be in the future")
        return value
    
    def validate_starting_price(self, value):
        """Validate starting price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Starting price must be greater than zero")
        return value
    
    def validate(self, data):
        """Validate reserve price is less than starting price"""
        reserve_price = data.get('reserve_price')
        starting_price = data.get('starting_price')
        
        if reserve_price and starting_price:
            if reserve_price >= starting_price:
                raise serializers.ValidationError({
                    'reserve_price': 'Reserve price must be less than starting price'
                })
        
        return data
