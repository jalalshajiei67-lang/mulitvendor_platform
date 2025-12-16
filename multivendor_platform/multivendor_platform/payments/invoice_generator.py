"""
PDF Invoice Generator for Premium Subscriptions
Generates Persian RTL invoices for payments
"""
from io import BytesIO
from datetime import datetime
from decimal import Decimal
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logger.warning("reportlab not installed. PDF invoice generation will not work.")


class InvoiceGenerator:
    """Generate PDF invoices for premium subscription payments"""
    
    def __init__(self):
        if not REPORTLAB_AVAILABLE:
            raise ImportError("reportlab is required for invoice generation. Install it with: pip install reportlab")
    
    def generate_invoice(self, invoice_obj, payment_obj) -> BytesIO:
        """
        Generate PDF invoice
        
        Args:
            invoice_obj: PaymentInvoice model instance
            payment_obj: PremiumSubscriptionPayment model instance
        
        Returns:
            BytesIO object containing PDF data
        """
        buffer = BytesIO()
        
        # Create PDF canvas
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # Set metadata
        p.setTitle(f"Invoice {invoice_obj.invoice_number}")
        p.setAuthor("Indexo Platform")
        p.setSubject(f"Payment Invoice for {payment_obj.user.username}")
        
        # Note: For proper Persian/Arabic text, you would need to:
        # 1. Register a Persian font (like Vazir, Shabnam, etc.)
        # 2. Use Arabic reshaper and python-bidi for RTL text
        # For now, we'll use a simple English-based invoice
        
        # Header
        y_position = height - 40 * mm
        
        # Company name
        p.setFont("Helvetica-Bold", 20)
        p.drawString(50 * mm, y_position, "INDEXO PLATFORM")
        
        # Invoice title
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50 * mm, y_position - 10 * mm, "PREMIUM SUBSCRIPTION INVOICE")
        
        # Invoice details
        y_position -= 25 * mm
        p.setFont("Helvetica", 10)
        
        details = [
            f"Invoice Number: {invoice_obj.invoice_number}",
            f"Issue Date: {invoice_obj.issue_date.strftime('%Y-%m-%d %H:%M')}",
            f"Due Date: {invoice_obj.due_date.strftime('%Y-%m-%d')}",
            "",
            f"Customer: {payment_obj.user.username}",
            f"Email: {payment_obj.user.email}",
            f"Track ID: {payment_obj.track_id}",
            f"Reference: {payment_obj.ref_number or 'N/A'}",
        ]
        
        for detail in details:
            p.drawString(50 * mm, y_position, detail)
            y_position -= 5 * mm
        
        # Payment details table
        y_position -= 10 * mm
        
        # Table header
        p.setFont("Helvetica-Bold", 11)
        p.drawString(50 * mm, y_position, "Description")
        p.drawString(120 * mm, y_position, "Amount (Rials)")
        
        y_position -= 2 * mm
        p.line(50 * mm, y_position, 170 * mm, y_position)
        y_position -= 5 * mm
        
        # Table rows
        p.setFont("Helvetica", 10)
        billing_period_display = payment_obj.get_billing_period_display()
        p.drawString(50 * mm, y_position, f"Premium Subscription - {billing_period_display}")
        p.drawRightString(170 * mm, y_position, f"{int(invoice_obj.subtotal):,}")
        
        y_position -= 8 * mm
        
        # Subtotal
        p.drawString(50 * mm, y_position, "Subtotal:")
        p.drawRightString(170 * mm, y_position, f"{int(invoice_obj.subtotal):,}")
        
        y_position -= 5 * mm
        
        # Tax (9% VAT)
        if invoice_obj.tax_amount > 0:
            p.drawString(50 * mm, y_position, "Tax (9% VAT):")
            p.drawRightString(170 * mm, y_position, f"{int(invoice_obj.tax_amount):,}")
            y_position -= 5 * mm
        
        # Draw line
        p.line(50 * mm, y_position, 170 * mm, y_position)
        y_position -= 5 * mm
        
        # Total
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50 * mm, y_position, "Total:")
        p.drawRightString(170 * mm, y_position, f"{int(invoice_obj.total_amount):,}")
        
        # Payment status
        y_position -= 10 * mm
        p.setFont("Helvetica", 10)
        
        if payment_obj.status == 'verified':
            p.setFillColorRGB(0, 0.5, 0)
            status_text = "PAID"
        else:
            p.setFillColorRGB(0.8, 0, 0)
            status_text = "PENDING"
        
        p.drawString(50 * mm, y_position, f"Payment Status: {status_text}")
        p.setFillColorRGB(0, 0, 0)
        
        if payment_obj.paid_at:
            y_position -= 5 * mm
            p.drawString(50 * mm, y_position, f"Paid At: {payment_obj.paid_at.strftime('%Y-%m-%d %H:%M')}")
        
        if payment_obj.card_number:
            y_position -= 5 * mm
            p.drawString(50 * mm, y_position, f"Card Number: {payment_obj.card_number}")
        
        # Footer
        y_position = 30 * mm
        p.setFont("Helvetica-Oblique", 8)
        p.drawCentredString(width / 2, y_position, "Thank you for using Indexo Platform")
        p.drawCentredString(width / 2, y_position - 4 * mm, "https://indexo.ir")
        
        # Finalize PDF
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return buffer
    
    def generate_and_save_invoice(self, invoice_obj, payment_obj) -> bool:
        """
        Generate PDF invoice and save to model
        
        Args:
            invoice_obj: PaymentInvoice model instance
            payment_obj: PremiumSubscriptionPayment model instance
        
        Returns:
            bool: True if successful
        """
        try:
            pdf_buffer = self.generate_invoice(invoice_obj, payment_obj)
            
            # Save to model
            filename = f"invoice_{invoice_obj.invoice_number}.pdf"
            invoice_obj.invoice_pdf.save(
                filename,
                ContentFile(pdf_buffer.getvalue()),
                save=True
            )
            
            logger.info(f"Invoice generated successfully: {invoice_obj.invoice_number}")
            return True
        
        except Exception as e:
            logger.error(f"Error generating invoice {invoice_obj.invoice_number}: {str(e)}")
            return False


def create_invoice_for_payment(payment_obj):
    """
    Create and generate invoice for a payment
    
    Args:
        payment_obj: PremiumSubscriptionPayment model instance
    
    Returns:
        PaymentInvoice instance or None
    """
    from .models import PaymentInvoice
    from decimal import Decimal
    
    try:
        # Check if invoice already exists
        if hasattr(payment_obj, 'invoice'):
            logger.info(f"Invoice already exists for payment {payment_obj.track_id}")
            return payment_obj.invoice
        
        # Calculate amounts
        subtotal = payment_obj.amount
        tax_rate = Decimal('0.09')  # 9% VAT
        tax_amount = subtotal * tax_rate
        total_amount = subtotal + tax_amount
        
        # Create invoice
        invoice = PaymentInvoice.objects.create(
            payment=payment_obj,
            subtotal=subtotal,
            tax_amount=tax_amount,
            total_amount=total_amount,
        )
        
        # Generate PDF
        if REPORTLAB_AVAILABLE:
            generator = InvoiceGenerator()
            generator.generate_and_save_invoice(invoice, payment_obj)
        else:
            logger.warning(f"Cannot generate PDF for invoice {invoice.invoice_number} - reportlab not available")
        
        return invoice
    
    except Exception as e:
        logger.error(f"Error creating invoice for payment {payment_obj.track_id}: {str(e)}")
        return None

