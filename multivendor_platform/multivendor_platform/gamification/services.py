from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

from django.db.models import Avg, Count, Q
from django.utils import timezone

from users.models import VendorProfile
from products.models import Product
from orders.models import Order
from .models import Badge, EarnedBadge, Invitation, PointsHistory, SupplierEngagement


@dataclass
class Metric:
    key: str
    label: str
    tip: str
    weight: float
    passed: bool


def _get_vendor_profile(user) -> Optional[VendorProfile]:
    if not user or not user.is_authenticated:
        return None
    return getattr(user, 'vendor_profile', None)


class GamificationService:
    SCORE_COLOR_STOPS: Dict[str, Tuple[int, int]] = {
        'danger': (0, 40),
        'warning': (40, 70),
        'success': (70, 100),
    }

    def __init__(self, vendor_profile: Optional[VendorProfile]):
        self.vendor_profile = vendor_profile

    @classmethod
    def for_user(cls, user):
        return cls(_get_vendor_profile(user))

    # ------------------------------------------------------------------
    # Engagement helpers
    # ------------------------------------------------------------------
    def get_or_create_engagement(self) -> Optional[SupplierEngagement]:
        if not self.vendor_profile:
            return None
        engagement, created = SupplierEngagement.objects.get_or_create(
            vendor_profile=self.vendor_profile,
            defaults={
                'total_points': 1,  # Minimum base score so it's never zero
                'today_points': 0,
                'current_streak_days': 0,
                'longest_streak_days': 0,
            },
        )
        # Ensure existing engagements also have at least 1 point
        if not created and engagement.total_points == 0:
            engagement.total_points = 1
            engagement.save(update_fields=['total_points'])
        return engagement

    def add_points(self, reason: str, points: int, metadata: Optional[dict] = None):
        engagement = self.get_or_create_engagement()
        if not engagement or points == 0:
            return
        engagement.total_points += max(points, 0)
        engagement.today_points += max(points, 0)
        # Ensure total_points is never zero (minimum base score)
        if engagement.total_points == 0:
            engagement.total_points = 1
        engagement.save(update_fields=['total_points', 'today_points', 'updated_at'])
        PointsHistory.objects.create(
            vendor_profile=self.vendor_profile,
            points=points,
            reason=reason,
            metadata=metadata or {},
        )

    # ------------------------------------------------------------------
    # Score calculations
    # ------------------------------------------------------------------
    def _empty_response(self, title: str, tips: List[str]) -> Dict:
        return {
            'title': title,
            'score': 0,
            'metrics': [],
            'tips': tips,
        }

    def compute_profile_score(self) -> Dict:
        if not self.vendor_profile:
            return self._empty_response('profile', ['برای شروع ابتدا پروفایل خود را بسازید.'])

        vendor = self.vendor_profile
        user = vendor.user
        metrics: List[Metric] = [
            Metric(
                'name',
                'نام و نام خانوادگی',
                'نام و نام خانوادگی خود را کامل وارد کنید.',
                bool(user.first_name and user.last_name),
                0.5,
            ),
            Metric(
                'contact',
                'اطلاعات تماس',
                'ایمیل و شماره تماس فعال را درج کنید.',
                bool(vendor.contact_email and vendor.contact_phone),
                0.5,
            ),
        ]
        return self._build_score_response('profile', metrics)

    def compute_product_score(self) -> Dict:
        if not self.vendor_profile:
            return self._empty_response('product', ['برای مشاهده امتیاز باید به عنوان فروشنده وارد شوید.'])

        latest_product: Optional[Product] = (
            Product.objects.filter(vendor=self.vendor_profile.user)
            .order_by('-updated_at')
            .first()
        )
        if not latest_product:
            return self._empty_response(
                'product',
                ['هنوز محصولی ثبت نشده است. روی دکمه افزودن محصول کلیک کنید.'],
            )

        description_plain = (latest_product.description or '').replace('<', ' ').replace('>', ' ')
        metrics: List[Metric] = [
            Metric(
                'name',
                'نام محصول',
                'نام دستگاه را ۱۰ تا ۶۰ کاراکتری بنویسید.',
                10 <= len(latest_product.name or '') <= 60,
                0.15,
            ),
            Metric(
                'description',
                'توضیحات',
                'توضیحات غنی با مشخصات فنی حداقل ۱۵۰ کلمه باشد.',
                len(description_plain.split()) >= 150,
                0.25,
            ),
            Metric(
                'images',
                'تصاویر',
                'حداقل ۳ تصویر واضح از زوایای مختلف آپلود کنید.',
                latest_product.images.count() >= 3 if hasattr(latest_product, 'images') else bool(latest_product.image),
                0.2,
            ),
            Metric(
                'pricing',
                'قیمت و موجودی',
                'قیمت و موجودی را تکمیل کنید.',
                bool(latest_product.price and latest_product.stock is not None),
                0.15,
            ),
            Metric(
                'category',
                'دسته‌بندی',
                'زیر دسته مناسب را انتخاب کنید.',
                latest_product.subcategories.exists(),
                0.15,
            ),
            Metric(
                'seo',
                'سئو',
                'نامک و توضیح کوتاه را پر کنید.',
                bool(latest_product.slug and latest_product.meta_description),
                0.1,
            ),
        ]
        return self._build_score_response('product', metrics)

    def compute_mini_site_score(self) -> Dict:
        if not self.vendor_profile:
            return self._empty_response('mini_site', ['پروفایل فروشنده یافت نشد.'])

        vendor = self.vendor_profile
        metrics: List[Metric] = [
            Metric('banner', 'بنر', 'یک تصویر بنر انتخاب کنید.', bool(vendor.banner_image), 0.18),
            Metric('colors', 'رنگ برند', 'رنگ اصلی و دوم را تنظیم کنید.', bool(vendor.brand_color_primary), 0.1),
            Metric(
                'slogan',
                'شعار',
                'یک شعار ۱۰ تا ۲۰۰ کاراکتری اضافه کنید.',
                bool(vendor.slogan and 10 <= len(vendor.slogan) <= 200),
                0.08,
            ),
            Metric(
                'about',
                'معرفی',
                'حداقل ۲۰۰ کاراکتر درباره خدمات خود بنویسید.',
                bool(vendor.about and len(vendor.about) >= 200),
                0.12,
            ),
            Metric(
                'contact',
                'راه‌های تماس',
                'تلفن یا واتساپ فعال وارد کنید.',
                bool(vendor.contact_phone or vendor.contact_email),
                0.1,
            ),
            Metric('media', 'ویدیو یا وب‌سایت', 'لینک ویدیو یا وب‌سایت اضافه کنید.', bool(vendor.video_url or vendor.website), 0.07),
            Metric('company', 'سال تاسیس و تعداد کارکنان', 'سال شروع و تعداد کارکنان را وارد کنید.', bool(vendor.year_established and vendor.employee_count), 0.05),
            Metric('certs', 'گواهینامه‌ها', 'لیست گواهینامه‌ها را وارد کنید.', bool(vendor.certifications), 0.12),
            Metric('awards', 'جوایز', 'جوایز و تقدیرنامه‌ها را ذکر کنید.', bool(vendor.awards), 0.08),
            Metric('social', 'شبکه‌های اجتماعی', 'حداقل دو شبکه اجتماعی اضافه کنید.', bool(vendor.social_media and len(vendor.social_media) >= 2), 0.1),
            Metric('seo', 'متای سئو', 'متای عنوان و توضیحات را تکمیل کنید.', bool(vendor.meta_title and vendor.meta_description), 0.08),
        ]
        return self._build_score_response('mini_site', metrics)

    def compute_portfolio_score(self) -> Dict:
        if not self.vendor_profile:
            return self._empty_response('portfolio', ['ابتدا پروفایل خود را کامل کنید.'])
        total_items = self.vendor_profile.portfolio_items.count()
        metrics = [
            Metric(
                'cases',
                'پروژه‌ها',
                'حداقل سه نمونه کار اضافه کنید.',
                total_items >= 3,
                1.0,
            )
        ]
        tips = [] if total_items >= 3 else ['دو نمونه کار دیگر اضافه کنید تا این بخش سبز شود.']
        response = self._build_score_response('portfolio', metrics)
        response['tips'] = tips
        return response

    def compute_team_score(self) -> Dict:
        if not self.vendor_profile:
            return self._empty_response('team', ['ابتدا پروفایل خود را کامل کنید.'])
        total_members = self.vendor_profile.team_members.count()
        metrics = [
            Metric(
                'members',
                'اعضای تیم',
                'حداقل دو عضو تیم اضافه کنید.',
                total_members >= 2,
                1.0,
            )
        ]
        tips = [] if total_members >= 2 else ['تصویر و نقش اعضای کلیدی تیم را اضافه کنید.']
        response = self._build_score_response('team', metrics)
        response['tips'] = tips
        return response

    def _build_score_response(self, title: str, metrics: List[Metric]) -> Dict:
        if not metrics:
            return {'title': title, 'score': 0, 'metrics': [], 'tips': []}
        total_weight = sum(metric.weight for metric in metrics)
        earned_weight = sum(metric.weight for metric in metrics if metric.passed)
        score = int(round((earned_weight / total_weight) * 100)) if total_weight else 0
        serialized_metrics = [
            {
                'key': metric.key,
                'label': metric.label,
                'tip': metric.tip,
                'weight': metric.weight,
                'passed': metric.passed,
            }
            for metric in metrics
        ]
        return {
            'title': title,
            'score': score,
            'metrics': serialized_metrics,
            'tips': [m.tip for m in metrics if not m.passed],
        }

    # ------------------------------------------------------------------
    # Section completion scoring
    # ------------------------------------------------------------------
    def award_section_completion_points(self, section: str) -> int:
        """
        Award points based on section completion score.
        Points are awarded proportionally to the score (0-100).
        Only awards points for score improvements to avoid double-counting.
        Accumulates scores from all sections to total_points.
        
        Args:
            section: One of 'profile', 'product', 'miniWebsite', 'portfolio', 'team'
        
        Returns:
            Points awarded (0 if no improvement or already awarded)
        """
        if not self.vendor_profile:
            return 0
        
        # Map section names to score computation methods
        score_methods = {
            'profile': self.compute_profile_score,
            'product': self.compute_product_score,
            'miniWebsite': self.compute_mini_site_score,
            'portfolio': self.compute_portfolio_score,
            'team': self.compute_team_score,
        }
        
        if section not in score_methods:
            return 0
        
        # Calculate current score
        score_result = score_methods[section]()
        current_score = score_result.get('score', 0)
        
        # Base points per section (maximum points when score is 100)
        section_base_points = {
            'profile': 50,
            'product': 100,
            'miniWebsite': 75,
            'portfolio': 50,
            'team': 50,
        }
        
        base_points = section_base_points.get(section, 50)
        
        # Check if we've already awarded points for this section
        engagement = self.get_or_create_engagement()
        if not engagement:
            return 0
        
        # Check recent history for this section to see previous score
        recent_history = PointsHistory.objects.filter(
            vendor_profile=self.vendor_profile,
            reason='section_completion',
            metadata__section=section
        ).order_by('-created_at').first()
        
        if recent_history:
            # Get the last recorded score for this section
            previous_score = recent_history.metadata.get('score', 0)
            
            # Only award points if score improved
            if current_score > previous_score:
                # Calculate points for the improvement
                score_improvement = current_score - previous_score
                improvement_points = int((score_improvement / 100) * base_points)
                
                if improvement_points > 0:
                    self.add_points(
                        'section_completion',
                        improvement_points,
                        metadata={
                            'section': section, 
                            'score': current_score, 
                            'previous_score': previous_score,
                            'improvement': score_improvement
                        }
                    )
                    return improvement_points
            # Score didn't improve, don't award points
            return 0
        else:
            # First time calculating points for this section
            # Award points based on current score (proportional)
            points_to_award = int((current_score / 100) * base_points)
            
            # Award at least 1 point if score > 0 to ensure accumulation
            if current_score > 0:
                if points_to_award < 1:
                    points_to_award = 1
                    
                self.add_points(
                    'section_completion',
                    points_to_award,
                    metadata={'section': section, 'score': current_score, 'is_first_award': True}
                )
                return points_to_award
        
        return 0

    def award_all_section_scores(self) -> Dict[str, int]:
        """
        Calculate and award points for all sections based on their current scores.
        This ensures all section completion scores are accumulated into total_points.
        
        Returns:
            Dictionary mapping section names to points awarded
        """
        sections = ['profile', 'product', 'miniWebsite', 'portfolio', 'team']
        awarded = {}
        
        for section in sections:
            points = self.award_section_completion_points(section)
            awarded[section] = points
        
        return awarded

    # ------------------------------------------------------------------
    # Response-time helpers
    # ------------------------------------------------------------------
    def register_order_view(self, order: Order):
        if not order.first_viewed_at:
            order.first_viewed_at = timezone.now()
            order.save(update_fields=['first_viewed_at'])

    def register_order_response(self, order: Order):
        now = timezone.now()
        if not order.first_responded_at:
            order.first_responded_at = now
        if order.first_viewed_at:
            duration = (now - order.first_viewed_at).total_seconds() / 60
        else:
            duration = None
        order.response_points_awarded = self._maybe_award_response_points(order, duration)
        order.save(update_fields=['first_responded_at', 'response_points_awarded', 'response_speed_bucket'])

    def _maybe_award_response_points(self, order: Order, duration_minutes: Optional[float]) -> bool:
        if duration_minutes is None:
            return False
        points = 0
        bucket = None
        if duration_minutes <= 60:
            points = 50
            bucket = 'sub_1h'
        elif duration_minutes <= 240:
            points = 30
            bucket = 'sub_4h'
        elif duration_minutes <= 1440:
            points = 15
            bucket = 'sub_24h'
        if not points:
            return False
        order.response_speed_bucket = bucket
        self.add_points('fast_response', points, metadata={'order_id': order.id, 'bucket': bucket})
        return True

    # ------------------------------------------------------------------
    # Tier calculation
    # ------------------------------------------------------------------
    def calculate_tier(self, points: int | None = None, reputation_score: float | None = None) -> str:
        """
        Calculate tier based on total points and reputation score.
        Diamond and Gold tiers require both points AND reputation thresholds.
        
        Args:
            points: Total points. If None, uses engagement total_points.
            reputation_score: Reputation score. If None, uses engagement reputation_score.
        
        Returns:
            Tier name: 'diamond', 'gold', 'silver', 'bronze', or 'inactive'
        """
        if points is None or reputation_score is None:
            engagement = self.get_or_create_engagement()
            if not engagement:
                return 'inactive'
            if points is None:
                points = engagement.total_points
            if reputation_score is None:
                reputation_score = engagement.reputation_score
        
        # Diamond tier requires: 1000+ points AND 80+ reputation
        if points >= 1000 and reputation_score >= 80:
            return 'diamond'
        # Gold tier requires: 500+ points AND 60+ reputation
        elif points >= 500 and reputation_score >= 60:
            return 'gold'
        # Lower tiers: points-based only
        elif points >= 200:
            return 'silver'
        elif points >= 50:
            return 'bronze'
        else:
            return 'inactive'
    
    def get_tier_thresholds(self) -> Dict[str, int]:
        """
        Get point thresholds for each tier.
        
        Returns:
            Dictionary mapping tier names to minimum points required
        """
        return {
            'diamond': 1000,
            'gold': 500,
            'silver': 200,
            'bronze': 50,
            'inactive': 0,
        }
    
    def get_next_tier_info(self, current_tier: str | None = None) -> Dict[str, str | int]:
        """
        Get information about the next tier.
        
        Args:
            current_tier: Current tier name. If None, calculates from engagement.
        
        Returns:
            Dictionary with 'name' and 'points_needed' keys
        """
        if current_tier is None:
            current_tier = self.calculate_tier()
        
        thresholds = self.get_tier_thresholds()
        tier_order = ['inactive', 'bronze', 'silver', 'gold', 'diamond']
        
        try:
            current_index = tier_order.index(current_tier)
            if current_index >= len(tier_order) - 1:
                # Already at highest tier
                return {
                    'name': None,
                    'points_needed': 0,
                    'current_tier': current_tier,
                }
            
            next_tier = tier_order[current_index + 1]
            engagement = self.get_or_create_engagement()
            current_points = engagement.total_points if engagement else 0
            next_threshold = thresholds[next_tier]
            points_needed = max(0, next_threshold - current_points)
            
            return {
                'name': next_tier,
                'points_needed': points_needed,
                'current_tier': current_tier,
                'next_tier_threshold': next_threshold,
            }
        except ValueError:
            # Invalid tier name
            return {
                'name': None,
                'points_needed': 0,
                'current_tier': current_tier,
            }
    
    def get_tier_color(self, tier: str | None = None) -> str:
        """
        Get color code for a tier.
        
        Args:
            tier: Tier name. If None, calculates from engagement.
        
        Returns:
            Color name for Vuetify/CSS
        """
        if tier is None:
            tier = self.calculate_tier()
        
        color_map = {
            'diamond': 'purple',
            'gold': 'amber',
            'silver': 'grey',
            'bronze': 'brown',
            'inactive': 'red',
        }
        return color_map.get(tier, 'grey')
    
    def get_tier_display_name(self, tier: str | None = None) -> str:
        """
        Get Persian display name for a tier.
        
        Args:
            tier: Tier name. If None, calculates from engagement.
        
        Returns:
            Persian display name
        """
        if tier is None:
            tier = self.calculate_tier()
        
        name_map = {
            'diamond': 'الماس',
            'gold': 'طلا',
            'silver': 'نقره',
            'bronze': 'برنز',
            'inactive': 'غیرفعال',
        }
        return name_map.get(tier, 'نامشخص')

    # ------------------------------------------------------------------
    # Reputation score calculation
    # ------------------------------------------------------------------
    def compute_reputation_score(self) -> float:
        """
        Compute reputation score based on endorsements, reviews, and response speed.
        Formula: (endorsements * 0.4) + (positive_reviews * 0.4) + (response_speed_bonus * 0.2)
        
        Returns:
            Reputation score (0-100)
        """
        if not self.vendor_profile:
            return 0.0
        
        engagement = self.get_or_create_engagement()
        if not engagement:
            return 0.0
        
        # 1. Endorsements component (0-100 scale)
        # Normalize endorsements: assume 10+ endorsements = 100 points
        # Scale: endorsements / 10 * 100, capped at 100
        endorsements_count = engagement.endorsements_received
        endorsements_score = min(100.0, (endorsements_count / 10.0) * 100.0)
        
        # 2. Positive reviews component (0-100 scale)
        # Count positive reviews (rating >= 4) from both SupplierComment and ProductReview
        from users.models import SupplierComment, ProductReview
        
        # Count supplier comments with rating >= 4
        supplier_positive_reviews = SupplierComment.objects.filter(
            supplier=self.vendor_profile,
            rating__gte=4,
            is_approved=True,
            is_flagged=False,
        ).count()
        
        # Count product reviews with rating >= 4 for products by this vendor
        product_positive_reviews = ProductReview.objects.filter(
            product__vendor=self.vendor_profile.user,
            rating__gte=4,
            is_approved=True,
            is_flagged=False,
        ).count()
        
        total_positive_reviews = supplier_positive_reviews + product_positive_reviews
        
        # Update positive_reviews_count in engagement
        engagement.positive_reviews_count = total_positive_reviews
        
        # Normalize positive reviews: assume 20+ positive reviews = 100 points
        # Scale: reviews / 20 * 100, capped at 100
        positive_reviews_score = min(100.0, (total_positive_reviews / 20.0) * 100.0)
        
        # 3. Response speed bonus (0-100 scale)
        # avg_response_minutes: lower is better
        # Convert to score: if avg_response_minutes <= 60, score = 100
        # If avg_response_minutes >= 1440 (24 hours), score = 0
        # Linear interpolation between 60 and 1440 minutes
        avg_response = engagement.avg_response_minutes
        if avg_response <= 0:
            # No response data yet
            response_speed_bonus = 50.0  # Default middle score
        elif avg_response <= 60:
            response_speed_bonus = 100.0  # Excellent (within 1 hour)
        elif avg_response >= 1440:
            response_speed_bonus = 0.0  # Poor (24+ hours)
        else:
            # Linear interpolation: 60 min = 100, 1440 min = 0
            # Formula: 100 - ((avg_response - 60) / (1440 - 60)) * 100
            response_speed_bonus = 100.0 - ((avg_response - 60.0) / (1440.0 - 60.0)) * 100.0
            response_speed_bonus = max(0.0, min(100.0, response_speed_bonus))
        
        # Calculate final reputation score using weighted formula
        reputation_score = (
            endorsements_score * 0.4 +
            positive_reviews_score * 0.4 +
            response_speed_bonus * 0.2
        )
        
        # Ensure score is between 0 and 100
        reputation_score = max(0.0, min(100.0, reputation_score))
        
        # Save to engagement
        engagement.reputation_score = reputation_score
        engagement.save(update_fields=['reputation_score', 'positive_reviews_count', 'updated_at'])
        # Award any badges that depend on updated reputation metrics
        self.check_and_award_badges()
        
        return reputation_score

    # ------------------------------------------------------------------
    # Badge helpers
    # ------------------------------------------------------------------
    def _get_badge_metrics(self) -> Dict[str, float | int]:
        """
        Collect metrics used for badge evaluation.
        """
        engagement = self.get_or_create_engagement()
        if not self.vendor_profile or not engagement:
            return {}

        invitations_accepted = Invitation.objects.filter(
            inviter=self.vendor_profile,
            status='accepted',
        ).count()

        return {
            'invitations_accepted': invitations_accepted,
            'positive_reviews': engagement.positive_reviews_count,
            'avg_response_minutes': engagement.avg_response_minutes or 0,
        }

    def evaluate_badge_criteria(self, badge: Badge, metrics: Dict[str, float | int]) -> bool:
        """
        Check whether provided metrics satisfy a badge's criteria.
        Criteria format: {"metric_name": {"min": X, "max": Y}}
        """
        criteria = badge.criteria or {}
        if not criteria:
            return False

        for metric_name, bounds in criteria.items():
            current_value = metrics.get(metric_name)
            if current_value is None:
                return False

            min_value = bounds.get('min')
            max_value = bounds.get('max')

            if min_value is not None and current_value < min_value:
                return False
            if max_value is not None and current_value > max_value:
                return False

        return True

    def get_badge_progress(self, badge: Badge) -> Dict[str, float | int]:
        """
        Calculate progress toward earning a badge.
        Returns a dict with current, target, and percentage.
        """
        metrics = self._get_badge_metrics()
        criteria = badge.criteria or {}
        if not criteria:
            return {'current': 0, 'target': 0, 'percentage': 0}

        # Use the first criterion as the primary target for progress display
        metric_name, bounds = next(iter(criteria.items()))
        current_value = float(metrics.get(metric_name, 0))
        min_value = bounds.get('min')
        max_value = bounds.get('max')

        target = 0.0
        percentage = 0.0

        if min_value is not None:
            target = float(min_value)
            percentage = min(100.0, (current_value / target) * 100.0 if target > 0 else 0.0)
        elif max_value is not None:
            target = float(max_value)
            # For max-bound goals, reaching or going below target is 100%
            if current_value <= target:
                percentage = 100.0
            else:
                percentage = max(0.0, min(100.0, (target / current_value) * 100.0 if current_value > 0 else 0.0))

        return {
            'current': current_value,
            'target': target,
            'percentage': round(percentage, 2),
        }

    def check_and_award_badges(self) -> List[Badge]:
        """
        Evaluate all active badges and award any newly earned ones.
        Returns a list of badges that were awarded during this call.
        """
        if not self.vendor_profile:
            return []

        engagement = self.get_or_create_engagement()
        if not engagement:
            return []

        metrics = self._get_badge_metrics()
        earned_badges = EarnedBadge.objects.filter(vendor_profile=self.vendor_profile).select_related('badge')
        earned_slugs = {eb.badge.slug for eb in earned_badges}

        newly_awarded: List[Badge] = []
        for badge in Badge.objects.filter(is_active=True):
            if badge.slug in earned_slugs:
                continue

            if not self.evaluate_badge_criteria(badge, metrics):
                continue

            EarnedBadge.objects.create(
                vendor_profile=self.vendor_profile,
                badge=badge,
                congratulation_message=f'تبریک! نشان {badge.title} را دریافت کردید.',
            )
            self.add_points('badge', 200, metadata={'badge_slug': badge.slug})
            newly_awarded.append(badge)

        return newly_awarded

    # ------------------------------------------------------------------
    # Task sequencing and progress tracking
    # ------------------------------------------------------------------
    def get_overall_progress(self) -> Dict[str, any]:
        """
        Calculate overall completion percentage and milestone progress.
        Returns progress data for the LinkedIn-style progress bar.
        """
        if not self.vendor_profile:
            return {
                'overall_percentage': 0,
                'milestones': [],
                'required_steps_completed': 0,
                'total_required_steps': 5
            }
        
        # Calculate scores for each section
        profile_score_data = self.compute_profile_score()
        mini_website_score_data = self.compute_mini_site_score()
        portfolio_score_data = self.compute_portfolio_score()
        team_score_data = self.compute_team_score()
        
        # Count products
        product_count = Product.objects.filter(vendor=self.vendor_profile.user).count()
        products_completed = product_count >= 3
        products_score = min(100, int((product_count / 3) * 100))
        
        # Define milestones with completion criteria
        milestones = [
            {
                'name': 'profile',
                'title': 'تکمیل پروفایل',
                'completed': profile_score_data.get('score', 0) >= 70,
                'score': profile_score_data.get('score', 0),
                'order': 1
            },
            {
                'name': 'miniWebsite',
                'title': 'تنظیمات فروشگاه',
                'completed': mini_website_score_data.get('score', 0) >= 70,
                'score': mini_website_score_data.get('score', 0),
                'order': 2
            },
            {
                'name': 'products',
                'title': 'افزودن محصولات',
                'completed': products_completed,
                'score': products_score,
                'order': 3,
                'current': product_count,
                'target': 3
            },
            {
                'name': 'team',
                'title': 'معرفی تیم',
                'completed': self.vendor_profile.team_members.count() >= 1,
                'score': 100 if self.vendor_profile.team_members.count() >= 1 else 0,
                'order': 4,
                'current': self.vendor_profile.team_members.count(),
                'target': 1
            },
            {
                'name': 'portfolio',
                'title': 'نمونه کارها',
                'completed': self.vendor_profile.portfolio_items.count() >= 1,
                'score': 100 if self.vendor_profile.portfolio_items.count() >= 1 else 0,
                'order': 5,
                'current': self.vendor_profile.portfolio_items.count(),
                'target': 1
            }
        ]
        
        # Count completed required steps
        required_steps_completed = sum(1 for m in milestones if m['completed'])
        
        # Calculate overall percentage (average of all milestone scores)
        total_score = sum(m['score'] for m in milestones)
        overall_percentage = int(total_score / len(milestones)) if milestones else 0
        
        return {
            'overall_percentage': overall_percentage,
            'milestones': milestones,
            'required_steps_completed': required_steps_completed,
            'total_required_steps': 5
        }
    
    def get_current_task(self) -> Dict[str, any]:
        """
        Determine the next task user should complete.
        Uses smart prioritization: sequential for required steps, then rotation for engagement.
        """
        if not self.vendor_profile:
            return None
        
        # Get progress data
        progress = self.get_overall_progress()
        milestones = progress['milestones']
        
        # Check required steps in sequence
        for milestone in sorted(milestones, key=lambda x: x['order']):
            if not milestone['completed']:
                return self._create_task_for_milestone(milestone)
        
        # All required steps completed - show engagement actions
        return self._get_engagement_task()
    
    def _create_task_for_milestone(self, milestone: Dict) -> Dict[str, any]:
        """Create a task object for a given milestone."""
        task_configs = {
            'profile': {
                'type': 'profile',
                'title': 'تکمیل پروفایل شما',
                'description': 'پروفایل کامل، اعتماد بیشتر مشتریان. نام، ایمیل و شماره تماس خود را وارد کنید.',
                'action_url': 'profile',
                'points': 50,
                'icon': 'mdi-account-circle'
            },
            'miniWebsite': {
                'type': 'mini_website',
                'title': 'تنظیمات فروشگاه آنلاین',
                'description': 'فروشگاه حرفه‌ای، جذب مشتری بیشتر. نام فروشگاه، توضیحات و تصویر بنر اضافه کنید.',
                'action_url': 'miniwebsite',
                'points': 75,
                'icon': 'mdi-store'
            },
            'products': {
                'type': 'products',
                'title': 'افزودن محصولات',
                'description': 'محصولات با توضیحات دقیق، فروش بیشتر. حداقل ۳ محصول با تصویر و قیمت اضافه کنید.',
                'action_url': 'products',
                'points': 100,
                'icon': 'mdi-package-variant',
                'current_progress': milestone.get('current', 0),
                'target_progress': milestone.get('target', 3)
            },
            'team': {
                'type': 'team',
                'title': 'معرفی تیم شما',
                'description': 'نمایش تیم، حرفه‌ای‌تر به نظر می‌رسید. حداقل یک نفر از اعضای تیم را معرفی کنید.',
                'action_url': 'team',
                'points': 50,
                'icon': 'mdi-account-group'
            },
            'portfolio': {
                'type': 'portfolio',
                'title': 'نمونه کارهای شما',
                'description': 'نمونه کارها، اعتبار شما را نشان می‌دهد. حداقل یک پروژه موفق خود را به نمایش بگذارید.',
                'action_url': 'portfolio',
                'points': 50,
                'icon': 'mdi-briefcase'
            }
        }
        
        config = task_configs.get(milestone['name'], {})
        return {
            **config,
            'is_required': True,
            'milestone_name': milestone['name']
        }
    
    def _get_engagement_task(self) -> Dict[str, any]:
        """
        Get an engagement task after all required steps are completed.
        Rotates between: invite peers, share insights, improve products/website.
        """
        from .models import SellerInsight
        
        # Count current engagements
        invitations_count = Invitation.objects.filter(
            inviter=self.vendor_profile,
            status='accepted'
        ).count()
        
        insights_count = SellerInsight.objects.filter(
            vendor_profile=self.vendor_profile
        ).count()
        
        product_score = self.compute_product_score().get('score', 0)
        mini_website_score = self.compute_mini_site_score().get('score', 0)
        
        # Priority: insights < invites < product improvement < website improvement
        if insights_count < 3:
            return {
                'type': 'insights',
                'title': 'اشتراک تجربه با دیگران',
                'description': 'تجربیات خود را با سایر فروشندگان به اشتراک بگذارید و ۱۵ امتیاز دریافت کنید.',
                'action_url': 'insights',
                'points': 15,
                'is_required': False,
                'icon': 'mdi-lightbulb-on',
                'current_progress': insights_count,
                'target_progress': 3
            }
        
        if invitations_count < 5:
            return {
                'type': 'invite',
                'title': 'دعوت همکاران',
                'description': 'همکاران خود را به پلتفرم دعوت کنید و برای هر دعوت موفق ۱۰۰ امتیاز دریافت کنید.',
                'action_url': 'invite',
                'points': 100,
                'is_required': False,
                'icon': 'mdi-account-multiple-plus',
                'current_progress': invitations_count,
                'target_progress': 5
            }
        
        if product_score < 80:
            return {
                'type': 'products',
                'title': 'بهبود محصولات',
                'description': 'محصولات خود را با توضیحات بهتر، تصاویر بیشتر و اطلاعات کامل‌تر بهبود دهید.',
                'action_url': 'products',
                'points': 20,
                'is_required': False,
                'icon': 'mdi-package-variant-closed'
            }
        
        if mini_website_score < 80:
            return {
                'type': 'mini_website',
                'title': 'بهبود فروشگاه',
                'description': 'فروشگاه خود را با افزودن گواهینامه‌ها، جوایز و شبکه‌های اجتماعی کامل‌تر کنید.',
                'action_url': 'miniwebsite',
                'points': 15,
                'is_required': False,
                'icon': 'mdi-store-edit'
            }
        
        # Default: Add more products
        return {
            'type': 'products',
            'title': 'افزودن محصول جدید',
            'description': 'محصولات بیشتر، فرصت فروش بیشتر. یک محصول جدید اضافه کنید.',
            'action_url': 'products',
            'points': 20,
            'is_required': False,
            'icon': 'mdi-plus-circle'
        }


def flag_review_velocity_if_needed(review_obj, reviewer, vendor_profile) -> bool:
    """
    Flag reviews that come from new accounts in a short time window for the same vendor.
    Returns True when the review was flagged.
    """
    from users.models import SupplierComment, ProductReview
    from django.utils import timezone
    from datetime import timedelta
    from gamification.models import ReviewFlagLog
    from django.contrib.contenttypes.models import ContentType

    now = timezone.now()
    # Define what counts as a new account and the velocity window
    new_account_cutoff = now - timedelta(days=7)
    if not reviewer or reviewer.date_joined < new_account_cutoff:
        return False

    window_start = now - timedelta(hours=1)
    if isinstance(review_obj, SupplierComment):
        qs = SupplierComment.objects.filter(
            supplier=vendor_profile,
            created_at__gte=window_start,
            user__date_joined__gte=new_account_cutoff,
        )
    elif isinstance(review_obj, ProductReview):
        qs = ProductReview.objects.filter(
            product__vendor=vendor_profile.user,
            created_at__gte=window_start,
            buyer__date_joined__gte=new_account_cutoff,
        )
    else:
        return False

    if qs.count() > 5:
        review_obj.is_flagged = True
        review_obj.flag_reason = 'review_velocity'
        review_obj.save(update_fields=['is_flagged', 'flag_reason'])

        ReviewFlagLog.objects.create(
            vendor_profile=vendor_profile,
            content_type=ContentType.objects.get_for_model(review_obj),
            object_id=review_obj.id,
            reason='review_velocity',
        )
        return True

    return False


__all__ = ['GamificationService', '_get_vendor_profile']
