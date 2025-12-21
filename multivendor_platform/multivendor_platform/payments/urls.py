"""
URLs for Payment APIs
"""
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment request
    path('premium/request/', views.request_premium_payment, name='request_premium_payment'),
    
    # Discount validation
    path('premium/validate-discount/', views.validate_discount_code, name='validate_discount_code'),
    
    # Callback from Zibal
    path('premium/callback/', views.payment_callback, name='payment_callback'),
    
    # Manual verification
    path('premium/verify/<str:track_id>/', views.verify_payment_manual, name='verify_payment'),
    
    # Payment history
    path('history/', views.payment_history, name='payment_history'),
    
    # Invoice download
    path('invoice/<int:invoice_id>/download/', views.download_invoice, name='download_invoice'),
]

