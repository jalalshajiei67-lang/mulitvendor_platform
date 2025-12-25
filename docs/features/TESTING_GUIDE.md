# Gamification Dashboard Testing Guide

## Quick Start Testing

### 1. Start the Development Servers

**Backend:**
```bash
cd multivendor_platform/multivendor_platform
python manage.py runserver
```

**Frontend:**
```bash
cd multivendor_platform/front_end/nuxt
npm run dev
```

---

## Test Scenarios

### Scenario 1: New Seller Onboarding
**Goal:** Verify task sequencing and progress tracking

1. **Create a new seller account** or use a test account with minimal data
2. **Navigate to Seller Dashboard** (`/seller/dashboard`)
3. **Verify Home Tab displays:**
   - ✅ StatusCard showing 0% or low completion
   - ✅ CurrentTaskCard showing "تکمیل پروفایل شما" (Complete Your Profile)
   - ✅ Milestone bar with 5 steps
   - ✅ Leaderboard section

4. **Click "شروع کنید" (Start) button**
   - ✅ Should navigate to "فروشگاه من" tab
   - ✅ Profile sub-tab should be active

5. **Complete Profile:**
   - Fill in: First Name, Last Name, Email, Phone
   - Click "ذخیره تغییرات" (Save Changes)
   - ✅ Should see celebration overlay with confetti
   - ✅ Should show "+50 امتیاز"
   - ✅ Should auto-close after 3 seconds

6. **Return to Home Tab:**
   - ✅ StatusCard should show updated percentage
   - ✅ First milestone (پروفایل) should be green/completed
   - ✅ CurrentTaskCard should now show "تنظیمات فروشگاه آنلاین" (Mini Website)
   - ✅ Total points should be at least 50

---

### Scenario 2: Complete All Required Steps
**Goal:** Verify full onboarding flow

1. **Mini Website Setup:**
   - Go to "فروشگاه من" → "تنظیمات فروشگاه"
   - Fill in: Store name, Description (100+ chars), Upload banner
   - Save settings
   - ✅ Celebration: "+75 امتیاز"
   - ✅ Next task: "افزودن محصولات"

2. **Add Products:**
   - Go to "فروشگاه من" → "محصولات من"
   - Click "افزودن محصول جدید"
   - Add 3 products with images and descriptions
   - ✅ After each: "+20 امتیاز"
   - ✅ Progress shows "1 از 3", "2 از 3", "3 از 3"
   - ✅ After 3rd: Next task is "معرفی تیم شما"

3. **Add Team Member:**
   - Go to "فروشگاه من" → "تیم ما"
   - Add at least 1 team member
   - ✅ Celebration: "+50 امتیاز"
   - ✅ Next task: "نمونه کارهای شما"

4. **Add Portfolio Item:**
   - Go to "فروشگاه من" → "نمونه کارها"
   - Add at least 1 portfolio project
   - ✅ Celebration: "+50 امتیاز"
   - ✅ Next task: Engagement action (insights/invites)

5. **Verify Completion:**
   - Go to Home Tab
   - ✅ StatusCard shows ~100% or high completion
   - ✅ All 5 milestones are green
   - ✅ CurrentTaskCard shows engagement task or completion message

---

### Scenario 3: Engagement Actions
**Goal:** Verify optional task rotation

1. **Share Insight:**
   - Go to "اشتراک تجربه" tab
   - Fill in title and content
   - Click "ارسال بینش"
   - ✅ Celebration: "+15 امتیاز"
   - ✅ Insight appears in feed

2. **Like an Insight:**
   - Click like button on any insight
   - ✅ Like count increases
   - ✅ Author gets +5 points

3. **Comment on Insight:**
   - Click "دیدگاه‌ها" button
   - Add a comment
   - Click "ارسال دیدگاه"
   - ✅ Comment appears
   - ✅ Commenter gets +5 points

---

### Scenario 4: Task Navigation
**Goal:** Verify task action buttons work

1. **From CurrentTaskCard, click "شروع کنید":**
   - ✅ For profile task: Goes to miniwebsite → profile tab
   - ✅ For mini_website task: Goes to miniwebsite → settings tab
   - ✅ For products task: Goes to miniwebsite → products tab
   - ✅ For team task: Goes to miniwebsite → team tab
   - ✅ For portfolio task: Goes to miniwebsite → portfolio tab
   - ✅ For insights task: Goes to insights tab
   - ✅ For invite task: Goes to /vendor/invite page

---

### Scenario 5: Mobile Responsiveness
**Goal:** Verify mobile layout

1. **Resize browser to mobile (< 600px):**
   - ✅ StatusCard circular progress is smaller (100px)
   - ✅ Milestone circles are smaller (32px)
   - ✅ Card padding reduces to 16px
   - ✅ Metrics stack vertically
   - ✅ Only first 3 tabs visible, rest in menu

2. **Test interactions:**
   - ✅ Task card CTA button is touch-friendly
   - ✅ Milestone tooltips work on tap
   - ✅ Celebration overlay is centered
   - ✅ All text is readable

---

### Scenario 6: Leaderboard
**Goal:** Verify leaderboard functionality

1. **View Leaderboard in Home Tab:**
   - ✅ Shows top 10 sellers
   - ✅ Top 3 have special badges/colors
   - ✅ Shows points, streak, tier for each
   - ✅ Current user's rank is displayed
   - ✅ Hover effects work

---

### Scenario 7: Points History
**Goal:** Verify points are tracked correctly

1. **Open Browser DevTools → Network Tab**
2. **Complete a task**
3. **Check API Response:**
   - ✅ `POST /api/gamification/tasks/complete/` returns:
     - `points_awarded`: correct amount
     - `celebration`: true
     - `next_task`: object with next task
     - `message`: Persian text

4. **Check Dashboard Refresh:**
   - ✅ `GET /api/gamification/dashboard/` called after completion
   - ✅ `status.total_points` increased
   - ✅ `progress.milestones` updated
   - ✅ `current_task` changed to next task

---

## API Testing

### Test Dashboard Endpoint
```bash
# Get auth token first
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test_seller", "password": "password123"}'

# Use token to get dashboard data
curl -X GET http://localhost:8000/api/gamification/dashboard/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Expected Response:**
```json
{
  "status": {
    "tier": "bronze",
    "tier_display": "برنز",
    "tier_color": "brown",
    "rank": 5,
    "total_points": 150,
    "reputation_score": 45,
    "current_streak_days": 3,
    "avg_response_minutes": 120
  },
  "progress": {
    "overall_percentage": 60,
    "milestones": [
      {
        "name": "profile",
        "title": "تکمیل پروفایل",
        "completed": true,
        "score": 85,
        "order": 1
      },
      // ... more milestones
    ],
    "required_steps_completed": 3,
    "total_required_steps": 5
  },
  "current_task": {
    "type": "team",
    "title": "معرفی تیم شما",
    "description": "نمایش تیم، حرفه‌ای‌تر به نظر می‌رسید...",
    "action_url": "team",
    "points": 50,
    "is_required": true,
    "icon": "mdi-account-group"
  },
  "leaderboard_position": 5
}
```

### Test Task Completion
```bash
curl -X POST http://localhost:8000/api/gamification/tasks/complete/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"task_type": "profile", "metadata": {}}'
```

**Expected Response:**
```json
{
  "points_awarded": 50,
  "celebration": true,
  "next_task": {
    "type": "mini_website",
    "title": "تنظیمات فروشگاه آنلاین",
    // ... task details
  },
  "progress": {
    "overall_percentage": 20,
    // ... progress details
  },
  "message": "عالی! 50 امتیاز دریافت کردید."
}
```

---

## Browser Console Tests

### Check Component Loading
```javascript
// In browser console on dashboard page
console.log('StatusCard loaded:', document.querySelector('.status-card') !== null)
console.log('CurrentTaskCard loaded:', document.querySelector('.current-task-card') !== null)
console.log('Leaderboard loaded:', document.querySelector('.leaderboard-section') !== null)
```

### Check State Management
```javascript
// In Vue DevTools
$vm0.$store.state.gamification.dashboardData
$vm0.$store.state.gamification.loading
```

---

## Common Issues & Solutions

### Issue 1: Celebration not showing
**Symptoms:** Task completes but no confetti
**Solution:** 
- Check browser console for errors
- Verify `canvas-confetti` is installed: `npm list canvas-confetti`
- Check that `showCelebration` is set to true in dashboard.vue

### Issue 2: Next task not updating
**Symptoms:** Same task shows after completion
**Solution:**
- Check API response has `next_task` field
- Verify `loadDashboardGamification()` is called after task completion
- Check for JavaScript errors in console

### Issue 3: Points not updating
**Symptoms:** Task completes but points stay the same
**Solution:**
- Check backend logs for errors in `CompleteTaskView`
- Verify user has vendor profile
- Check `SupplierEngagement` model is created

### Issue 4: Milestone not turning green
**Symptoms:** Task completed but milestone still shows incomplete
**Solution:**
- Check milestone completion criteria in `get_overall_progress()`
- Verify score thresholds are met (70% for profile/mini website)
- Refresh dashboard data

---

## Performance Testing

### Measure Dashboard Load Time
```javascript
performance.mark('dashboard-start')
// ... after dashboard loads
performance.mark('dashboard-end')
performance.measure('dashboard-load', 'dashboard-start', 'dashboard-end')
console.log(performance.getEntriesByName('dashboard-load')[0].duration)
```

**Target:** < 2000ms on 3G connection

### Check API Calls
1. Open Network tab in DevTools
2. Refresh dashboard
3. **Expected calls:**
   - 1x `GET /api/gamification/dashboard/`
   - 1x `GET /api/gamification/leaderboard/`
   - NO multiple separate calls for scores/badges/engagement

---

## Accessibility Testing

### Keyboard Navigation
- ✅ Tab key navigates through all interactive elements
- ✅ Enter key activates buttons
- ✅ Tooltips show on focus

### Screen Reader
- ✅ StatusCard announces completion percentage
- ✅ CurrentTaskCard announces task title and description
- ✅ Buttons have descriptive labels
- ✅ Progress indicators have aria-labels

### Color Contrast
- ✅ Text meets WCAG AA standards (4.5:1 ratio)
- ✅ Tier colors are distinguishable
- ✅ Works in high contrast mode

---

## Regression Testing

### Legacy Features Still Working
- ✅ Product management
- ✅ Order processing
- ✅ Chat functionality
- ✅ Customer pool
- ✅ Reviews display
- ✅ Profile editing

### API Backward Compatibility
- ✅ Old `/api/gamification/score/` still works
- ✅ Old `/api/gamification/engagement/` still works
- ✅ Old `/api/gamification/badges/` still works

---

## Load Testing (Optional)

### Simulate Multiple Users
```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test dashboard endpoint
ab -n 100 -c 10 -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/gamification/dashboard/
```

**Target:** 
- < 200ms average response time
- < 500ms 95th percentile
- 0% error rate

---

## Final Checklist

Before marking as "Ready for Production":

- [ ] All scenarios pass (1-7)
- [ ] API tests return expected data
- [ ] No console errors
- [ ] Mobile layout works correctly
- [ ] Celebration triggers properly
- [ ] Points are awarded correctly
- [ ] Task sequencing is logical
- [ ] Leaderboard updates
- [ ] Backward compatibility maintained
- [ ] Performance targets met
- [ ] Accessibility standards met
- [ ] Documentation is complete

---

## Need Help?

### Check Logs
**Backend:**
```bash
tail -f multivendor_platform/multivendor_platform/debug.log
```

**Frontend:**
Browser DevTools → Console

### Contact Points
- Backend issues: Check `gamification/views.py` and `gamification/services.py`
- Frontend issues: Check `pages/seller/dashboard.vue` and `stores/gamification.ts`
- API issues: Check `gamification/urls.py` and `gamification/serializers.py`

---

**Last Updated:** December 11, 2025
**Version:** 1.0
**Status:** Ready for Testing ✅

