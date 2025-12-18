# Auction System

Complete auction system for the multivendor platform with tiered submission, blind bidding, admin validation, and deposit forfeiture.

## Features

- **Tiered Submission**: Free requests (forms only) vs Verified requests (with deposit)
- **Blind Bidding**: Sellers see "Bidder #X", buyers see real seller names
- **Feature Templates**: Dynamic forms based on subcategory templates
- **Deposit System**: 5,000,000 Toman deposit for verified requests
- **Early Award**: Buyers can close auctions early (with restrictions for live auctions)
- **Deposit Forfeiture**: Automatic forfeiture after 72 hours if buyer doesn't select winner
- **Admin Review**: All auctions require admin approval before going active

## Models

- `AuctionRequest`: Main auction model
- `Bid`: Seller bids with identity masking
- `AuctionDepositPayment`: Zibal payment integration
- `AuctionPhoto`: Photo attachments
- `AuctionDocument`: Document attachments (verified requests only)
- `AuctionReport`: Admin-written reports
- `AuctionNotification`: Event notifications

## API Endpoints

- `GET /api/auctions/auctions/` - List buyer's auctions
- `POST /api/auctions/auctions/` - Create auction request
- `GET /api/auctions/auctions/{id}/` - Get auction details
- `POST /api/auctions/auctions/{id}/accept_bid/` - Accept bid and close early
- `POST /api/auctions/auctions/{id}/close_early/` - Close auction early
- `GET /api/auctions/auction-list/` - List active auctions (for sellers)
- `POST /api/auctions/bids/` - Create bid
- `GET /api/auctions/bids/?auction={id}` - Get bids for auction
- `POST /api/auctions/deposit/request/` - Request deposit payment
- `GET /api/auctions/deposit/callback/` - Zibal payment callback
- `POST /api/auctions/photos/upload/` - Upload photo
- `POST /api/auctions/documents/upload/` - Upload document (verified only)

## Management Commands

### Check Auction Deposits

Checks for expired auction deposits and forfeits them according to the 72-hour rule.

```bash
# Dry run (no changes)
python manage.py check_auction_deposits --dry-run

# Actual run
python manage.py check_auction_deposits
```

**What it does:**
- Finds auctions closed > 72 hours ago
- Checks if buyer hasn't selected a winner
- Verifies deposit status is 'held_in_escrow'
- Forfeits deposit and distributes:
  - 50% to platform (admin fee)
  - 25% to top bidder
  - 25% to second bidder (if exists)
- Marks auction as 'abandoned'
- Sends notifications to all parties

**Cron Job Setup:**

Run hourly via cron:
```bash
# Setup script
./setup-cron-auction-deposits.sh

# Or manually add to crontab:
0 * * * * cd /path/to/project && python manage.py check_auction_deposits >> /var/log/auction-deposits.log 2>&1
```

## Workflow

### Phase 1: Request & Filtering
1. Buyer clicks "Request Auction" on product page
2. Redirected to signup if not authenticated
3. Fills multi-step form:
   - Select subcategory (loads feature templates)
   - Fill technical specs
   - Choose auction style (sealed/live_reverse)
   - Set start/end time
   - Upload photos
   - Option to pay deposit (5M Toman) for verified request
4. Admin reviews and approves/rejects

### Phase 2: Bidding Room
1. System publishes approved auction
2. Notifications sent to sellers in subcategory
3. Sellers see commitment badges:
   - 🟢 Green: Deposit Paid
   - 🟡 Yellow: Verified Company / No Deposit
   - ⚪ Grey: Guest User
4. Sellers submit bids with compliance matrix
5. Identity masking: sellers see "Bidder #X", buyer sees real names

### Phase 3: Selection & Closing
1. Buyer can accept bid and close early
   - Live auctions: Cannot close in last 1 hour
   - Sealed auctions: Can close anytime
2. Admin writes report after closing
3. All participants can view report

### Phase 4: Financial Settlement
1. If buyer paid deposit but doesn't select winner within 72 hours:
   - Warning email at 48 hours
   - Automatic forfeiture at 72 hours
   - Deposit split: 50% platform, 25% bidder #1, 25% bidder #2

## Settings

Add to `settings.py`:
```python
AUCTION_DEPOSIT_AMOUNT = 5000000  # 5,000,000 Toman
```

## Testing

```bash
# Test deposit forfeiture (dry run)
python manage.py check_auction_deposits --dry-run

# Test deposit forfeiture (actual)
python manage.py check_auction_deposits
```

## Admin Panel

Access at `/admin/auctions/` to:
- View all auctions
- Approve/reject requests
- Write reports
- View bids with seller names
- Manage deposit payments

## Notifications

Automatic notifications sent for:
- Auction published (to sellers)
- Bid received (to buyer)
- Auction closed (to all participants)
- Deposit forfeiture warning (48 hours)
- Deposit forfeited (72 hours)

## Identity Masking

- **Buyer sees**: Real seller names and IDs
- **Seller (own bid)**: Real name, "You" as bidder number
- **Seller (other bids)**: "Bidder #X", no name/ID

## Document Upload Restriction

Documents can only be uploaded if:
- `deposit_status == 'paid'` or `'held_in_escrow'`
- OR `user_type == 'paid'` (premium user)

Frontend and backend both enforce this restriction.

## Production Checklist

- [ ] Run migrations: `python manage.py makemigrations auctions && python manage.py migrate`
- [ ] Setup cron job: `./setup-cron-auction-deposits.sh`
- [ ] Test payment flow with Zibal
- [ ] Test deposit forfeiture command
- [ ] Verify notifications are working
- [ ] Test identity masking
- [ ] Test document upload restrictions
- [ ] Monitor logs: `tail -f /var/log/auction-deposits.log`

## Support

For issues, check:
- Logs: `/var/log/auction-deposits.log`
- Django logs
- Admin panel for auction status

