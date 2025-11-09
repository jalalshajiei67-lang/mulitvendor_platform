<!-- src/views/ProductDetail.vue - Vuetify Material Design 3 -->
<template>
  <v-container fluid class="pa-0 product-detail-container">
    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-16">
      <v-col cols="12" class="text-center">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
        <p class="text-h6 mt-4">{{ t('loadingProduct') }}</p>
      </v-col>
    </v-row>

    <!-- Error State -->
    <v-alert
      v-else-if="error"
      type="error"
      variant="tonal"
      prominent
      class="ma-4"
    >
      <v-row align="center">
        <v-col>
          <div class="text-h6">{{ error }}</div>
        </v-col>
      </v-row>
    </v-alert>

    <!-- Product Content -->
    <div v-else-if="product">
    <!-- Breadcrumbs -->
    <v-breadcrumbs
      :items="breadcrumbItems"
      class="px-2 px-sm-4 py-1 py-sm-2 breadcrumb-rtl"
      divider="/"
    >
        <template v-slot:prepend>
          <v-icon size="small">mdi-home</v-icon>
        </template>
      </v-breadcrumbs>

      <!-- Main Product Section -->
      <v-container class="py-3 py-sm-4 py-md-6">
        <v-row>
          <!-- Product Images Section -->
          <v-col cols="12" md="6" class="mb-4 mb-md-0">
            <v-card elevation="4" rounded="lg">
              <!-- Main Image Carousel -->
              <v-carousel
                v-if="product.images && product.images.length > 0"
                v-model="currentImageIndex"
                :height="display.xs.value ? 300 : display.sm.value ? 400 : 500"
                hide-delimiter-background
                show-arrows="hover"
                :cycle="false"
                :continuous="false"
              >
                <v-carousel-item
                  v-for="(image, index) in product.images"
                  :key="image.id || index"
                  :src="image.image_url || image.image"
                  cover
                  @click="openImageModal(index)"
                  class="cursor-pointer"
                >
                  <template v-slot:placeholder>
                    <v-row
                      class="fill-height ma-0"
                      align="center"
                      justify="center"
                    >
                      <v-progress-circular
                        indeterminate
                        color="primary"
                      ></v-progress-circular>
                    </v-row>
                  </template>
                </v-carousel-item>
              </v-carousel>

              <!-- Fallback if no images -->
              <div v-else class="d-flex align-center justify-center" :style="{ height: display.xs.value ? '300px' : '500px', backgroundColor: '#f5f5f5' }">
                <v-icon :size="display.xs.value ? 48 : 64" color="grey">mdi-image-off</v-icon>
              </div>

              <!-- Thumbnail Strip -->
              <v-card-text v-if="product.images && product.images.length > 1" class="pa-2">
                <v-row dense>
                  <v-col
                    v-for="(image, index) in product.images"
                    :key="'thumb-' + index"
                    cols="2"
                  >
                    <v-img
                      :src="image.image_url || image.image"
                      aspect-ratio="1"
                      cover
                      class="rounded cursor-pointer"
                      :class="{ 'thumbnail-active': currentImageIndex === index }"
                      @click="setCurrentImage(index)"
                    >
                      <template v-slot:placeholder>
                        <v-row
                          class="fill-height ma-0"
                          align="center"
                          justify="center"
                        >
                          <v-progress-circular
                            indeterminate
                            color="primary"
                            size="24"
                          ></v-progress-circular>
                        </v-row>
                      </template>
                    </v-img>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- Product Info Section -->
          <v-col cols="12" md="6">
            <v-card elevation="4" rounded="lg" class="pa-4 pa-sm-5 pa-md-6">
              <!-- Product Title -->
              <h1 class="text-h4 text-sm-h3 font-weight-bold mb-3 mb-sm-4">{{ product.name }}</h1>

              <!-- Category and Vendor -->
              <div class="d-flex align-center mb-3 mb-sm-4 flex-wrap ga-2">
                <v-chip
                  color="primary"
                  variant="elevated"
                  prepend-icon="mdi-tag"
                  :size="display.xs.value ? 'small' : 'default'"
                >
                  {{ product.category_name }}
                </v-chip>

                <v-chip
                  color="secondary"
                  variant="tonal"
                  prepend-icon="mdi-store"
                  :size="display.xs.value ? 'small' : 'default'"
                >
                  {{ t('soldBy') }}: {{ product.vendor_name }}
                </v-chip>
              </div>

              <v-divider class="my-3 my-sm-4"></v-divider>

              <!-- Price -->
              <div class="mb-4 mb-sm-6">
                <div class="text-h5 text-sm-h4 font-weight-bold text-primary">${{ product.price }}</div>
                <div class="text-body-2 text-sm-body-1 text-medium-emphasis mt-2">
                  <v-icon size="small" class="ml-1">mdi-package-variant</v-icon>
                  {{ t('inStock') }}: {{ product.stock }} {{ t('items') || 'عدد' }}
                </div>
              </div>

              <v-divider class="my-3 my-sm-4"></v-divider>

              <!-- Description -->
              <div class="mb-4 mb-sm-6">
                <h3 class="text-subtitle-1 text-sm-h6 font-weight-bold mb-2 mb-sm-3">{{ t('description') }}</h3>
                <div class="text-body-2 text-sm-body-1 text-justify product-description" v-html="product.description"></div>
              </div>

              <!-- Action Buttons -->
              <v-card-actions class="pa-0 flex-column flex-sm-row ga-2 ga-sm-3">
                <v-btn
                  color="primary"
                  :size="display.xs.value ? 'large' : 'x-large'"
                  prepend-icon="mdi-cart-plus"
                  variant="elevated"
                  rounded="lg"
                  :block="display.xs.value"
                  class="flex-sm-grow-1"
                >
                  {{ t('addToCart') }}
                </v-btn>

                <v-btn
                  color="info"
                  :size="display.xs.value ? 'large' : 'x-large'"
                  prepend-icon="mdi-file-document-edit-outline"
                  variant="elevated"
                  rounded="lg"
                  :block="display.xs.value"
                  class="flex-sm-grow-1"
                  @click="showRFQDialog = true"
                >
                  درخواست استعلام قیمت
                </v-btn>

                <v-btn
                  v-if="isOwner"
                  color="warning"
                  :size="display.xs.value ? 'large' : 'x-large'"
                  prepend-icon="mdi-pencil"
                  variant="elevated"
                  rounded="lg"
                  :to="`/products/${product.id}/edit`"
                  :block="display.xs.value"
                >
                  {{ t('editProduct') }}
                </v-btn>

                <v-btn
                  v-if="isOwner"
                  color="error"
                  :size="display.xs.value ? 'large' : 'x-large'"
                  prepend-icon="mdi-delete"
                  variant="elevated"
                  rounded="lg"
                  @click="confirmDelete"
                  :block="display.xs.value"
                >
                  {{ t('deleteProduct') }}
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

        <!-- Comments Section -->
        <v-row class="mt-4 mt-sm-6 mt-md-8">
          <v-col cols="12">
            <v-card elevation="4" rounded="lg">
              <v-card-title class="text-h6 text-sm-h5 font-weight-bold d-flex align-center pa-4 pa-sm-5">
                <v-icon class="ml-2" :size="display.xs.value ? 'default' : 'large'">mdi-comment-multiple</v-icon>
                {{ t('comments') }} ({{ product.comment_count || 0 }})
              </v-card-title>

              <v-divider></v-divider>

              <!-- Average Rating -->
              <v-card-text v-if="product.average_rating" class="pa-3 pa-sm-4">
                <v-chip
                  color="warning"
                  variant="elevated"
                  :size="display.xs.value ? 'default' : 'large'"
                  prepend-icon="mdi-star"
                  class="font-weight-bold"
                >
                  {{ product.average_rating }} / 5
                </v-chip>
                <span class="text-caption text-sm-body-2 text-medium-emphasis mr-2">{{ t('averageRating') }}</span>
              </v-card-text>

              <v-divider v-if="product.average_rating"></v-divider>

              <!-- Comment Form -->
              <v-card-text v-if="isAuthenticated" class="pa-3 pa-sm-4">
                <h3 class="text-subtitle-1 text-sm-h6 font-weight-bold mb-3 mb-sm-4">{{ t('addComment') }}</h3>
                
                <!-- Rating Input -->
                <div class="mb-3 mb-sm-4">
                  <label class="text-body-2 text-sm-body-1 font-weight-bold mb-2 d-block">{{ t('rating') }}:</label>
                  <v-rating
                    v-model="commentForm.rating"
                    color="warning"
                    active-color="warning"
                    hover
                    :size="display.xs.value ? 'default' : 'large'"
                  ></v-rating>
                </div>

                <!-- Comment Text -->
                <v-textarea
                  v-model="commentForm.content"
                  :label="t('writeComment')"
                  variant="outlined"
                  :rows="display.xs.value ? 3 : 4"
                  rounded="lg"
                ></v-textarea>

                <v-btn
                  color="primary"
                  :size="display.xs.value ? 'default' : 'large'"
                  prepend-icon="mdi-send"
                  @click="submitComment"
                  :loading="submittingComment"
                  :disabled="!commentForm.content"
                  variant="elevated"
                  rounded="lg"
                  :block="display.xs.value"
                >
                  {{ submittingComment ? t('saving') : t('submitComment') }}
                </v-btn>
              </v-card-text>

              <!-- Login Prompt -->
              <v-card-text v-else class="pa-3 pa-sm-4">
                <v-alert
                  type="info"
                  variant="tonal"
                  :prominent="!display.xs.value"
                  icon="mdi-account-alert"
                  :text="display.xs.value ? 'لطفاً برای نوشتن نظر وارد شوید' : undefined"
                >
                  <template v-if="!display.xs.value">لطفاً برای نوشتن نظر وارد شوید</template>
                </v-alert>
              </v-card-text>

              <v-divider></v-divider>

              <!-- Comments List -->
              <v-card-text class="pa-3 pa-sm-4">
                <div v-if="!product.comments || product.comments.length === 0" class="text-center py-6 py-sm-8">
                  <v-icon :size="display.xs.value ? 48 : 64" color="grey-lighten-1">mdi-comment-off</v-icon>
                  <p class="text-subtitle-1 text-sm-h6 text-medium-emphasis mt-3 mt-sm-4">{{ t('noCommentsYet') }}</p>
                  <p class="text-caption text-sm-body-2 text-medium-emphasis">{{ t('beTheFirst') }}</p>
                </div>

                <div v-else>
                  <v-list :lines="display.xs.value ? 'two' : 'three'">
                    <template v-for="comment in topLevelComments" :key="comment.id">
                      <v-list-item class="px-0">
                        <template v-slot:prepend>
                          <v-avatar color="primary" :size="display.xs.value ? 40 : 48">
                            <v-icon :size="display.xs.value ? 'small' : 'default'">mdi-account</v-icon>
                          </v-avatar>
                        </template>

                        <v-list-item-title class="font-weight-bold mb-1 text-body-2 text-sm-body-1">
                          {{ comment.author_name }}
                          <v-rating
                            :model-value="comment.rating"
                            color="warning"
                            density="compact"
                            :size="display.xs.value ? 'x-small' : 'small'"
                            readonly
                            class="d-inline-flex mr-2"
                          ></v-rating>
                        </v-list-item-title>

                        <v-list-item-subtitle class="text-caption mb-1 mb-sm-2">
                          {{ formatDate(comment.created_at) }}
                        </v-list-item-subtitle>

                        <div class="text-body-2 text-sm-body-1 mt-1 mt-sm-2">{{ comment.content }}</div>

                        <template v-slot:append>
                          <v-btn
                            v-if="isAuthenticated"
                            variant="text"
                            :size="display.xs.value ? 'x-small' : 'small'"
                            prepend-icon="mdi-reply"
                            @click="replyToComment(comment)"
                          >
                            {{ display.xs.value ? '' : t('reply') }}
                          </v-btn>
                        </template>
                      </v-list-item>

                      <!-- Replies -->
                      <v-list
                        v-if="comment.replies && comment.replies.length > 0"
                        class="pr-6 pr-sm-12"
                      >
                        <v-list-item
                          v-for="reply in comment.replies"
                          :key="reply.id"
                          class="px-0"
                        >
                          <template v-slot:prepend>
                            <v-avatar color="secondary" :size="display.xs.value ? 32 : 40">
                              <v-icon :size="display.xs.value ? 'x-small' : 'small'">mdi-account</v-icon>
                            </v-avatar>
                          </template>

                          <v-list-item-title class="font-weight-bold mb-1 text-body-2 text-sm-body-1">
                            {{ reply.author_name }}
                            <v-rating
                              :model-value="reply.rating"
                              color="warning"
                              density="compact"
                              :size="display.xs.value ? 'x-small' : 'small'"
                              readonly
                              class="d-inline-flex mr-2"
                            ></v-rating>
                          </v-list-item-title>

                          <v-list-item-subtitle class="text-caption mb-1 mb-sm-2">
                            {{ formatDate(reply.created_at) }}
                          </v-list-item-subtitle>

                          <div class="text-body-2 text-sm-body-1 mt-1 mt-sm-2">{{ reply.content }}</div>
                        </v-list-item>
                      </v-list>

                      <v-divider class="my-3 my-sm-4"></v-divider>
                    </template>
                  </v-list>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>

    <!-- Image Modal Dialog with Zoom -->
    <v-dialog
      v-model="showImageModal"
      fullscreen
      transition="dialog-bottom-transition"
    >
      <v-card color="black">
        <v-toolbar color="black" dark :density="display.xs.value ? 'compact' : 'default'">
          <v-toolbar-title :class="display.xs.value ? 'text-body-2' : 'text-h6'">
            {{ display.xs.value ? `${modalImageIndex + 1}/${product?.images?.length}` : `${product?.name} - ${t('image') || 'تصویر'} ${modalImageIndex + 1} / ${product?.images?.length}` }}
          </v-toolbar-title>
          <v-spacer></v-spacer>

          <!-- Zoom Controls - Hide on mobile for space -->
          <template v-if="!display.xs.value">
            <v-btn icon @click="zoomOut" :disabled="zoomLevel <= 0.5">
              <v-icon>mdi-magnify-minus</v-icon>
            </v-btn>
            <v-btn icon @click="resetZoom">
              <v-icon>mdi-fit-to-page</v-icon>
            </v-btn>
            <v-btn icon @click="zoomIn" :disabled="zoomLevel >= 3">
              <v-icon>mdi-magnify-plus</v-icon>
            </v-btn>
          </template>

          <v-btn icon @click="closeImageModal">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>

        <v-card-text class="pa-0 d-flex align-center justify-center" style="height: calc(100vh - 64px); overflow: hidden;">
          <v-img
            v-if="modalImageUrl"
            :src="modalImageUrl"
            max-height="100%"
            max-width="100%"
            contain
            :style="{ transform: `scale(${zoomLevel})`, cursor: 'move' }"
            @wheel.prevent="handleWheel"
          ></v-img>
        </v-card-text>

        <!-- Navigation Arrows -->
        <v-btn
          v-if="product?.images && product.images.length > 1"
          icon
          :size="display.xs.value ? 'default' : 'large'"
          color="white"
          class="modal-nav-btn modal-nav-right"
          @click="previousModalImage"
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>

        <v-btn
          v-if="product?.images && product.images.length > 1"
          icon
          :size="display.xs.value ? 'default' : 'large'"
          color="white"
          class="modal-nav-btn modal-nav-left"
          @click="nextModalImage"
        >
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>

        <!-- Thumbnail Strip at Bottom -->
        <div
          v-if="product?.images && product.images.length > 1"
          class="modal-thumbnails"
        >
          <v-sheet color="black" class="pa-2 pa-sm-4">
            <v-row dense justify="center">
              <v-col
                v-for="(image, index) in product.images"
                :key="'modal-thumb-' + index"
                cols="auto"
              >
                <v-img
                  :src="image.image_url || image.image"
                  :width="display.xs.value ? 60 : 80"
                  :height="display.xs.value ? 60 : 80"
                  cover
                  class="rounded cursor-pointer"
                  :class="{ 'modal-thumbnail-active': modalImageIndex === index }"
                  @click="setModalImage(index)"
                ></v-img>
              </v-col>
            </v-row>
          </v-sheet>
        </div>
      </v-card>
    </v-dialog>

    <!-- RFQ Form Dialog -->
    <RFQForm
      v-model="showRFQDialog"
      :product-id="product?.id"
      :category-id="product?.primary_category"
      @submitted="handleRFQSubmitted"
      @error="handleRFQError"
    />

    <!-- RFQ Success/Error Snackbar -->
    <v-snackbar
      v-model="rfqSuccess"
      color="success"
      :timeout="3000"
      location="top"
    >
      درخواست استعلام قیمت با موفقیت ارسال شد
    </v-snackbar>

    <v-snackbar
      v-model="rfqError"
      color="error"
      :timeout="5000"
      location="top"
    >
      {{ rfqError }}
    </v-snackbar>
  </v-container>
</template>

<script>
import { useProductStore } from '@/stores/modules/productStore'
import { useAuthStore } from '@/stores/auth'
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDisplay } from 'vuetify'
import { useHead } from '@unhead/vue'
import RFQForm from '@/components/RFQForm.vue'

export default {
  name: 'ProductDetail',
  components: {
    RFQForm
  },
  setup() {
    const productStore = useProductStore()
    const authStore = useAuthStore()
    const route = useRoute()
    const router = useRouter()
    const display = useDisplay()

    const productSlug = ref(route.params.slug)
    const currentImageIndex = ref(0)
    const showImageModal = ref(false)
    const modalImageUrl = ref('')
    const modalImageIndex = ref(0)
    const zoomLevel = ref(1)
    const commentForm = ref({
      content: '',
      rating: 5,
      parent: null
    })
    const submittingComment = ref(false)
    const showRFQDialog = ref(false)
    const rfqError = ref(null)
    const rfqSuccess = ref(false)

    const product = computed(() => productStore.currentProduct)
    const loading = computed(() => productStore.loading)
    const error = computed(() => productStore.error)
    const isAuthenticated = computed(() => authStore.isAuthenticated)

    const isOwner = computed(() => {
      return (
        authStore.isAuthenticated && product.value && authStore.user.id === product.value.vendor
      )
    })

    const topLevelComments = computed(() => {
      if (!product.value || !product.value.comments) return []
      return product.value.comments.filter(comment => !comment.parent)
    })

    const breadcrumbItems = computed(() => {
      if (!product.value) {
        return [
          { title: t.value('home'), to: '/', disabled: false },
          { title: t.value('products'), to: '/products', disabled: false },
          { title: t.value('loading'), disabled: true }
        ]
      }

      const items = [
        { title: t.value('home'), to: '/', disabled: false },
      ]

      if (product.value.breadcrumb_hierarchy && product.value.breadcrumb_hierarchy.length > 0) {
        product.value.breadcrumb_hierarchy.forEach(item => {
          items.push({
            title: item.name,
            to: `/${item.type}s/${item.slug}`,
            disabled: false
          })
        })
      } else {
        items.push({ title: t.value('products'), to: '/products', disabled: false })
      }

      items.push({ title: product.value.name, disabled: true })

      return items
    })

    const stripHtml = (text) => {
      if (typeof text !== 'string') {
        return ''
      }
      return text.replace(/<[^>]+>/g, ' ')
    }

    const truncate = (text, maxLength = 160) => {
      if (typeof text !== 'string') {
        return undefined
      }
      const clean = text.replace(/\s+/g, ' ').trim()
      if (!clean) {
        return undefined
      }
      if (clean.length <= maxLength) {
        return clean
      }
      return `${clean.slice(0, maxLength - 3)}...`
    }

    const fallbackDescription = 'مشخصات کامل محصول و نحوه همکاری با تامین‌کننده در ایندکسو.'

    const productSummary = computed(() => {
      if (!product.value) {
        return fallbackDescription
      }

      const descriptionCandidates = [
        product.value.meta_description,
        product.value.short_description,
        stripHtml(product.value.description)
      ].filter(candidate => typeof candidate === 'string' && candidate.trim().length > 0)

      if (!descriptionCandidates.length) {
        return fallbackDescription
      }

      return truncate(descriptionCandidates[0]) || fallbackDescription
    })

    const productPrimaryImage = computed(() => {
      if (!product.value) {
        return undefined
      }
      if (product.value.primary_image) {
        return product.value.primary_image
      }
      if (product.value.cover_image) {
        return product.value.cover_image
      }
      if (product.value.images && product.value.images.length > 0) {
        const firstImage = product.value.images[0]
        return firstImage.image_url || firstImage.image
      }
      return undefined
    })

    const staticOrigin = import.meta.env.VITE_SITE_URL || ''

    const canonicalUrl = computed(() => {
      const origin = typeof window !== 'undefined' && window.location?.origin
        ? window.location.origin
        : staticOrigin

      if (!origin) {
        return undefined
      }

      return `${origin.replace(/\/+$/, '')}${route.fullPath}`
    })

    useHead(() => {
      const title = product.value?.name || 'جزئیات محصول'
      const description = productSummary.value
      const image = productPrimaryImage.value
      const url = canonicalUrl.value

      const metaTags = [
        {
          key: 'og:type',
          property: 'og:type',
          content: 'product'
        },
        title && {
          key: 'og:title',
          property: 'og:title',
          content: title
        },
        description && {
          key: 'description',
          name: 'description',
          content: description
        },
        description && {
          key: 'og:description',
          property: 'og:description',
          content: description
        },
        url && {
          key: 'og:url',
          property: 'og:url',
          content: url
        },
        image && {
          key: 'og:image',
          property: 'og:image',
          content: image
        },
        title && {
          key: 'twitter:title',
          name: 'twitter:title',
          content: title
        },
        description && {
          key: 'twitter:description',
          name: 'twitter:description',
          content: description
        },
        image && {
          key: 'twitter:image',
          name: 'twitter:image',
          content: image
        },
        {
          key: 'twitter:card',
          name: 'twitter:card',
          content: image ? 'summary_large_image' : 'summary'
        }
      ].filter(Boolean)

      const linkTags = url
        ? [
            {
              key: 'canonical',
              rel: 'canonical',
              href: url
            }
          ]
        : []

      return {
        title,
        meta: metaTags,
        link: linkTags
      }
    })

    const setCurrentImage = (index) => {
      currentImageIndex.value = index
    }

    const openImageModal = (index) => {
      if (product.value?.images) {
        modalImageIndex.value = index
        const image = product.value.images[index]
        modalImageUrl.value = image.image_url || image.image
      }
      showImageModal.value = true
      zoomLevel.value = 1
    }

    const closeImageModal = () => {
      showImageModal.value = false
      modalImageUrl.value = ''
      zoomLevel.value = 1
    }

    const nextModalImage = () => {
      if (!product.value?.images) return
      modalImageIndex.value = (modalImageIndex.value + 1) % product.value.images.length
      const nextImage = product.value.images[modalImageIndex.value]
      modalImageUrl.value = nextImage.image_url || nextImage.image
      zoomLevel.value = 1
    }

    const previousModalImage = () => {
      if (!product.value?.images) return
      modalImageIndex.value = modalImageIndex.value === 0
        ? product.value.images.length - 1
        : modalImageIndex.value - 1
      const prevImage = product.value.images[modalImageIndex.value]
      modalImageUrl.value = prevImage.image_url || prevImage.image
      zoomLevel.value = 1
    }

    const setModalImage = (index) => {
      if (!product.value?.images) return
      modalImageIndex.value = index
      const image = product.value.images[index]
      modalImageUrl.value = image.image_url || image.image
      zoomLevel.value = 1
    }

    const zoomIn = () => {
      if (zoomLevel.value < 3) {
        zoomLevel.value += 0.25
      }
    }

    const zoomOut = () => {
      if (zoomLevel.value > 0.5) {
        zoomLevel.value -= 0.25
      }
    }

    const resetZoom = () => {
      zoomLevel.value = 1
    }

    const handleWheel = (event) => {
      event.preventDefault()
      if (event.deltaY < 0) {
        zoomIn()
      } else {
        zoomOut()
      }
    }

    const handleKeyPress = (event) => {
      if (!showImageModal.value) return

      switch(event.key) {
        case 'ArrowLeft':
          nextModalImage()
          break
        case 'ArrowRight':
          previousModalImage()
          break
        case 'Escape':
          closeImageModal()
          break
        case '+':
        case '=':
          zoomIn()
          break
        case '-':
        case '_':
          zoomOut()
          break
        case '0':
          resetZoom()
          break
      }
    }

    const confirmDelete = () => {
      if (confirm(t.value('confirmDelete') + ` "${product.value.name}"?`)) {
        productStore
          .deleteProduct(product.value.id)
          .then(() => {
            router.push('/products')
          })
          .catch((error) => {
            console.error('Error deleting product:', error)
          })
      }
    }

    const handleRFQSubmitted = (data) => {
      rfqSuccess.value = true
      showRFQDialog.value = false
    }

    const handleRFQError = (errorMessage) => {
      rfqError.value = errorMessage
    }

    const submitComment = async () => {
      if (!commentForm.value.content || !product.value?.id) return

      submittingComment.value = true
      try {
        await productStore.createProductComment(product.value.id, commentForm.value)
        commentForm.value.content = ''
        commentForm.value.rating = 5
        commentForm.value.parent = null
        alert(t.value('commentSubmitted') || 'نظر شما ثبت شد')
      } catch (error) {
        console.error('Error submitting comment:', error)
        alert(t.value('failedToSubmitComment') || 'خطا در ثبت نظر')
      } finally {
        submittingComment.value = false
      }
    }

    const replyToComment = (comment) => {
      commentForm.value.parent = comment.id
      commentForm.value.content = `@${comment.author_name} `
      window.scrollTo({ top: document.querySelector('.comment-form')?.offsetTop || 0, behavior: 'smooth' })
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('fa-IR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    onMounted(() => {
      if (productSlug.value) {
        productStore.fetchProductBySlug(productSlug.value)
      }
      window.addEventListener('keydown', handleKeyPress)
    })

    onUnmounted(() => {
      window.removeEventListener('keydown', handleKeyPress)
    })

    watch(
      () => route.params.slug,
      async (newSlug) => {
        productSlug.value = newSlug
        currentImageIndex.value = 0
        if (newSlug) {
          try {
            await productStore.fetchProductBySlug(newSlug)
          } catch (error) {
            console.error('Error fetching product by slug:', error)
          }
        }
      },
    )

    watch(
      () => product.value,
      (newProduct) => {
        if (newProduct) {
          currentImageIndex.value = 0
        }
      }
    )

    const t = computed(() => productStore.t)

    return {
      product,
      loading,
      error,
      isOwner,
      isAuthenticated,
      breadcrumbItems,
      currentImageIndex,
      showImageModal,
      modalImageUrl,
      modalImageIndex,
      zoomLevel,
      commentForm,
      submittingComment,
      topLevelComments,
      showRFQDialog,
      rfqError,
      rfqSuccess,
      handleRFQSubmitted,
      handleRFQError,
      display,
      setCurrentImage,
      openImageModal,
      closeImageModal,
      nextModalImage,
      previousModalImage,
      setModalImage,
      zoomIn,
      zoomOut,
      resetZoom,
      handleWheel,
      confirmDelete,
      submitComment,
      replyToComment,
      formatDate,
      t,
      Math,
      productSlug
    }
  },
}
</script>

<style scoped>
/* Breadcrumb RTL styling */
.breadcrumb-rtl {
  direction: rtl;
}

/* Thumbnail active state */
.thumbnail-active {
  border: 3px solid rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 0 0 2px rgba(var(--v-theme-primary), 0.3);
}

.cursor-pointer {
  cursor: pointer;
}

/* Modal navigation buttons */
.modal-nav-btn {
  position: fixed;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1000;
  opacity: 0.8;
  transition: opacity 0.3s;
}

.modal-nav-btn:hover {
  opacity: 1;
}

.modal-nav-right {
  right: 20px;
}

.modal-nav-left {
  left: 20px;
}

/* Modal thumbnails */
.modal-thumbnails {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.modal-thumbnail-active {
  border: 3px solid rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 0 10px rgba(var(--v-theme-primary), 0.8);
}

/* Responsive adjustments */
@media (max-width: 960px) {
  .modal-nav-btn {
    width: 40px;
    height: 40px;
  }

  .modal-nav-right {
    right: 10px;
  }

  .modal-nav-left {
    left: 10px;
  }
}

/* Mobile specific adjustments */
@media (max-width: 600px) {
  .modal-nav-btn {
    width: 36px;
    height: 36px;
    opacity: 0.7;
  }

  .modal-nav-right {
    right: 5px;
  }

  .modal-nav-left {
    left: 5px;
  }
}

/* Container width improvements for better desktop experience */
.product-detail-container {
  max-width: 100%;
  padding-left: 16px;
  padding-right: 16px;
}

@media (min-width: 960px) {
  .product-detail-container {
    max-width: 100%;
    padding-left: 24px;
    padding-right: 24px;
  }
}

@media (min-width: 1280px) {
  .product-detail-container {
    max-width: 1600px;
    margin: 0 auto;
    padding-left: 32px;
    padding-right: 32px;
  }
}

@media (min-width: 1920px) {
  .product-detail-container {
    max-width: 1800px;
    margin: 0 auto;
    padding-left: 40px;
    padding-right: 40px;
  }
}

/* Product Description HTML Content Styling */
.product-description {
  line-height: 1.8;
  direction: rtl;
}

.product-description h2,
.product-description h3,
.product-description h4 {
  font-weight: bold;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: rgb(var(--v-theme-primary));
}

.product-description h2 {
  font-size: 1.5rem;
}

.product-description h3 {
  font-size: 1.25rem;
}

.product-description p {
  margin-bottom: 1rem;
  text-align: justify;
}

.product-description img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 15px auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.product-description table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  background: #fff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  border-radius: 8px;
  overflow: hidden;
}

.product-description table td {
  padding: 12px;
  border: 1px solid #ddd;
}

.product-description table tr:nth-child(even) {
  background-color: #f8f9fa;
}

.product-description table tr:hover {
  background-color: #f0f0f0;
}

.product-description ul,
.product-description ol {
  margin: 1rem 0;
  padding-right: 2rem;
}

.product-description li {
  margin-bottom: 0.5rem;
}

/* Responsive adjustments for description */
@media (max-width: 600px) {
  .product-description h2 {
    font-size: 1.25rem;
  }

  .product-description h3 {
    font-size: 1.1rem;
  }

  .product-description table {
    font-size: 0.875rem;
  }

  .product-description table td {
    padding: 8px;
  }
}
</style>
