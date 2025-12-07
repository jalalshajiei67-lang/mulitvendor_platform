from django.contrib import admin
from .models import ChatRoom, ChatMessage, ChatParticipant, GuestSession, TypingStatus


@admin.register(GuestSession)
class GuestSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'identifier', 'linked_user', 'created_at']
    list_filter = ['created_at', 'linked_user']
    search_fields = ['session_id', 'identifier', 'linked_user__username']
    readonly_fields = ['session_id', 'created_at']
    raw_id_fields = ['linked_user']


class ChatParticipantInline(admin.TabularInline):
    model = ChatParticipant
    extra = 0
    readonly_fields = ['joined_at', 'last_read_at']
    raw_id_fields = ['user']


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['id', 'sender', 'created_at', 'is_read', 'read_at']
    fields = ['sender', 'guest_session', 'content', 'is_read', 'created_at']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['room_id', 'get_participants', 'product', 'guest_session', 'is_archived', 'created_at', 'updated_at']
    list_filter = ['is_archived', 'created_at', 'updated_at']
    search_fields = ['room_id', 'product__name', 'participants__username']
    readonly_fields = ['room_id', 'created_at', 'updated_at']
    raw_id_fields = ['product', 'guest_session']
    inlines = [ChatParticipantInline, ChatMessageInline]
    
    def get_participants(self, obj):
        return ', '.join([p.username for p in obj.participants.all()])
    get_participants.short_description = 'Participants'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_sender', 'room', 'content_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['content', 'sender__username', 'room__room_id']
    readonly_fields = ['id', 'created_at', 'read_at']
    raw_id_fields = ['room', 'sender', 'guest_session']
    date_hierarchy = 'created_at'
    
    def get_sender(self, obj):
        if obj.sender:
            return obj.sender.username
        elif obj.guest_session:
            return f"Guest ({obj.guest_session.session_id})"
        return "Unknown"
    get_sender.short_description = 'Sender'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(ChatParticipant)
class ChatParticipantAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'joined_at', 'last_read_at']
    list_filter = ['joined_at']
    search_fields = ['user__username', 'room__room_id']
    readonly_fields = ['joined_at']
    raw_id_fields = ['room', 'user']


@admin.register(TypingStatus)
class TypingStatusAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'is_typing', 'updated_at']
    list_filter = ['is_typing', 'updated_at']
    search_fields = ['user__username', 'room__room_id']
    readonly_fields = ['updated_at']
    raw_id_fields = ['room', 'user']









