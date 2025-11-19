<template>
  <v-card rounded="xl" elevation="2" class="leaderboard-widget">
    <v-card-title class="d-flex justify-space-between align-center">
      <span class="text-h6">{{ title }}</span>
      <v-chip color="primary" size="small" variant="flat">Top {{ entries.length }}</v-chip>
    </v-card-title>
    <v-divider></v-divider>
    <v-list density="comfortable">
      <v-list-item
        v-for="(entry, idx) in entries"
        :key="entry.vendor"
        class="leaderboard-row"
      >
        <template #prepend>
          <v-avatar color="primary" size="36" class="me-3">
            <span class="text-body-2">{{ idx + 1 }}</span>
          </v-avatar>
        </template>
        <template #title>
          <div class="d-flex justify-space-between align-center">
            <span>{{ entry.vendor }}</span>
            <strong>{{ entry.points }} امتیاز</strong>
          </div>
        </template>
        <template #subtitle>
          <span class="text-caption text-medium-emphasis">سریال: {{ entry.streak }} روز</span>
        </template>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script setup lang="ts">
import type { LeaderboardEntry } from '~/stores/gamification'

const props = withDefaults(defineProps<{ title?: string; entries: LeaderboardEntry[] }>(), {
  title: 'برترین‌های این هفته',
  entries: () => []
})
</script>
