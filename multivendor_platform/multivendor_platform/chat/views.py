from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Max
from django.shortcuts import get_object_or_404
from .models import ChatRoom, ChatMessage, GuestSession, ChatParticipant
from .serializers import (
    ChatRoomSerializer, ChatMessageSerializer, GuestSessionSerializer,
    ChatRoomCreateSerializer, LinkGuestSessionSerializer
)
from .permissions import IsChatParticipant, IsVendorOrAdmin, IsAdminUser
from products.models import Product


class MessagePagination(PageNumberPagination):
    """Pagination for messages"""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class ChatRoomViewSet(viewsets.ModelViewSet):
    """ViewSet for managing chat rooms"""
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.AllowAny]  # Individual actions have their own permissions
    lookup_field = 'room_id'
    
    def get_queryset(self):
        """Get chat rooms for current user or guest session"""
        user = self.request.user
        
        if user.is_authenticated:
            if user.is_staff:
                # Admin can see all rooms
                return ChatRoom.objects.all().prefetch_related('participants', 'product')
            
            # Regular users see only their rooms
            return ChatRoom.objects.filter(
                participants=user
            ).distinct().prefetch_related('participants', 'product')
        else:
            # Guest users - filter by guest session
            guest_session_id = self.request.query_params.get('guest_session')
            if guest_session_id:
                try:
                    guest_session = GuestSession.objects.get(session_id=guest_session_id)
                    return ChatRoom.objects.filter(
                        guest_session=guest_session
                    ).prefetch_related('participants', 'product')
                except GuestSession.DoesNotExist:
                    pass
            
            # Return empty queryset if no valid guest session
            return ChatRoom.objects.none()
    
    def list(self, request, *args, **kwargs):
        """List all chat rooms for the user or guest"""
        queryset = self.get_queryset().annotate(
            last_message_time=Max('messages__created_at')
        ).order_by('-last_message_time')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsChatParticipant])
    def messages(self, request, room_id=None):
        """Get messages for a specific room"""
        room = self.get_object()
        messages = room.messages.select_related('sender', 'guest_session').order_by('created_at')
        
        # Paginate messages
        paginator = MessagePagination()
        page = paginator.paginate_queryset(messages, request)
        
        if page is not None:
            serializer = ChatMessageSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsChatParticipant])
    def mark_read(self, request, room_id=None):
        """Mark all messages in room as read"""
        room = self.get_object()
        
        # Guest users don't have read tracking
        if not request.user.is_authenticated:
            return Response({'status': 'Guest users do not have read tracking'})
        
        try:
            participant = ChatParticipant.objects.get(room=room, user=request.user)
            participant.mark_as_read()
            return Response({'status': 'messages marked as read'})
        except ChatParticipant.DoesNotExist:
            return Response(
                {'error': 'You are not a participant of this room'},
                status=status.HTTP_403_FORBIDDEN
            )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_guest_session(request):
    """Create a guest session for anonymous users"""
    identifier = request.data.get('identifier', 'unknown')
    
    guest_session = GuestSession.objects.create(identifier=identifier)
    serializer = GuestSessionSerializer(guest_session)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def link_guest_session(request):
    """Link a guest session to the authenticated user"""
    serializer = LinkGuestSessionSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    guest_session_id = serializer.validated_data['guest_session_id']
    
    try:
        guest_session = GuestSession.objects.get(session_id=guest_session_id)
        
        # Link guest session to user
        if guest_session.linked_user:
            return Response(
                {'error': 'Guest session is already linked to another user'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        guest_session.linked_user = request.user
        guest_session.save()
        
        # Update chat rooms: add user as participant if they were guests
        chat_rooms = ChatRoom.objects.filter(guest_session=guest_session)
        for room in chat_rooms:
            if not room.participants.filter(id=request.user.id).exists():
                ChatParticipant.objects.create(room=room, user=request.user)
        
        return Response({
            'status': 'Guest session linked successfully',
            'linked_rooms': chat_rooms.count()
        })
        
    except GuestSession.DoesNotExist:
        return Response(
            {'error': 'Guest session not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def start_chat(request):
    """Start a new chat or return existing one"""
    # Log incoming request for debugging
    print("=== Start Chat Request ===")
    print("Request data:", request.data)
    print("User authenticated:", request.user.is_authenticated)
    print("User:", request.user if request.user.is_authenticated else "Anonymous")
    
    serializer = ChatRoomCreateSerializer(data=request.data)
    
    if not serializer.is_valid():
        print("Validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    vendor_id = serializer.validated_data['vendor_id']
    product_id = serializer.validated_data.get('product_id')
    initial_message = serializer.validated_data.get('initial_message', '')
    
    vendor = get_object_or_404(User, id=vendor_id)
    product = None
    if product_id:
        product = get_object_or_404(Product, id=product_id)
    
    # Determine if user is authenticated or guest
    user = request.user if request.user.is_authenticated else None
    guest_session = None
    
    if not user:
        # Create or get guest session from request
        guest_session_id = request.data.get('guest_session_id')
        if guest_session_id:
            try:
                guest_session = GuestSession.objects.get(session_id=guest_session_id)
            except GuestSession.DoesNotExist:
                guest_session = GuestSession.objects.create(
                    identifier=request.data.get('identifier', 'unknown')
                )
        else:
            guest_session = GuestSession.objects.create(
                identifier=request.data.get('identifier', 'unknown')
            )
    
    # Check if room already exists
    existing_room = None
    if user:
        # For authenticated users
        existing_room = ChatRoom.objects.filter(
            participants=user
        ).filter(
            participants=vendor
        ).filter(
            product=product
        ).first()
    elif guest_session:
        # For guest sessions
        existing_room = ChatRoom.objects.filter(
            guest_session=guest_session,
            product=product
        ).filter(participants=vendor).first()
    
    if existing_room:
        serializer = ChatRoomSerializer(existing_room, context={'request': request})
        return Response(serializer.data)
    
    # Create new room
    room = ChatRoom.objects.create(
        product=product,
        guest_session=guest_session if not user else None
    )
    
    # Add participants
    if user:
        ChatParticipant.objects.create(room=room, user=user)
    ChatParticipant.objects.create(room=room, user=vendor)
    
    # Send initial message if provided
    if initial_message:
        ChatMessage.objects.create(
            room=room,
            sender=user if user else None,
            guest_session=guest_session if not user else None,
            content=initial_message
        )
    
    serializer = ChatRoomSerializer(room, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsVendorOrAdmin])
def vendor_rooms(request):
    """Get all chat rooms for the vendor"""
    user = request.user
    
    rooms = ChatRoom.objects.filter(
        participants=user
    ).prefetch_related('participants', 'product').annotate(
        last_message_time=Max('messages__created_at')
    ).order_by('-last_message_time')
    
    # Calculate unread count for each room
    serializer = ChatRoomSerializer(rooms, many=True, context={'request': request})
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_rooms(request):
    """Get all chat rooms for admin monitoring"""
    rooms = ChatRoom.objects.all().prefetch_related(
        'participants', 'product'
    ).annotate(
        last_message_time=Max('messages__created_at')
    ).order_by('-last_message_time')
    
    # Filter by query params
    search = request.query_params.get('search')
    if search:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        rooms = rooms.filter(
            Q(participants__username__icontains=search) |
            Q(product__name__icontains=search)
        ).distinct()
    
    serializer = ChatRoomSerializer(rooms, many=True, context={'request': request})
    
    return Response(serializer.data)


# Import User model at module level
from django.contrib.auth import get_user_model
User = get_user_model()

