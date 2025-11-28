<template>
  <div class="product-share-buttons">
    <v-divider class="mb-3 mt-2"></v-divider>
    <div class="share-section">
      <div class="text-caption text-medium-emphasis mb-2 d-flex align-center gap-2">
        <v-icon size="16" color="grey-darken-1">mdi-share-variant</v-icon>
        <span>اشتراک‌گذاری</span>
      </div>
      <div class="share-buttons-grid">
        <!-- WhatsApp -->
        <a
          :href="whatsappUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="share-btn-link whatsapp-btn"
          title="اشتراک در واتساپ"
        >
          <v-btn
            class="share-btn"
            variant="tonal"
            block
          >
            <v-icon size="20">mdi-whatsapp</v-icon>
          </v-btn>
          <span class="share-label">واتساپ</span>
        </a>

        <!-- Telegram -->
        <a
          :href="telegramUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="share-btn-link telegram-btn"
          title="اشتراک در تلگرام"
        >
          <v-btn
            class="share-btn"
            variant="tonal"
            block
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.13-.31-1.09-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z" fill="currentColor"/>
            </svg>
          </v-btn>
          <span class="share-label">تلگرام</span>
        </a>

        <!-- Eitaa -->
        <a
          :href="eitaaUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="share-btn-link eitaa-btn"
          title="اشتراک در ایتا"
        >
          <v-btn
            class="share-btn"
            variant="tonal"
            block
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5" fill="none"/>
              <path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
            </svg>
          </v-btn>
          <span class="share-label">ایتا</span>
        </a>

        <!-- Rubika -->
        <a
          :href="rubikaUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="share-btn-link rubika-btn"
          title="اشتراک در روبیکا"
        >
          <v-btn
            class="share-btn"
            variant="tonal"
            block
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5" fill="none"/>
              <path d="M12 8v4l3 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
              <circle cx="12" cy="12" r="1.5" fill="currentColor"/>
            </svg>
          </v-btn>
          <span class="share-label">روبیکا</span>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  url: string
  title?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: ''
})

const config = useRuntimeConfig()
const baseUrl = config.public.siteUrl || (process.client ? window.location.origin : 'https://indexo.ir')
const productUrl = computed(() => {
  if (props.url.startsWith('http')) {
    return props.url
  }
  return `${baseUrl}${props.url.startsWith('/') ? props.url : `/${props.url}`}`
})

const encodedUrl = computed(() => encodeURIComponent(productUrl.value))
const encodedTitle = computed(() => encodeURIComponent(props.title || ''))

// WhatsApp sharing URL
const whatsappUrl = computed(() => {
  return `https://wa.me/?text=${encodedUrl.value}`
})

// Telegram sharing URL
const telegramUrl = computed(() => {
  return `https://t.me/share/url?url=${encodedUrl.value}${props.title ? `&text=${encodedTitle.value}` : ''}`
})

// Eitaa sharing URL
const eitaaUrl = computed(() => {
  return `https://eitaa.com/share?url=${encodedUrl.value}`
})

// Rubika sharing URL
const rubikaUrl = computed(() => {
  return `https://rubika.ir/share?url=${encodedUrl.value}`
})
</script>

<style scoped>
.product-share-buttons {
  width: 100%;
}

.share-section {
  width: 100%;
}

.share-buttons-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.5rem;
}

.share-btn-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.375rem;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s ease;
}

.share-btn-link:hover {
  transform: translateY(-1px);
}

.share-btn-link:active {
  transform: translateY(0);
}

.share-btn {
  width: 100%;
  min-width: 40px;
  height: 40px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.share-label {
  font-size: 0.75rem;
  line-height: 1.2;
  text-align: center;
  font-weight: 500;
  color: rgba(var(--v-theme-on-surface), 0.7);
  transition: color 0.2s ease;
}

.share-btn-link:hover .share-label {
  color: rgba(var(--v-theme-on-surface), 0.9);
}

/* WhatsApp Button */
.whatsapp-btn .share-btn {
  color: #25D366 !important;
  background-color: rgba(37, 211, 102, 0.08) !important;
}

.whatsapp-btn:hover .share-btn {
  background-color: rgba(37, 211, 102, 0.12) !important;
}

.whatsapp-btn .share-label {
  color: #25D366;
}

/* Telegram Button */
.telegram-btn .share-btn {
  color: #0088cc !important;
  background-color: rgba(0, 136, 204, 0.08) !important;
}

.telegram-btn:hover .share-btn {
  background-color: rgba(0, 136, 204, 0.12) !important;
}

.telegram-btn .share-label {
  color: #0088cc;
}

.telegram-btn svg {
  width: 20px;
  height: 20px;
}

/* Eitaa Button */
.eitaa-btn .share-btn {
  color: #00A859 !important;
  background-color: rgba(0, 168, 89, 0.08) !important;
}

.eitaa-btn:hover .share-btn {
  background-color: rgba(0, 168, 89, 0.12) !important;
}

.eitaa-btn .share-label {
  color: #00A859;
}

.eitaa-btn svg {
  width: 20px;
  height: 20px;
}

/* Rubika Button */
.rubika-btn .share-btn {
  color: #FF6B35 !important;
  background-color: rgba(255, 107, 53, 0.08) !important;
}

.rubika-btn:hover .share-btn {
  background-color: rgba(255, 107, 53, 0.12) !important;
}

.rubika-btn .share-label {
  color: #FF6B35;
}

.rubika-btn svg {
  width: 20px;
  height: 20px;
}

/* Responsive Design */
@media (max-width: 600px) {
  .share-buttons-grid {
    gap: 0.375rem;
  }
  
  .share-btn {
    height: 36px;
    min-width: 36px;
  }
  
  .share-btn :deep(.v-icon),
  .share-btn svg {
    width: 18px !important;
    height: 18px !important;
  }
  
  .share-label {
    font-size: 0.7rem;
  }
  
  .share-btn-link {
    gap: 0.25rem;
  }
}
</style>

