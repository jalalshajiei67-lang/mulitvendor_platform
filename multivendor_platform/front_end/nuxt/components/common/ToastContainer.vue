<template>
  <v-snackbar
    v-model="toast.visible"
    :color="toast.color"
    :timeout="toast.timeout"
    location="top"
    multi-line
  >
    {{ toast.message }}
    <template #actions>
      <v-btn variant="text" @click="hideToast">
        بستن
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useToast } from '~/composables/useToast'

const { toastState, hideToast } = useToast()
const toast = computed(() => toastState.value)
</script>



