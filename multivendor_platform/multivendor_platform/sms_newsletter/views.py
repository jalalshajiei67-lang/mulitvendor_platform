from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models import Q
from .models import Seller
from .serializers import SellerSerializer, SellerListSerializer, SendSmsSerializer
from .services import send_sms_via_kavenegar
from products.models import Subcategory


class SellerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing sellers with filtering by working fields.
    Admin only.
    """
    queryset = Seller.objects.all().prefetch_related('working_fields')
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SellerListSerializer
        return SellerSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by working fields (subcategories)
        working_field_ids = self.request.query_params.getlist('working_fields')
        if working_field_ids:
            # Convert to integers
            try:
                working_field_ids = [int(id) for id in working_field_ids if id]
                if working_field_ids:
                    # Filter sellers that have at least one of the selected working fields
                    queryset = queryset.filter(working_fields__id__in=working_field_ids).distinct()
            except ValueError:
                pass  # Invalid IDs, ignore filter
        
        return queryset.order_by('name')


@api_view(['POST'])
@permission_classes([IsAdminUser])
def send_sms_view(request):
    """
    Send SMS to selected sellers via Kavenegar API.
    
    POST /api/sms-newsletter/send/
    Body: {
        "seller_ids": [1, 2, 3],
        "working_field_ids": [10, 20]  # Optional
    }
    """
    serializer = SendSmsSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid data', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    seller_ids = serializer.validated_data['seller_ids']
    working_field_ids = serializer.validated_data.get('working_field_ids', [])
    
    # Filter name is required
    if not working_field_ids:
        return Response(
            {'error': 'working_field_ids is required. Please apply a filter first.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get sellers
    try:
        sellers = Seller.objects.filter(id__in=seller_ids).prefetch_related('working_fields')
        if sellers.count() != len(seller_ids):
            return Response(
                {'error': 'Some seller IDs not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        return Response(
            {'error': f'Error fetching sellers: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Get filter name from working field IDs
    try:
        subcategories = Subcategory.objects.filter(id__in=working_field_ids)
        if not subcategories.exists():
            return Response(
                {'error': 'No valid working fields found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Combine names, limit to 45 chars
        names = [sc.name for sc in subcategories]
        filter_name = ", ".join(names)
        if len(filter_name) > 45:
            # Try to fit as many as possible within 45 chars
            result = ""
            for name in names:
                if len(result) + len(name) + 2 <= 45:  # +2 for ", "
                    if result:
                        result += ", "
                    result += name
                else:
                    break
            if not result:  # Even first name is too long
                result = names[0][:42] + "..."
            else:
                result = result[:42] + "..."
            filter_name = result
    except Exception as e:
        return Response(
            {'error': f'Error fetching working fields: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Send SMS to each seller
    results = []
    for seller in sellers:
        result = send_sms_via_kavenegar(seller, filter_name=filter_name)
        results.append({
            'seller_id': seller.id,
            'seller_name': seller.name,
            'mobile_number': seller.mobile_number,
            'success': result['success'],
            'message': result['message']
        })
    
    # Count successes and failures
    success_count = sum(1 for r in results if r['success'])
    failure_count = len(results) - success_count
    
    return Response({
        'total': len(results),
        'success_count': success_count,
        'failure_count': failure_count,
        'results': results
    }, status=status.HTTP_200_OK)

