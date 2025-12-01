import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class GuestSession(models.Model):
    """Track anonymous guest users before they register"""
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    identifier = models.CharField(max_length=255, help_text="Browser fingerprint or identifier")
    linked_user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='guest_sessions',
        help_text="User account linked after registration"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Guest Session"
        verbose_name_plural = "Guest Sessions"
        ordering = ['-created_at']
    
    def __str__(self):
        if self.linked_user:
            return f"Guest {self.session_id} (linked to {self.linked_user.username})"
        return f"Guest {self.session_id}"


class ChatRoom(models.Model):
    """One-on-one chat room between users"""
    room_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    participants = models.ManyToManyField(
        User, 
        through='ChatParticipant',
        related_name='chat_rooms'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chat_rooms',
        help_text="Product this chat is about (if any)"
    )
    guest_session = models.ForeignKey(
        GuestSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chat_rooms',
        help_text="Guest session if chat started anonymously"
    )
    is_archived = models.BooleanField(default=False, help_text="Archived chats are hidden")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Chat Room"
        verbose_name_plural = "Chat Rooms"
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['-updated_at']),
            models.Index(fields=['room_id']),
        ]
    
    def __str__(self):
        participant_names = ', '.join([p.username for p in self.participants.all()[:3]])
        if self.product:
            return f"Chat about {self.product.name}: {participant_names}"
        return f"Chat: {participant_names}"
    
    def get_other_participant(self, user):
        """Get the other participant in a 1-on-1 chat"""
        return self.participants.exclude(id=user.id).first()
    
    def get_unread_count(self, user):
        """Get unread message count for a specific user"""
        participant = self.chatparticipant_set.filter(user=user).first()
        if not participant:
            return 0
        
        if participant.last_read_at:
            return self.messages.filter(created_at__gt=participant.last_read_at).exclude(sender=user).count()
        return self.messages.exclude(sender=user).count()
    
    def get_last_message(self):
        """Get the most recent message in this room"""
        return self.messages.order_by('-created_at').first()


class ChatParticipant(models.Model):
    """Through model for chat room participants with metadata"""
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Chat Participant"
        verbose_name_plural = "Chat Participants"
        unique_together = ['room', 'user']
        ordering = ['joined_at']
    
    def __str__(self):
        return f"{self.user.username} in {self.room.room_id}"
    
    def mark_as_read(self):
        """Mark all messages as read up to now"""
        self.last_read_at = timezone.now()
        self.save(update_fields=['last_read_at'])


class ChatMessage(models.Model):
    """Individual message in a chat room"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_messages',
        help_text="Null if sent by guest"
    )
    guest_session = models.ForeignKey(
        GuestSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages',
        help_text="Guest session if sent by guest"
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        verbose_name = "Chat Message"
        verbose_name_plural = "Chat Messages"
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['room', 'created_at']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        sender_name = self.sender.username if self.sender else f"Guest {self.guest_session.session_id}"
        return f"{sender_name}: {self.content[:50]}"
    
    def mark_as_read(self):
        """Mark this message as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    @classmethod
    def delete_old_messages(cls, days=90):
        """Delete messages older than specified days (default 90 days / 3 months)"""
        cutoff_date = timezone.now() - timedelta(days=days)
        old_messages = cls.objects.filter(created_at__lt=cutoff_date)
        count = old_messages.count()
        old_messages.delete()
        return count


class TypingStatus(models.Model):
    """Track who is typing in which room (temporary real-time data)"""
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='typing_statuses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_typing = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Typing Status"
        verbose_name_plural = "Typing Statuses"
        unique_together = ['room', 'user']
        ordering = ['-updated_at']
    
    def __str__(self):
        status = "typing" if self.is_typing else "stopped"
        return f"{self.user.username} {status} in {self.room.room_id}"
    
    @classmethod
    def cleanup_stale_statuses(cls, minutes=5):
        """Remove typing statuses older than specified minutes"""
        cutoff_time = timezone.now() - timedelta(minutes=minutes)
        cls.objects.filter(updated_at__lt=cutoff_time).delete()







