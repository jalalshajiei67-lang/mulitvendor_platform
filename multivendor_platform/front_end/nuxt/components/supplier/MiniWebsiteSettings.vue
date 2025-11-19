<template>
  <div class="mini-website-settings" dir="rtl">
    <v-card elevation="2">
      <v-card-title class="text-h5 font-weight-bold d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <v-icon color="primary" class="me-2">mdi-palette</v-icon>
          تنظیمات وب‌سایت مینی
        </div>
        <ClientOnly>
          <div v-if="supplierId" class="text-caption text-medium-emphasis">
            <v-icon size="small" class="me-1">mdi-link</v-icon>
            <a 
              :href="fullPreviewUrl" 
              target="_blank" 
              class="text-decoration-none"
              @click.stop
            >
              {{ previewUrl }}
            </a>
          </div>
        </ClientOnly>
      </v-card-title>

      <v-card-text>
        <v-form ref="formRef" v-model="formValid">
          <!-- Branding Section -->
          <v-card class="mb-4" elevation="1">
            <v-card-title class="text-subtitle-1 font-weight-bold bg-grey-lighten-4">
              <v-icon size="small" class="me-2">mdi-brush</v-icon>
              برندینگ و ظاهر
            </v-card-title>
            <v-card-text>
              <v-row>
                <!-- Banner Image -->
                <v-col cols="12">
                  <div class="mb-2 text-subtitle-2 font-weight-bold">تصویر بنر (1920x400 پیکسل)</div>
                  <div v-if="previewBanner" class="mb-3">
                    <v-img :src="previewBanner" height="200" cover class="rounded">
                      <v-btn
                        icon="mdi-close"
                        size="small"
                        color="error"
                        class="ma-2"
                        @click="removeBanner"
                      ></v-btn>
                    </v-img>
                  </div>
                  <v-file-input
                    v-model="bannerFile"
                    label="انتخاب تصویر بنر"
                    prepend-icon="mdi-image"
                    accept="image/*"
                    @change="onBannerChange"
                    variant="outlined"
                    density="comfortable"
                  ></v-file-input>
                </v-col>

                <!-- Brand Colors -->
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.brand_color_primary"
                    label="رنگ اصلی برند"
                    type="color"
                    prepend-icon="mdi-palette"
                    variant="outlined"
                    density="comfortable"
                    hint="رنگ اصلی که در سراسر سایت استفاده می‌شود"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.brand_color_secondary"
                    label="رنگ ثانویه برند"
                    type="color"
                    prepend-icon="mdi-palette"
                    variant="outlined"
                    density="comfortable"
                    hint="رنگ ثانویه برای تنوع بصری"
                  ></v-text-field>
                </v-col>

                <!-- Slogan -->
                <v-col cols="12">
                  <v-text-field
                    v-model="formData.slogan"
                    label="شعار شرکت"
                    prepend-icon="mdi-text-short"
                    variant="outlined"
                    density="comfortable"
                    placeholder="مثال: بهترین تولیدکننده ماشین‌آلات صنعتی"
                    counter="200"
                    :rules="[v => !v || v.length <= 200 || 'حداکثر 200 کاراکتر']"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- Company Information -->
          <v-card class="mb-4" elevation="1">
            <v-card-title class="text-subtitle-1 font-weight-bold bg-grey-lighten-4">
              <v-icon size="small" class="me-2">mdi-domain</v-icon>
              اطلاعات شرکت
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model.number="formData.year_established"
                    label="سال تاسیس"
                    prepend-icon="mdi-calendar"
                    type="number"
                    variant="outlined"
                    density="comfortable"
                    :min="1900"
                    :max="new Date().getFullYear()"
                    placeholder="مثال: 1395"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model.number="formData.employee_count"
                    label="تعداد کارمندان"
                    prepend-icon="mdi-account-group"
                    type="number"
                    variant="outlined"
                    density="comfortable"
                    :min="1"
                    placeholder="مثال: 50"
                  ></v-text-field>
                </v-col>

                <v-col cols="12">
                  <v-text-field
                    v-model="formData.video_url"
                    label="لینک ویدیو معرفی"
                    prepend-icon="mdi-video"
                    variant="outlined"
                    density="comfortable"
                    placeholder="لینک یوتیوب یا آپارات"
                    hint="ویدیوی معرفی شرکت شما"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- Certifications & Awards -->
          <v-card class="mb-4" elevation="1">
            <v-card-title class="text-subtitle-1 font-weight-bold bg-grey-lighten-4">
              <v-icon size="small" class="me-2">mdi-certificate</v-icon>
              گواهینامه‌ها و جوایز
            </v-card-title>
            <v-card-text>
              <!-- Certifications -->
              <div class="mb-4">
                <div class="d-flex align-center justify-space-between mb-2">
                  <div class="text-subtitle-2 font-weight-bold">گواهینامه‌ها</div>
                  <v-btn
                    size="small"
                    color="primary"
                    prepend-icon="mdi-plus"
                    @click="addCertification"
                  >
                    افزودن گواهینامه
                  </v-btn>
                </div>
                <v-card
                  v-for="(cert, index) in certifications"
                  :key="index"
                  class="mb-2"
                  variant="outlined"
                >
                  <v-card-text class="pa-3">
                    <v-row dense>
                      <v-col cols="12" md="5">
                        <v-text-field
                          v-model="cert.title"
                          label="عنوان گواهینامه"
                          density="compact"
                          variant="outlined"
                          hide-details
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="4">
                        <v-text-field
                          v-model="cert.issuer"
                          label="صادرکننده"
                          density="compact"
                          variant="outlined"
                          hide-details
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="2">
                        <v-text-field
                          v-model="cert.date"
                          label="تاریخ"
                          density="compact"
                          variant="outlined"
                          hide-details
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="1" class="d-flex align-center">
                        <v-btn
                          icon="mdi-delete"
                          size="small"
                          color="error"
                          variant="text"
                          @click="removeCertification(index)"
                        ></v-btn>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </div>

              <!-- Awards -->
              <div>
                <div class="d-flex align-center justify-space-between mb-2">
                  <div class="text-subtitle-2 font-weight-bold">جوایز</div>
                  <v-btn
                    size="small"
                    color="primary"
                    prepend-icon="mdi-plus"
                    @click="addAward"
                  >
                    افزودن جایزه
                  </v-btn>
                </div>
                <v-card
                  v-for="(award, index) in awards"
                  :key="index"
                  class="mb-2"
                  variant="outlined"
                >
                  <v-card-text class="pa-3">
                    <v-row dense>
                      <v-col cols="12" md="4">
                        <v-text-field
                          v-model="award.title"
                          label="عنوان جایزه"
                          density="compact"
                          variant="outlined"
                          hide-details
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="3">
                        <v-text-field
                          v-model="award.issuer"
                          label="اهدا کننده"
                          density="compact"
                          variant="outlined"
                          hide-details
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="2">
                        <v-text-field
                          v-model="award.year"
                          label="سال"
                          density="compact"
                          variant="outlined"
                          hide-details
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="2">
                        <v-text-field
                          v-model="award.description"
                          label="توضیحات"
                          density="compact"
                          variant="outlined"
                          hide-details
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="1" class="d-flex align-center">
                        <v-btn
                          icon="mdi-delete"
                          size="small"
                          color="error"
                          variant="text"
                          @click="removeAward(index)"
                        ></v-btn>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </div>
            </v-card-text>
          </v-card>

          <!-- Social Media -->
          <v-card class="mb-4" elevation="1">
            <v-card-title class="text-subtitle-2 font-weight-bold bg-grey-lighten-4">
              <v-icon size="small" class="me-2">mdi-share-variant</v-icon>
              شبکه‌های اجتماعی
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="socialMedia.linkedin"
                    label="لینکدین"
                    prepend-icon="mdi-linkedin"
                    variant="outlined"
                    density="comfortable"
                    placeholder="https://linkedin.com/company/..."
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="socialMedia.instagram"
                    label="اینستاگرام"
                    prepend-icon="mdi-instagram"
                    variant="outlined"
                    density="comfortable"
                    placeholder="https://instagram.com/..."
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="socialMedia.telegram"
                    label="تلگرام"
                    prepend-icon="mdi-telegram"
                    variant="outlined"
                    density="comfortable"
                    placeholder="https://t.me/..."
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="socialMedia.whatsapp"
                    label="واتساپ"
                    prepend-icon="mdi-whatsapp"
                    variant="outlined"
                    density="comfortable"
                    placeholder="https://wa.me/..."
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- SEO Settings -->
          <v-card class="mb-4" elevation="1">
            <v-card-title class="text-subtitle-1 font-weight-bold bg-grey-lighten-4">
              <v-icon size="small" class="me-2">mdi-search-web</v-icon>
              تنظیمات سئو
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="formData.meta_title"
                    label="عنوان سئو"
                    prepend-icon="mdi-format-title"
                    variant="outlined"
                    density="comfortable"
                    counter="60"
                    hint="عنوانی که در نتایج گوگل نمایش داده می‌شود"
                    :rules="[v => !v || v.length <= 60 || 'حداکثر 60 کاراکتر']"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-textarea
                    v-model="formData.meta_description"
                    label="توضیحات سئو"
                    prepend-icon="mdi-text"
                    variant="outlined"
                    rows="3"
                    counter="160"
                    hint="توضیحاتی که در نتایج گوگل نمایش داده می‌شود"
                    :rules="[v => !v || v.length <= 160 || 'حداکثر 160 کاراکتر']"
                  ></v-textarea>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-form>
      </v-card-text>

      <v-card-actions class="px-4 pb-4">
        <v-btn
          color="primary"
          size="large"
          prepend-icon="mdi-content-save"
          :loading="saving"
          :disabled="!formValid"
          @click="saveSettings"
        >
          ذخیره تنظیمات
        </v-btn>
        <v-btn
          color="secondary"
          size="large"
          variant="outlined"
          prepend-icon="mdi-eye"
          :disabled="!supplierId || loadingSettings"
          :loading="loadingSettings"
          @click="previewWebsite"
        >
          پیش‌نمایش سایت
        </v-btn>
        <ClientOnly>
          <v-btn
            v-if="supplierId"
            icon="mdi-content-copy"
            size="small"
            variant="text"
            @click="copyPreviewUrl"
            class="ms-2"
          >
            <v-tooltip activator="parent" location="top">کپی لینک</v-tooltip>
          </v-btn>
        </ClientOnly>
        <v-spacer></v-spacer>
        <v-btn
          variant="text"
          @click="resetForm"
        >
          بازنشانی
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Success Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000" location="top">
      {{ snackbarMessage }}
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useSupplierApi } from '~/composables/useSupplierApi'

const authStore = useAuthStore()
const supplierApi = useSupplierApi()

const formRef = ref()
const formValid = ref(false)
const saving = ref(false)
const loadingSettings = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const supplierId = ref<number | null>(null)
const bannerFile = ref<File[]>([])
const previewBanner = ref<string>('')
const isMounted = ref(false)

const formData = ref({
  brand_color_primary: '#1976D2',
  brand_color_secondary: '#424242',
  slogan: '',
  year_established: null as number | null,
  employee_count: null as number | null,
  video_url: '',
  meta_title: '',
  meta_description: ''
})

const certifications = ref<any[]>([])
const awards = ref<any[]>([])
const socialMedia = ref({
  linkedin: '',
  instagram: '',
  telegram: '',
  whatsapp: ''
})

const addCertification = () => {
  certifications.value.push({ title: '', issuer: '', date: '' })
}

const removeCertification = (index: number) => {
  certifications.value.splice(index, 1)
}

const addAward = () => {
  awards.value.push({ title: '', issuer: '', year: '', description: '' })
}

const removeAward = (index: number) => {
  awards.value.splice(index, 1)
}

const previewUrl = computed(() => {
  return supplierId.value ? `/suppliers/${supplierId.value}` : null
})

const fullPreviewUrl = computed(() => {
  if (!previewUrl.value) return '#'
  if (import.meta.client && typeof window !== 'undefined') {
    return window.location.origin + previewUrl.value
  }
  return previewUrl.value
})

const onBannerChange = (event: Event) => {
  const files = (event.target as HTMLInputElement).files
  if (files && files[0]) {
    const reader = new FileReader()
    reader.onload = (e) => {
      previewBanner.value = e.target?.result as string
    }
    reader.readAsDataURL(files[0])
  }
}

const removeBanner = () => {
  bannerFile.value = []
  previewBanner.value = ''
}

const loadCurrentSettings = async () => {
  loadingSettings.value = true
  try {
    // Always refresh the authenticated user to ensure we get the full vendor profile
    // (login response only includes limited vendor fields and misses mini-site branding data)
    let user = authStore.user
    try {
      const refreshedUser = await authStore.fetchCurrentUser()
      if (refreshedUser) {
        user = refreshedUser
      }
    } catch (err) {
      console.warn('Error refreshing current user during mini-site load:', err)
    }

    let vendorProfile: any = null

    // Try to get vendor profile from the refreshed user first
    if (user?.vendor_profile) {
      vendorProfile = user.vendor_profile
    } else if (authStore.vendorProfile) {
      vendorProfile = authStore.vendorProfile
    }
    
    if (vendorProfile && vendorProfile.id) {
      supplierId.value = vendorProfile.id
      console.log('Vendor profile loaded, ID:', vendorProfile.id, 'Store name:', vendorProfile.store_name)
      
      formData.value = {
        brand_color_primary: vendorProfile.brand_color_primary || '#1976D2',
        brand_color_secondary: vendorProfile.brand_color_secondary || '#424242',
        slogan: vendorProfile.slogan || '',
        year_established: vendorProfile.year_established || null,
        employee_count: vendorProfile.employee_count || null,
        video_url: vendorProfile.video_url || '',
        meta_title: vendorProfile.meta_title || '',
        meta_description: vendorProfile.meta_description || ''
      }

      if (vendorProfile.banner_image) {
        previewBanner.value = vendorProfile.banner_image
      }

      certifications.value = vendorProfile.certifications || []
      awards.value = vendorProfile.awards || []
      socialMedia.value = vendorProfile.social_media || {
        linkedin: '',
        instagram: '',
        telegram: '',
        whatsapp: ''
      }
    } else {
      console.warn('No vendor profile found for user', { user, vendorProfile: authStore.vendorProfile })
      snackbarMessage.value = 'پروفایل تامین‌کننده یافت نشد. لطفاً با پشتیبانی تماس بگیرید.'
      snackbarColor.value = 'warning'
      snackbar.value = true
    }
  } catch (error) {
    console.error('Error loading settings:', error)
    snackbarMessage.value = 'خطا در بارگذاری تنظیمات'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    loadingSettings.value = false
  }
}

const saveSettings = async () => {
  if (!formValid.value) return

  saving.value = true

  try {
    const updateData: any = {
      ...formData.value,
      certifications: certifications.value.filter(c => c.title),
      awards: awards.value.filter(a => a.title),
      social_media: socialMedia.value
    }

    // Handle banner upload if changed
    if (bannerFile.value.length > 0) {
      updateData.banner_image = bannerFile.value[0]
    }

    await supplierApi.updateSupplierProfile(updateData)
    
    // Refresh user data to get updated vendor_profile
    try {
      await authStore.fetchCurrentUser()
    } catch (err) {
      console.warn('Error refreshing user data:', err)
    }
    
    // Reload settings to show updated data
    await loadCurrentSettings()
    
    // Clear banner file after successful upload
    bannerFile.value = []

    snackbarMessage.value = 'تنظیمات با موفقیت ذخیره شد'
    snackbarColor.value = 'success'
    snackbar.value = true
  } catch (error) {
    console.error('Error saving settings:', error)
    snackbarMessage.value = 'خطا در ذخیره تنظیمات'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    saving.value = false
  }
}

const resetForm = () => {
  loadCurrentSettings()
}

const previewWebsite = async () => {
  console.log('Preview clicked, supplierId:', supplierId.value, 'previewUrl:', previewUrl.value)
  
  if (!supplierId.value) {
    // Try to reload settings first
    await loadCurrentSettings()
    if (!supplierId.value) {
      snackbarMessage.value = 'لطفاً ابتدا اطلاعات را بارگذاری کنید'
      snackbarColor.value = 'warning'
      snackbar.value = true
      return
    }
  }
  
  if (previewUrl.value) {
    try {
      const fullUrl = window.location.origin + previewUrl.value
      console.log('Opening preview URL:', fullUrl)
      
      // Try window.open first
      const newWindow = window.open(fullUrl, '_blank', 'noopener,noreferrer')
      
      if (!newWindow || newWindow.closed || typeof newWindow.closed === 'undefined') {
        // Popup blocked, try alternative method
        console.warn('Popup blocked, trying alternative method')
        // Create a temporary link and click it
        const link = document.createElement('a')
        link.href = fullUrl
        link.target = '_blank'
        link.rel = 'noopener noreferrer'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      }
    } catch (error) {
      console.error('Error opening preview:', error)
      snackbarMessage.value = 'خطا در باز کردن پیش‌نمایش. لطفاً URL را کپی کنید: ' + previewUrl.value
      snackbarColor.value = 'error'
      snackbar.value = true
    }
  } else {
    snackbarMessage.value = 'لطفاً ابتدا اطلاعات را بارگذاری کنید'
    snackbarColor.value = 'warning'
    snackbar.value = true
  }
}

const copyPreviewUrl = async () => {
  if (previewUrl.value) {
    const fullUrl = window.location.origin + previewUrl.value
    try {
      await navigator.clipboard.writeText(fullUrl)
      snackbarMessage.value = 'لینک کپی شد: ' + fullUrl
      snackbarColor.value = 'success'
      snackbar.value = true
    } catch (error) {
      console.error('Error copying URL:', error)
      snackbarMessage.value = 'خطا در کپی کردن لینک'
      snackbarColor.value = 'error'
      snackbar.value = true
    }
  }
}

onMounted(() => {
  isMounted.value = true
  loadCurrentSettings()
})
</script>

<style scoped>
.mini-website-settings {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

