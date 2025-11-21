from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rooms', views.ChatRoomViewSet, basename='chatroom')

urlpatterns = [
    path('', include(router.urls)),
    path('guest-session/', views.create_guest_session, name='create-guest-session'),
    path('link-guest-session/', views.link_guest_session, name='link-guest-session'),
    path('start/', views.start_chat, name='start-chat'),
    path('vendor/rooms/', views.vendor_rooms, name='vendor-rooms'),
    path('admin/rooms/', views.admin_rooms, name='admin-rooms'),
]

