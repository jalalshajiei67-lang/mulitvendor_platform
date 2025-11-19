from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from django.db.models import Avg, Count
from django.utils import timezone

from users.models import VendorProfile
from products.models import Product
from orders.models import Order
from .models import SupplierEngagement, PointsHistory


@dataclass
class Metric:
    key: str
    label: str
    tip: str
    weight: float
    passed: bool


def _get_vendor_profile(user) -> VendorProfile | None:
    if not user or not user.is_authenticated:
        return None
    return getattr(user, 'vendor_profile', None)


class GamificationService:
    SCORE_COLOR_STOPS: Dict[str, Tuple[int, int]] = {
        'danger': (0, 40),
        'warning': (40, 70),
        'success': (70, 100),
    }

    def __init__(self, vendor_profile: VendorProfile | None):
        self.vendor_profile = vendor_profile

    @classmethod
    def for_user(cls, user):
        return cls(_get_vendor_profile(user))

    # ------------------------------------------------------------------
    # Engagement helpers
    # ------------------------------------------------------------------
    def get_or_create_engagement(self) -> SupplierEngagement | None:
        if not self.vendor_profile:
            return None
        engagement, _ = SupplierEngagement.objects.get_or_create(
            vendor_profile=self.vendor_profile,
            defaults={
                'total_points': 0,
                'today_points': 0,
                'current_streak_days': 0,
                'longest_streak_days': 0,
            },
        )
        return engagement

    def add_points(self, reason: str, points: int, metadata: dict | None = None):
        engagement = self.get_or_create_engagement()
        if not engagement or points == 0:
            return
        engagement.total_points += max(points, 0)
        engagement.today_points += max(points, 0)
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
        metrics: List[Metric] = [
            Metric('name', 'نام فروشگاه', 'نام فروشگاه را کامل وارد کنید.', bool(vendor.store_name), 0.2),
            Metric(
                'description',
                'توضیحات',
                'داستان کوتاهی درباره تجربه کاری اضافه کنید.',
                bool(vendor.description and len(vendor.description) >= 100),
                0.25,
            ),
            Metric(
                'contact',
                'اطلاعات تماس',
                'ایمیل و شماره تماس فعال را درج کنید.',
                bool(vendor.contact_email and vendor.contact_phone),
                0.25,
            ),
            Metric('website', 'وب‌سایت', 'اگر وب‌سایت دارید لینک را قرار دهید.', bool(vendor.website), 0.1),
            Metric(
                'social',
                'شبکه‌های اجتماعی',
                'حداقل یک شبکه اجتماعی اضافه کنید.',
                bool(vendor.social_media and len(vendor.social_media) > 0),
                0.2,
            ),
        ]
        return self._build_score_response('profile', metrics)

    def compute_product_score(self) -> Dict:
        if not self.vendor_profile:
            return self._empty_response('product', ['برای مشاهده امتیاز باید به عنوان فروشنده وارد شوید.'])

        latest_product: Product | None = (
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

    def _maybe_award_response_points(self, order: Order, duration_minutes: float | None) -> bool:
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


__all__ = ['GamificationService', '_get_vendor_profile']
