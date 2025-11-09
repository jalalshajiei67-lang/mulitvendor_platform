<template>
  <v-card rounded="xl" elevation="2" class="product-card" hover @click="openProduct">
    <div class="image-wrapper">
      <v-img
        v-if="product.primary_image"
        :src="product.primary_image"
        :alt="product.title"
        height="220"
        cover
      />
      <div v-else class="no-image">
        <v-icon size="48" color="grey-lighten-1">mdi-cube-outline</v-icon>
      </div>
      <v-chip
        v-if="product.is_featured"
        size="small"
        color="warning"
        class="badge"
      >
        {{ t('featured') }}
      </v-chip>
    </div>

    <v-card-text class="pa-5">
      <v-chip
        v-if="product.category_name"
        size="small"
        class="mb-3"
        color="primary"
        variant="tonal"
      >
        {{ product.category_name }}
      </v-chip>

      <h3 class="text-h6 font-weight-bold mb-2 line-clamp-2">
        {{ product.title }}
      </h3>
      <p class="text-body-2 text-medium-emphasis line-clamp-2 mb-4">
        {{ product.short_description }}
      </p>

      <div class="d-flex align-center justify-space-between">
        <div>
          <div class="text-caption text-medium-emphasis">{{ t('price') }}</div>
          <div class="text-h6 font-weight-bold">
            {{ product.price ? formatPrice(product.price) : t('contactForPrice') }}
          </div>
        </div>
        <v-btn color="primary" variant="tonal">
          {{ t('view') }}
          <v-icon class="mr-2">mdi-arrow-left</v-icon>
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
const props = defineProps<{
  product: Record<string, any>
}>()

const productStore = useProductStore()
const t = productStore.t

const formatPrice = (value: number | string) => {
  const amount = Number(value)
  if (Number.isNaN(amount)) {
    return value
  }

  return new Intl.NumberFormat('fa-IR').format(amount) + ' تومان'
}

const openProduct = () => {
  navigateTo(`/products/${props.product.slug ?? props.product.id}`)
}
</script>

<style scoped>
.product-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.12);
}

.image-wrapper {
  position: relative;
  border-top-left-radius: inherit;
  border-top-right-radius: inherit;
  overflow: hidden;
}

.no-image {
  height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
}

.badge {
  position: absolute;
  top: 14px;
  right: 14px;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

