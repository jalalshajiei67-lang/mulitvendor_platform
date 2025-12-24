<template>
  <div class="global-search" ref="searchContainer">
    <div class="search-input-wrapper">
      <input
        type="text"
        v-model="searchQuery"
        @focus="isFocused = true"
        @keydown.escape="closeResults"
        @keydown.down.prevent="navigateResults('down')"
        @keydown.up.prevent="navigateResults('up')"
        @keydown.enter.prevent="handleEnterKey"
        placeholder="جستجو در محصولات و وبلاگ..."
        class="search-input"
      />
      <svg 
        class="search-icon" 
        @click="performFullSearch"
        xmlns="http://www.w3.org/2000/svg" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path 
          stroke-linecap="round" 
          stroke-linejoin="round" 
          stroke-width="2" 
          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" 
        />
      </svg>
      <button 
        v-if="searchQuery" 
        @click="clearSearch" 
        class="clear-button"
        aria-label="پاک کردن جستجو"
      >
        ×
      </button>
    </div>

    <!-- Autocomplete Dropdown -->
    <Transition name="dropdown">
      <div 
        v-if="showResults && (hasResults || isLoading)" 
        class="search-results"
      >
        <!-- Loading State -->
        <div v-if="isLoading" class="search-loading">
          <div class="spinner"></div>
          <span>در حال جستجو...</span>
        </div>

        <!-- No Results -->
        <div v-else-if="!hasResults" class="no-results">
          <p>نتیجه‌ای یافت نشد</p>
        </div>

        <!-- Results -->
        <div v-else class="results-container">
          <!-- Products -->
          <div v-if="results.products && results.products.length > 0" class="result-section">
            <h3 class="section-title">محصولات</h3>
            <NuxtLink
              v-for="(product, index) in results.products"
              :key="'product-' + product.id"
              :to="product.slug ? `/products/${product.slug}` : `/products/${product.id}`"
              @click="closeResults"
              class="result-item"
              :class="{ 'highlighted': highlightedIndex === getProductIndex(index) }"
              @mouseenter="highlightedIndex = getProductIndex(index)"
            >
              <div class="result-image">
                <img 
                  v-if="product.primary_image" 
                  :src="formatImageUrl(product.primary_image)" 
                  :alt="product.name"
                  loading="lazy"
                  @error="handleImageError"
                />
                <div v-else class="placeholder-image">
                  <span>تصویر</span>
                </div>
              </div>
              <div class="result-content">
                <div class="result-title">{{ product.name }}</div>
                <div class="result-meta">
                  <span class="badge badge-product">محصول</span>
                  <span class="result-price">{{ formatPrice(product.price) }} تومان</span>
                </div>
              </div>
            </NuxtLink>
          </div>

          <!-- Blogs -->
          <div v-if="results.blogs && results.blogs.length > 0" class="result-section">
            <h3 class="section-title">وبلاگ</h3>
            <NuxtLink
              v-for="(blog, index) in results.blogs"
              :key="'blog-' + blog.id"
              :to="`/blog/${blog.slug}`"
              @click="closeResults"
              class="result-item"
              :class="{ 'highlighted': highlightedIndex === getBlogIndex(index) }"
              @mouseenter="highlightedIndex = getBlogIndex(index)"
            >
              <div class="result-image">
                <img 
                  v-if="blog.featured_image" 
                  :src="blog.featured_image" 
                  :alt="blog.title"
                />
                <div v-else class="placeholder-image">
                  <span>تصویر</span>
                </div>
              </div>
              <div class="result-content">
                <div class="result-title">{{ blog.title }}</div>
                <div class="result-meta">
                  <span class="badge badge-blog">وبلاگ</span>
                  <span class="result-excerpt">{{ truncate(blog.excerpt, 60) }}</span>
                </div>
              </div>
            </NuxtLink>
          </div>

          <!-- View All Results Link -->
          <div v-if="results.total > totalDisplayed" class="view-all">
            <span>{{ results.total - totalDisplayed }} نتیجه دیگر...</span>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useSearchApi, type SearchResults } from '~/composables/useSearchApi'
import { debounce } from '~/composables/useDebounce'
import { formatImageUrl } from '~/utils/imageUtils'

const searchApi = useSearchApi()
const searchQuery = ref('')
const results = ref<SearchResults>({ products: [], blogs: [], total: 0 })
const isLoading = ref(false)
const isFocused = ref(false)
const highlightedIndex = ref(-1)
const searchContainer = ref<HTMLElement | null>(null)

const showResults = computed(() => {
  return isFocused.value && searchQuery.value.length >= 2
})

const hasResults = computed(() => {
  return results.value.total > 0
})

const totalDisplayed = computed(() => {
  return (results.value.products?.length || 0) + (results.value.blogs?.length || 0)
})

// Debounced search function
const performSearch = debounce(async (query: string) => {
  if (!query || query.length < 2) {
    results.value = { products: [], blogs: [], total: 0 }
    isLoading.value = false
    return
  }

  isLoading.value = true
  try {
    const response = await searchApi.globalSearch(query, 5)
    results.value = response
    highlightedIndex.value = -1
  } catch (error) {
    console.error('Search error:', error)
    results.value = { products: [], blogs: [], total: 0 }
  } finally {
    isLoading.value = false
  }
}, 300) // 300ms debounce

// Watch search query
watch(searchQuery, (newQuery) => {
  if (newQuery.length >= 2) {
    performSearch(newQuery)
  } else {
    results.value = { products: [], blogs: [], total: 0 }
    isLoading.value = false
  }
})

// Helper methods
const getProductIndex = (index: number) => index
const getBlogIndex = (index: number) => (results.value.products?.length || 0) + index

const navigateResults = (direction: 'up' | 'down') => {
  const totalResults = totalDisplayed.value
  if (totalResults === 0) return

  if (direction === 'down') {
    highlightedIndex.value = (highlightedIndex.value + 1) % totalResults
  } else {
    highlightedIndex.value = highlightedIndex.value <= 0 
      ? totalResults - 1 
      : highlightedIndex.value - 1
  }
}

const selectResult = () => {
  if (highlightedIndex.value === -1) return

  const productsCount = results.value.products?.length || 0
  
  if (highlightedIndex.value < productsCount) {
    const product = results.value.products[highlightedIndex.value]
    if (product.slug) {
      navigateTo(`/products/${product.slug}`)
    } else {
      navigateTo(`/products/${product.id}`)
    }
  } else {
    const blogIndex = highlightedIndex.value - productsCount
    const blog = results.value.blogs[blogIndex]
    navigateTo(`/blog/${blog.slug}`)
  }
  
  closeResults()
}

// Perform full search and navigate to products page
const performFullSearch = () => {
  if (!searchQuery.value || !searchQuery.value.trim()) {
    return
  }

  closeResults()
  navigateTo({
    path: '/products',
    query: { search: searchQuery.value.trim() }
  })
}

// Handle Enter key - if a result is highlighted, select it; otherwise perform full search
const handleEnterKey = () => {
  if (highlightedIndex.value >= 0) {
    selectResult()
  } else {
    performFullSearch()
  }
}

const clearSearch = () => {
  searchQuery.value = ''
  results.value = { products: [], blogs: [], total: 0 }
  highlightedIndex.value = -1
}

const closeResults = () => {
  isFocused.value = false
  highlightedIndex.value = -1
}

const handleImageError = (event: Event) => {
  // Silently handle image errors - hide broken images
  const target = event.target as HTMLImageElement
  if (target) {
    target.style.display = 'none'
    // Show placeholder instead
    const placeholder = target.nextElementSibling as HTMLElement
    if (placeholder && placeholder.classList.contains('placeholder-image')) {
      placeholder.style.display = 'flex'
    }
  }
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('fa-IR').format(price)
}

const truncate = (text: string, length: number) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

// Click outside to close
const handleClickOutside = (event: MouseEvent) => {
  if (searchContainer.value && !searchContainer.value.contains(event.target as Node)) {
    closeResults()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.global-search {
  position: relative;
  width: 100%;
  max-width: 500px;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 0.75rem 3rem 0.75rem 1rem;
  border: 2px solid rgba(var(--v-theme-on-surface), 0.12);
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: rgb(var(--v-theme-surface));
  direction: rtl;
}

/* Mobile-optimized search input */
@media (max-width: 959px) {
  .search-input {
    padding: 1rem 3.5rem 1rem 1.25rem;
    font-size: 1.125rem;
    border-radius: 12px;
    border-width: 2px;
  }
  
  .search-icon {
    right: 1.25rem;
    width: 24px;
    height: 24px;
  }
  
  .clear-button {
    left: 1.25rem;
    width: 28px;
    height: 28px;
    font-size: 1.75rem;
  }
}

.search-input:focus {
  outline: none;
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 0 0 3px rgba(var(--v-theme-primary), 0.1);
}

.search-icon {
  position: absolute;
  right: 1rem;
  width: 20px;
  height: 20px;
  color: rgba(var(--v-theme-on-surface), 0.5);
  cursor: pointer;
  transition: color 0.2s;
  z-index: 1;
  padding: 4px;
  margin: -4px;
  box-sizing: content-box;
}

.search-icon:hover {
  color: rgb(var(--v-theme-primary));
}

.search-icon:active {
  color: rgb(var(--v-theme-primary));
}

.clear-button {
  position: absolute;
  left: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: rgba(var(--v-theme-on-surface), 0.5);
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s;
}

.clear-button:hover {
  background-color: rgba(var(--v-theme-on-surface), 0.06);
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.search-results {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  left: 0;
  background: rgb(var(--v-theme-surface));
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(var(--v-theme-on-surface), 0.15);
  max-height: 500px;
  overflow-y: auto;
  z-index: 1000;
  direction: rtl;
}

.search-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  gap: 1rem;
  color: rgba(var(--v-theme-on-surface), 0.6);
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(var(--v-theme-on-surface), 0.06);
  border-top: 2px solid rgb(var(--v-theme-primary));
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-results {
  padding: 2rem;
  text-align: center;
  color: rgba(var(--v-theme-on-surface), 0.5);
}

.results-container {
  padding: 0.5rem 0;
}

.result-section {
  padding: 0.5rem 0;
}

.result-section:not(:last-child) {
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.06);
}

.section-title {
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  font-weight: bold;
  color: rgba(var(--v-theme-on-surface), 0.6);
  margin: 0;
  background-color: rgba(var(--v-theme-surface), 0.97);
}

.result-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  text-decoration: none;
  color: rgba(var(--v-theme-on-surface), 0.87);
  transition: background-color 0.2s;
  cursor: pointer;
}

.result-item:hover,
.result-item.highlighted {
  background-color: rgba(var(--v-theme-primary), 0.04);
}

.result-image {
  width: 50px;
  height: 50px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
  background-color: rgba(var(--v-theme-on-surface), 0.06);
}

.result-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(var(--v-theme-on-surface), 0.08);
  color: rgba(var(--v-theme-on-surface), 0.5);
  font-size: 0.75rem;
}

.result-content {
  flex: 1;
  min-width: 0;
}

.result-title {
  font-weight: 500;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.result-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: rgba(var(--v-theme-on-surface), 0.6);
}

.badge {
  display: inline-block;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge-product {
  background-color: rgba(var(--v-theme-primary), 0.1);
  color: rgb(var(--v-theme-primary));
}

.badge-blog {
  background-color: rgba(var(--v-theme-accent), 0.1);
  color: rgb(var(--v-theme-accent));
}

.result-price {
  font-weight: 500;
  color: rgb(var(--v-theme-primary));
}

.result-excerpt {
  color: rgba(var(--v-theme-on-surface), 0.5);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.view-all {
  padding: 0.75rem 1rem;
  text-align: center;
  color: rgba(var(--v-theme-on-surface), 0.6);
  font-size: 0.875rem;
  background-color: rgba(var(--v-theme-surface), 0.97);
  border-top: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

/* Dropdown transition */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Scrollbar styling */
.search-results::-webkit-scrollbar {
  width: 6px;
}

.search-results::-webkit-scrollbar-track {
  background: rgba(var(--v-theme-surface), 0.5);
  border-radius: 4px;
}

.search-results::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-primary), 0.4);
  border-radius: 4px;
}

.search-results::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-primary), 0.6);
}

/* Responsive */
@media (max-width: 768px) {
  .global-search {
    max-width: 100%;
  }

  .search-results {
    max-height: 400px;
  }
}
</style>

