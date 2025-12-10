<template>
  <v-tooltip location="bottom" :text="tooltipText" open-delay="100">
    <template #activator="{ props: tooltipProps }">
      <v-avatar
        v-bind="tooltipProps"
        :size="avatarSize"
        :color="tierColors[tier]?.bg || 'grey-lighten-2'"
        class="badge-icon d-inline-flex align-center justify-center"
        variant="flat"
      >
        <v-icon :color="tierColors[tier]?.icon || 'white'" :size="iconSize">
          {{ badge.icon || 'mdi-trophy' }}
        </v-icon>
      </v-avatar>
    </template>
  </v-tooltip>
</template>

<script setup lang="ts">
const props = defineProps<{
  badge: {
    slug: string
    title: string
    icon?: string
    tier?: string
    description?: string
  }
  size?: 'xs' | 'sm' | 'md' | 'lg'
}>()

const tierColors: Record<string, { bg: string; icon: string }> = {
  bronze: { bg: '#d97757', icon: '#fff' },
  silver: { bg: '#9e9e9e', icon: '#fff' },
  gold: { bg: '#f6c343', icon: '#5d4100' },
  diamond: { bg: '#9c27b0', icon: '#fff' }
}

const tier = computed(() => props.badge.tier || 'bronze')
const tooltipText = computed(() => props.badge.description || props.badge.title)

const avatarSize = computed(() => {
  switch (props.size) {
    case 'xs':
      return 28
    case 'sm':
      return 34
    case 'lg':
      return 48
    default:
      return 40
  }
})

const iconSize = computed(() => {
  switch (props.size) {
    case 'xs':
      return 16
    case 'sm':
      return 18
    case 'lg':
      return 24
    default:
      return 20
  }
})
</script>

<style scoped>
.badge-icon {
  border: 1px solid rgba(255, 255, 255, 0.2);
}
</style>

