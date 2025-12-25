# Scroll to Plan Implementation

## Overview

Added smooth scroll functionality to the Plans Overview stat cards. When users click on any of the three plan cards at the top, the page smoothly scrolls to the corresponding plan card below.

## Implementation Details

### 1. **Template Changes**

Added click handlers to each stat card:

```html
<div class="plan-stat-card free-stat" @click="scrollToPlan('free')">
  <div class="plan-stat-card premium-stat" @click="scrollToPlan('premium')">
    <div
      class="plan-stat-card commission-stat"
      @click="scrollToPlan('commission')"
    ></div>
  </div>
</div>
```

### 2. **Plan Card Refs**

Added template refs to each plan card for reference:

```html
<div ref="freePlanRef" class="plan-card free-plan">
  <div ref="premiumPlanRef" class="plan-card premium-plan featured">
    <div ref="commissionPlanRef" class="plan-card commission-plan"></div>
  </div>
</div>
```

### 3. **Script Implementation**

#### Refs Definition:

```typescript
const freePlanRef = ref<HTMLDivElement | null>(null);
const premiumPlanRef = ref<HTMLDivElement | null>(null);
const commissionPlanRef = ref<HTMLDivElement | null>(null);
```

#### Scroll Function:

```typescript
function scrollToPlan(planType: PlanType) {
  let element: HTMLDivElement | null | undefined = null;

  if (planType === "free") {
    element = freePlanRef.value;
  } else if (planType === "premium") {
    element = premiumPlanRef.value;
  } else if (planType === "commission") {
    element = commissionPlanRef.value;
  }

  if (element) {
    element.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  }
}
```

## Features

✅ **Smooth Scrolling**: Uses `scrollIntoView()` with `behavior: 'smooth'`
✅ **Mobile Compatible**: Works on all device sizes
✅ **No Auto-Selection**: Clicking stat card only scrolls, doesn't select the plan
✅ **RTL Compatible**: Works perfectly with Persian/RTL layout
✅ **Visual Feedback**: Stat cards show cursor pointer and active states

## User Experience

1. User sees 3 plan stat cards at the top
2. User clicks on a stat card (e.g., "پلن پریمیوم")
3. Page smoothly scrolls to that plan's full card
4. Plan card is now in view for detailed inspection
5. No automatic selection - user can still choose other plans

## Browser Support

- Chrome 76+
- Firefox 36+
- Safari 15.4+
- Edge 76+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Scroll Behavior Options

Currently set to:

- `behavior: 'smooth'` - Smooth animation
- `block: 'start'` - Aligns to top of viewport

## Future Enhancements

1. Add scroll offset for better header spacing
2. Add visual animation/highlight when plan comes into view
3. Add "Back to Top" button in plans section
4. Integrate with URL hash (#free, #premium, #commission)
5. Add keyboard navigation support

## Testing Checklist

- [x] Click on "پلن رایگان" stat → scrolls to Free plan
- [x] Click on "پلن پریمیوم" stat → scrolls to Premium plan
- [x] Click on "پلن کمیسیونی" stat → scrolls to Commission plan
- [x] Works on mobile view
- [x] Works on tablet view
- [x] Works on desktop view
- [x] RTL layout correct
- [x] No plan is auto-selected after scroll
- [x] Smooth animation working
