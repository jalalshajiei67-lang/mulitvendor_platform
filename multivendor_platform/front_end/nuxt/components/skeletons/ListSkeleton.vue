<template>
  <div class="list-skeleton">
    <v-row :class="{ 'flex-column': variant === 'list' }" class="gap-4">
      <template v-for="i in count" :key="i">
        <v-col
          v-if="variant === 'grid'"
          :cols="cols"
          :sm="sm"
          :md="md"
          :lg="lg"
        >
          <component :is="cardComponent" />
        </v-col>
        <v-col
          v-else
          cols="12"
        >
          <component :is="cardComponent" :variant="variant" />
        </v-col>
      </template>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import ProductCardSkeleton from './ProductCardSkeleton.vue'
import BlogCardSkeleton from './BlogCardSkeleton.vue'
import SupplierCardSkeleton from './SupplierCardSkeleton.vue'

const props = withDefaults(
  defineProps<{
    type?: 'product' | 'blog' | 'supplier'
    variant?: 'grid' | 'list'
    count?: number
    cols?: number | string
    sm?: number | string
    md?: number | string
    lg?: number | string
  }>(),
  {
    type: 'product',
    variant: 'grid',
    count: 6,
    cols: 12,
    sm: 6,
    md: 4,
    lg: 3
  }
)

const cardComponent = computed(() => {
  switch (props.type) {
    case 'blog':
      return BlogCardSkeleton
    case 'supplier':
      return SupplierCardSkeleton
    default:
      return ProductCardSkeleton
  }
})
</script>

<style scoped>
.list-skeleton {
  width: 100%;
}
</style>

