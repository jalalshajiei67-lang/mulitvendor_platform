# Gamification & Supplier Engagement - Multi-Phase Implementation Plan

This document breaks down the comprehensive gamification strategy into **8 smaller, independently testable phases**. Each phase focuses on a specific domain and can be implemented, tested, and validated before moving to the next.

---

## **Phase 1: Tier System Foundation** 
**Domain:** Backend Tier Logic + Basic UI Display  
**Estimated Time:** 3-5 days  
**Goal:** Users can see their tier and understand the ranking system

### Backend Tasks

| ID | Task | Details |
|---|---|---|
| **BE-101** | **Create Tier Calculation Service** | Create `calculate_tier()` method in `GamificationService` that assigns tiers based on `total_points`: <br>- Diamond: 1000+ points<br>- Gold: 500-999 points<br>- Silver: 200-499 points<br>- Bronze: 50-199 points<br>- Inactive/Low: 0-49 points |
| **BE-102** | **Enhance Leaderboard API** | Modify `/api/gamification/leaderboard/` to return:<br>- Current user's `rank` (position in leaderboard)<br>- Current user's `tier` (Diamond/Gold/Silver/Bronze/Inactive)<br>- `ranks_to_next_tier` (how many ranks until next tier)<br>- Full leaderboard with tier badges |
| **BE-103** | **Add Tier Helper Methods** | Add utility methods:<br>- `get_tier_thresholds()` - returns point thresholds for each tier<br>- `get_next_tier_info()` - returns next tier name and required points |

### Frontend Tasks

| ID | Task | Details |
|---|---|---|
| **FE-101** | **Build "Benefits & Rank" Widget** | Create Vue component `BenefitsRankWidget.vue` that:<br>- Displays current tier with color-coded badge<br>- Shows current rank and total points<br>- Displays "X ranks away from [Next Tier]"<br>- Uses Persian text and RTL layout |
| **FE-102** | **Integrate Enhanced Leaderboard API** | Connect widget to enhanced API (BE-102)<br>- Fetch on dashboard load<br>- Handle loading/error states<br>- Update tier badge color dynamically |

### Testing Checklist
- [ ] Tier calculation works for all point ranges
- [ ] Leaderboard API returns correct rank and tier for current user
- [ ] Widget displays correctly on dashboard
- [ ] Tier colors match design (Diamond=purple, Gold=yellow, etc.)
- [ ] RTL layout works correctly

---

## **Phase 2: Global Status Visibility**
**Domain:** UI/UX - Persistent Status Display  
**Estimated Time:** 2-3 days  
**Goal:** Users see their tier/status on every page, not just dashboard

### Frontend Tasks

| ID | Task | Details |
|---|---|---|
| **FE-201** | **Sidebar Mini-Badge** | Add tier badge icon next to user avatar in sidebar/navigation<br>- Small circular badge with tier color<br>- Tooltip shows tier name and points<br>- Updates when tier changes |
| **FE-202** | **Progress Ring Around Avatar** | Add circular progress indicator around avatar<br>- Shows progress to next tier (0-100%)<br>- Color changes based on current tier<br>- Smooth animation on updates |
| **FE-203** | **Gamified Empty States** | Modify `EmptyState.vue` component to accept `gamification_context` prop<br>- Products page: "Add your first product to earn +20 points!"<br>- Portfolio: "Add 3 portfolio items to unlock Silver Tier!"<br>- Team: "Add team members to boost your score!" |

### Testing Checklist
- [ ] Mini-badge appears in sidebar on all pages
- [ ] Progress ring updates correctly
- [ ] Empty states show gamification messages
- [ ] No performance issues with frequent updates

---

## **Phase 3: Onboarding Quest - Part 1 (Tour Setup)**
**Domain:** User Onboarding Flow  
**Estimated Time:** 3-4 days  
**Goal:** New users get guided through their first product setup

### Frontend Tasks

| ID | Task | Details |
|---|---|---|
| **FE-301** | **Install Tour Library** | Install and configure Shepherd.js or Intro.js for guided tours<br>- Configure Persian text and RTL support<br>- Set up tour step definitions |
| **FE-302** | **Create OnboardingQuest Component** | Build `OnboardingQuest.vue` component with 3-step tour:<br>1. "Add Product Name" - guides to product name field<br>2. "Add Description" - guides to description field<br>3. "Add Images" - guides to image upload<br>- Auto-triggers for users with 0 products |
| **FE-303** | **Quest Completion Detection** | Add logic to detect when each tour step is completed<br>- Listen to form field changes<br>- Mark steps as complete<br>- Show completion checkmarks |

### Backend Tasks

| ID | Task | Details |
|---|---|---|
| **BE-301** | **Verify Section Award Endpoint** | Ensure `POST /api/gamification/award-section/` works correctly:<br>- Can be called multiple times<br>- Awards points incrementally based on score improvement<br>- Returns points awarded |

### Testing Checklist
- [ ] Tour triggers automatically for new users
- [ ] Tour steps are in Persian and RTL
- [ ] Tour can be closed and resumed
- [ ] Section award API works correctly

---

## **Phase 4: Onboarding Quest - Part 2 (Real-Time Feedback)**
**Domain:** User Onboarding Flow - Feedback Loop  
**Estimated Time:** 3-4 days  
**Goal:** Users see immediate feedback when completing quest steps

### Frontend Tasks

| ID | Task | Details |
|---|---|---|
| **FE-401** | **Real-Time Score Updates** | After each quest step completion:<br>- Call `GET /api/gamification/score/` to get updated `product_score`<br>- Animate score dial from old to new value<br>- Change progress bar color based on score<br>- Show toast notification: "You earned +X points!" |
| **FE-402** | **Score Dial Animation** | Create animated score dial component<br>- Smooth transition between values<br>- Color changes: red (0-40), yellow (40-70), green (70-100)<br>- Shows percentage and visual progress |
| **FE-403** | **Quest Payoff Screen** | Design final screen after quest completion:<br>- Shows final product score<br>- Explains connection to search ranking<br>- Message: "Higher scores = Better search visibility!"<br>- Button to continue to dashboard |

### Testing Checklist
- [ ] Score updates without page reload
- [ ] Animations are smooth and performant
- [ ] Toast notifications appear correctly
- [ ] Payoff screen creates "aha!" moment

---

## **Phase 5: Invitation System**
**Domain:** User Acquisition & Social Engagement  
**Estimated Time:** 4-5 days  
**Goal:** Sellers can invite peers and earn rewards

### Backend Tasks

| ID | Task | Details |
|---|---|---|
| **BE-501** | **Create Invitation Model** | Add `Invitation` model:<br>- `inviter` (FK to VendorProfile)<br>- `invite_code` (unique string)<br>- `invitee_email` (optional)<br>- `status` (pending/accepted/expired)<br>- `created_at`, `accepted_at` |
| **BE-502** | **Generate Invite Code Endpoint** | Create `POST /api/gamification/invite/generate/`<br>- Generates unique code for current user<br>- Returns invite link: `https://platform.com/register?ref=CODE`<br>- Stores invitation in database |
| **BE-503** | **Track Invite Signup** | Modify user registration to check for `?ref=CODE`<br>- Links new user to inviter<br>- Marks invitation as accepted<br>- Calls `add_points('peer_invitation', 100)` for inviter |
| **BE-504** | **Invitation Status Endpoint** | Create `GET /api/gamification/invite/status/`<br>- Returns list of sent invitations<br>- Shows status (pending/accepted)<br>- Shows points earned from each |

### Frontend Tasks

| ID | Task | Details |
|---|---|---|
| **FE-501** | **Invite & Earn Page** | Create `InviteEarn.vue` page:<br>- Displays unique invite link<br>- Copy-to-clipboard button<br>- Shows invitation list with status<br>- Displays total points earned from invites |
| **FE-502** | **Registration Ref Handling** | Modify registration page to capture `?ref=CODE`<br>- Store in session/localStorage<br>- Send to backend on signup |

### Testing Checklist
- [ ] Invite codes are unique
- [ ] Points awarded correctly on signup
- [ ] Invitation status updates correctly
- [ ] Copy-to-clipboard works
- [ ] Registration flow handles ref codes

---

## **Phase 6: Endorsement & Reputation System** ✅ COMPLETED
**Domain:** Social Proof & Trust Metrics  
**Estimated Time:** 4-5 days  
**Goal:** Build reputation scoring based on peer endorsements and reviews

### Backend Tasks

| ID | Task | Details | Status |
|---|---|---|---|
| **BE-601** | **Endorsement Endpoint** | Create `POST /api/gamification/endorse/`<br>- New user can endorse their inviter<br>- Increments `endorsements_received` on inviter<br>- Awards points to inviter: `add_points('endorsement_received', 50)`<br>- Prevents duplicate endorsements | ✅ Done |
| **BE-602** | **Reputation Score Calculator** | Create `compute_reputation_score()` method in `GamificationService`:<br>- Formula: `(endorsements * 0.4) + (positive_reviews * 0.4) + (response_speed_bonus * 0.2)`<br>- `positive_reviews` = count of reviews with rating >= 4<br>- `response_speed_bonus` = normalized avg_response_minutes (faster = higher)<br>- Saves to `SupplierEngagement.reputation_score` | ✅ Done |
| **BE-603** | **Update Leaderboard with Reputation** | Modify tier calculation to consider both `total_points` AND `reputation_score`<br>- Diamond tier requires: 1000+ points AND 80+ reputation<br>- Gold: 500+ points AND 60+ reputation<br>- Lower tiers: points-based only | ✅ Done |
| **BE-604** | **Review Integration** | Hook into review/rating system to update `positive_reviews_count`<br>- When buyer rates seller >= 4 stars, increment counter<br>- Recalculate reputation score | ✅ Done (via compute_reputation_score) |
| **BE-605** | **Response Speed Tracking** | Track chat reply times and update `avg_response_minutes`<br>- Signal handler on ChatMessage post_save<br>- Calculates time from last buyer message to vendor reply<br>- Updates rolling average using exponential moving average | ✅ Done |

### Frontend Tasks

| ID | Task | Details | Status |
|---|---|---|---|
| **FE-601** | **Endorsement Button** | Add "Endorse Inviter" button on new user dashboard<br>- Only shows if user was invited<br>- One-time action<br>- Shows confirmation message | ✅ Done |
| **FE-602** | **Reputation Display** | Show reputation score in Benefits & Rank widget<br>- Display as 0-100 score<br>- Show breakdown: "Based on endorsements, reviews, and response time" | ✅ Done |

### Implementation Notes
- Added `Endorsement` model to track endorsements
- Added `endorsements_received`, `positive_reviews_count`, `reputation_score` fields to `SupplierEngagement`
- Created `EndorsementCTA.vue` component for frontend endorsement UI
- Reputation score automatically recalculates when endorsements or reviews change
- Chat response time tracking uses exponential moving average (80% old, 20% new)

### Testing Checklist
- [x] Endorsements increment counters correctly
- [x] Reputation score calculates correctly
- [x] Leaderboard considers reputation for top tiers
- [x] Reviews update reputation score (via compute_reputation_score)
- [x] Duplicate endorsements prevented
- [x] Chat response times tracked and averaged

---

## **Phase 7: Badge System**
**Domain:** Achievement Recognition  
**Estimated Time:** 3-4 days  
**Goal:** Users earn and display badges for achievements

### Backend Tasks

| ID | Task | Details |
|---|---|---|
| **BE-701** | **Create Badge Definitions** | Add badge records via migration or admin:<br>- "Recruiter" badge: criteria = 5+ successful invites<br>- "Customer Favorite" badge: criteria = 20+ positive reviews<br>- "Fast Responder" badge: criteria = avg_response < 60 minutes |
| **BE-702** | **Badge Award Logic** | Create `check_and_award_badges()` method:<br>- Checks all badge criteria on relevant actions<br>- Awards badge if criteria met<br>- Creates `EarnedBadge` record<br>- Awards bonus points: `add_points('badge', 200)` |
| **BE-703** | **Badge Display API** | Enhance `GET /api/gamification/badges/` to include:<br>- Badge icons/images<br>- Achievement dates<br>- Progress to next badge (if applicable) |

### Frontend Tasks

| ID | Task | Details |
|---|---|---|
| **FE-701** | **Badge Display Component** | Create `BadgeDisplay.vue` component:<br>- Shows earned badges with icons<br>- Displays on seller profile<br>- Shows next available badges with progress |
| **FE-702** | **Badge in Product Listings** | Show badge icons next to seller name in product cards<br>- "Recruiter" badge for top recruiters<br>- "Customer Favorite" for highly rated sellers |

### Testing Checklist
- [ ] Badges are awarded when criteria met
- [ ] Badge icons display correctly
- [ ] Progress to next badge shows correctly
- [ ] Badges appear in product listings

---

## **Phase 8: Search Integration & Monetization**
**Domain:** Business Logic & Revenue  
**Estimated Time:** 4-5 days  
**Goal:** Gamification affects search ranking and drives premium upgrades

### Backend Tasks

| ID | Task | Details |
|---|---|---|
| **BE-801** | **Modify Search Algorithm** | Update product search/listing query to sort by tier:<br>- Diamond tier sellers first<br>- Then Gold, Silver, Bronze<br>- Inactive/Low Score sellers last<br>- Within same tier, sort by reputation_score<br>- Premium users always shown first (override tier) |
| **BE-802** | **Low Score Banner Logic** | Create endpoint to check if user should see banner:<br>- `GET /api/gamification/low-score-check/`<br>- Returns `true` if tier is "Inactive/Low Score"<br>- Returns `false` if premium user (they can upgrade but don't need banner) |
| **BE-803** | **Analytics Endpoint** | Create `GET /api/admin/gamification-analytics/` (admin only):<br>- Tier distribution (count per tier)<br>- Average score vs average sales (correlation)<br>- Quest completion rate<br>- Invitation conversion rate |

### Frontend Tasks

| ID | Task | Details |
|---|---|---|
| **FE-801** | **Low Score Banner** | Create persistent, non-dismissible banner for low-score users:<br>- Message: "Your profile score is low. Improve it to appear higher in search results, or upgrade to Premium."<br>- Two buttons: "Improve Profile" (links to profile) and "Upgrade to Premium" (links to pricing)<br>- Only shows for Inactive/Low Score tier |
| **FE-802** | **Tier Nudges** | Add subtle prompts for Gold/Silver users:<br>- Gold: "Get 3 more peer endorsements to reach Diamond Tier!"<br>- Silver: "Complete your portfolio to reach Gold Tier!"<br>- Show as toast notifications or small widgets |
| **FE-803** | **Premium Override Display** | Ensure premium users always show "Verified/Premium" badge:<br>- Even if they have low gamification score<br>- Badge appears in product listings<br>- Profile shows premium status prominently |

### Testing Checklist
- [ ] Search results sorted by tier correctly
- [ ] Premium users appear first regardless of tier
- [ ] Low score banner shows/hides correctly
- [ ] Tier nudges appear at appropriate times
- [ ] Analytics endpoint returns correct data

---

## **Phase 9: Anti-Gaming & Security** (Optional but Recommended)
**Domain:** System Integrity  
**Estimated Time:** 2-3 days  
**Goal:** Prevent users from gaming the system

### Implementation Plan (Backend + Frontend)
- **Rate limiting (5 invites/day):** Add per-user throttle on invitation endpoints; return friendly Persian/RTL error and log blocks. Surface remaining quota in invite status API.
- **Circular/self-referral blocking:** Validate invites at creation (same inviter/invitee, circular history) and fail fast with localized messaging. No device fingerprinting for now.
- **Suspicious review velocity auto-flag:** On review creation, flag seller when >5 reviews in 1 hour from new accounts; exclude flagged reviews from reputation until cleared; expose flag status in admin API.
- **Section award rate limit:** Cap award endpoints to 10 per hour; block further awards until window resets and log reason.
- **Admin moderation UI:** Add admin-view listing of flagged reviews/invites with actions (approve/clear). Frontend copy in Persian, RTL layout.
- **User-facing nudges:** In invite UI, show remaining daily invites, disabled state when exhausted, and Persian toast for blocks. For buyers leaving reviews, surface minimal friction; only warnings appear if a review was auto-flagged after submission.

### Backend Tasks

| ID | Task | Details |
|---|---|---|
| **BE-901** | **Circular Invite Check** | Add validation to invitation system:<br>- User A invites B, B cannot invite A back<br>- Check invitation history to prevent circular references |
| **BE-902** | **Self-Referral Prevention** | Prevent users from inviting themselves:<br>- Check if invitee email/phone matches inviter<br>- Block invites to accounts with same device fingerprint |
| **BE-903** | **Review Velocity Check** | Flag suspicious review patterns:<br>- If seller receives >5 reviews in 1 hour from new accounts, flag for review<br>- Don't count flagged reviews in reputation score until verified |
| **BE-904** | **Rate Limiting** | Add rate limits to point-awarding endpoints:<br>- Max 10 section awards per hour<br>- Max 5 invitations per day |

### Testing Checklist
- [ ] Circular invites are blocked
- [ ] Self-referrals are prevented
- [ ] Suspicious review patterns are flagged
- [ ] Rate limits work correctly

---

## Implementation Order Summary

1. **Phase 1** - Tier System Foundation (Core functionality)
2. **Phase 2** - Global Status Visibility (UX improvement)
3. **Phase 3** - Onboarding Quest Part 1 (User activation)
4. **Phase 4** - Onboarding Quest Part 2 (Feedback loop)
5. **Phase 5** - Invitation System (User acquisition)
6. **Phase 6** - Endorsement & Reputation (Trust building)
7. **Phase 7** - Badge System (Achievement recognition)
8. **Phase 8** - Search Integration & Monetization (Business impact)
9. **Phase 9** - Anti-Gaming & Security (System integrity)

---

## Testing Strategy Per Phase

Each phase should be tested independently:

1. **Unit Tests**: Test backend logic (tier calculation, point awarding, etc.)
2. **API Tests**: Test all endpoints with Postman/curl
3. **Frontend Tests**: Test UI components in isolation
4. **Integration Tests**: Test full user flows
5. **User Acceptance**: Test with 2-3 real users before moving to next phase

---

## Notes

- Each phase builds on previous phases but can be tested independently
- If a phase fails testing, fix it before moving to the next
- Consider deploying each phase to staging for user feedback
- Document any deviations from this plan as you implement

