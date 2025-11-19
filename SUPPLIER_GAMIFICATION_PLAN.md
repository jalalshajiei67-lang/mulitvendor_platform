# Supplier Dashboard Gamification & Quality System (Non‑Technical Friendly)

## 1. Why we are doing this
Our average supplier is over 40, runs a busy machinery workshop or dealership, and is more comfortable with WhatsApp than
complicated dashboards. The gamification system must therefore:
- speak in plain Persian, avoid tech jargon, and use friendly icons/tooltips;
- guide users step by step like a coach (similar to Yoast) while they fill products, profile, and mini website data, using machinery-ready examples (e.g., “دستگاه تولید فوم پلی‌یورتان”);
- celebrate effort with simple rewards (points, streaks, badges) that are easy to understand at a glance;
- highlight urgent tasks such as replying to orders quickly, because responsiveness builds trust and leads to more orders.

## 2. Four pillars (always visible in UI copy)
1. **راهنمای قدم‌به‌قدم** – Yoast-style scoring widgets with “traffic light” colors and short hints.
2. **امتیاز و نشان‌ها** – Points for every action, badges for milestones, and weekly reminders showing progress.
3. **پاسخ‌گویی سریع** – Order view/response timers that reward the quickest helpers.
4. **داشبورد ساده** – Widgets on the supplier home tab showing today’s tasks, points, and streak in one glance.

## 3. Friendly Yoast-like Score Component (`front_end/nuxt/components/gamification/FormQualityScore.vue`)
- **Inputs**: receives a `metrics` array (label, weight, validator function, tip text, bonus). Validators return plain-language
  status strings (“خیلی کوتاه است – حداقل ۱۰ کلمه”).
- **Display**: big circular gauge (0‑100) with traffic-light colors, checklist with emoji icons ✅⚠️❌, and a progress bar.
- **Tone**: every tip ends with an action (“یک جمله درباره مزیت اصلی اضافه کنید”) and, where possible, references machinery
  scenarios (“قدرت موتور دستگاه بسته‌بندی را بنویسید”). Include a “Need help?” link that opens a short FAQ modal with
  examples/screenshots.
- **Accessibility**: RTL layout, 16px+ fonts, voice-over friendly labels, keyboard focus states.
- **Events**: emits `score-change` and `metric-feedback` so forms can show inline nudges.

## 4. Product Creation Gamification (`front_end/nuxt/components/supplier/ProductForm.vue`)
| Metric | Plain-language check | Weight | Friendly extra guidance |
| --- | --- | --- | --- |
| **نام محصول** | 10‑60 characters, no English-only titles | 15% | Show machinery-ready examples (“دستگاه برش لیزر ۱۵۰۰ وات مدل MX‑500”) |
| **توضیحات** | ≥150 words, use bullet list component | 25% | Offer template button: مقدمه → مشخصات فنی → خدمات پس از فروش |
| **تصاویر** | 3‑20 photos, mark one as main | 20% | Drag‑and‑drop with “photo tips” popover showing angle examples for دستگاه‌ها |
| **قیمت و موجودی** | Price + stock both filled | 10% | “اگر موجودی نامحدود است، تیک را بزنید” |
| **دسته‌بندی** | Select full path | 10% | Show breadcrumb preview |
| **ویژگی‌ها و برچسب‌ها** | At least 3 attributes | 5% | Suggest common tags per category (e.g., “توان ۵۰۰ وات”، “تغذیه اتوماتیک”) |
| **سئو (لینک، توضیح کوتاه)** | Slug unique, meta 140‑160 chars | 10% | Preview card like Google result |
| **وضعیت نمایش** | Active/featured reviewed | 5% | Explain difference using tooltip |

Additional user-friendly touches:
- A floating “Coach” chip summarizing the top two improvements (e.g., “۲ عکس از نمای جانبی دستگاه اضافه کنید تا امتیاز شما سبز شود”).
- Auto-save drafts to prevent data loss if a user navigates away.
- On submit, call backend to store the score history for analytics and badge checks.
- Provide ready-to-use text snippets such as “این دستگاه مناسب کارگاه‌های تولید قطعات خودرو است و ظرفیت تولید ۳۰۰۰ عدد در ساعت دارد”.

## 5. Profile Tab Gamification (`front_end/nuxt/pages/seller/dashboard.vue` – Profile form)
| Metric | Why it matters to suppliers | Weight | Notes |
| --- | --- | --- | --- |
| **نام و نام خانوادگی** | Appears on invoices and trust badges | 15% | Validate Persian letters, show check mark |
| **اطلاعات تماس** | Customers know how to reach you | 30% | Phone mask + WhatsApp toggle + email verification state |
| **آدرس و موقعیت** | Needed for shipping quotes | 15% | Map pin UI with “مشاهده روی نقشه” |
| **لوگو / عکس پروفایل** | Builds recognition | 15% | Simple uploader with cropping presets |
| **شرح فروشگاه** | Shows experience and specialties | 15% | Provide text starter (“ما از سال ۱۳۸۵ سازنده دستگاه‌های بسته‌بندی هستیم…”) |
| **شبکه‌های اجتماعی** | Shows activity and proof | 10% | At least one link (IG/LinkedIn/Telegram) |

- Score chip sits above the form with color-coded background.
- A helper banner explains: “هر بخش کامل = امتیاز بیشتر، جستجو بالاتر و اعتماد بیشتر مشتریان خطوط تولید”.

## 6. Mini Website Gamification (Settings + Portfolio + Team)
### 6.1 Settings (`front_end/nuxt/components/supplier/MiniWebsiteSettings.vue`)
| Metric | Friendly explanation | Weight |
| --- | --- | --- |
| **بنر و رنگ برند** | “یک عکس عریض از خط تولید یا دستگاه شاخص و رنگ هماهنگ انتخاب کنید” | 18% |
| **شعار کوتاه** | 10‑200 chars, highlight value prop (“ارائه‌دهنده خط کامل بسته‌بندی خرما”) | 8% |
| **معرفی فروشگاه** | 200+ chars with story + USP bullets | 12% |
| **راه‌های تماس (تلفن/واتساپ/تلگرام)** | Customers choose their preferred channel | 10% |
| **وب‌سایت / ویدیو معرفی** | Optional but earns trust | 7% |
| **سال تأسیس + تعداد کارکنان** | Shows experience | 5% |
| **گواهینامه‌ها** | Upload photos or PDF links (ISO 9001, CE، استاندارد ملی) | 12% |
| **جوایز و رضایت‌نامه‌ها** | “حداقل یک مورد وارد کنید” (مثلاً تقدیرنامه از کارخانه فولاد) | 8% |
| **شبکه‌های اجتماعی** | ≥2 links validated | 10% |
| **متای سئو** | Title ≤60 chars, desc ≤160 | 10% |

### 6.2 Portfolio & Team Tabs
- **Portfolio**: Score becomes green after at least 3 items, each with image + result summary + optional testimonial audio (allow
  WhatsApp voice import). Pre-fill example cards such as “نصب خط تولید دستکش صنعتی در کرمان – کاهش ضایعات ۱۵٪”.
- **Team**: Encourage uploading 2+ members with roles. Provide quick photo cropper and description placeholder (“مسئول فروش – ۱۰ سال تجربه”).
- Completion of both tabs grants the “وب‌سایت حرفه‌ای” badge.

## 7. Engagement Tracking (Backend – `multivendor_platform/gamification/models.py`)
Create human-readable models:
- `SupplierEngagement`: supplier FK, total_points, today_points, current_streak_days, longest_streak_days, last_login,
  avg_response_minutes, last_tip_shown (so we avoid repeating tips).
- `Badge`: slug, title, tier, icon, Persian description, `criteria` JSON.
- `EarnedBadge`: supplier FK, badge FK, achieved_at, congratulation_message.
- `PointsHistory`: supplier FK, points, reason (enum: login, product_save, fast_response, etc.), metadata (e.g., order_id, machine_category), created_at.
- `LeaderboardSnapshot`: period (week/month), data JSON, generated_at.
- Signals listen to login/product/profile/mini-website saves and order events to update points & streaks.

## 8. API Layer (plain responses)
- `GET /api/gamification/score/` → `{ product: {score, tips}, profile: {...}, miniWebsite: {...}, portfolio: {...}, team: {...} }` (tips reference machinery-friendly advice such as “ولتاژ کاری و توان موتور را ذکر کنید”).
- `GET /api/gamification/engagement/` → points, streak info, last tips, time-on-dashboard.
- `GET /api/gamification/badges/` → unlocked + next targets.
- `GET /api/gamification/leaderboard/` → overall, weekly, monthly, response-time.
- `GET /api/gamification/points/` → paginated ledger with friendly reason text.
- `POST /api/gamification/track-action/` → record UI actions (e.g., “watched tutorial on دستگاه شرینک پک maintenance”).
- `POST /api/orders/{id}/track-view/` & `POST /api/orders/{id}/track-response/` → capture timestamps for response-time rewards.

## 9. Frontend Store & Composable
- Pinia store (`front_end/nuxt/stores/gamification.ts`): holds scores, streaks, points, badge list, and helper getters like
  `nextMilestone`.
- Composable (`front_end/nuxt/composables/useGamification.ts`): fetches backend data, runs the weighted scoring helpers, and exposes
  `showFriendlyTip(metricKey)` for forms with context-aware examples (e.g., recommend stating “قطعات یدکی ۲ سال موجود است”).
- Add caching + hydration so data persists when navigating between tabs.

## 10. Dashboard Widgets (`front_end/nuxt/components/gamification/*.vue`)
1. **FormQualityScore.vue** – used inside each form.
2. **EngagementWidget.vue** – card with today’s streak, “points to next badge,” and a large single CTA (“امروز دستگاه جدید خود را ثبت کنید”).
3. **BadgeDisplay.vue** – grid with tier colors (Bronze, Silver, Gold) and expandable descriptions.
4. **LeaderboardWidget.vue** – tabs for overall/weekly/monthly/response, highlight current supplier row, and show badge icons (e.g., “بهترین عرضه‌کننده دستگاه‌های CNC این هفته”).
5. **RespondNowChip.vue** – attaches to order cards with countdown timers and motivational text (“اگر تا ۳۰ دقیقه آینده پاسخ استعلام دستگاه بسته‌بندی را بدهید ۵۰ امتیاز می‌گیرید”).

## 11. Order Response Gamification (`multivendor_platform/orders/models.py` + API)
- Add `first_viewed_at`, `first_responded_at`, `response_points_awarded` (bool), and `response_speed_bucket`.
- Server computes response duration and grants points once per order (showing messages like “پاسخ سریع به استعلام قطعات دستگاه دوخت باعث شد ۳۰ امتیاز بگیرید”):
  - < 1 ساعت → 50 points + badge progress.
  - < 4 ساعت → 30 points.
  - < 24 ساعت → 15 points.
- Weekly “Fast Responders” leaderboard (minimum 5 handled orders). Display medal chips next to supplier names.

## 12. Points, Badges, Leaderboards (keep math simple)
### Points
| Action | Points | Notes |
| --- | --- | --- |
| Daily login (once/day) | 5 | Show toast: “روز خوبی داشته باشید، ۵ امتیاز گرفتید!” |
| Product saved with score ≥70 | 20 | +10 bonus if ≥90 |
| Profile updated to green zone | 15 | |
| Mini website section completed | 15 | Portfolio/Team each adds 10 |
| Fast order response | 15‑50 | Based on tier |
| Watching a tutorial or attending webinar | 10 | Track via `track-action` (e.g., “آموزش تنظیم و نگهداری دستگاه پرکن مایعات”) |
| Unlocking a badge | 25‑100 | Bronze/Silver/Gold |

### Badges
- **کیفیت فرم‌ها**: محصول کامل، پروفایل کامل، وب‌سایت حرفه‌ای (bronze ≥80, silver ≥90, gold 100 for 7 days).
- **تعامل**: حضور روزانه (۷/۳۰/۱۰۰ روز)، قهرمان هفتگی (۴/۱۲ هفته فعال)، استاد محصولات (۱۰/۵۰/۱۰۰ محصول)، نگهداری پروفایل (۹۵+ برای ۳۰ روز).
- **پاسخ‌دهی**: پاسخ آذرخش (<۱h ۱۰/۵۰/۱۰۰ سفارش)، پاسخ سریع (<۴h ۲۵/۱۰۰/۵۰۰ سفارش)، تأمین‌کننده قابل اعتماد (<۲۴h ۵۰/۲۰۰/۱۰۰۰ سفارش).
- **قدردانی محلی**: “کسب‌وکار خانوادگی” (پروفایل با داستان ۵۰۰ کلمه + عکس تیم) to resonate with older owners, و “نصب موفق خط تولید” (۳ پروژه پورتفولیو با نتایج قابل اندازه‌گیری).

### Leaderboards
- Overall (total points, reset annually but keep archives).
- Weekly (top 10) + Monthly (top 20) highlight new faces; include “you are X points away from top 10”.
- Response time leaderboard (rolling 30 days).
- Category-specific best product quality scores (e.g., بهترین عرضه‌کننده دستگاه‌های نجاری، بسته‌بندی، یا خطوط مونتاژ).

## 13. Persistence & Background Jobs
- Nightly task rebuilds leaderboard snapshots, decays streaks for inactive users, and sends friendly reminders via email/SMS.
- Celery tasks or signals calculate badges asynchronously so form saves stay fast.
- Index `supplier_id`, `first_viewed_at`, `first_responded_at` for reporting.

## 14. Testing & User Validation
1. Unit tests for scoring helpers with boundary inputs (no images, long descriptions, specs missing critical machine data such as voltage).
2. API tests for each endpoint with authenticated suppliers.
3. Frontend tests (Cypress/Playwright) to ensure traffic light colors change as expected and that RTL layout holds on mobile.
4. Usability sessions with 5 non-technical suppliers (over 40) to verify wording, tooltip usefulness, and that they understand how
   to earn points/badges.
5. Performance smoke tests on leaderboard queries.

## 15. Rollout Plan
1. **Backend foundation** – models, migrations, points logic, order tracking.
2. **Frontend foundation** – Pinia store, composable, FormQualityScore component with sample metrics.
3. **Integrations** – wire ProductForm, Profile tab, Mini Website tabs, Portfolio, Team.
4. **Dashboard widgets** – EngagementWidget, BadgeDisplay, LeaderboardWidget, RespondNow chips.
5. **Pilot group** – Enable for 20 machinery suppliers (mix of تولید، فروش قطعات یدکی، و خطوط بسته‌بندی) and collect feedback via in-app survey.
6. **Full release** – Launch to all suppliers with short tutorial video + FAQ focusing on machinery examples.
