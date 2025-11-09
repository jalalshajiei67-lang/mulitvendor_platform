// src/stores/index.js
// Central export for all stores

// Existing stores
export { useAuthStore } from './auth.js';
export { useBlogStore } from './blog.js';
export { useCounterStore } from './counter.js';

// New modular stores
export { useDepartmentStore } from './modules/departmentStore.js';
export { useCategoryStore } from './modules/categoryStore.js';
export { useSubcategoryStore } from './modules/subcategoryStore.js';
export { useProductStore } from './modules/productStore.js';
export { useOrderStore } from './modules/orderStore.js';

// Re-export the old product store for backward compatibility
// This can be removed once all components are updated
export { useProductStore as useProductsStore } from './modules/productStore.js';
