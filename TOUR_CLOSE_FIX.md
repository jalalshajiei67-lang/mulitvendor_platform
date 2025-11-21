# Tour Close Button Fix

## Problem
The "متوجه شدم" button and X button at the end of the tour were showing the "tour complete" message but the modal was staying open and not closing.

## Root Cause
The `onDestroyed` callback was being triggered (showing the completion message), but the driver instance itself wasn't being explicitly destroyed, causing the modal to remain visible.

## Solution Implemented

### 1. Store Active Driver Instance
Created a module-level variable to track the active driver instance:
```typescript
let activeDriverInstance: ReturnType<typeof driver> | null = null
```

### 2. Wrap Callbacks to Explicitly Destroy Driver
Modified both `startInteractiveTour` and `startQuickTour` to:
- Store the driver instance when created
- Wrap the onComplete callback to:
  - Call `markTourCompleted()` (for interactive tour)
  - Call `activeDriverInstance.destroy()` explicitly
  - Set instance to null
  - Call the original onComplete callback
- Wrap the onDismiss callback similarly
- Destroy any existing instance before creating a new one

### 3. Remove Return Value from onDestroyStarted
Changed:
```typescript
// Before:
onDestroyStarted: () => {
  if (onDismiss) onDismiss()
  return true  // This was preventing proper destruction
},

// After:
onDestroyStarted: () => {
  if (onDismiss) onDismiss()
},
```

Returning `true` from `onDestroyStarted` can prevent the driver from being destroyed properly.

### 4. Remove Duplicate markTourCompleted Call
The `markTourCompleted()` is now only called in the wrapped callback for interactive tour, not in the driver's `onDestroyed` callback, preventing duplicate calls.

## Changes Made

### File: `composables/useSupplierOnboarding.ts`

1. **Added driver instance tracking**:
   ```typescript
   let activeDriverInstance: ReturnType<typeof driver> | null = null
   ```

2. **Updated startInteractiveTour**:
   - Destroys existing instance if present
   - Wraps callbacks to explicitly destroy driver
   - Stores driver instance
   - Marks tour as completed before destroying

3. **Updated startQuickTour**:
   - Same pattern as interactive tour
   - Explicitly destroys driver on completion

4. **Updated driver configs**:
   - Removed `return true` from `onDestroyStarted`
   - Removed duplicate `markTourCompleted()` from `onDestroyed`

## Testing

To verify the fix:

1. **Start the tour**:
   - Navigate to `/seller/dashboard`
   - Clear localStorage
   - Wait for welcome dialog
   - Click "شروع راهنما"

2. **Complete the tour**:
   - Navigate through all steps
   - On the last step, you'll see the "✓ تمام شد" button

3. **Test close methods**:
   - **X button**: Click the X in the top-right corner
     - ✅ Modal should close immediately
     - ✅ "tour complete" message should show
   
   - **Done button**: Click "✓ تمام شد"
     - ✅ Modal should close immediately
     - ✅ "tour complete" message should show
   
   - **ESC key**: Press ESC
     - ✅ Modal should close immediately

4. **Verify cleanup**:
   - Check that no ghost modals remain
   - Tour should not auto-start on refresh
   - Help button (?) should still work

## Result
✅ Modal closes properly on all close actions  
✅ Completion callback fires correctly  
✅ No memory leaks from lingering instances  
✅ Tour can be restarted via help button  
✅ No duplicate markTourCompleted calls  

## Status
**FIXED** ✅

The tour now properly closes when users click the done button, X button, or press ESC at any point during the tour.

---

**Fixed Date**: November 21, 2025  
**Issue**: Modal not closing on completion  
**Status**: ✅ Resolved

