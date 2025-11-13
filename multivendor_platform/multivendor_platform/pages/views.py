from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import AboutPage, ContactPage
from .serializers import AboutPageSerializer, ContactPageSerializer


class AboutPageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for About Us page.
    GET /api/pages/about/ - Get the About Us page content
    """
    queryset = AboutPage.objects.all()
    serializer_class = AboutPageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """
        Get the current About Us page (since only one instance exists)
        Endpoint: /api/pages/about/current/
        """
        try:
            page = AboutPage.objects.first()
            if page:
                serializer = self.get_serializer(page)
                return Response(serializer.data)
            return Response(
                {'detail': 'صفحه درباره ما هنوز ایجاد نشده است'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ContactPageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Contact Us page.
    GET /api/pages/contact/ - Get the Contact Us page content
    """
    queryset = ContactPage.objects.all()
    serializer_class = ContactPageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """
        Get the current Contact Us page (since only one instance exists)
        Endpoint: /api/pages/contact/current/
        """
        try:
            page = ContactPage.objects.first()
            if page:
                serializer = self.get_serializer(page)
                return Response(serializer.data)
            return Response(
                {'detail': 'صفحه تماس با ما هنوز ایجاد نشده است'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

