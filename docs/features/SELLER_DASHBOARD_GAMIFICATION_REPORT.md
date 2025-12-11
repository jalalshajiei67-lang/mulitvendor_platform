# Seller Dashboard Gamification - Full Report

**Generated:** December 2024  
**Scope:** Current Features, Functionality, Frontend Architecture, Data Flow, UX & Engagement

---

## Executive Summary

The seller dashboard gamification system is a comprehensive engagement platform designed to motivate suppliers (primarily 40+ years old) to complete their profiles, add products, and maintain active engagement. The system uses a tier-based ranking system, point accumulation, reputation scoring, and real-time feedback to guide users toward better profile completion and search visibility.

**Key Highlights:**
- ✅ **11 Active Gamification Components** integrated into the seller dashboard
- ✅ **Tier System** with 5 levels (Diamond, Gold, Silver, Bronze, Inactive)
- ✅ **Reputation Scoring** based on endorsements, reviews, and response time
- ✅ **Real-time Score Tracking** for product, profile, and mini-website sections
- ✅ **Onboarding Tour** with 20 interactive steps
- ✅ **Endorsement System** for peer validation
- ✅ **Badge System** for achievement recognition
- ✅ **Leaderboard** for competitive engagement

---

## 1. Current Features & Functionality

### 1.1 Tier System

The platform uses a 5-tier ranking system based on total points and reputation score:

| Tier | Points Range | Reputation Requirement | Color | Icon |
|------|--------------|------------------------|-------|------|
| **Diamond** | 1000+ | 80+ | Purple | `mdi-diamond-stone` |
| **Gold** | 500-999 | 60+ | Amber | `mdi-trophy` |
| **Silver** | 200-499 | - | Grey | `mdi-medal` |
| **Bronze** | 50-199 | - | Brown | `mdi-award` |
| **Inactive** | 0-49 | - | Red | `mdi-account-off` |

**Features:**
- Tier calculation considers both `total_points` AND `reputation_score` for top tiers
- Visual tier badges with color-coded avatars
- Progress indicators showing distance to next tier
- Tier-specific benefits displayed in expandable panels

### 1.2 Reputation System

Reputation score (0-100) is calculated using:
- **Endorsements** (40% weight): Peer endorsements from invited users
- **Positive Reviews** (40% weight): Reviews with rating >= 4 stars
- **Response Speed** (20% weight): Average chat response time (faster = higher)

**Implementation:**
- Automatic recalculation when endorsements or reviews change
- Exponential moving average for response time (80% old, 20% new)
- Visual reputation display with color-coded progress bars

### 1.3 Point System

Points are awarded for various actions:

| Action | Points | Description |
|--------|--------|-------------|
| Login | 5 | Daily login bonus |
| Product Save | 20 | Adding/updating a product |
| Profile Update | 15 | Completing profile information |
| Mini Site | 15 | Setting up mini-website |
| Fast Response | 20 | Quick order/chat response |
| Tutorial | 10 | Completing tutorials |
| Peer Invitation | 100 | Successful invite signup |
| Endorsement Received | 50 | Being endorsed by peer |

**Tracking:**
- `total_points`: Lifetime accumulated points
- `today_points`: Points earned today (resets daily)
- `current_streak_days`: Consecutive days of activity
- `longest_streak_days`: Best streak record

### 1.4 Section Scoring

Real-time quality scores (0-100) for different sections:

1. **Product Score**: Based on name, description, images, price, category
2. **Profile Score**: Based on first name, last name, email, phone
3. **Mini Website Score**: Based on store name, description, settings
4. **Portfolio Score**: Based on portfolio items count and quality
5. **Team Score**: Based on team members count

**Scoring Logic:**
- Traffic light system: Red (0-40), Yellow (40-70), Green (70-100)
- Weighted metrics with actionable tips
- Real-time updates as users fill forms

---

## 2. Frontend Components

### 2.1 Active Components

#### 2.1.1 BenefitsRankWidget
**Location:** `components/gamification/BenefitsRankWidget.vue`  
**Purpose:** Primary tier and rank display widget

**Features:**
- Large tier badge with icon (80px avatar)
- Current rank display ("رتبه X")
- Total points display
- Reputation score with progress bar
- Progress to next tier indicator
- Expandable tier benefits panels
- Color-coded by tier (purple/amber/grey/brown/red)

**Data Source:**
```typescript
gamificationStore.userRank
gamificationStore.userTier
gamificationStore.engagement?.total_points
gamificationStore.engagement?.reputation_score
gamificationStore.ranksToNextTier
gamificationStore.nextTier
gamificationStore.nextTierPointsNeeded
```

#### 2.1.2 LowScoreBanner
**Location:** `components/gamification/LowScoreBanner.vue`  
**Purpose:** Warning banner for low-score users

**Features:**
- Non-dismissible alert for Inactive tier users
- Shows current tier, points, and reputation
- Two CTAs: "تکمیل پروفایل" and "ارتقای پریمیوم"
- Only displays when `low_score: true` and `is_premium: false`

**Visibility Logic:**
- Checks `gamificationStore.lowScoreStatus.low_score`
- Hidden for premium users

#### 2.1.3 EndorsementCTA
**Location:** `components/gamification/EndorsementCTA.vue`  
**Purpose:** One-time endorsement action for new users

**Features:**
- Shows only if user was invited and hasn't endorsed yet
- Displays inviter name
- Awards 50 points to inviter on endorsement
- One-time action (disappears after use)

**API Integration:**
- `GET /api/gamification/can-endorse/` - Checks eligibility
- `POST /api/gamification/endorse/` - Submits endorsement

#### 2.1.4 TierNudge
**Location:** `components/gamification/TierNudge.vue`  
**Purpose:** Motivational prompts for Gold/Silver users

**Features:**
- Shows only for Gold and Silver tier users (not premium)
- Contextual messages:
  - Gold: "فاصله کمی تا الماس دارید!" (3 more endorsements needed)
  - Silver: "یک قدم تا طلایی شدن" (complete portfolio + 5 endorsements)
- Displays current endorsements and reputation score
- Two action buttons for profile improvement

#### 2.1.5 SetupProgressWidget
**Location:** `components/gamification/SetupProgressWidget.vue`  
**Purpose:** Onboarding progress indicator

**Features:**
- Shows progress percentage for tour completion
- Displays "X از Y مرحله انجام شده"
- "ادامه راه‌اندازی" button to resume tour
- Replaces BenefitsRankWidget when tour is in progress

**Integration:**
- Uses `useSupplierOnboarding()` composable
- Tracks progress in localStorage

#### 2.1.6 EngagementWidget
**Location:** `components/gamification/EngagementWidget.vue`  
**Purpose:** Daily engagement metrics display

**Features:**
- Today's points counter
- Total points display (formatted: 1K, 2.5K, etc.)
- Streak indicator with fire icon
- Average response time display
- Dynamic CTA button based on today's activity

**Metrics Displayed:**
- `today_points`: Points earned today
- `total_points`: Lifetime points
- `current_streak_days`: Current streak
- `avg_response_minutes`: Average response time

#### 2.1.7 BadgeDisplay
**Location:** `components/gamification/BadgeDisplay.vue`  
**Purpose:** Achievement badges showcase

**Features:**
- Grid layout showing available badges
- Tier-based color coding (bronze/silver/gold)
- Progress bars for incomplete badges
- "دریافت شده" chip for earned badges
- Empty state for users with no badges

**Data Structure:**
```typescript
{
  slug: string
  title: string
  tier: 'bronze' | 'silver' | 'gold'
  icon: string
  description: string
  is_earned?: boolean
  progress?: { current: number; target: number; percentage: number }
}
```

#### 2.1.8 LeaderboardWidget
**Location:** `components/gamification/LeaderboardWidget.vue`  
**Purpose:** Competitive ranking display

**Features:**
- Top 5 sellers display
- Position badges with medals for top 3
- Points and streak display per entry
- Color-coded positions (amber/grey/deep-orange)
- Empty state for new leaderboards

**Data Source:**
- `gamificationStore.leaderboard` (top 5 entries)
- Fetched via `GET /api/gamification/leaderboard/?limit=5`

#### 2.1.9 FormQualityScore
**Location:** `components/gamification/FormQualityScore.vue`  
**Purpose:** Yoast-style quality scoring widget

**Features:**
- Circular progress indicator (0-100)
- Traffic light color system (red/yellow/green)
- Metric checklist with pass/fail indicators
- Actionable tips section
- Animated score transitions
- Weighted metric display

**Usage:**
- Embedded in profile form
- Embedded in product forms
- Real-time score updates as user types

#### 2.1.10 Section Scores Display
**Location:** `pages/seller/dashboard.vue` (lines 228-302)  
**Purpose:** Quick overview of all section scores

**Features:**
- Product score with progress bar
- Profile score with progress bar
- Mini Website score with progress bar
- Color-coded chips (success/warning/error)
- "بهبود امتیازها" button linking to miniwebsite tab

#### 2.1.11 Quick Actions
**Location:** `pages/seller/dashboard.vue` (lines 310-349)  
**Purpose:** Gamified action shortcuts

**Features:**
- "افزودن محصول جدید" (+20 points)
- "تکمیل پروفایل" (increases profile score)
- "بهبود فروشگاه" (increases mini-website score)
- Direct navigation to relevant forms

---

## 3. Data Flow Architecture

### 3.1 State Management (Pinia Store)

**Store Location:** `stores/gamification.ts`

**State Structure:**
```typescript
{
  scores: {
    product: ScorePayload | null
    profile: ScorePayload | null
    miniWebsite: ScorePayload | null
    portfolio: ScorePayload | null
    team: ScorePayload | null
  }
  engagement: {
    total_points: number
    today_points: number
    current_streak_days: number
    longest_streak_days: number
    avg_response_minutes: number
    endorsements_received: number
    reputation_score: number
  }
  badges: Badge[]
  earnedBadges: any[]
  leaderboard: LeaderboardEntry[]
  userRank: number | null
  userTier: string | null
  ranksToNextTier: number | null
  nextTier: string | null
  nextTierPointsNeeded: number
  lowScoreStatus: {
    low_score: boolean
    tier: string | null
    is_premium: boolean
    points: number
    reputation_score: number
  }
  loading: boolean
}
```

**Store Methods:**
- `fetchScores()` - Fetches all section scores
- `fetchEngagement()` - Fetches engagement metrics
- `fetchBadges()` - Fetches available and earned badges
- `fetchLeaderboard()` - Fetches leaderboard data
- `fetchLowScoreStatus()` - Checks if user has low score
- `hydrate()` - Fetches all data in parallel
- `updateLocalScore(key, payload)` - Updates local score cache

### 3.2 API Integration Layer

**Composable Location:** `composables/useGamification.ts`

**API Methods:**
```typescript
fetchScores() → GET /api/gamification/score/
fetchEngagement() → GET /api/gamification/engagement/
fetchBadges() → GET /api/gamification/badges/
fetchLowScoreCheck() → GET /api/gamification/low-score-check/
fetchLeaderboard(params) → GET /api/gamification/leaderboard/
trackAction(action, metadata, points) → POST /api/gamification/track-action/
generateInviteCode(email?) → POST /api/gamification/invite/generate/
getInvitationStatus() → GET /api/gamification/invite/status/
endorseInviter() → POST /api/gamification/endorse/
canEndorse() → GET /api/gamification/can-endorse/
```

### 3.3 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Seller Dashboard                          │
│                  (pages/seller/dashboard.vue)                │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ onMounted()
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              useGamificationStore.hydrate()                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Scores   │  │Engagement│  │  Badges  │  │Leaderboard│    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│              useGamificationApi() Composable               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │fetchScores│  │fetchEngag│  │fetchBadge│  │fetchLeader│    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend API Endpoints                     │
│  /api/gamification/score/                                    │
│  /api/gamification/engagement/                                │
│  /api/gamification/badges/                                    │
│  /api/gamification/leaderboard/                                │
└─────────────────────────────────────────────────────────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│              GamificationService (Backend)                   │
│  - compute_product_score()                                    │
│  - compute_profile_score()                                    │
│  - calculate_tier()                                           │
│  - compute_reputation_score()                                 │
└─────────────────────────────────────────────────────────────┘
```

### 3.4 Real-time Updates

**Score Updates:**
1. User fills form field
2. Local validation runs
3. `updateLocalScore()` updates store
4. Component re-renders with new score
5. On save, `POST /api/gamification/award-section/` called
6. Store refreshed via `hydrate()`

**Engagement Updates:**
- Triggered after point-awarding actions
- `gamificationStore.fetchEngagement()` called
- Components reactively update via Vue reactivity

**Tier Updates:**
- Calculated server-side based on points + reputation
- Fetched via leaderboard API
- Updates when engagement data changes

---

## 4. UX & Engagement Features

### 4.1 Onboarding Experience

**Interactive Tour System:**
- **Library:** driver.js v1.4.0
- **Steps:** 20 interactive steps in Persian
- **Features:**
  - RTL support
  - Large fonts (18px description, 24px title)
  - Progress tracking ("X از Y")
  - Resume capability
  - Action waiting (waits for user input)

**Tour Flow:**
1. Welcome message
2. Products tab navigation
3. Add product button
4. Product name input
5. Product description input
6. Product price input
7. Product category selection
8. Product save
9. Success message
10. Mini website tab
11. Settings section
12. Store name input
13. Store description input
14. Settings save
15. Portfolio section
16. Add portfolio item
17. Team section
18. Add team member
19. Completion message

**Progress Widget:**
- Shows when tour is in progress or dismissed
- Displays completion percentage
- "ادامه راه‌اندازی" button to resume

### 4.2 Visual Feedback

**Color Coding:**
- **Success (Green):** Score 70-100, tier benefits, earned badges
- **Warning (Yellow):** Score 40-70, tier nudges
- **Error (Red):** Score 0-40, low score banner
- **Tier Colors:** Purple (Diamond), Amber (Gold), Grey (Silver), Brown (Bronze), Red (Inactive)

**Animations:**
- Score dial smooth transitions (400ms)
- Progress bar updates
- Hover effects on cards
- Loading states with spinners

**Icons:**
- Tier-specific icons (diamond, trophy, medal, award)
- Action icons (fire for streak, shield for reputation)
- Status icons (check, alert, info)

### 4.3 Engagement Mechanics

**Streak System:**
- Visual fire icon with color intensity
- "X روز متوالی" display
- Encourages daily activity

**Progress Indicators:**
- Circular progress for scores
- Linear progress for tier advancement
- Percentage displays
- "X ranks away from [Next Tier]"

**Achievement Recognition:**
- Badge display with tier colors
- "دریافت شده" chips
- Progress bars for incomplete badges
- Congratulation messages

**Competitive Elements:**
- Leaderboard with top 5 sellers
- Rank display ("رتبه X")
- Medal icons for top 3
- Points and streak comparison

### 4.4 Motivational Messaging

**Persian Language:**
- All UI text in Persian
- Friendly, non-technical language
- Action-oriented tips
- Contextual encouragement

**Examples:**
- "فاصله کمی تا الماس دارید!" (You're close to Diamond!)
- "همین حالا امتیاز جمع کنید" (Earn points right now)
- "عالی! ادامه دهید" (Great! Keep going)
- "امروز محصول جدید ثبت کنید" (Add a new product today)

**Contextual CTAs:**
- Dynamic button text based on activity
- Tier-specific suggestions
- Section-specific improvement tips

### 4.5 Empty States

**Gamified Empty States:**
- "Add your first product to earn +20 points!"
- "Add 3 portfolio items to unlock Silver Tier!"
- "Add team members to boost your score!"

**Encouragement:**
- Clear next steps
- Point rewards mentioned
- Visual icons and colors

---

## 5. Technical Implementation Details

### 5.1 Component Architecture

**Component Hierarchy:**
```
pages/seller/dashboard.vue
├── LowScoreBanner
├── EndorsementCTA
├── BenefitsRankWidget (or SetupProgressWidget)
├── TierNudge
├── Section Scores Display
├── Quick Actions
├── EngagementWidget
├── BadgeDisplay
└── LeaderboardWidget
```

**Component Communication:**
- Props down, events up pattern
- Shared store for global state
- Computed properties for reactive updates

### 5.2 Reactive Data Flow

**Vue 3 Composition API:**
```typescript
const gamificationStore = useGamificationStore()

// Reactive computed properties
const userTier = computed(() => gamificationStore.userTier)
const userRank = computed(() => gamificationStore.userRank)
const engagement = computed(() => gamificationStore.engagement)

// Watchers for updates
watch(profileScore, (score) => {
  gamificationStore.updateLocalScore('profile', {
    title: 'profile',
    score,
    metrics: profileMetrics.value,
    tips: profileTips.value
  })
})
```

### 5.3 API Error Handling

**Error States:**
- Loading indicators during fetches
- Graceful degradation on API failures
- Console warnings for non-critical errors
- User-friendly error messages in Persian

**Retry Logic:**
- Automatic retry on network errors
- Fallback to cached data when available
- Silent failures for non-critical endpoints

### 5.4 Performance Optimizations

**Data Fetching:**
- Parallel API calls via `Promise.all()`
- Single `hydrate()` call on mount
- Selective updates after actions
- Caching in Pinia store

**Rendering:**
- Computed properties for derived data
- Lazy loading for heavy components
- Virtual scrolling for long lists
- Image optimization for badges

**Memory Management:**
- Store cleanup on unmount
- Event listener cleanup
- Timer cleanup for animations

### 5.5 Mobile Responsiveness

**Breakpoints:**
- Mobile: < 600px
- Tablet: 600px - 960px
- Desktop: > 960px

**Adaptations:**
- Responsive grid layouts
- Collapsible sections
- Touch-friendly buttons
- Optimized font sizes
- Stacked layouts on mobile

---

## 6. Integration Points

### 6.1 Dashboard Integration

**Location:** `pages/seller/dashboard.vue`

**Integration Points:**
1. **Home Tab:**
   - LowScoreBanner (top)
   - EndorsementCTA (conditional)
   - BenefitsRankWidget or SetupProgressWidget
   - TierNudge
   - Section scores display
   - Quick actions
   - EngagementWidget, BadgeDisplay, LeaderboardWidget

2. **Profile Tab:**
   - FormQualityScore component
   - Real-time score updates
   - Award section on save

3. **Products Tab:**
   - FormQualityScore in product forms
   - Point awards on product save
   - Score refresh after save

### 6.2 Backend Integration

**Django Models:**
- `SupplierEngagement` - Main engagement data
- `PointsHistory` - Point transaction ledger
- `Badge` - Badge definitions
- `EarnedBadge` - User badge achievements
- `Invitation` - Invitation tracking
- `Endorsement` - Endorsement records

**Services:**
- `GamificationService` - Core business logic
- Score calculation methods
- Tier calculation
- Reputation calculation
- Point awarding

**Signals:**
- Product save → Award points
- Profile update → Award points
- Review creation → Update reputation
- Chat message → Track response time
- Invitation acceptance → Award points

### 6.3 Third-party Integrations

**Tour Library:**
- driver.js for onboarding tour
- Custom RTL styling
- Persian text support

**UI Framework:**
- Vuetify 3 components
- Material Design icons
- Custom color themes

---

## 7. User Journey Examples

### 7.1 New User Journey

1. **First Visit:**
   - Sees SetupProgressWidget
   - Onboarding tour auto-starts
   - Guided through product creation

2. **Product Creation:**
   - FormQualityScore shows real-time feedback
   - Tips appear as user types
   - Score updates dynamically
   - +20 points on save

3. **Profile Completion:**
   - Section scores display
   - FormQualityScore guides completion
   - +15 points on save
   - Tier may upgrade

4. **Engagement:**
   - BenefitsRankWidget shows current tier
   - EngagementWidget shows daily progress
   - BadgeDisplay shows available badges
   - LeaderboardWidget shows ranking

### 7.2 Returning User Journey

1. **Dashboard Load:**
   - BenefitsRankWidget shows tier/rank
   - EngagementWidget shows streak
   - Section scores display current status
   - TierNudge shows if applicable

2. **Daily Activity:**
   - Login → +5 points
   - Add product → +20 points
   - Respond to chat → +20 points (if fast)
   - Streak counter increments

3. **Tier Advancement:**
   - Points accumulate
   - Reputation improves
   - Tier upgrades when thresholds met
   - BenefitsRankWidget updates
   - New tier benefits unlocked

### 7.3 Low-Score User Journey

1. **Warning Display:**
   - LowScoreBanner appears (non-dismissible)
   - Shows current tier, points, reputation
   - Two CTAs: improve profile or upgrade premium

2. **Improvement Path:**
   - Guided to profile completion
   - FormQualityScore shows what's missing
   - Points awarded for completions
   - Tier may upgrade from Inactive

3. **Premium Option:**
   - Can upgrade to bypass low score
   - Premium badge overrides tier
   - Banner disappears

---

## 8. Data Metrics & Analytics

### 8.1 Tracked Metrics

**Engagement Metrics:**
- Total points
- Today's points
- Current streak
- Longest streak
- Average response time

**Quality Metrics:**
- Product score (0-100)
- Profile score (0-100)
- Mini website score (0-100)
- Portfolio score (0-100)
- Team score (0-100)

**Social Metrics:**
- Endorsements received
- Reputation score (0-100)
- Positive reviews count
- Invitations sent/accepted

**Competitive Metrics:**
- Current rank
- Tier level
- Ranks to next tier
- Points to next tier

### 8.2 Point History

**Transaction Ledger:**
- All point awards logged
- Reason for each award
- Metadata (product ID, order ID, etc.)
- Timestamp

**Available via:**
- `GET /api/gamification/points/` (paginated)

---

## 9. Current Limitations & Considerations

### 9.1 Known Limitations

1. **Real-time Updates:**
   - Score updates require manual refresh after some actions
   - No WebSocket for live updates

2. **Badge System:**
   - Badge definitions exist but full automation may be incomplete
   - Progress tracking may not update in real-time

3. **Leaderboard:**
   - Limited to top 5 display
   - No pagination for full leaderboard
   - No time period filters (weekly/monthly)

4. **Onboarding Tour:**
   - Progress saved in localStorage (not server-side)
   - No analytics on tour completion rates

### 9.2 Performance Considerations

1. **API Calls:**
   - Multiple parallel calls on mount
   - Could benefit from request batching
   - No request deduplication

2. **Data Caching:**
   - Store persists during session
   - No offline support
   - No background refresh

3. **Component Rendering:**
   - All widgets render on mount
   - Could use lazy loading for below-fold content

### 9.3 UX Considerations

1. **Information Density:**
   - Many widgets on home tab
   - Could be overwhelming for new users
   - Consider progressive disclosure

2. **Mobile Experience:**
   - Some widgets may be cramped on small screens
   - Stacked layout helps but could be optimized

3. **Accessibility:**
   - RTL support is good
   - Color coding may not be accessible for color-blind users
   - Consider additional visual indicators

---

## 10. Recommendations

### 10.1 Short-term Improvements

1. **Real-time Score Updates:**
   - Implement WebSocket or polling for live score updates
   - Show toast notifications for point awards

2. **Badge Progress:**
   - Real-time badge progress updates
   - Notification when badge is earned
   - Badge achievement animations

3. **Leaderboard Enhancements:**
   - Add pagination
   - Add time period filters
   - Show user's position if not in top 5

### 10.2 Medium-term Enhancements

1. **Analytics Dashboard:**
   - Track engagement metrics over time
   - Show point earning trends
   - Streak visualization

2. **Personalized Recommendations:**
   - AI-powered suggestions for improvement
   - Context-aware tips based on user behavior
   - Predictive tier advancement timeline

3. **Social Features:**
   - Compare with similar sellers
   - Share achievements
   - Peer comparison

### 10.3 Long-term Vision

1. **Gamification Marketplace:**
   - Exchange points for premium features
   - Unlock exclusive tools
   - Tier-based feature access

2. **Community Features:**
   - Seller forums
   - Mentorship programs
   - Success stories

3. **Advanced Analytics:**
   - Correlation between gamification and sales
   - ROI tracking
   - A/B testing framework

---

## 11. Code References

### 11.1 Key Files

**Frontend:**
- `pages/seller/dashboard.vue` - Main dashboard page
- `stores/gamification.ts` - Pinia store
- `composables/useGamification.ts` - API composable
- `components/gamification/*.vue` - All gamification components

**Backend:**
- `gamification/views.py` - API endpoints
- `gamification/services.py` - Business logic
- `gamification/models.py` - Data models
- `gamification/urls.py` - URL routing

### 11.2 Component Locations

```
front_end/nuxt/
├── pages/seller/dashboard.vue
├── stores/gamification.ts
├── composables/
│   ├── useGamification.ts
│   └── useSupplierOnboarding.ts
└── components/gamification/
    ├── BenefitsRankWidget.vue
    ├── LowScoreBanner.vue
    ├── EndorsementCTA.vue
    ├── TierNudge.vue
    ├── SetupProgressWidget.vue
    ├── EngagementWidget.vue
    ├── BadgeDisplay.vue
    ├── LeaderboardWidget.vue
    └── FormQualityScore.vue
```

---

## 12. Conclusion

The seller dashboard gamification system is a comprehensive, well-architected engagement platform that successfully motivates suppliers to complete their profiles and maintain active engagement. The system uses a multi-layered approach combining:

- **Tier-based ranking** for competitive motivation
- **Point accumulation** for action rewards
- **Reputation scoring** for trust building
- **Real-time feedback** for immediate guidance
- **Onboarding tour** for user education
- **Visual feedback** for engagement

The implementation follows Vue 3 best practices, uses Pinia for state management, and integrates seamlessly with the Django backend. The Persian language support and RTL layout ensure accessibility for the target audience.

**Overall Assessment:** ✅ **Production Ready** with room for enhancements in real-time updates, analytics, and advanced features.

---

**Report End**

