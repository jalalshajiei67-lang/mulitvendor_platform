from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from .models import ReverseAuction, AuctionInvitation, Bid
from products.models import Product


class AuctionService:
    """Service class for auction business logic"""
    
    @staticmethod
    def auto_invite_suppliers(auction):
        """
        Automatically invite suppliers based on category match.
        Finds suppliers who have active products in the same category.
        """
        if not auction.category:
            return []
        
        # Find suppliers who have active products in this category
        suppliers_with_products = User.objects.filter(
            products__category=auction.category,
            products__is_active=True
        ).distinct()
        
        # Only invite suppliers (users with seller role)
        invited_users = []
        for supplier in suppliers_with_products:
            # Check if user is a seller
            try:
                profile = supplier.profile
                if profile.is_seller():
                    # Create invitation if it doesn't exist
                    invitation, created = AuctionInvitation.objects.get_or_create(
                        auction=auction,
                        supplier=supplier
                    )
                    if created:
                        invited_users.append(supplier)
            except:
                # If profile doesn't exist, skip
                continue
        
        return invited_users
    
    @staticmethod
    def calculate_all_ranks(auction):
        """
        Recalculate rank for all bids in an auction.
        This should be called after a new bid is placed.
        """
        # Get all bids ordered by amount (lowest first)
        bids = Bid.objects.filter(auction=auction).order_by('amount', 'created_at')
        
        rank = 1
        previous_amount = None
        for bid in bids:
            # If amount is same as previous, keep same rank
            if previous_amount is not None and bid.amount == previous_amount:
                # Don't increment rank for ties
                pass
            else:
                # New rank for new amount
                rank = rank
            
            bid.rank = rank
            bid.is_winning = (rank == 1)
            bid.save(update_fields=['rank', 'is_winning'])
            
            previous_amount = bid.amount
            rank += 1
    
    @staticmethod
    def check_soft_close(auction):
        """
        Check if auction should be extended (soft close).
        If a bid is placed in the last 5 minutes, extend by 5 minutes.
        Returns True if extended, False otherwise.
        """
        return auction.extend_deadline()
    
    @staticmethod
    def validate_bid(auction, supplier, amount):
        """
        Validate that a bid meets all requirements:
        1. Auction must be active
        2. Supplier must be invited
        3. Amount must be less than supplier's previous bid (or starting price if first bid)
        4. Amount must respect minimum decrement if set
        5. Must be before deadline
        
        Returns (is_valid: bool, error_message: str)
        """
        # Check auction is active
        if auction.status != 'active':
            return False, "Auction is not active"
        
        # Check deadline hasn't passed
        if timezone.now() >= auction.deadline:
            return False, "Auction deadline has passed"
        
        # Check supplier is invited
        try:
            invitation = AuctionInvitation.objects.get(auction=auction, supplier=supplier)
        except AuctionInvitation.DoesNotExist:
            return False, "You are not invited to this auction"
        
        # Check amount is less than starting price
        if amount >= auction.starting_price:
            return False, f"Bid must be less than starting price ({auction.starting_price})"
        
        # Check against previous bid
        previous_bid = Bid.objects.filter(
            auction=auction,
            supplier=supplier
        ).order_by('-created_at').first()
        
        if previous_bid:
            # Must be lower than previous bid
            if amount >= previous_bid.amount:
                return False, f"Bid must be lower than your previous bid ({previous_bid.amount})"
            
            # Check minimum decrement
            if auction.minimum_decrement > 0:
                decrement = previous_bid.amount - amount
                if decrement < auction.minimum_decrement:
                    return False, f"Bid must be at least {auction.minimum_decrement} lower than your previous bid"
        else:
            # First bid - check minimum decrement from starting price
            if auction.minimum_decrement > 0:
                decrement = auction.starting_price - amount
                if decrement < auction.minimum_decrement:
                    return False, f"Bid must be at least {auction.minimum_decrement} lower than starting price"
        
        return True, None
    
    @staticmethod
    def close_auction(auction):
        """
        Close an auction when deadline passes.
        Marks status as 'closed' and sends notifications.
        """
        if auction.status == 'active':
            auction.status = 'closed'
            auction.save(update_fields=['status'])
            # TODO: Send notifications to buyer and suppliers
            return True
        return False
    
    @staticmethod
    def award_auction(auction, winning_bid):
        """
        Award an auction to a winning bid.
        Sets the winner and updates status to 'awarded'.
        """
        if auction.status != 'closed':
            return False, "Auction must be closed before awarding"
        
        if winning_bid.auction != auction:
            return False, "Bid does not belong to this auction"
        
        auction.winner = winning_bid
        auction.status = 'awarded'
        auction.save(update_fields=['winner', 'status'])
        
        # Mark bid as winning
        winning_bid.is_winning = True
        winning_bid.save(update_fields=['is_winning'])
        
        return True, None

