# Payment Management System

## Overview

This Django app handles premium subscription payments through the Zibal payment gateway.

## Features

- ✅ Zibal payment gateway integration
- ✅ Monthly/Quarterly/Semiannual/Yearly subscriptions
- ✅ Automatic subscription activation
- ✅ PDF invoice generation
- ✅ Payment history tracking
- ✅ Automatic expiry checking
- ✅ Renewal reminders

## Quick Start

### 1. Install Dependencies

```bash
pip install requests reportlab
```

### 2. Set Environment Variables

```env
ZIBAL_MERCHANT=zibal  # Use 'zibal' for testing
SITE_URL=http://localhost:8000
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Premium Tier

```python
from users.models import PricingTier

premium = PricingTier.objects.create(
    slug='premium',
    name='Premium',
    pricing_type='subscription',
    monthly_price=1500000,
    monthly_price_rial=15000000,
    daily_customer_unlock_limit=0,
    allow_marketplace_visibility=True
)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/payments/premium/request/` | Request payment |
| GET | `/api/payments/premium/callback/` | Zibal callback |
| POST | `/api/payments/premium/verify/<track_id>/` | Manual verify |
| GET | `/api/payments/history/` | Payment history |
| GET | `/api/payments/invoice/<id>/download/` | Download invoice |

## Models

### PremiumSubscriptionPayment

Stores payment transactions with Zibal tracking information.

**Key fields:**
- `track_id`: Zibal transaction ID
- `status`: pending/paid/verified/failed/cancelled
- `amount`: Amount in Rials
- `billing_period`: monthly/quarterly/semiannual/yearly

### PaymentInvoice

Stores invoices for verified payments.

**Key fields:**
- `invoice_number`: Auto-generated unique number
- `invoice_pdf`: PDF file
- `total_amount`: Total including tax

## Management Commands

### Check Expired Subscriptions

```bash
# Dry run (no changes)
python manage.py check_subscription_expiry --dry-run

# Actual run
python manage.py check_subscription_expiry
```

Run daily via cron:
```cron
0 1 * * * python manage.py check_subscription_expiry
```

### Send Renewal Reminders

```bash
# 3 days before expiry
python manage.py send_renewal_reminders --days=3
```

Run daily via cron:
```cron
0 9 * * * python manage.py send_renewal_reminders --days=3
```

## Testing

```bash
python manage.py test payments
```

## Admin Panel

Access at `/admin/` to:
- View all payments
- Filter by status
- Download invoices
- Mark payments as failed
- Regenerate invoices

## Documentation

Full documentation (in Persian) available at:
- `docs/ZIBAL_PAYMENT_INTEGRATION.md` - Complete integration guide
- `docs/ZIBAL_IMPLEMENTATION_SUMMARY.md` - Implementation summary

## Production Checklist

- [ ] Get real merchant ID from Zibal
- [ ] Update `ZIBAL_MERCHANT` in environment
- [ ] Set `SITE_URL` to production URL
- [ ] Install reportlab: `pip install reportlab`
- [ ] Create Premium PricingTier
- [ ] Setup cron jobs for management commands
- [ ] Test complete payment flow
- [ ] Monitor logs

## Support

For issues related to:
- **Zibal:** https://zibal.ir/support
- **Platform:** Check logs and documentation

## Version

Current version: 1.0.0  
Last updated: December 2024

