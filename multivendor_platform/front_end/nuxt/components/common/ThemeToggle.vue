<template>
  <v-btn
    icon
    variant="text"
    size="small"
    :title="isDark ? 'حالت روشن' : 'حالت تاریک'"
    @click="toggleTheme"
    class="theme-toggle-btn"
    :color="isDark ? 'warning' : 'primary'"
  >
    <v-icon>{{ isDark ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
  </v-btn>
</template>

<script setup lang="ts">
const { isDark, toggleTheme } = useAppTheme()
</script>

<style scoped>
.theme-toggle-btn {
  transition: transform 0.2s ease;
}

.theme-toggle-btn:hover {
  transform: scale(1.1);
}
</style>

