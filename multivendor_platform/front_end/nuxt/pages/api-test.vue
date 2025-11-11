<template>
  <v-container fluid dir="rtl" class="api-test">
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">تست اتصال API</h1>
        <v-alert type="info" variant="tonal" class="mb-4">
          این صفحه برای تست اتصال به API استفاده می‌شود. در محیط production این صفحه را حذف کنید.
        </v-alert>
      </v-col>
    </v-row>

    <v-row>
      <!-- Blog Posts Test -->
      <v-col cols="12" md="4">
        <v-card elevation="2" class="h-100">
          <v-card-title>تست پست‌های وبلاگ</v-card-title>
          <v-card-text>
            <v-btn
              color="primary"
              :loading="loading"
              :disabled="loading"
              @click="testBlogPosts"
              block
              class="mb-4"
            >
              تست API پست‌های وبلاگ
            </v-btn>
            <div v-if="postsResult">
              <h3 class="text-subtitle-1 mb-2">نتیجه:</h3>
              <v-textarea
                :model-value="JSON.stringify(postsResult, null, 2)"
                readonly
                variant="outlined"
                rows="10"
                class="font-monospace"
              ></v-textarea>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Blog Categories Test -->
      <v-col cols="12" md="4">
        <v-card elevation="2" class="h-100">
          <v-card-title>تست دسته‌بندی‌های وبلاگ</v-card-title>
          <v-card-text>
            <v-btn
              color="primary"
              :loading="loading"
              :disabled="loading"
              @click="testBlogCategories"
              block
              class="mb-4"
            >
              تست API دسته‌بندی‌های وبلاگ
            </v-btn>
            <div v-if="categoriesResult">
              <h3 class="text-subtitle-1 mb-2">نتیجه:</h3>
              <v-textarea
                :model-value="JSON.stringify(categoriesResult, null, 2)"
                readonly
                variant="outlined"
                rows="10"
                class="font-monospace"
              ></v-textarea>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Direct API Test -->
      <v-col cols="12" md="4">
        <v-card elevation="2" class="h-100">
          <v-card-title>تست مستقیم API</v-card-title>
          <v-card-text>
            <v-btn
              color="primary"
              :loading="loading"
              :disabled="loading"
              @click="testDirectApi"
              block
              class="mb-4"
            >
              تست مستقیم API
            </v-btn>
            <div v-if="directResult">
              <h3 class="text-subtitle-1 mb-2">نتیجه:</h3>
              <v-textarea
                :model-value="JSON.stringify(directResult, null, 2)"
                readonly
                variant="outlined"
                rows="10"
                class="font-monospace"
              ></v-textarea>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Error Display -->
    <v-row v-if="error">
      <v-col cols="12">
        <v-alert type="error" variant="tonal" prominent>
          <v-alert-title>خطا:</v-alert-title>
          <pre class="mt-2">{{ error }}</pre>
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useBlogApi } from '~/composables/useBlogApi'
import { useApiFetch } from '~/composables/useApiFetch'

definePageMeta({
  layout: 'default'
})

useHead({
  title: 'تست API',
  meta: [
    {
      name: 'robots',
      content: 'noindex, nofollow'
    }
  ]
})

const blogApi = useBlogApi()
const loading = ref(false)
const postsResult = ref<any>(null)
const categoriesResult = ref<any>(null)
const directResult = ref<any>(null)
const error = ref<string | null>(null)

const testBlogPosts = async () => {
  loading.value = true
  error.value = null
  postsResult.value = null

  try {
    console.log('Testing blog posts API...')
    const response = await blogApi.getBlogPosts({ page_size: 5 })
    console.log('Blog posts response:', response)
    postsResult.value = response
  } catch (err: any) {
    console.error('Blog posts error:', err)
    error.value = err?.data?.detail || err?.message || 'خطا در اتصال به API'
  } finally {
    loading.value = false
  }
}

const testBlogCategories = async () => {
  loading.value = true
  error.value = null
  categoriesResult.value = null

  try {
    console.log('Testing blog categories API...')
    const response = await blogApi.getBlogCategories()
    console.log('Blog categories response:', response)
    categoriesResult.value = response
  } catch (err: any) {
    console.error('Blog categories error:', err)
    error.value = err?.data?.detail || err?.message || 'خطا در اتصال به API'
  } finally {
    loading.value = false
  }
}

const testDirectApi = async () => {
  loading.value = true
  error.value = null
  directResult.value = null

  try {
    console.log('Testing direct API call...')
    const response = await useApiFetch('blog/posts/', {
      params: { page_size: 5 }
    })
    console.log('Direct API response:', response)
    directResult.value = response
  } catch (err: any) {
    console.error('Direct API error:', err)
    error.value = err?.data?.detail || err?.message || 'خطا در اتصال به API'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.api-test {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.font-monospace {
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>

