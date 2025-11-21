from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatRoom, ChatMessage, ChatParticipant, GuestSession

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data in chat"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class GuestSessionSerializer(serializers.ModelSerializer):
    """Serializer for guest sessions"""
    class Meta:
        model = GuestSession
        fields = ['session_id', 'identifier', 'linked_user', 'created_at']
        read_only_fields = ['session_id', 'created_at']


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for chat messages"""
    sender_username = serializers.SerializerMethodField()
    sender_details = UserSerializer(source='sender', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'room', 'sender', 'sender_username', 'sender_details',
            'guest_session', 'content', 'is_read', 'read_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'read_at', 'is_read']
    
    def get_sender_username(self, obj):
        if obj.sender:
            return obj.sender.username
        elif obj.guest_session:
            return f"Guest"
        return "Unknown"


class ChatParticipantSerializer(serializers.ModelSerializer):
    """Serializer for chat participants"""
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = ChatParticipant
        fields = ['user', 'user_details', 'joined_at', 'last_read_at']
        read_only_fields = ['joined_at', 'last_read_at']


class ChatRoomSerializer(serializers.ModelSerializer):
    """Serializer for chat rooms"""
    participants_details = UserSerializer(source='participants', many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    other_participant = serializers.SerializerMethodField()
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    
    class Meta:
        model = ChatRoom
        fields = [
            'room_id', 'participants', 'participants_details', 'product',
            'product_name', 'product_id', 'guest_session', 'is_archived',
            'created_at', 'updated_at', 'last_message', 'unread_count',
            'other_participant'
        ]
        read_only_fields = ['room_id', 'created_at', 'updated_at']
    
    def get_last_message(self, obj):
        last_msg = obj.get_last_message()
        if last_msg:
            return ChatMessageSerializer(last_msg).data
        return None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.get_unread_count(request.user)
        return 0
    
    def get_other_participant(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            other = obj.get_other_participant(request.user)
            if other:
                return UserSerializer(other).data
        return None


class ChatRoomCreateSerializer(serializers.Serializer):
    """Serializer for creating chat rooms"""
    product_id = serializers.IntegerField(required=False, allow_null=True)
    vendor_id = serializers.IntegerField(required=True)
    initial_message = serializers.CharField(required=False, allow_blank=True)
    
    def validate_vendor_id(self, value):
        """Validate that vendor exists"""
        try:
            user = User.objects.get(id=value)
            # User exists - they can receive chat messages even without VendorProfile
            # The VendorProfile is optional for basic chat functionality
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
    
    def validate_product_id(self, value):
        """Validate that product exists if provided"""
        if value:
            from products.models import Product
            try:
                Product.objects.get(id=value)
                return value
            except Product.DoesNotExist:
                raise serializers.ValidationError("Product not found")
        return value


class LinkGuestSessionSerializer(serializers.Serializer):
    """Serializer for linking guest session to user"""
    guest_session_id = serializers.UUIDField(required=True)
    
    def validate_guest_session_id(self, value):
        """Validate that guest session exists"""
        try:
            GuestSession.objects.get(session_id=value)
            return value
        except GuestSession.DoesNotExist:
            raise serializers.ValidationError("Guest session not found")

