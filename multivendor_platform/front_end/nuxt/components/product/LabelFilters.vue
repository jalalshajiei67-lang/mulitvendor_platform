<template>
  <v-card class="label-filters" elevation="0" rounded="xl" border>
    <div v-if="labelStore.loading" class="label-filters__loading">
      <v-progress-circular indeterminate color="primary" size="40" />
      <p class="text-caption text-medium-emphasis mt-3">در حال بارگذاری فیلترها...</p>
    </div>
    <div v-else-if="labelStore.error" class="label-filters__error px-6 py-4">
      <v-icon color="error" size="32" class="mb-2">mdi-alert-circle</v-icon>
      <p class="text-body-2 text-error">{{ labelStore.error }}</p>
    </div>
    <template v-else>
      <!-- Empty state message only if no groups AND component is showing based on category selection -->
      <div v-if="!groups.length && subcategoryId !== null" class="label-filters__empty px-6 py-4 text-center">
        <v-icon color="grey" size="40" class="mb-2">mdi-filter-off</v-icon>
        <p class="text-body-2 text-medium-emphasis">
          هیچ فیلتر برچسبی برای نمایش وجود ندارد.
        </p>
      </div>
      
      <!-- Filter Search (only show if there are many labels) -->
      <div v-if="groups.length && totalLabelsCount > 10" class="filter-search pa-4 pb-0">
        <v-text-field
          v-model="searchQuery"
          variant="outlined"
          density="compact"
          placeholder="جستجو در فیلترها..."
          prepend-inner-icon="mdi-magnify"
          clearable
          hide-details
          class="filter-search__input"
        />
      </div>

      <v-expansion-panels v-model="expandedPanels" multiple flat class="label-expansion-panels">
        <v-expansion-panel
          v-for="(group, index) in filteredGroups"
          :key="group.id"
          :value="index"
          class="label-group-panel"
        >
          <v-expansion-panel-title class="label-group__header">
            <div class="d-flex align-center justify-space-between w-100 pr-4">
              <div class="d-flex align-center gap-3">
                <div class="group-icon-wrapper" :style="{ backgroundColor: getGroupColorLight(index) }">
                  <v-icon :color="getGroupIconColor(index)" size="20">{{ getGroupIcon(index) }}</v-icon>
                </div>
                <div>
                  <div class="d-flex align-center gap-2">
                    <span class="text-subtitle-2 font-weight-bold">{{ group.name }}</span>
                    <v-chip
                      v-if="getSelectedCountForGroup(group)"
                      size="x-small"
                      color="success"
                      variant="flat"
                      class="selection-badge"
                    >
                      {{ getSelectedCountForGroup(group) }}
                    </v-chip>
                  </div>
                  <p v-if="group.description" class="text-caption text-medium-emphasis mt-0 mb-0">
                    {{ group.description }}
                  </p>
                </div>
              </div>
              <v-btn
                v-if="getSelectedCountForGroup(group)"
                variant="text"
                size="x-small"
                color="error"
                class="clear-group-btn"
                @click.stop="clearGroup(group)"
              >
                <v-icon size="16">mdi-close-circle</v-icon>
                <span class="mr-1">پاک کردن</span>
              </v-btn>
            </div>
          </v-expansion-panel-title>
          
          <v-expansion-panel-text class="label-group__content">
            <div class="label-group__chips">
              <v-chip
                v-for="label in group.labels"
                :key="label.slug"
                size="small"
                :variant="isSelected(label.slug) ? 'flat' : 'outlined'"
                :class="['label-chip', { 'label-chip--active': isSelected(label.slug) }]"
                :style="getLabelStyle(label)"
                :elevation="isSelected(label.slug) ? 3 : 0"
                @click="toggleLabel(label.slug)"
              >
                <template #prepend>
                  <v-icon v-if="isSelected(label.slug)" size="16" class="check-icon">mdi-check-circle</v-icon>
                </template>
                <span class="label-text">{{ label.name }}</span>
              </v-chip>
            </div>
          </v-expansion-panel-text>
        </v-expansion-panel>

      </v-expansion-panels>

      <!-- Sorting/Ordering Filter - Always Last -->
      <div v-if="filteredGroups.length > 0" class="sorting-divider">
        <v-divider />
      </div>
      
      <div class="sorting-section pa-4">
        <v-select
          v-model="localOrdering"
          :items="orderingOptions"
          variant="outlined"
          density="comfortable"
          label="مرتب‌سازی"
          clearable
          hide-details
          class="sorting-select"
        >
          <template #prepend-inner>
            <v-icon color="info" size="20">mdi-sort</v-icon>
          </template>
          <template #selection="{ item }">
            <div class="d-flex align-center">
              <v-icon size="16" color="success" class="ml-2">mdi-check-circle</v-icon>
              <span class="font-weight-medium">{{ item.title }}</span>
            </div>
          </template>
          <template #item="{ props, item }">
            <v-list-item v-bind="props" class="sorting-menu-item">
              <template #prepend>
                <v-icon color="info" size="18">mdi-sort-variant</v-icon>
              </template>
            </v-list-item>
          </template>
        </v-select>
      </div>

      <!-- Quick Actions Footer -->
      <div v-if="normalizedSelection.length > 0 || localOrdering" class="filter-actions">
        <v-divider />
        <div class="pa-3 d-flex align-center justify-space-between">
          <div class="d-flex align-center gap-2">
            <v-icon size="18" color="primary">mdi-filter-check</v-icon>
            <span class="text-caption">
              <strong>{{ normalizedSelection.length + (localOrdering ? 1 : 0) }}</strong> فیلتر انتخاب شده
            </span>
          </div>
          <v-btn
            variant="text"
            size="small"
            color="error"
            prepend-icon="mdi-close-circle"
            @click="clearAllFilters"
          >
            پاک کردن همه
          </v-btn>
        </div>
      </div>
    </template>
  </v-card>
</template>

<script setup lang="ts">
import { computed, onMounted, watch, ref } from 'vue'
import type { PropType } from 'vue'

import { useLabelStore } from '~/stores/label'

const props = defineProps({
  subcategoryId: {
    type: Number as PropType<number | null>,
    default: null
  },
  modelValue: {
    type: Array as PropType<string[]>,
    default: () => []
  },
  ordering: {
    type: String as PropType<string | null>,
    default: null
  }
})

const emit = defineEmits<{
  (event: 'update:modelValue', value: string[]): void
  (event: 'update:ordering', value: string | null): void
  (event: 'subcategory-changed', subcategoryId: number | null): void
  (event: 'labels-loaded', groupsCount: number): void
}>()

const labelStore = useLabelStore()

// Local state
const searchQuery = ref('')
const expandedPanels = ref<number[]>([])

// Ordering options
const orderingOptions = [
  { title: 'جدیدترین', value: '-created_at' },
  { title: 'ارزان‌ترین', value: 'price' },
  { title: 'گران‌ترین', value: '-price' }
]

// Local ordering state
const localOrdering = ref<string | null>(props.ordering)

// Watch for external changes to ordering prop
watch(() => props.ordering, (newValue) => {
  localOrdering.value = newValue
})

// Emit ordering changes
watch(localOrdering, (newValue) => {
  emit('update:ordering', newValue)
})

const normalizedSelection = computed(() => props.modelValue ?? [])

const groups = computed(() => {
  // labelStore.labelGroups is now guaranteed to be an array via computed getter
  const filteredGroups = labelStore.labelGroups
    .map((group) => ({
      ...group,
      labels: (group.labels || []).filter((label) => label.is_active && label.is_filterable)
    }))
    .filter((group) => group.labels.length > 0)
  
  // Emit the count of groups to parent
  emit('labels-loaded', filteredGroups.length)
  
  return filteredGroups
})

// Filtered groups based on search query
const filteredGroups = computed(() => {
  if (!searchQuery.value) {
    return groups.value
  }
  
  const query = searchQuery.value.toLowerCase().trim()
  return groups.value
    .map((group) => ({
      ...group,
      labels: group.labels.filter((label: any) => 
        label.name.toLowerCase().includes(query) || 
        group.name.toLowerCase().includes(query)
      )
    }))
    .filter((group) => group.labels.length > 0)
})

// Total count of all labels
const totalLabelsCount = computed(() => {
  return groups.value.reduce((count, group) => count + group.labels.length, 0)
})

const isSelected = (slug: string) => normalizedSelection.value.includes(slug)

const toggleLabel = (slug: string) => {
  const nextSelection = [...normalizedSelection.value]
  const index = nextSelection.indexOf(slug)

  if (index === -1) {
    nextSelection.push(slug)
  } else {
    nextSelection.splice(index, 1)
  }

  emit('update:modelValue', nextSelection)
}

const getLabelStyle = (label: Record<string, any>) => {
  const isActiveLabel = isSelected(label.slug)
  
  if (!label.color) {
    return {}
  }

  // Active state: solid color with white text
  if (isActiveLabel) {
    return {
      borderColor: label.color,
      color: '#fff',
      backgroundColor: label.color,
      fontWeight: '600'
    }
  }

  // Inactive state: outlined with colored border
  return {
    borderColor: label.color,
    color: label.color,
    backgroundColor: 'transparent'
  }
}

// Helper method to get icon for each group based on index
const getGroupIcon = (index: number) => {
  const icons = ['mdi-factory', 'mdi-ruler', 'mdi-star', 'mdi-tag', 'mdi-label', 'mdi-bookmark']
  return icons[index % icons.length]
}

// Helper method to get icon color for each group
const getGroupIconColor = (index: number) => {
  const colors = ['primary', 'success', 'warning', 'info', 'secondary', 'error']
  return colors[index % colors.length]
}

// Get light background color for icon wrapper
const getGroupColorLight = (index: number) => {
  const colors = [
    'rgba(var(--v-theme-primary), 0.08)',
    'rgba(var(--v-theme-success), 0.08)',
    'rgba(var(--v-theme-warning), 0.08)',
    'rgba(var(--v-theme-info), 0.08)',
    'rgba(var(--v-theme-secondary), 0.08)',
    'rgba(var(--v-theme-error), 0.08)'
  ]
  return colors[index % colors.length]
}

// Get count of selected labels in a group
const getSelectedCountForGroup = (group: Record<string, any>) => {
  const labels = Array.isArray(group.labels) ? group.labels : []
  return labels.filter((label: Record<string, any>) => isSelected(label.slug)).length
}

// Clear all filters in a specific group
const clearGroup = (group: Record<string, any>) => {
  const labels = Array.isArray(group.labels) ? group.labels : []
  const groupSlugs = labels.map((label: Record<string, any>) => label.slug)
  const nextSelection = normalizedSelection.value.filter((slug) => !groupSlugs.includes(slug))
  emit('update:modelValue', nextSelection)
}

// Clear ordering
const clearOrdering = () => {
  localOrdering.value = null
}

// Clear all filters
const clearAllFilters = () => {
  emit('update:modelValue', [])
  localOrdering.value = null
}

// Initialize expanded panels - expand first panel and panels with selections
const initializeExpandedPanels = () => {
  const expanded: number[] = []
  groups.value.forEach((group, index) => {
    if (index === 0 || getSelectedCountForGroup(group) > 0) {
      expanded.push(index)
    }
  })
  expandedPanels.value = expanded
}

onMounted(() => {
  void labelStore.fetchLabelGroupsForSubcategory(props.subcategoryId, true)
})

watch(groups, () => {
  // Auto-expand panels when groups load or change
  if (expandedPanels.value.length === 0) {
    initializeExpandedPanels()
  }
}, { immediate: true })

watch(
  () => props.subcategoryId,
  (newId, oldId) => {
    if (newId === oldId) {
      return
    }
    void labelStore.fetchLabelGroupsForSubcategory(newId, true)
    emit('update:modelValue', [])
    emit('subcategory-changed', newId)
    // Reset search and expanded panels
    searchQuery.value = ''
    expandedPanels.value = []
  }
)
</script>

<style scoped>
.label-filters {
  border: 1px solid rgba(var(--v-theme-on-surface), 0.12);
  background: rgba(var(--v-theme-surface), 1);
  overflow: hidden;
}

.label-filters__loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  min-height: 160px;
}

.label-filters__error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 120px;
}

.label-filters__empty {
  min-height: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* Filter Search */
.filter-search {
  background: rgba(var(--v-theme-primary), 0.02);
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.06);
}

.filter-search__input {
  font-size: 0.875rem;
}

/* Expansion Panels */
.label-expansion-panels {
  background: transparent;
}

.label-group-panel {
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.06);
  transition: all 0.2s ease;
}

.label-group-panel:last-child {
  border-bottom: none;
}

.label-group-panel:hover {
  background-color: rgba(var(--v-theme-primary), 0.02);
}

/* Group Header */
.label-group__header {
  padding: 16px 20px !important;
  min-height: auto !important;
}

.group-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.label-group-panel:hover .group-icon-wrapper {
  transform: scale(1.05);
}

.clear-group-btn {
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.clear-group-btn:hover {
  opacity: 1;
}

.selection-badge {
  animation: badgePulse 0.4s ease-out;
}

@keyframes badgePulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.15);
  }
}

/* Group Content */
.label-group__content {
  padding-top: 8px !important;
  padding-bottom: 16px !important;
}

.label-group__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 0 4px;
}

/* Sorting Panel */
.sorting-divider {
  margin-top: 8px;
}

.sorting-section {
  background: rgba(var(--v-theme-info), 0.02);
  border-top: 2px solid rgba(var(--v-theme-info), 0.12);
  transition: background-color 0.2s ease;
}

.sorting-section:hover {
  background: rgba(var(--v-theme-info), 0.04);
}

.sorting-select {
  max-width: 100%;
}

.sorting-select :deep(.v-field) {
  box-shadow: 0 2px 8px rgba(var(--v-theme-on-surface), 0.04);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(var(--v-theme-surface), 1);
}

.sorting-select :deep(.v-field:hover) {
  box-shadow: 0 4px 12px rgba(var(--v-theme-on-surface), 0.08);
  border-color: rgba(var(--v-theme-info), 0.3);
}

.sorting-select :deep(.v-field--focused) {
  box-shadow: 0 4px 16px rgba(var(--v-theme-info), 0.12);
}

.sorting-menu-item {
  transition: all 0.2s ease;
  border-radius: 8px;
  margin: 4px 8px;
}

.sorting-menu-item:hover {
  background: rgba(var(--v-theme-info), 0.08) !important;
  transform: translateX(-4px);
}

/* Label Chips */
.label-chip {
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  border-width: 1.5px;
  border-style: solid;
  user-select: none;
  position: relative;
  overflow: hidden;
}

.label-chip::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: currentColor;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.label-chip:hover::before {
  opacity: 0.08;
}

.label-chip:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(var(--v-theme-on-surface), 0.2);
}

.label-chip:active {
  transform: translateY(0) scale(0.97);
}

.label-chip--active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(var(--v-theme-on-surface), 0.25);
}

.label-chip--active:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(var(--v-theme-on-surface), 0.3);
}

.label-text {
  position: relative;
  z-index: 1;
}

.check-icon {
  position: relative;
  z-index: 1;
  margin-left: -2px;
}

/* Filter Actions Footer */
.filter-actions {
  background: rgba(var(--v-theme-primary), 0.02);
  border-top: 1px solid rgba(var(--v-theme-on-surface), 0.06);
}

/* Utility classes */
.gap-2 {
  gap: 8px;
}

.gap-3 {
  gap: 12px;
}

/* Mobile Optimizations */
@media (max-width: 959px) {
  .label-group__header {
    padding: 14px 16px !important;
  }
  
  .group-icon-wrapper {
    width: 36px;
    height: 36px;
  }
  
  .label-group__content {
    padding-bottom: 12px !important;
  }
  
  .label-group__chips {
    gap: 8px;
  }
  
  .label-chip {
    font-size: 0.8125rem;
  }
  
  .clear-group-btn {
    font-size: 0.75rem;
  }
  
  .sorting-section {
    padding: 12px 18px !important;
  }
}

/* Small Mobile Optimizations */
@media (max-width: 599px) {
  .filter-search {
    padding: 12px 16px 0 16px;
  }
  
  .label-group__header {
    padding: 12px 14px !important;
  }
  
  .group-icon-wrapper {
    width: 32px;
    height: 32px;
  }
  
  .label-group__chips {
    gap: 6px;
  }
  
  .label-chip {
    font-size: 0.75rem;
    height: 28px;
  }
  
  .label-filters__empty {
    min-height: 140px;
  }
  
  .filter-actions {
    padding: 8px !important;
  }
  
  .sorting-section {
    padding: 12px 16px !important;
  }
}

/* RTL Support */
[dir="rtl"] .check-icon {
  margin-left: 0;
  margin-right: -2px;
}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
  .label-filters {
    border-color: rgba(var(--v-theme-on-surface), 0.15);
  }
  
  .filter-search {
    background: rgba(var(--v-theme-primary), 0.05);
  }
  
  .label-chip:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }
  
  .label-chip--active {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
  }
  
  .label-chip--active:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
  }
}

/* Animation for selected chips */
@keyframes chipSelect {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.label-chip--active {
  animation: chipSelect 0.3s ease-out;
}

/* Smooth transitions */
.label-group-panel,
.label-chip,
.group-icon-wrapper,
.clear-group-btn {
  will-change: transform;
}
</style>


