<template>
  <v-card rounded="xl" elevation="2" class="badge-display">
    <v-card-title class="text-h6">{{ title }}</v-card-title>
    <v-card-text>
      <v-row>
        <v-col v-for="badge in badges" :key="badge.slug" cols="12" md="6">
          <v-sheet class="pa-3 rounded-lg" :class="tierClass(badge.tier)">
            <div class="d-flex justify-space-between align-center">
              <div>
                <p class="text-subtitle-2 font-weight-bold mb-1">{{ badge.title }}</p>
                <p class="text-caption text-medium-emphasis mb-2">{{ badge.description }}</p>
                <v-chip size="small" class="text-caption" color="primary" variant="flat">
                  {{ badge.category }}
                </v-chip>
              </div>
              <v-icon size="36">{{ badge.icon || 'mdi-trophy' }}</v-icon>
            </div>
          </v-sheet>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import type { Badge } from '~/stores/gamification'

const props = withDefaults(defineProps<{ badges: Badge[]; title?: string }>(), {
  badges: () => [],
  title: 'نشان‌های در دسترس'
})

const tierClass = (tier: string) => {
  const classes: Record<string, string> = {
    bronze: 'tier-bronze',
    silver: 'tier-silver',
    gold: 'tier-gold'
  }
  return classes[tier] ?? 'tier-bronze'
}
</script>

<style scoped>
.tier-bronze {
  background: linear-gradient(135deg, #f1e1d0, #f7f1ea);
}
.tier-silver {
  background: linear-gradient(135deg, #e3eaf1, #f7f9fb);
}
.tier-gold {
  background: linear-gradient(135deg, #ffe8a1, #fff5d7);
}
</style>
