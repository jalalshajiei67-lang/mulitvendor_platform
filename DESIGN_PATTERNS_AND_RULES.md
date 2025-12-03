# Design Patterns & Design Rules

This document outlines the design patterns, component structure, styling conventions, and design rules used throughout the multivendor platform.

---

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [Color System](#color-system)
3. [Typography](#typography)
4. [Spacing & Layout](#spacing--layout)
5. [Component Patterns](#component-patterns)
6. [RTL Support](#rtl-support)
7. [Responsive Design](#responsive-design)
8. [Animation & Transitions](#animation--transitions)
9. [Accessibility](#accessibility)
10. [Vuetify Configuration](#vuetify-configuration)

---

## Design Philosophy

### Core Principles

1. **Mobile-First Design**
   - All components and layouts must be designed for mobile devices first
   - Desktop enhancements are added through progressive enhancement
   - Touch-friendly interactions (minimum 44x44px touch targets)

2. **RTL (Right-to-Left) Support**
   - All layouts must support RTL direction
   - All text and UX copy must be in Persian
   - Icons and navigation elements must mirror appropriately

3. **Material Design 3**
   - Using Vuetify 3 as the UI framework
   - Following Material Design 3 principles
   - Consistent elevation, rounded corners, and spacing

4. **Readability & Content-First**
   - Medium.com-inspired typography for content areas
   - Generous spacing and line-height for readability
   - Clear visual hierarchy

---

## Color System

### Primary Color Palette

**Light Theme:**
```css
primary: '#4CAF50'           /* Green - Primary brand color */
secondary: '#388E3C'         /* Dark Green */
accent: '#69F0AE'            /* Light Green Accent */
error: '#D32F2F'             /* Red */
info: '#0277BD'              /* Info Blue */
success: '#2E7D32'           /* Green */
warning: '#F57C00'           /* Orange/Amber */
background: '#FFFFFF'        /* White */
surface: '#FFFFFF'           /* White */
```

**Dark Theme:**
```css
primary: '#81C784'           /* Lighter Green for dark theme */
secondary: '#A5D6A7'         /* Light Green */
accent: '#B9F6CA'            /* Very Light Green */
background: '#121212'        /* Dark Background */
surface: '#1E1E1E'           /* Dark Surface */
```

### Green Color Variants

The theme includes comprehensive green variants:
- `green-lighten-5` through `green-lighten-1`
- `green-darken-1` through `green-darken-4`
- `green-accent-1` through `green-accent-4`

### Color Usage Guidelines

- **Primary**: Main actions, links, brand elements
- **Secondary**: Supporting actions, category chips
- **Accent**: Featured items, highlights
- **Error**: Error messages, destructive actions
- **Success**: Success messages, positive indicators
- **Warning**: Warning messages, caution states

### Semantic Colors

Always use Vuetify theme variables for colors:
```vue
<!-- Good -->
<v-btn color="primary">Button</v-btn>
<div :style="{ color: 'rgb(var(--v-theme-primary))' }">

<!-- Bad -->
<div style="color: #4CAF50">
```

---

## Typography

### Font Family

**Primary Font Stack:**
```css
font-family: 'Vazirmatn', 'IRANSans', 'Segoe UI', Tahoma, Arial, -apple-system, sans-serif;
```

### Font Sizes

**Responsive Font Sizes:**
```css
/* Mobile (< 600px) */
font-size: 14px;

/* Tablet (600px - 960px) */
font-size: 15px;

/* Desktop (≥ 960px) */
font-size: 16px;
```

### Typography Scale (Vuetify)

- `text-h1` - 6rem (96px) - Page titles
- `text-h2` - 3.75rem (60px) - Section titles
- `text-h3` - 3rem (48px) - Subsection titles
- `text-h4` - 2.125rem (34px) - Card titles
- `text-h5` - 1.5rem (24px) - Small headings
- `text-h6` - 1.25rem (20px) - Product card titles
- `text-subtitle-1` - 1rem (16px) - Subtitles
- `text-subtitle-2` - 0.875rem (14px) - Small subtitles
- `text-body-1` - 1rem (16px) - Body text
- `text-body-2` - 0.875rem (14px) - Small body text
- `text-caption` - 0.75rem (12px) - Captions, metadata

### Content Typography (Medium.com-inspired)

For content areas (product descriptions, blog posts):

```css
/* Headings */
h1 {
  font-size: 2.5rem;
  margin-top: 3rem;
  margin-bottom: 1.5rem;
  line-height: 1.3;
  font-weight: 700;
}

h2 {
  font-size: 2rem;
  margin-top: 2.5rem;
  margin-bottom: 1.25rem;
  line-height: 1.3;
  font-weight: 700;
}

h3 {
  font-size: 1.75rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
  line-height: 1.3;
  font-weight: 700;
}

/* Paragraphs */
p {
  line-height: 1.8;
  margin-bottom: 1.75rem;
  color: rgba(var(--v-theme-on-surface), 0.87);
  font-size: 1.05rem;
  text-align: justify;
  max-width: 65ch;
}

/* First paragraph after heading */
h1 + p, h2 + p, h3 + p {
  margin-top: 0.5rem;
}
```

### Text Colors

```css
/* Primary text */
color: rgba(var(--v-theme-on-surface), 0.96);

/* Secondary text */
color: rgba(var(--v-theme-on-surface), 0.87);

/* Disabled/Muted text */
color: rgba(var(--v-theme-on-surface), 0.72);

/* Placeholder text */
color: rgba(var(--v-theme-on-surface), 0.56);
```

---

## Spacing & Layout

### Spacing Scale

Vuetify uses a 4px base spacing unit:
- `pa-1` = 4px padding all
- `pa-2` = 8px padding all
- `pa-3` = 12px padding all
- `pa-4` = 16px padding all
- `pa-5` = 20px padding all
- `pa-6` = 24px padding all
- `pa-8` = 32px padding all

### Container Spacing

**Mobile (< 960px):**
```css
padding-left: 16px;
padding-right: 16px;
```

**Tablet (960px - 1280px):**
```css
padding-left: 24px;
padding-right: 24px;
```

**Desktop (≥ 1280px):**
```css
max-width: 1400px - 1600px;
margin: 0 auto;
padding-left: 32px;
padding-right: 32px;
```

### Grid Spacing

**Product Grid:**
```css
/* Mobile/Tablet */
--v-gutter-x: 12px;
--v-gutter-y: 16px;

/* Desktop (≥ 960px) */
--v-gutter-x: 16px;
--v-gutter-y: 18px;

/* Large Desktop (≥ 1280px) */
--v-gutter-x: 18px;
--v-gutter-y: 20px;
```

### Layout Structure

**Standard Page Layout:**
```vue
<v-container class="py-3 py-sm-4 py-md-6">
  <v-row>
    <v-col cols="12" md="8">
      <!-- Main content -->
    </v-col>
    <v-col cols="12" md="4">
      <!-- Sidebar -->
    </v-col>
  </v-row>
</v-container>
```

---

## Component Patterns

### Component Organization

```
components/
├── admin/           # Admin-specific components
├── auth/            # Authentication components
├── blog/            # Blog-related components
├── chat/            # Chat components
├── common/          # Shared/common components
├── gamification/    # Gamification widgets
├── layout/          # Layout components (Header, Footer)
├── product/         # Product-related components
├── skeletons/       # Loading skeleton components
└── supplier/        # Supplier-related components
```

### Component Naming Conventions

- **PascalCase** for component names: `ProductCard.vue`
- **camelCase** for variables and functions: `productName`, `fetchProduct()`
- **kebab-case** for props: `:product-id`, `:vendor-name`

### Standard Component Structure

```vue
<template>
  <!-- Component template -->
</template>

<script setup lang="ts">
// Imports
import { ref, computed } from 'vue'

// Props
interface Props {
  productId: number
}

const props = defineProps<Props>()

// State
const loading = ref(false)

// Computed
const productName = computed(() => {
  // ...
})

// Methods
const fetchProduct = async () => {
  // ...
}
</script>

<style scoped>
/* Component-specific styles */
</style>
```

### Card Components

**Standard Card Pattern:**
```vue
<v-card elevation="2" rounded="xl" class="pa-6">
  <v-card-title class="text-h5 font-weight-bold mb-4">
    Card Title
  </v-card-title>
  <v-card-text>
    <!-- Card content -->
  </v-card-text>
</v-card>
```

**Card Defaults (Vuetify Config):**
- `elevation: 2` (default)
- `rounded: 'lg'` or `rounded: 'xl'` (extra-large for major cards)

### Button Components

**Button Defaults:**
```vue
<v-btn
  color="primary"
  size="large"
  rounded="lg"
  elevation="2"
>
  Button Text
</v-btn>
```

**Button Variants:**
- `variant="flat"` - Flat button (no elevation)
- `variant="outlined"` - Outlined button
- `variant="tonal"` - Tonal button
- `variant="text"` - Text button

### Form Components

**Standard Form Fields:**
```vue
<v-text-field
  v-model="field"
  label="Label"
  variant="outlined"
  density="comfortable"
  :rules="[rules.required]"
/>

<v-select
  v-model="selection"
  :items="options"
  variant="outlined"
  density="comfortable"
/>
```

**Form Field Defaults:**
- `variant: 'outlined'`
- `density: 'comfortable'`

### Loading States

**Skeleton Loaders:**
Use skeleton components while loading:
```vue
<ProductCardSkeleton v-if="loading" />
<ProductCard v-else :product="product" />
```

**Available Skeletons:**
- `ProductCardSkeleton`
- `ProductDetailSkeleton`
- `BlogCardSkeleton`
- `BlogDetailSkeleton`
- `SupplierCardSkeleton`
- `SupplierDetailSkeleton`
- `ListSkeleton`

---

## RTL Support

### Global RTL Configuration

**HTML Direction:**
```css
html {
  direction: rtl;
  text-align: right;
}

body {
  direction: rtl;
  text-align: right;
}
```

**Vuetify RTL:**
```typescript
rtl: true,  // Enabled globally in Vuetify config
locale: {
  rtl: {
    fa: true
  }
}
```

### RTL Utility Classes

```css
/* Margin utilities */
.mr-auto {
  margin-right: 0 !important;
  margin-left: auto !important;
}

.ml-auto {
  margin-left: 0 !important;
  margin-right: auto !important;
}

/* Padding utilities */
.pr-auto {
  padding-right: 0 !important;
  padding-left: auto !important;
}

.pl-auto {
  padding-left: 0 !important;
  padding-right: auto !important;
}

/* Text alignment */
.text-right {
  text-align: right !important;
}

.text-left {
  text-align: left !important;
}

/* Flex direction */
.flex-row-reverse {
  flex-direction: row-reverse !important;
}
```

### RTL-Specific Adjustments

**List Items:**
```css
.v-list-item__prepend {
  margin-inline-start: 0;
  margin-inline-end: 16px;
}

.v-list-item__append {
  margin-inline-start: 16px;
  margin-inline-end: 0;
}
```

**Toolbar:**
```css
.v-toolbar .v-toolbar__content {
  flex-direction: row-reverse;
}
```

### Icons in RTL

Use appropriate icons that make sense in RTL context:
- Navigation: Use `mdi-chevron-left` for forward, `mdi-chevron-right` for back
- Breadcrumbs: Reverse arrow direction
- Carousels: Swap left/right navigation

---

## Responsive Design

### Breakpoints

Vuetify default breakpoints:
- `xs`: 0-599px (Mobile)
- `sm`: 600-959px (Tablet Portrait)
- `md`: 960-1279px (Tablet Landscape)
- `lg`: 1280-1919px (Desktop)
- `xl`: 1920px+ (Large Desktop)

### Mobile-First Approach

Always design for mobile first, then enhance for larger screens:

```vue
<!-- Mobile-first: 12 columns on mobile -->
<v-col cols="12" md="6" lg="4">
  <!-- Content -->
</v-col>
```

### Responsive Utilities

**Display Utilities:**
```vue
<template>
  <div v-if="mdAndUp">Desktop only</div>
  <div v-if="smAndDown">Mobile/Tablet only</div>
</template>

<script setup>
import { useDisplay } from 'vuetify'

const { mdAndUp, smAndDown } = useDisplay()
</script>
```

**Spacing Utilities:**
```vue
<!-- Responsive padding -->
<div class="pa-2 pa-sm-4 pa-md-6">
  <!-- 8px on mobile, 16px on tablet, 24px on desktop -->
</div>

<!-- Responsive margins -->
<div class="ma-2 ma-md-4">
  <!-- 8px margin on mobile, 16px on desktop -->
</div>
```

### Container Responsive Patterns

```vue
<v-container
  class="py-3 py-sm-4 py-md-6"
  :class="{
    'px-4': true,
    'px-sm-6': true,
    'px-md-8': true
  }"
>
  <!-- Content -->
</v-container>
```

### Responsive Grid Patterns

**Product Grid:**
```vue
<v-row>
  <v-col
    v-for="product in products"
    :key="product.id"
    cols="12"
    sm="6"
    md="4"
    lg="3"
  >
    <ProductCard :product="product" />
  </v-col>
</v-row>
```

---

## Animation & Transitions

### Standard Transitions

**Fade Transition:**
```css
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.fade-in {
  animation: fadeIn 0.3s ease-in;
}
```

**Slide Fade Transition:**
```css
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s ease-in;
}

.slide-fade-enter-from {
  transform: translateY(-10px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
```

### Hover Effects

**Card Hover:**
```css
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
}

/* Reduced on mobile */
@media (max-width: 600px) {
  .card:hover {
    transform: translateY(-4px);
  }
}
```

**Link Hover:**
```css
a {
  transition: opacity 0.3s ease;
}

@media (hover: hover) {
  a:hover {
    opacity: 0.8;
  }
}
```

### Loading States

**Skeleton Animation:**
Vuetify's skeleton loader includes built-in shimmer animation.

**Loading Spinner:**
```vue
<v-progress-circular
  indeterminate
  color="primary"
  size="64"
/>
```

---

## Accessibility

### Semantic HTML

- Use semantic HTML elements (`<nav>`, `<main>`, `<article>`, `<section>`)
- Proper heading hierarchy (h1 → h2 → h3)
- Alt text for all images

### ARIA Labels

```vue
<v-btn
  :icon="icon"
  aria-label="Button description"
/>
```

### Keyboard Navigation

- All interactive elements must be keyboard accessible
- Focus indicators should be visible
- Tab order should follow visual order (RTL-aware)

### Color Contrast

- Ensure sufficient contrast ratios (WCAG AA minimum)
- Don't rely solely on color to convey information
- Use icons and text together

---

## Vuetify Configuration

### Default Component Props

**Cards:**
```typescript
VCard: {
  elevation: 2,
  rounded: 'lg',
}
```

**Buttons:**
```typescript
VBtn: {
  rounded: 'lg',
  elevation: 2,
}
```

**Form Fields:**
```typescript
VTextField: {
  variant: 'outlined',
  density: 'comfortable',
}

VSelect: {
  variant: 'outlined',
  density: 'comfortable',
}

VTextarea: {
  variant: 'outlined',
  density: 'comfortable',
}
```

**Chips:**
```typescript
VChip: {
  rounded: 'lg',
}
```

### Theme Variables

Access theme colors using CSS variables:
```css
/* Primary color */
color: rgb(var(--v-theme-primary));

/* Surface color with opacity */
background: rgba(var(--v-theme-surface), 0.95);

/* Text color with opacity */
color: rgba(var(--v-theme-on-surface), 0.87);
```

### Icons

- Default icon set: Material Design Icons (MDI)
- Icon size: Use Vuetify size props (`size="small"`, `size="large"`)
- Icon colors: Use Vuetify color system

---

## Persian/Localization

### Text Content

- **All UX copy must be in Persian**
- Use proper Persian typography (Vazirmatn/IRANSans fonts)
- Persian number formatting: Use `Intl.NumberFormat('fa-IR')`

### Date Formatting

Use Persian date picker component:
```vue
<PersianDatePicker v-model="date" />
```

### Number Formatting

```typescript
const formatPrice = (value: number | string) => {
  const amount = Number(value)
  if (Number.isNaN(amount)) {
    return value
  }
  return new Intl.NumberFormat('fa-IR').format(amount) + ' تومان'
}
```

### Direction

- All text should be right-aligned
- Icons and navigation should mirror appropriately
- Layouts should flow right-to-left

---

## Best Practices

### Code Organization

1. **Composition API**: Always use Composition API (`<script setup>`)
2. **TypeScript**: Use TypeScript for all components
3. **Pinia Stores**: Use Pinia for state management
4. **Composables**: Extract reusable logic to composables

### Performance

1. **Lazy Loading**: Use `Lazy` prefix for heavy components
   ```vue
   <LazyRFQForm v-if="showDialog" />
   ```

2. **Image Loading**: Always use `loading="lazy"` for images
   ```vue
   <v-img src="..." loading="lazy" />
   ```

3. **Code Splitting**: Use dynamic imports for large components

### Error Handling

```vue
<v-alert
  v-if="error"
  type="error"
  variant="tonal"
  prominent
>
  {{ error }}
</v-alert>
```

### Loading States

Always show loading states:
```vue
<ProductCardSkeleton v-if="loading" />
<ProductCard v-else :product="product" />
```

---

## Component Examples

### Product Card Pattern

```vue
<template>
  <v-card rounded="xl" elevation="2" class="product-card" hover>
    <v-img
      :src="product.primary_image"
      height="220"
      cover
      loading="lazy"
    />
    <v-card-text class="pa-5">
      <v-chip size="small" color="primary" variant="tonal" class="mb-3">
        {{ product.category_name }}
      </v-chip>
      <h3 class="text-h6 font-weight-bold mb-2">
        {{ product.name }}
      </h3>
      <p class="text-body-2 text-medium-emphasis mb-4">
        {{ product.short_description }}
      </p>
      <div class="text-h5 font-weight-bold">
        {{ formatPrice(product.price) }}
      </div>
    </v-card-text>
  </v-card>
</template>
```

### Page Layout Pattern

```vue
<template>
  <v-container class="py-3 py-sm-4 py-md-6">
    <!-- Breadcrumbs -->
    <v-breadcrumbs :items="breadcrumbs" class="pa-0 mb-4" />

    <!-- Page Title -->
    <h1 class="text-h3 text-md-h2 font-weight-bold mb-4">
      Page Title
    </h1>

    <!-- Content -->
    <v-row>
      <v-col cols="12" md="8">
        <!-- Main content -->
      </v-col>
      <v-col cols="12" md="4">
        <!-- Sidebar -->
      </v-col>
    </v-row>
  </v-container>
</template>
```

---

## File Locations

### Theme Configuration
- `multivendor_platform/front_end/nuxt/nuxt.config.ts` - Vuetify theme config

### Global Styles
- `multivendor_platform/front_end/nuxt/assets/css/base.css` - Base styles
- `multivendor_platform/front_end/nuxt/assets/css/main.css` - Main styles, RTL support

### Layout Components
- `multivendor_platform/front_end/nuxt/layouts/default.vue` - Default layout
- `multivendor_platform/front_end/nuxt/components/layout/` - Layout components

---

## References

- [Vuetify 3 Documentation](https://vuetifyjs.com/)
- [Material Design 3 Guidelines](https://m3.material.io/)
- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [Nuxt 3 Documentation](https://nuxt.com/docs)

---

**Last Updated:** 2025-01-27

