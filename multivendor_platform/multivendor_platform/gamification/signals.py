from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import SupplierComment, ProductReview
from gamification.services import flag_review_velocity_if_needed, _get_vendor_profile


@receiver(post_save, sender=SupplierComment)
def flag_supplier_comment(sender, instance, created, **kwargs):
    if not created:
        return
    vendor_profile = instance.supplier
    reviewer = instance.user
    if vendor_profile and reviewer:
        flag_review_velocity_if_needed(instance, reviewer, vendor_profile)


@receiver(post_save, sender=ProductReview)
def flag_product_review(sender, instance, created, **kwargs):
    if not created:
        return
    vendor_profile = _get_vendor_profile(instance.product.vendor)
    reviewer = instance.buyer
    if vendor_profile and reviewer:
        flag_review_velocity_if_needed(instance, reviewer, vendor_profile)

