import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import ChatRoom, ChatMessage, ChatParticipant, GuestSession, TypingStatus

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time chat"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.user = None
        self.guest_session = None
        self.room_groups = set()
        
        # Authenticate user from query string or headers
        await self.authenticate()
        
        if not self.user and not self.guest_session:
            # Neither authenticated user nor guest session
            await self.close()
            return
        
        await self.accept()
        
        # Send connection success message
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'user': self.user.username if self.user else None,
            'guest_session': str(self.guest_session.session_id) if self.guest_session else None,
        }))
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Leave all room groups
        for room_group_name in self.room_groups:
            await self.channel_layer.group_discard(
                room_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'join_room':
                await self.join_room(data)
            elif message_type == 'leave_room':
                await self.leave_room(data)
            elif message_type == 'send_message':
                await self.send_chat_message(data)
            elif message_type == 'mark_read':
                await self.mark_messages_read(data)
            elif message_type == 'typing':
                await self.handle_typing(data)
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Unknown message type: {message_type}'
                }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': str(e)
            }))
    
    async def join_room(self, data):
        """Join a chat room"""
        room_id = data.get('room_id')
        if not room_id:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'room_id is required'
            }))
            return
        
        # Check if user has access to this room
        has_access = await self.check_room_access(room_id)
        if not has_access:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Access denied to this room'
            }))
            return
        
        room_group_name = f'chat_{room_id}'
        self.room_groups.add(room_group_name)
        
        # Join room group
        await self.channel_layer.group_add(
            room_group_name,
            self.channel_name
        )
        
        await self.send(text_data=json.dumps({
            'type': 'room_joined',
            'room_id': room_id
        }))
    
    async def leave_room(self, data):
        """Leave a chat room"""
        room_id = data.get('room_id')
        if not room_id:
            return
        
        room_group_name = f'chat_{room_id}'
        if room_group_name in self.room_groups:
            self.room_groups.remove(room_group_name)
            
            await self.channel_layer.group_discard(
                room_group_name,
                self.channel_name
            )
            
            await self.send(text_data=json.dumps({
                'type': 'room_left',
                'room_id': room_id
            }))
    
    async def send_chat_message(self, data):
        """Send a chat message"""
        room_id = data.get('room_id')
        content = data.get('content', '').strip()
        
        if not room_id or not content:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'room_id and content are required'
            }))
            return
        
        # Check room access
        has_access = await self.check_room_access(room_id)
        if not has_access:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Access denied to this room'
            }))
            return
        
        # Save message to database
        message = await self.save_message(room_id, content)
        
        if not message:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Failed to save message'
            }))
            return
        
        room_group_name = f'chat_{room_id}'
        
        # Broadcast message to room group
        await self.channel_layer.group_send(
            room_group_name,
            {
                'type': 'chat_message',
                'message_id': str(message['id']),
                'room_id': room_id,
                'sender': message['sender'],
                'sender_username': message['sender_username'],
                'content': content,
                'created_at': message['created_at'],
                'is_read': False,
            }
        )
    
    async def mark_messages_read(self, data):
        """Mark messages as read"""
        room_id = data.get('room_id')
        
        if not room_id:
            return
        
        # Mark messages as read in database
        await self.mark_room_messages_read(room_id)
        
        # Notify other participants
        room_group_name = f'chat_{room_id}'
        await self.channel_layer.group_send(
            room_group_name,
            {
                'type': 'messages_read',
                'room_id': room_id,
                'user_id': self.user.id if self.user else None,
            }
        )
    
    async def handle_typing(self, data):
        """Handle typing indicator"""
        room_id = data.get('room_id')
        is_typing = data.get('is_typing', False)
        
        if not room_id:
            return
        
        # Update typing status
        await self.update_typing_status(room_id, is_typing)
        
        # Broadcast typing status to room
        room_group_name = f'chat_{room_id}'
        await self.channel_layer.group_send(
            room_group_name,
            {
                'type': 'user_typing',
                'room_id': room_id,
                'user_id': self.user.id if self.user else None,
                'username': self.user.username if self.user else f'Guest',
                'is_typing': is_typing,
            }
        )
    
    # Group message handlers
    async def chat_message(self, event):
        """Receive message from room group"""
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message_id': event['message_id'],
            'room_id': event['room_id'],
            'sender': event['sender'],
            'sender_username': event['sender_username'],
            'content': event['content'],
            'created_at': event['created_at'],
            'is_read': event['is_read'],
        }))
    
    async def messages_read(self, event):
        """Receive read receipt from room group"""
        # Don't send read receipt to the user who marked as read
        if self.user and event['user_id'] == self.user.id:
            return
        
        await self.send(text_data=json.dumps({
            'type': 'read_receipt',
            'room_id': event['room_id'],
            'user_id': event['user_id'],
        }))
    
    async def user_typing(self, event):
        """Receive typing status from room group"""
        # Don't send typing indicator back to the typing user
        if self.user and event['user_id'] == self.user.id:
            return
        
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'room_id': event['room_id'],
            'user_id': event['user_id'],
            'username': event['username'],
            'is_typing': event['is_typing'],
        }))
    
    # Database operations
    @database_sync_to_async
    def authenticate(self):
        """Authenticate user from token or create guest session"""
        # Try to get token from query string
        query_string = self.scope.get('query_string', b'').decode()
        params = dict(param.split('=') for param in query_string.split('&') if '=' in param)
        token_key = params.get('token')
        guest_session_id = params.get('guest_session')
        
        print(f"=== WebSocket Authentication ===")
        print(f"Query string: {query_string}")
        print(f"Token key: {token_key}")
        print(f"Guest session ID: {guest_session_id}")
        
        # Try token authentication
        if token_key:
            try:
                token = Token.objects.select_related('user').get(key=token_key)
                self.user = token.user
                print(f"Authenticated as user: {self.user.username}")
                return
            except Token.DoesNotExist:
                print("Token not found")
                pass
        
        # Try guest session
        if guest_session_id:
            try:
                self.guest_session = GuestSession.objects.get(session_id=guest_session_id)
                # If guest session is linked to a user, use that user
                if self.guest_session.linked_user:
                    self.user = self.guest_session.linked_user
                    print(f"Guest session linked to user: {self.user.username}")
                else:
                    print(f"Guest session authenticated: {self.guest_session.session_id}")
                return
            except GuestSession.DoesNotExist:
                print("Guest session not found")
                pass
        
        print("No authentication provided")
    
    @database_sync_to_async
    def check_room_access(self, room_id):
        """Check if user/guest has access to a room"""
        try:
            room = ChatRoom.objects.get(room_id=room_id)
            
            # Debug logging
            print(f"=== Checking Room Access ===")
            print(f"Room ID: {room_id}")
            print(f"User: {self.user}")
            print(f"Guest Session: {self.guest_session}")
            print(f"Room participants: {list(room.participants.all())}")
            print(f"Room guest_session: {room.guest_session}")
            
            # Admin has access to all rooms
            if self.user and self.user.is_staff:
                print("Access granted: User is admin")
                return True
            
            # Check if user is a participant
            if self.user and room.participants.filter(id=self.user.id).exists():
                print("Access granted: User is participant")
                return True
            
            # Check if room is associated with this guest session
            if self.guest_session and room.guest_session == self.guest_session:
                print("Access granted: Guest session matches")
                return True
            
            print("Access denied: No matching criteria")
            return False
        except ChatRoom.DoesNotExist:
            print(f"Room not found: {room_id}")
            return False
    
    @database_sync_to_async
    def save_message(self, room_id, content):
        """Save message to database"""
        try:
            room = ChatRoom.objects.get(room_id=room_id)
            
            message = ChatMessage.objects.create(
                room=room,
                sender=self.user if self.user else None,
                guest_session=self.guest_session if not self.user else None,
                content=content,
            )
            
            return {
                'id': str(message.id),
                'sender': self.user.id if self.user else None,
                'sender_username': self.user.username if self.user else f'Guest',
                'content': content,
                'created_at': message.created_at.isoformat(),
            }
        except Exception as e:
            print(f"Error saving message: {e}")
            return None
    
    @database_sync_to_async
    def mark_room_messages_read(self, room_id):
        """Mark all messages in room as read for current user"""
        if not self.user:
            return
        
        try:
            room = ChatRoom.objects.get(room_id=room_id)
            participant = ChatParticipant.objects.get(room=room, user=self.user)
            participant.mark_as_read()
        except (ChatRoom.DoesNotExist, ChatParticipant.DoesNotExist):
            pass
    
    @database_sync_to_async
    def update_typing_status(self, room_id, is_typing):
        """Update typing status for user in room"""
        if not self.user:
            return
        
        try:
            room = ChatRoom.objects.get(room_id=room_id)
            TypingStatus.objects.update_or_create(
                room=room,
                user=self.user,
                defaults={'is_typing': is_typing}
            )
        except ChatRoom.DoesNotExist:
            pass

