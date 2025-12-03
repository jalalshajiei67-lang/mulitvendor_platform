<template>
  <v-card 
    rounded="xl" 
    elevation="0" 
    class="badge-display h-100"
    variant="tonal"
    color="secondary"
  >
    <v-card-title class="d-flex align-center justify-space-between px-4 pt-4 pb-2">
      <div class="d-flex align-center gap-2">
        <v-icon color="secondary">mdi-trophy-outline</v-icon>
        <span class="text-h6 font-weight-bold">{{ title }}</span>
      </div>
      <v-chip 
        v-if="badges.length > 0" 
        size="small" 
        color="secondary" 
        variant="flat"
      >
        {{ badges.length }} نشان
      </v-chip>
    </v-card-title>
    <v-card-text class="px-4 pb-4">
      <div v-if="badges.length === 0" class="text-center py-8">
        <v-icon size="64" color="grey-lighten-1" class="mb-3">mdi-trophy-outline</v-icon>
        <p class="text-body-2 text-medium-emphasis">هنوز نشانی دریافت نکرده‌اید</p>
        <p class="text-caption text-medium-emphasis mt-1">با تکمیل فرم‌ها و فعالیت بیشتر نشان دریافت کنید</p>
      </div>
      <v-row v-else dense>
        <v-col 
          v-for="badge in badges" 
          :key="badge.slug" 
          cols="12" 
          sm="6"
        >
          <v-sheet 
            class="badge-card pa-3 rounded-lg h-100" 
            :class="tierClass(badge.tier)"
            elevation="1"
          >
            <div class="d-flex align-start gap-3">
              <v-avatar 
                :color="tierAvatarColor(badge.tier)" 
                size="48"
                variant="flat"
                class="flex-shrink-0"
              >
                <v-icon :color="tierIconColor(badge.tier)" size="24">
                  {{ badge.icon || 'mdi-trophy' }}
                </v-icon>
              </v-avatar>
              <div class="flex-grow-1 min-width-0">
                <p class="text-subtitle-2 font-weight-bold mb-1">{{ badge.title }}</p>
                <p class="text-caption text-medium-emphasis mb-2 line-clamp-2">
                  {{ badge.description }}
                </p>
                <v-chip 
                  size="x-small" 
                  :color="tierChipColor(badge.tier)" 
                  variant="flat"
                  class="text-caption"
                >
                  {{ getTierLabel(badge.tier) }}
                </v-chip>
              </div>
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

const tierAvatarColor = (tier: string) => {
  const colors: Record<string, string> = {
    bronze: 'deep-orange',
    silver: 'grey',
    gold: 'amber'
  }
  return colors[tier] ?? 'deep-orange'
}

const tierIconColor = (tier: string) => {
  return 'white'
}

const tierChipColor = (tier: string) => {
  const colors: Record<string, string> = {
    bronze: 'deep-orange',
    silver: 'grey-darken-1',
    gold: 'amber-darken-2'
  }
  return colors[tier] ?? 'deep-orange'
}

const getTierLabel = (tier: string) => {
  const labels: Record<string, string> = {
    bronze: 'برنزی',
    silver: 'نقره‌ای',
    gold: 'طلایی'
  }
  return labels[tier] ?? 'برنزی'
}
</script>

<style scoped>
.badge-display {
  transition: transform 0.2s ease;
}

.badge-display:hover {
  transform: translateY(-2px);
}

.badge-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.badge-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
}

.tier-bronze {
  background: linear-gradient(135deg, rgba(255, 152, 0, 0.1), rgba(255, 152, 0, 0.05));
  border: 1px solid rgba(255, 152, 0, 0.2);
}

.tier-silver {
  background: linear-gradient(135deg, rgba(158, 158, 158, 0.1), rgba(158, 158, 158, 0.05));
  border: 1px solid rgba(158, 158, 158, 0.2);
}

.tier-gold {
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.15), rgba(255, 193, 7, 0.08));
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.min-width-0 {
  min-width: 0;
}

.gap-2 {
  gap: 8px;
}

.gap-3 {
  gap: 12px;
}

@media (max-width: 600px) {
  .badge-card {
    padding: 12px !important;
  }
}
</style>
