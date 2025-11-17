<template>
  <v-card class="label-filters" elevation="1" rounded="xl">
    <div v-if="labelStore.loading" class="label-filters__loading">
      <v-progress-circular indeterminate color="primary" size="40" />
      <p class="text-caption text-medium-emphasis mt-3">در حال بارگذاری فیلترها...</p>
    </div>
    <div v-else-if="labelStore.error" class="label-filters__error px-6 py-4">
      <v-icon color="error" size="32" class="mb-2">mdi-alert-circle</v-icon>
      <p class="text-body-2 text-error">{{ labelStore.error }}</p>
    </div>
    <template v-else>
      <div v-if="!groups.length" class="label-filters__empty px-6 py-8 text-center">
        <v-icon color="grey" size="48" class="mb-3">mdi-filter-off</v-icon>
        <p class="text-body-2 text-medium-emphasis">
          هیچ فیلتری برای نمایش وجود ندارد.
        </p>
        <p class="text-caption text-medium-emphasis mt-1">
          لطفاً یک دسته‌بندی یا زیرشاخه انتخاب کنید.
        </p>
      </div>
      <section v-for="(group, index) in groups" :key="group.id" class="label-group">
        <header class="label-group__header">
          <div class="d-flex align-center justify-space-between">
            <div>
              <div class="d-flex align-center gap-2">
                <v-icon :color="getGroupIconColor(index)" size="18">{{ getGroupIcon(index) }}</v-icon>
                <span class="text-subtitle-2 font-weight-bold">{{ group.name }}</span>
                <v-chip
                  v-if="getSelectedCountForGroup(group)"
                  size="x-small"
                  color="success"
                  variant="flat"
                >
                  {{ getSelectedCountForGroup(group) }}
                </v-chip>
              </div>
              <p v-if="group.description" class="text-caption text-medium-emphasis mt-1 mr-6">
                {{ group.description }}
              </p>
            </div>
          </div>
        </header>
        <div class="label-group__chips">
          <v-chip
            v-for="label in group.labels"
            :key="label.slug"
            size="small"
            :variant="isSelected(label.slug) ? 'flat' : 'tonal'"
            :class="['label-chip', { 'label-chip--active': isSelected(label.slug) }]"
            :style="getLabelStyle(label)"
            :elevation="isSelected(label.slug) ? 2 : 0"
            @click="toggleLabel(label.slug)"
          >
            <v-icon v-if="isSelected(label.slug)" start size="14">mdi-check</v-icon>
            {{ label.name }}
          </v-chip>
        </div>
      </section>
    </template>
  </v-card>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from 'vue'
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
  }
})

const emit = defineEmits<{
  (event: 'update:modelValue', value: string[]): void
  (event: 'subcategory-changed', subcategoryId: number | null): void
  (event: 'labels-loaded', groupsCount: number): void
}>()

const labelStore = useLabelStore()

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

  // Active state: solid color
  if (isActiveLabel) {
    return {
      borderColor: label.color,
      color: '#fff',
      backgroundColor: label.color
    }
  }

  // Inactive state: tonal
  return {
    borderColor: label.color,
    color: label.color,
    backgroundColor: `${label.color}1f`
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

// Get count of selected labels in a group
const getSelectedCountForGroup = (group: Record<string, any>) => {
  const labels = Array.isArray(group.labels) ? group.labels : []
  return labels.filter((label: Record<string, any>) => isSelected(label.slug)).length
}

onMounted(() => {
  void labelStore.fetchLabelGroupsForSubcategory(props.subcategoryId, true)
})

watch(
  () => props.subcategoryId,
  (newId, oldId) => {
    if (newId === oldId) {
      return
    }
    void labelStore.fetchLabelGroupsForSubcategory(newId, true)
    emit('update:modelValue', [])
    emit('subcategory-changed', newId)
  }
)
</script>

<style scoped>
.label-filters {
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
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

.label-group {
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.06);
  padding: 20px 24px;
  transition: background-color 0.2s ease;
  position: relative;
}

.label-group:last-child {
  border-bottom: none;
}

.label-group:hover {
  background-color: rgba(var(--v-theme-primary), 0.02);
}

.label-group::before {
  content: '';
  position: absolute;
  right: 0;
  top: 0;
  width: 3px;
  height: 0;
  background: rgb(var(--v-theme-primary));
  transition: height 0.3s ease;
}

.label-group:hover::before {
  height: 100%;
}

.label-group__header {
  margin-bottom: 12px;
}

.label-group__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.label-chip {
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1.5px solid transparent;
  user-select: none;
}

.label-chip:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 4px 12px rgba(var(--v-theme-on-surface), 0.15);
}

.label-chip:active {
  transform: translateY(0) scale(0.98);
}

.label-chip--active {
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(var(--v-theme-on-surface), 0.2);
}

.label-chip--active:hover {
  box-shadow: 0 4px 16px rgba(var(--v-theme-on-surface), 0.25);
}

/* Animation for chips */
@keyframes chipPop {
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
  animation: chipPop 0.3s ease-out;
}

/* Utility classes */
.gap-2 {
  gap: 8px;
}

/* Mobile Optimizations */
@media (max-width: 959px) {
  .label-group {
    padding: 16px 18px;
  }
  
  .label-group__chips {
    gap: 6px;
  }
  
  .label-chip {
    font-size: 0.85rem;
  }
}

/* Small Mobile Optimizations */
@media (max-width: 599px) {
  .label-group {
    padding: 14px 16px;
  }
  
  .label-filters__empty {
    min-height: 140px;
  }
}
</style>

