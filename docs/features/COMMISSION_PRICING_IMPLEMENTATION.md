# Commission-Based Pricing Plan Implementation

## Overview
This document describes the implementation of a commission-based pricing plan for the multivendor platform. This plan allows vendors to sell without monthly subscription fees, paying only a percentage commission on their sales.

## Business Requirements

### Commission Structure
- **5%** commission for orders under 1,000,000,000 Toman (1 billion)
- **3%** commission for orders above 1,000,000,000 Toman
- Commission calculated on: **Total order amount (excluding shipping and VAT)**
- Commission deducted when: **Vendor payment is made (after order delivery)**

### Plan Features
- ✅ Unlimited customers
- ✅ Unlimited products
- ✅ Marketplace visibility
- ✅ Standard support
- ❌ No monthly fee
- ⚠️ Requires signed contract and bank guarantee

### Activation Requirements
1. Complete vendor profile (store name, email, phone, address)
2. Accept terms and conditions
3. Sign and upload contract
4. Submit bank guarantee document with:
   - Guarantee amount
   - Expiry date
   - Valid bank document
5. Admin approval

## Technical Implementation

### 1. Database Changes

#### PricingTier Model Updates
**File:** `multivendor_platform/users/models.py`

New fields added:
```python
# Pricing type
pricing_type = CharField(choices=['subscription', 'commission'])
is_commission_based = BooleanField(default=False)

# Commission rates
commission_rate_low = DecimalField(max_digits=5, decimal_places=2)  # e.g., 5.00
commission_rate_high = DecimalField(max_digits=5, decimal_places=2)  # e.g., 3.00
commission_threshold = DecimalField(max_digits=20, decimal_places=2)  # e.g., 1000000000

# Subscription price
monthly_price = DecimalField(max_digits=10, decimal_places=2, null=True)
```

Methods added:
- `calculate_commission(order_amount)` - Calculate commission for given amount
- `get_commission_tier()` - Get or create commission tier

#### VendorSubscription Model Updates
**File:** `multivendor_platform/users/models.py`

New fields for contract management:
```python
# Contract
contract_signed = BooleanField(default=False)
contract_signed_at = DateTimeField(null=True)
contract_document = FileField(upload_to='vendor_contracts/')

# Bank Guarantee
bank_guarantee_submitted = BooleanField(default=False)
bank_guarantee_document = FileField(upload_to='bank_guarantees/')
bank_guarantee_amount = DecimalField(max_digits=20, decimal_places=2)
bank_guarantee_expiry = DateField()

# Terms & Approval
terms_accepted = BooleanField(default=False)
terms_accepted_at = DateTimeField(null=True)
admin_approved = BooleanField(default=False)
admin_approved_at = DateTimeField(null=True)
admin_approved_by = ForeignKey(User, null=True)
rejection_reason = TextField(null=True)

# Commission Tracking
total_commission_charged = DecimalField(default=0)
total_sales_volume = DecimalField(default=0)
```

Methods added:
- `can_activate_commission_plan()` - Check if vendor meets requirements
- `is_commission_plan_ready()` - Check if fully activated
- `record_commission_sale(sale_amount, commission_amount)` - Track commission

#### Order Model Updates
**File:** `multivendor_platform/orders/models.py`

New fields for commission tracking:
```python
commission_amount = DecimalField(default=0)
commission_rate = DecimalField(max_digits=5, decimal_places=2, null=True)
commission_paid = BooleanField(default=False)
commission_paid_at = DateTimeField(null=True)
vendor_payout_amount = DecimalField(null=True)
vendor_paid = BooleanField(default=False)
vendor_paid_at = DateTimeField(null=True)
```

Methods added:
- `calculate_commission()` - Calculate commission based on vendor's tier
- `apply_commission()` - Apply commission to order
- `mark_vendor_paid()` - Mark vendor as paid and record commission

### 2. Database Migrations

#### Migration 0010: Commission Pricing (Users App)
**File:** `multivendor_platform/users/migrations/0010_add_commission_based_pricing.py`

- Adds all commission-related fields to PricingTier
- Adds contract and guarantee fields to VendorSubscription
- Creates default commission tier with 5%/3% rates

#### Migration 0008: Commission Tracking (Orders App)
**File:** `multivendor_platform/orders/migrations/0008_add_commission_tracking.py`

- Adds commission tracking fields to Order model

### 3. API Endpoints

#### Vendor Endpoints

**GET /api/users/pricing-tiers/**
- List all available pricing tiers
- Returns commission rates and thresholds

**GET /api/users/seller/subscription/**
- Get current subscription with commission info
- Returns commission tracking data

**POST /api/users/seller/commission/activate/**
- Activate commission plan
- Requires: `terms_accepted: true`
- Validates profile completeness

**POST /api/users/seller/commission/upload-contract/**
- Upload signed contract
- Body: `contract_document` (file)

**POST /api/users/seller/commission/upload-guarantee/**
- Upload bank guarantee
- Body:
  - `bank_guarantee_document` (file)
  - `bank_guarantee_amount` (number)
  - `bank_guarantee_expiry` (date)

**GET /api/users/seller/commission/status/**
- Get commission plan status
- Returns:
  - Missing requirements
  - Approval status
  - Documents status

#### Admin Endpoints

**GET /api/users/admin/commission-requests/**
- List all commission plan requests
- Query params:
  - `status`: 'pending', 'approved', 'incomplete'

**POST /api/users/admin/commission-requests/{id}/approve/**
- Approve commission plan activation
- Records admin and timestamp

**POST /api/users/admin/commission-requests/{id}/reject/**
- Reject commission plan activation
- Body: `rejection_reason` (required)

#### Order Status Update (Enhanced)
**POST /api/users/admin/orders/{id}/status/**
- When status changed to 'delivered'
- Automatically calculates and applies commission
- Updates vendor payout amount

### 4. Frontend Components

#### PricingPlans.vue
**File:** `front_end/nuxt/components/seller/PricingPlans.vue`

Features:
- Displays 3 pricing tiers: Free, Premium, Commission
- Commission plan card with:
  - Green theme (success colors)
  - Prominent display of 5%/3% rates
  - "Contract required" indicator
  - Activation button opens dialog

Enhanced comparison grid showing:
- Monthly cost
- Commission percentage
- Customer limits
- Requirements

#### CommissionPlanActivation.vue
**File:** `front_end/nuxt/components/seller/CommissionPlanActivation.vue`

4-step wizard:
1. **Profile Check** - Validates vendor profile completeness
2. **Terms & Conditions** - Accept T&C for commission plan
3. **Contract Upload** - Download template, sign, and upload
4. **Bank Guarantee** - Upload guarantee with amount and expiry

Features:
- Step-by-step progress indicator
- Validation at each step
- File upload with preview
- Success/error messaging
- Persian (RTL) interface

### 5. Commission Calculation Flow

```
1. Order Created
   └─> Order total saved

2. Order Delivered (Status = 'delivered')
   └─> apply_commission() called
       ├─> Get vendor subscription
       ├─> Check if commission-based
       ├─> Calculate commission:
       │   ├─> If amount < 1B Toman: 5%
       │   └─> If amount >= 1B Toman: 3%
       ├─> Calculate vendor payout
       └─> Update order fields

3. Vendor Payment Processing
   └─> mark_vendor_paid() called
       ├─> Record commission in subscription
       ├─> Update total_commission_charged
       ├─> Update total_sales_volume
       └─> Set vendor_paid = True
```

### 6. Validation Rules

#### Profile Completeness Check
Required fields for commission plan activation:
- ✅ Vendor Profile: store_name, contact_email, contact_phone, address
- ✅ User Profile: phone

#### Contract Validation
- ✅ File format: PDF, JPG, PNG
- ✅ Must be uploaded before activation
- ✅ Signed timestamp recorded

#### Bank Guarantee Validation
- ✅ File format: PDF, JPG, PNG
- ✅ Amount must be specified
- ✅ Expiry date must be provided
- ✅ Document must be from bank

#### Admin Approval
- ✅ All documents submitted
- ✅ Profile complete
- ✅ Terms accepted
- ⚠️ Manual admin review required

## Usage Examples

### For Vendors

#### 1. Check Available Plans
```javascript
const response = await $api('/api/users/pricing-tiers/')
// Returns: [free, premium, commission] tiers with rates
```

#### 2. Activate Commission Plan
```javascript
// Step 1: Accept terms
await $api('/api/users/seller/commission/activate/', {
  method: 'POST',
  body: { terms_accepted: true }
})

// Step 2: Upload contract
const contractForm = new FormData()
contractForm.append('contract_document', contractFile)
await $api('/api/users/seller/commission/upload-contract/', {
  method: 'POST',
  body: contractForm
})

// Step 3: Upload guarantee
const guaranteeForm = new FormData()
guaranteeForm.append('bank_guarantee_document', guaranteeFile)
guaranteeForm.append('bank_guarantee_amount', '10000000')
guaranteeForm.append('bank_guarantee_expiry', '2025-12-31')
await $api('/api/users/seller/commission/upload-guarantee/', {
  method: 'POST',
  body: guaranteeForm
})
```

#### 3. Check Status
```javascript
const status = await $api('/api/users/seller/commission/status/')
// Returns: approval status, missing requirements, documents
```

### For Admins

#### 1. View Pending Requests
```javascript
const requests = await $api('/api/users/admin/commission-requests/?status=pending')
```

#### 2. Approve Request
```javascript
await $api(`/api/users/admin/commission-requests/${subscriptionId}/approve/`, {
  method: 'POST'
})
```

#### 3. Reject Request
```javascript
await $api(`/api/users/admin/commission-requests/${subscriptionId}/reject/`, {
  method: 'POST',
  body: { rejection_reason: 'ضمانت‌نامه نامعتبر است' }
})
```

## Testing Checklist

### Backend Tests
- [ ] Commission calculation (5% under threshold, 3% above)
- [ ] Profile validation checks
- [ ] Contract upload and storage
- [ ] Bank guarantee upload and storage
- [ ] Admin approval workflow
- [ ] Order commission application
- [ ] Vendor payment tracking

### Frontend Tests
- [ ] Commission plan display in pricing page
- [ ] Activation dialog workflow
- [ ] File upload functionality
- [ ] Validation error messages
- [ ] Success notifications
- [ ] Admin approval interface

### Integration Tests
- [ ] End-to-end activation flow
- [ ] Order with commission calculation
- [ ] Vendor payout calculation
- [ ] Commission tracking accuracy

## Security Considerations

1. **File Upload Security**
   - Validate file types (PDF, JPG, PNG only)
   - Limit file sizes
   - Store in secure location with access control

2. **Contract Integrity**
   - Store original upload timestamp
   - Track contract modifications
   - Admin-only access to contract files

3. **Bank Guarantee**
   - Verify expiry dates
   - Alert when guarantee expires
   - Require renewal before expiry

4. **Commission Calculation**
   - Double-check calculations
   - Log all commission charges
   - Audit trail for disputes

## Future Enhancements

1. **Automated Contract Generation**
   - Generate contracts with vendor details
   - Digital signature integration
   - Email contract to vendor

2. **Commission Analytics**
   - Dashboard showing commission earned
   - Monthly commission reports
   - Trending commission data

3. **Multiple Commission Tiers**
   - Category-based commission rates
   - Volume-based discounts
   - Promotional commission rates

4. **Payment Integration**
   - Automatic commission deduction
   - Direct vendor payouts
   - Invoice generation

5. **Notification System**
   - Alert vendor when approved/rejected
   - Remind admin of pending requests
   - Notify when guarantee expires

## Deployment Notes

### Migration Steps
```bash
# 1. Apply migrations
python manage.py migrate users 0010_add_commission_based_pricing
python manage.py migrate orders 0008_add_commission_tracking

# 2. Create commission tier (automatic via migration)
# Verify with:
python manage.py shell
>>> from users.models import PricingTier
>>> PricingTier.objects.get(slug='commission')

# 3. Update frontend dependencies
cd front_end/nuxt
npm install
npm run build
```

### Configuration
No environment variables needed. Commission rates configured in database via PricingTier model.

### Monitoring
Monitor:
- Commission calculations for accuracy
- File uploads for storage usage
- Admin approval queue length
- Vendor activation success rate

## Support & Troubleshooting

### Common Issues

**Issue:** Vendor can't activate commission plan
- Check profile completeness via `/api/users/seller/commission/status/`
- Verify all required fields are filled

**Issue:** Commission not calculated
- Verify order status is 'delivered'
- Check vendor is on commission-based tier
- Review order total_amount is set

**Issue:** Admin can't approve request
- Ensure contract and guarantee are uploaded
- Verify all documents are accessible

## Conclusion

The commission-based pricing plan provides vendors with a flexible, low-risk option to grow their business without upfront subscription costs. The implementation ensures proper tracking, security, and admin oversight while maintaining a user-friendly experience.

For questions or issues, refer to the API documentation or contact the development team.
