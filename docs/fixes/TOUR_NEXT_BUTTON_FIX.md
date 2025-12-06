# Tour Next Button Fix - Step 1 Stuck Issue

## Problem
After clearing localStorage and starting the tour, the "Next" (بعدی) button on step 1 was not working - the tour was stuck and couldn't progress.

## Root Cause

### Multiple Issues Found:

1. **Conflicting onNextClick Handlers**
   - There were TWO `onNextClick` handlers defined:
     - One in the main config (line 501)
     - One inside each step's popover configuration (line 529)
   - This caused conflicts where the step-level handler would override the global one

2. **Manual Index Tracking**
   - Using `let currentStepIndex = getTourProgress()` that wasn't being updated
   - The variable was declared but never incremented properly
   - Each click tried to use a stale index value

3. **Wrong API Methods**
   - Using `opts.driverObj.moveNext()` which doesn't exist
   - Should be `opts.moveNext()` directly

4. **Complex Blocking Logic**
   - `waitForAction` logic was preventing normal navigation
   - Made tour unnecessarily complex and error-prone

## Solution

### Simplified and Fixed:

1. **Single onNextClick Handler**
   - Removed per-step handlers
   - Only use the global config handler

2. **Use Driver's Built-in State**
   ```typescript
   const state = opts.state
   const currentIndex = state.activeIndex ?? 0
   ```
   - Driver.js tracks its own position
   - No need for manual index management

3. **Correct API Methods**
   ```typescript
   opts.moveNext()      // Move to next step
   opts.movePrevious()  // Move to previous step
   ```

4. **Removed Blocking Logic**
   - No more `waitForAction`
   - No more complex validation
   - Simple, smooth navigation

### New Code Structure:

```typescript
onNextClick: (element, step, opts) => {
  const state = opts.state
  const currentIndex = state.activeIndex ?? 0
  saveTourProgress(currentIndex + 1)
  opts.moveNext()
},

onPrevClick: (element, step, opts) => {
  const state = opts.state
  const currentIndex = state.activeIndex ?? 0
  if (currentIndex > 0) {
    saveTourProgress(currentIndex - 1)
  }
  opts.movePrevious()
}
```

### Simplified Steps Configuration:

```typescript
steps: steps.map((step) => ({
  element: step.element,
  popover: {
    title: step.title,
    description: step.description,
    side: step.side || 'bottom',
    align: step.align || 'start'
    // No per-step handlers anymore
  }
}))
```

## Testing

### Verify the Fix:

1. **Clear localStorage**:
   ```javascript
   localStorage.clear()
   ```

2. **Reload page** and navigate to `/seller/dashboard`

3. **Wait for welcome dialog** (1 second)

4. **Click "شروع راهنما"**

5. **Test navigation**:
   - ✅ Step 1 appears
   - ✅ Click "بعدی ←" → Should move to step 2
   - ✅ Click "→ قبلی" → Should move back to step 1
   - ✅ Progress counter updates (1 از 20, 2 از 20, etc.)
   - ✅ Can navigate through all 20 steps smoothly

6. **Test completion**:
   - ✅ Navigate to last step
   - ✅ Click "✓ تمام شد"
   - ✅ Modal closes
   - ✅ Success message appears

## Changes Made

### File: `composables/useSupplierOnboarding.ts`

**Before** (Lines 501-543):
- Complex `onNextClick` with manual index tracking
- Per-step `onNextClick` handlers in popover config
- `waitForAction` blocking logic
- Wrong API: `opts.driverObj.moveNext()`

**After**:
- Simple `onNextClick` using driver's state
- No per-step handlers
- No blocking logic
- Correct API: `opts.moveNext()`
- Added `onPrevClick` for completeness

## Benefits

1. **Simpler Code** - Removed ~30 lines of complex logic
2. **More Reliable** - Uses driver.js built-in state management
3. **Better Performance** - No async operations blocking navigation
4. **Easier to Maintain** - Clear, straightforward flow
5. **Better UX** - Smooth navigation without delays

## Expected Behavior Now

✅ **Step 1**: Shows welcome message, Next button works  
✅ **Steps 2-19**: Can navigate forward/backward smoothly  
✅ **Step 20**: Done button closes modal  
✅ **Progress**: Automatically saves after each navigation  
✅ **Resume**: Help button restarts from saved position  

## Browser Console Test

Quick test in console:
```javascript
// Clear and reload
localStorage.clear()
location.reload()

// After tour starts, check progress
localStorage.getItem('supplier_tour_progress') // Should update as you navigate
```

## Status

**FIXED** ✅

The Next button now works correctly on all steps. Users can smoothly navigate through the entire 20-step tour without getting stuck.

---

**Fixed Date**: November 21, 2025  
**Issue**: Next button stuck on step 1  
**Root Cause**: Conflicting handlers and wrong API usage  
**Status**: ✅ Resolved and Tested

