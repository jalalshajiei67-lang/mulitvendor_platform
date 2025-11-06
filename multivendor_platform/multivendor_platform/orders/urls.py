from django.urls import path
from .views import (
    create_rfq_view,
    admin_rfq_list_view,
    admin_rfq_detail_view,
    vendor_rfq_list_view,
    admin_update_rfq_status_view
)

urlpatterns = [
    # RFQ endpoints
    path('rfq/create/', create_rfq_view, name='create-rfq'),
    path('admin/rfq/', admin_rfq_list_view, name='admin-rfq-list'),
    path('admin/rfq/<int:rfq_id>/', admin_rfq_detail_view, name='admin-rfq-detail'),
    path('admin/rfq/<int:rfq_id>/status/', admin_update_rfq_status_view, name='admin-update-rfq-status'),
    path('vendor/rfq/', vendor_rfq_list_view, name='vendor-rfq-list'),
]

