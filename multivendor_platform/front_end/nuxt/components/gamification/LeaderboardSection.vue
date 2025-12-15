<template>
  <v-card elevation="2" rounded="xl" class="leaderboard-section">
    <v-card-title class="pa-6 d-flex align-center justify-space-between">
      <div class="d-flex align-center gap-2">
        <v-icon size="28" color="primary">mdi-trophy</v-icon>
        <span class="text-h6 font-weight-bold">فروشندگان پیشرو</span>
      </div>
      <v-chip
        v-if="userRank"
        color="primary"
        variant="tonal"
        size="small"
      >
        رتبه شما: {{ userRank }}
      </v-chip>
    </v-card-title>

    <v-divider />

    <v-card-text class="pa-4">
      <v-list v-if="leaderboard.length > 0" density="comfortable" class="pa-0">
        <v-list-item
          v-for="(entry, index) in leaderboard"
          :key="index"
          rounded="lg"
          class="mb-2"
          :class="{ 'user-entry': isCurrentUser(entry) }"
        >
          <template #prepend>
            <v-avatar
              :color="getRankColor(index + 1)"
              size="48"
              class="rank-avatar"
            >
              <v-icon v-if="index < 3" size="24" color="white">
                {{ getRankIcon(index + 1) }}
              </v-icon>
              <span v-else class="text-h6 font-weight-bold text-white">
                {{ index + 1 }}
              </span>
            </v-avatar>
          </template>

          <v-list-item-title class="font-weight-bold text-body-1">
            {{ entry.vendor }}
          </v-list-item-title>

          <v-list-item-subtitle class="d-flex align-center gap-2 mt-1">
            <v-chip size="x-small" variant="text" density="compact">
              <v-icon start size="16">mdi-star</v-icon>
              {{ entry.points.toLocaleString('fa-IR') }}
            </v-chip>
            <v-chip
              v-if="entry.streak > 0"
              size="x-small"
              variant="text"
              density="compact"
            >
              <v-icon start size="16" color="orange">mdi-fire</v-icon>
              {{ entry.streak }} روز
            </v-chip>
            <v-chip
              v-if="entry.tier"
              :color="getTierColor(entry.tier)"
              size="x-small"
              variant="tonal"
              density="compact"
            >
              {{ getTierDisplay(entry.tier) }}
            </v-chip>
          </v-list-item-subtitle>
        </v-list-item>
      </v-list>

      <v-alert
        v-else
        type="info"
        variant="tonal"
        rounded="lg"
        density="compact"
      >
        با فعالیت مستمر و جلب رضایت مشتریان، نام شما در اینجا خواهد درخشید.
      </v-alert>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
interface LeaderboardEntry {
  vendor: string
  points: number
  streak: number
  tier: string
  reputation_score?: number
}

defineProps<{
  leaderboard: LeaderboardEntry[]
  userRank: number | null
  currentUserName?: string
}>()

const getRankColor = (rank: number): string => {
  const colors: Record<number, string> = {
    1: 'amber',
    2: 'grey',
    3: 'deep-orange'
  }
  return colors[rank] || 'primary'
}

const getRankIcon = (rank: number): string => {
  const icons: Record<number, string> = {
    1: 'mdi-trophy',
    2: 'mdi-medal',
    3: 'mdi-medal-outline'
  }
  return icons[rank] || 'mdi-account'
}

const getTierColor = (tier: string): string => {
  const colors: Record<string, string> = {
    diamond: 'purple',
    gold: 'amber',
    silver: 'grey',
    bronze: 'brown',
    inactive: 'red'
  }
  return colors[tier] || 'grey'
}

const getTierDisplay = (tier: string): string => {
  const displays: Record<string, string> = {
    diamond: 'الماس',
    gold: 'طلا',
    silver: 'نقره',
    bronze: 'برنز',
    inactive: 'غیرفعال'
  }
  return displays[tier] || tier
}

const isCurrentUser = (entry: LeaderboardEntry): boolean => {
  // This would need to be enhanced to properly identify current user
  return false
}
</script>

<style scoped>
.leaderboard-section {
  height: 100%;
}

.rank-avatar {
  font-weight: 800;
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.user-entry {
  background: rgba(var(--v-theme-primary), 0.1);
  border: 2px solid rgb(var(--v-theme-primary));
}

.v-list-item {
  transition: transform 0.2s ease, background-color 0.2s ease;
}

.v-list-item:hover {
  transform: translateX(-4px);
  background: rgba(var(--v-theme-primary), 0.05);
}
</style>

