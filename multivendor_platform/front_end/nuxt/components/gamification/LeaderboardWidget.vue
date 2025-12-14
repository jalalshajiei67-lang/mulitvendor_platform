<template>
  <v-card 
    rounded="xl" 
    elevation="0" 
    class="leaderboard-widget h-100"
    variant="tonal"
    color="info"
  >
    <v-card-title class="d-flex justify-space-between align-center px-4 pt-4 pb-2">
      <div class="d-flex align-center gap-2">
        <v-icon color="info">mdi-podium</v-icon>
        <span class="text-h6 font-weight-bold">{{ title }}</span>
      </div>
      <v-chip 
        v-if="entries.length > 0" 
        color="info" 
        size="small" 
        variant="flat"
      >
        Top {{ entries.length }}
      </v-chip>
    </v-card-title>
    <v-divider class="mx-4"></v-divider>
    <v-card-text class="px-0 py-2">
      <div v-if="entries.length === 0" class="text-center py-8 px-4">
        <v-icon size="64" color="grey-lighten-1" class="mb-3">mdi-podium-outline</v-icon>
        <p class="text-body-2 text-medium-emphasis">هنوز داده‌ای وجود ندارد</p>
        <p class="text-caption text-medium-emphasis mt-1">با فعالیت بیشتر در جدول برترین‌ها قرار بگیرید و از مزایای آن بهره ببرید</p>
      </div>
      <v-list v-else density="comfortable" class="bg-transparent">
        <v-list-item
          v-for="(entry, idx) in entries"
          :key="entry.vendor"
          class="leaderboard-row px-4"
          :class="{ 'top-three': idx < 3 }"
        >
          <template #prepend>
            <div class="position-badge me-3">
              <v-avatar 
                :color="getPositionColor(idx)" 
                size="40"
                variant="flat"
              >
                <span class="text-body-2 font-weight-bold">{{ idx + 1 }}</span>
              </v-avatar>
              <v-icon 
                v-if="idx < 3" 
                :color="getMedalColor(idx)"
                size="20"
                class="medal-icon"
              >
                mdi-medal
              </v-icon>
            </div>
          </template>
          <template #title>
            <div class="d-flex justify-space-between align-center flex-wrap gap-2">
              <span class="font-weight-medium">{{ entry.vendor }}</span>
              <div class="d-flex align-center gap-2">
                <v-icon size="16" color="primary">mdi-star</v-icon>
                <strong class="text-primary">{{ formatNumber(entry.points) }}</strong>
              </div>
            </div>
          </template>
          <template #subtitle>
            <div class="d-flex align-center gap-2 mt-1">
              <v-icon size="14" color="warning">mdi-fire</v-icon>
              <span class="text-caption text-medium-emphasis">
                {{ entry.streak }} روز متوالی
              </span>
            </div>
          </template>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import type { LeaderboardEntry } from '~/stores/gamification'

const props = withDefaults(defineProps<{ title?: string; entries: LeaderboardEntry[] }>(), {
  title: 'برترین‌های این هفته',
  entries: () => []
})

const getPositionColor = (index: number) => {
  if (index === 0) return 'amber'
  if (index === 1) return 'grey'
  if (index === 2) return 'deep-orange'
  return 'primary'
}

const getMedalColor = (index: number) => {
  if (index === 0) return 'amber'
  if (index === 1) return 'grey'
  return 'deep-orange'
}

const formatNumber = (num: number) => {
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}
</script>

<style scoped>
.leaderboard-widget {
  transition: transform 0.2s ease;
}

.leaderboard-widget:hover {
  transform: translateY(-2px);
}

.leaderboard-row {
  transition: background 0.2s ease;
  border-radius: 8px;
  margin: 4px 0;
}

.leaderboard-row:hover {
  background: rgba(var(--v-theme-surface), 0.5);
}

.leaderboard-row.top-three {
  background: rgba(var(--v-theme-surface), 0.3);
}

.position-badge {
  position: relative;
  display: inline-block;
}

.medal-icon {
  position: absolute;
  top: -4px;
  right: -4px;
  background: white;
  border-radius: 50%;
  padding: 2px;
}

.gap-2 {
  gap: 8px;
}

@media (max-width: 600px) {
  .leaderboard-row {
    padding: 8px 12px !important;
  }
}
</style>
