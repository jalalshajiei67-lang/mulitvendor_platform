# Store Modularization Migration Guide

## Overview
We've successfully modularized your Vue.js Pinia stores from one large `products.js` file into separate, focused modules.

## New Store Structure

```
src/stores/
├── index.js                 # Central exports
├── auth.js                  # Existing (unchanged)
├── blog.js                  # Existing (unchanged)
├── counter.js               # Existing (unchanged)
├── modules/
│   ├── departmentStore.js   # New - Department management
│   ├── categoryStore.js     # New - Category management
│   ├── subcategoryStore.js  # New - Subcategory management
│   ├── productStore.js      # New - Product management (refactored)
│   └── orderStore.js        # New - Order management
└── utils/
    └── translations.js      # Shared Persian translations
```

## How to Update Your Components

### 1. Update Import Statements

**Before:**
```javascript
import { useProductsStore } from '@/stores/products';
```

**After:**
```javascript
import { 
  useDepartmentStore, 
  useCategoryStore, 
  useSubcategoryStore, 
  useProductStore 
} from '@/stores';
```

### 2. Update Component Usage

**Before:**
```javascript
const productStore = useProductsStore();

// Accessing categories from product store
const categories = computed(() => productStore.categories);
await productStore.fetchCategories();
```

**After:**
```javascript
const departmentStore = useDepartmentStore();
const categoryStore = useCategoryStore();
const subcategoryStore = useSubcategoryStore();
const productStore = useProductStore();

// Accessing categories from dedicated category store
const categories = computed(() => categoryStore.categories);
await categoryStore.fetchCategories();
```

### 3. Cross-Store Communication

When you need data from multiple stores, you can use them together:

```javascript
// Example: Get products for a specific subcategory
const loadSubcategoryProducts = async (subcategoryId) => {
  await subcategoryStore.fetchSubcategory(subcategoryId);
  await productStore.fetchProducts({ subcategory: subcategoryId });
};

// Example: Get hierarchical data
const loadDepartmentData = async (departmentId) => {
  await departmentStore.fetchDepartment(departmentId);
  await categoryStore.fetchCategories({ department: departmentId });
  await subcategoryStore.fetchSubcategories({ department: departmentId });
};
```

### 4. Specific Updates for Your Components

#### DepartmentManagement.vue
```javascript
// Update imports
import { useDepartmentStore } from '@/stores';

// Update usage
const departmentStore = useDepartmentStore();
const departments = computed(() => departmentStore.departments);
const loading = computed(() => departmentStore.isLoading);
```

#### CategoryManagement.vue
```javascript
// Update imports
import { useCategoryStore } from '@/stores';

// Update usage
const categoryStore = useCategoryStore();
const categories = computed(() => categoryStore.categories);
```

#### SubcategoryManagement.vue
```javascript
// Update imports
import { useSubcategoryStore } from '@/stores';

// Update usage
const subcategoryStore = useSubcategoryStore();
const subcategories = computed(() => subcategoryStore.subcategories);
```

#### ProductList.vue / ProductDetail.vue
```javascript
// Update imports
import { useProductStore } from '@/stores';

// Update usage (mostly the same, but cleaner)
const productStore = useProductStore();
const products = computed(() => productStore.products);
```

### 5. Backward Compatibility

The old `products.js` file remains for backward compatibility. You can gradually migrate components one by one.

### 6. New Features Available

#### Subcategory Store Features
- `getSubcategoriesByCategory(categoryId)` - Get subcategories for a category
- `getSubcategoriesByDepartment(departmentId)` - Get subcategories for a department
- `getNewProductsBySubcategory(subcategoryId)` - For your most viewed subcategory page

#### Category Store Features
- `getCategoriesByDepartment(departmentId)` - Get categories for a department
- `getCategoryBySlug(slug)` - Find category by slug

#### Department Store Features
- `getDepartmentBySlug(slug)` - Find department by slug
- `activeDepartments` - Filter active departments only

### 7. Testing the Migration

1. **Start with one component** - Update `DepartmentManagement.vue` first
2. **Test thoroughly** - Ensure all functionality works as expected
3. **Gradually migrate** - Update other components one by one
4. **Remove old store** - Once all components are migrated, you can remove the old `products.js`

### 8. Future Extensibility

The new structure makes it easy to add new modules:
- `reviewStore.js` - For product reviews
- `cartStore.js` - For shopping cart
- `wishlistStore.js` - For wishlist functionality
- `analyticsStore.js` - For store analytics

## Quick Start Example

Here's a complete example of how to use the new stores in a component:

```javascript
<template>
  <div>
    <div v-if="departmentStore.isLoading">{{ $t('loading') }}</div>
    <div v-else>
      <div v-for="dept in departmentStore.activeDepartments" :key="dept.id">
        <h3>{{ dept.name }}</h3>
        <button @click="loadDepartmentData(dept.id)">
          {{ $t('viewCategories') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useDepartmentStore, useCategoryStore } from '@/stores';

const departmentStore = useDepartmentStore();
const categoryStore = useCategoryStore();

const activeDepartments = computed(() => departmentStore.activeDepartments);

const loadDepartmentData = async (departmentId) => {
  await categoryStore.fetchCategories({ department: departmentId });
};

onMounted(() => {
  departmentStore.fetchDepartments();
});
</script>
```

## Need Help?

If you encounter any issues during migration:
1. Check the browser console for errors
2. Verify all imports are correct
3. Ensure API endpoints match the new store structure
4. Test each component individually before moving to the next
