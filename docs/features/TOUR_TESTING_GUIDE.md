# 🧪 Onboarding Tour Testing Guide

## Quick Start Testing

### Step 1: Reset Tour State
First, clear your localStorage to simulate a first-time user:

**Option A - Via Browser Console:**
```javascript
localStorage.removeItem('supplier_tour_completed')
localStorage.removeItem('supplier_tour_dismissed')
localStorage.removeItem('supplier_tour_progress')
```

**Option B - Via Browser DevTools:**
1. Press `F12` to open DevTools
2. Go to **Application** tab
3. Click **Local Storage** → Your site URL
4. Delete these keys:
   - `supplier_tour_completed`
   - `supplier_tour_dismissed`
   - `supplier_tour_progress`

### Step 2: Navigate to Dashboard
```
http://localhost:3000/seller/dashboard
```

### Step 3: Expected Behavior

#### ✅ First Visit Experience
1. **Wait 1 second** after page loads
2. **Welcome dialog appears** with:
   - Large title: "خوش آمدید!"
   - Description of what the tour covers
   - Three options at bottom:
     - Blue button: "شروع راهنما" (Start Guide)
     - Gray text button: "دیگر نشان نده" (Don't show again)

3. **Click "شروع راهنما"**
4. **Tour starts** - You'll see:
   - A spotlight/highlight on the first element
   - A popover with title and description in Persian
   - Progress indicator at top (e.g., "1 از 20")
   - Navigation buttons:
     - "بعدی ←" (Next)
     - "→ قبلی" (Previous) 
     - X button to close

## How the Tour Works (Non-Interactive Mode)

The tour is **guide-along style**, not blocking:

### What This Means:
- ✅ Tour highlights elements one by one
- ✅ Shows instructions for each step
- ✅ You can read and follow along
- ✅ Click "Next" to move to next step
- ✅ You can click the actual UI elements while tour is running
- ✅ Tour doesn't wait for you to complete actions
- ✅ You can close tour anytime (progress is saved)

### Example Flow:
```
Step 1: Tour highlights "Products Tab"
        Instructions: "اینجا محصولاتی که می‌فروشید را اضافه کنید"
        You: Read it, click "Next" when ready

Step 2: Tour highlights "Add Product Button"  
        Instructions: "روی این دکمه کلیک کنید تا محصول اول خود را اضافه کنیم"
        You: Can click the button OR just click "Next" in tour

Step 3: Tour shows Product Form fields
        Instructions: "نام محصول را بنویسید..."
        You: Can fill the form OR just click "Next" to continue tour
```

## Testing All 20 Steps

### Tour Flow Checklist:

1. **Welcome** ✓
   - Popover appears with welcome message
   - No specific element highlighted

2. **Products Tab** ✓
   - Highlights the "محصولات" tab
   - Instructions in Persian

3. **Add Product Button** ✓
   - Highlights the "+ افزودن محصول جدید" button
   - Can be in header or empty state

4. **Product Name Input** ✓
   - Opens product form (you may need to click add button)
   - Highlights name field
   - Shows example: "مبل راحتی سه نفره"

5. **Product Description** ✓
   - Highlights TipTap editor
   - Explains importance of description

6. **Product Price** ✓
   - Highlights price input field
   - Shows example: "۲۰۰۰۰۰۰"

7. **Product Category** ✓
   - Highlights category dropdown
   - Instructions to select appropriate category

8. **Save Product Button** ✓
   - Highlights the save button
   - Explains to click save

9. **Success Message** ✓
   - Shows congratulations
   - No specific element highlighted

10. **Mini Website Tab** ✓
    - Highlights "وب‌سایت مینی" tab
    - Explains it's like store front

11. **Settings Section** ✓
    - Highlights "تنظیمات" sub-tab in miniwebsite
    - Explains where to enter store info

12. **Store Name Input** ✓
    - Opens settings (you may need to click)
    - Highlights store name field

13. **Store Description** ✓
    - Highlights description textarea
    - Shows examples

14. **Settings Save Button** ✓
    - Highlights save button in settings

15. **Portfolio Section** ✓
    - Highlights "نمونه کارها" sub-tab
    - Explains portfolio purpose

16. **Add Portfolio Button** ✓
    - Highlights "+ افزودن نمونه کار" button

17. **Team Section** ✓
    - Highlights "تیم" sub-tab
    - Explains team introduction

18. **Add Team Button** ✓
    - Highlights "+ افزودن عضو تیم" button

19. **Completion** ✓
    - Final congratulations message
    - "متوجه شدم" button to finish

## Testing Navigation

### Forward Navigation:
1. Click "بعدی ←" (Next) button
2. **Expected**: Tour moves to next step
3. **Check**: Progress counter increases (1→2→3...)

### Backward Navigation:
1. Click "→ قبلی" (Previous) button  
2. **Expected**: Tour goes back one step
3. **Check**: Progress counter decreases

### Close Tour:
1. Click X button (top-right of popover)
2. **Expected**: 
   - Tour closes immediately
   - Progress is saved in localStorage
   - Help button (?) remains visible

### Resume Tour:
1. After closing tour midway
2. Refresh page
3. Click floating help button (?)
4. **Expected**: Tour resumes from where you left off

## Testing Completion

### Complete Full Tour:
1. Go through all 20 steps
2. On last step, click "متوجه شدم"
3. **Expected**:
   - Modal closes
   - Green snackbar shows: "راهنما با موفقیت تکمیل شد!"
   - localStorage has `supplier_tour_completed: "true"`
   - Welcome dialog won't show on next visit
   - Help button still available to restart tour

### Test "Don't Show Again":
1. Reset localStorage
2. Navigate to dashboard
3. In welcome dialog, click "دیگر نشان نده"
4. Confirm the dialog
5. **Expected**:
   - Dialog closes
   - localStorage has `supplier_tour_dismissed: "true"`
   - Dialog won't appear on page refresh
   - Tour still accessible via help button (?)

## Testing Help Button

### Location:
- Fixed position at **bottom-left** corner
- Blue circular button with "?" icon
- Should be visible at all times

### Test Help Button:
1. Complete or dismiss tour
2. Look for floating "?" button (bottom-left)
3. Hover over it - tooltip shows "راهنمای استفاده"
4. Click it
5. **Expected**: Tour restarts from beginning

## Testing Mobile Responsiveness

### Test on Mobile (or resize browser):
1. Resize browser to mobile width (< 600px)
2. Start tour
3. **Check**:
   - Popover fits on screen
   - Text is readable (18-24px)
   - Buttons are touch-friendly
   - Help button positioned correctly
   - No horizontal scroll

## Testing RTL Layout

### Verify RTL:
1. Start tour
2. **Check**:
   - Text aligns to right
   - Progress indicator on right side
   - "بعدی ←" shows left arrow (moves forward)
   - "→ قبلی" shows right arrow (moves back)
   - Popover appears on appropriate side of element

## Common Issues & Solutions

### Issue: Welcome Dialog Doesn't Appear
**Solution**:
- Check localStorage is cleared
- Wait 1 full second after page load
- Check console for JavaScript errors
- Verify you're on `/seller/dashboard` as a seller user

### Issue: Tour Elements Not Highlighting
**Solution**:
- Elements might not be rendered yet
- Try clicking tabs manually first
- Check that data-tour attributes exist:
  ```bash
  # Check in browser console:
  document.querySelectorAll('[data-tour]').length
  # Should return > 0
  ```

### Issue: Tour Skips Steps
**Solution**:
- Some steps require elements that only appear after actions
- This is normal - tour shows steps in sequence
- Users follow along manually

### Issue: Modal Won't Close
**Solution**:
- Should be fixed with latest updates
- Try ESC key
- Check console for errors
- Clear cache and reload

## Browser Console Testing

### Check Tour State:
```javascript
// Is tour completed?
localStorage.getItem('supplier_tour_completed')

// Is tour dismissed?
localStorage.getItem('supplier_tour_dismissed')

// Current progress (step number)
localStorage.getItem('supplier_tour_progress')

// Check all tour elements
document.querySelectorAll('[data-tour]').length
// Should return 21

// List all tour IDs
Array.from(document.querySelectorAll('[data-tour]')).map(el => el.getAttribute('data-tour'))
```

### Manually Trigger Tour:
```javascript
// In browser console, if tour composable is available
const { startTour, resetTour } = useSupplierOnboarding()

// Reset and start fresh
resetTour()
startTour()
```

## Performance Testing

### Load Time:
- Tour should load with page (no delay)
- Welcome dialog appears after 1 second
- No impact on page performance

### Memory:
- Check browser memory before/after tour
- Should be < 1MB additional memory
- No memory leaks after closing

## Accessibility Testing

### Keyboard Navigation:
1. Start tour
2. Press `Tab` key
3. **Expected**: Can focus on Next/Previous/Close buttons
4. Press `Enter` on focused button
5. **Expected**: Button action executes

### Screen Reader:
1. Enable screen reader (NVDA/JAWS/VoiceOver)
2. Start tour
3. **Expected**: 
   - Tour title is announced
   - Description is announced
   - Button labels are announced

## Production Readiness Checklist

Before deploying to production:

- [ ] Welcome dialog appears on first visit
- [ ] All 20 steps work in sequence
- [ ] Navigation (Next/Previous) works
- [ ] Close button closes tour
- [ ] "متوجه شدم" button closes tour
- [ ] Progress is saved between sessions
- [ ] "Don't show again" works permanently
- [ ] Help button (?) triggers tour
- [ ] Mobile layout is responsive
- [ ] RTL layout displays correctly
- [ ] Persian text displays properly
- [ ] No console errors
- [ ] No memory leaks
- [ ] Works in Chrome, Firefox, Safari, Edge

## Quick Test Script

Run this in your browser console after navigating to dashboard:

```javascript
// Reset tour
localStorage.removeItem('supplier_tour_completed')
localStorage.removeItem('supplier_tour_dismissed')
localStorage.removeItem('supplier_tour_progress')

// Reload page
location.reload()

// After reload, wait for welcome dialog (1 second)
// Then manually test:
// 1. Click "شروع راهنما"
// 2. Navigate through a few steps
// 3. Close with X button
// 4. Click help button (?) to resume
// 5. Complete full tour
```

## Expected Results Summary

✅ **First visit**: Welcome dialog appears automatically  
✅ **Tour flow**: All 20 steps highlight correctly  
✅ **Navigation**: Next/Previous buttons work  
✅ **Closing**: X button and done button close tour  
✅ **Progress**: Saved between sessions  
✅ **Help button**: Always accessible for manual trigger  
✅ **Mobile**: Responsive and touch-friendly  
✅ **RTL**: Proper right-to-left layout  
✅ **Persian**: All text displays correctly  

## Need Help?

If tour isn't working:
1. Check browser console for errors
2. Verify localStorage is clear
3. Ensure you're logged in as a seller
4. Try in incognito/private window
5. Check that npm packages are installed: `npm install`
6. Restart dev server: `npm run dev`

---

**Testing Date**: November 21, 2025  
**Tour Version**: 1.0.0  
**Status**: Ready for Testing ✅

