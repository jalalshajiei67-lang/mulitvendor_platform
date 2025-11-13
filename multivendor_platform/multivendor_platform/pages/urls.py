from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AboutPageViewSet, ContactPageViewSet

# Create a router for the API endpoints
router = DefaultRouter()
router.register(r'about', AboutPageViewSet, basename='about-page')
router.register(r'contact', ContactPageViewSet, basename='contact-page')

app_name = 'pages'

urlpatterns = [
    path('', include(router.urls)),
]

