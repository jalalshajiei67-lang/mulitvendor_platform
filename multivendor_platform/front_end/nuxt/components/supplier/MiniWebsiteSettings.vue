<template>
  <div class="mini-website-settings" dir="rtl">
    <v-card elevation="2">
      <v-card-title class="text-h5 font-weight-bold d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <v-icon color="primary" class="me-2">mdi-palette</v-icon>
          تنظیمات صفحه فروشگاه شما
        </div>
        <ClientOnly>
          <div v-if="supplierId" class="text-caption text-medium-emphasis">
            <v-icon size="small" class="me-1">mdi-link</v-icon>
            <span class="me-2">آدرس صفحه شما:</span>
            <a 
              :href="fullPreviewUrl" 
              target="_blank" 
              class="text-decoration-none text-primary"
              @click.stop.prevent="previewWebsite"
            >
              {{ previewUrl }}
            </a>
          </div>
        </ClientOnly>
      </v-card-title>

      <v-card-text>
        <FormQualityScore
          class="mb-4"
          title="امتیاز وب‌سایت مینی"
          caption="چند قدم تا صفحه حرفه‌ای"
          :score="miniSiteScore"
          :metrics="miniSiteMetrics"
          :tips="miniSiteTips"
        />
        <v-form ref="formRef" v-model="formValid">
          <!-- Branding Section -->
          <v-card class="mb-4" elevation="1">
            <v-card-title class="text-subtitle-1 font-weight-bold bg-grey-lighten-4">
              <v-icon size="small" class="me-2">mdi-brush</v-icon>
              رنگ و ظاهر صفحه فروشگاه
            </v-card-title>
            <v-card-text>
              <div class="text-body-2 text-medium-emphasis mb-4">
                در این بخش می‌توانید رنگ‌ها و تصویر بالای صفحه فروشگاه خود را تنظیم کنید.
              </div>
              <v-row>
                <!-- Banner Image -->
                <v-col cols="12">
                  <div class="mb-2 text-subtitle-2 font-weight-bold">تصویر بالای صفحه</div>
                  <div class="text-caption text-medium-emphasis mb-2">
                    یک تصویر زیبا برای بالای صفحه فروشگاه خود انتخاب کنید. تصویر باید عریض باشد (مثل تصاویر بنر).
                  </div>
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
                    label="انتخاب تصویر از کامپیوتر یا موبایل"
                    prepend-icon="mdi-image"
                    accept="image/*"
                    @change="onBannerChange"
                    variant="outlined"
                    density="comfortable"
                    hint="فقط فایل‌های تصویری (jpg, png و غیره)"
                  ></v-file-input>
                </v-col>

                <!-- Brand Colors -->
                <v-col cols="12" md="6">
                  <div class="text-subtitle-2 font-weight-bold mb-2">رنگ اصلی صفحه</div>
                  <v-text-field
                    v-model="formData.brand_color_primary"
                    label="رنگ اصلی"
                    type="color"
                    prepend-icon="mdi-palette"
                    variant="outlined"
                    density="comfortable"
                    hint="این رنگ در دکمه‌ها و بخش‌های مهم صفحه نمایش داده می‌شود"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <div class="text-subtitle-2 font-weight-bold mb-2">رنگ دوم</div>
                  <v-text-field
                    v-model="formData.brand_color_secondary"
                    label="رنگ دوم"
                    type="color"
                    prepend-icon="mdi-palette"
                    variant="outlined"
                    density="comfortable"
                    hint="رنگ دوم برای زیباتر شدن صفحه (اختیاری)"
                  ></v-text-field>
                </v-col>

                <!-- Slogan -->
                <v-col cols="12">
                  <v-text-field
                    v-model="formData.slogan"
                    label="شعار یا جمله معرفی کوتاه"
                    prepend-icon="mdi-text-short"
                    variant="outlined"
                    density="comfortable"
                    placeholder="مثال: بهترین تولیدکننده ماشین‌آلات صنعتی"
                    hint="یک جمله کوتاه که معرفی کننده شماست (حداکثر 200 حرف)"
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
              اطلاعات فروشگاه و تماس
            </v-card-title>
            <v-card-text>
              <div class="text-body-2 text-medium-emphasis mb-4">
                اطلاعات اصلی فروشگاه خود را در این بخش وارد کنید. این اطلاعات در صفحه فروشگاه شما نمایش داده می‌شود.
              </div>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="formData.store_name"
                    label="نام فروشگاه *"
                    prepend-icon="mdi-store"
                    variant="outlined"
                    density="comfortable"
                    hint="نام فروشگاه یا شرکت شما (این فیلد اجباری است)"
                    :rules="[v => !!v || 'لطفاً نام فروشگاه را وارد کنید']"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-textarea
                    v-model="formData.description"
                    label="توضیحات فروشگاه"
                    prepend-icon="mdi-text"
                    rows="4"
                    variant="outlined"
                    density="comfortable"
                    hint="در مورد فروشگاه، محصولات و خدمات خود توضیح دهید. این متن در صفحه فروشگاه شما نمایش داده می‌شود."
                    placeholder="مثال: ما یک شرکت تولیدی با بیش از 20 سال سابقه در زمینه تولید ماشین‌آلات صنعتی هستیم..."
                  ></v-textarea>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.contact_email"
                    label="ایمیل تماس"
                    prepend-icon="mdi-email-outline"
                    type="email"
                    variant="outlined"
                    density="comfortable"
                    hint="ایمیلی که مشتریان می‌توانند با شما تماس بگیرند"
                    placeholder="info@example.com"
                    :rules="emailRules"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.contact_phone"
                    label="شماره تماس"
                    prepend-icon="mdi-phone-outline"
                    variant="outlined"
                    density="comfortable"
                    hint="شماره تلفن یا موبایل برای تماس مشتریان"
                    placeholder="09123456789"
                    :rules="phoneRules"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="formData.website"
                    label="آدرس وب‌سایت (در صورت داشتن)"
                    prepend-icon="mdi-web"
                    variant="outlined"
                    density="comfortable"
                    placeholder="https://example.com"
                    hint="اگر وب‌سایت جداگانه‌ای دارید، آدرس آن را اینجا وارد کنید (اختیاری)"
                    :rules="urlRules"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="formData.year_established"
                    :items="persianYears"
                    label="سال تاسیس"
                    prepend-icon="mdi-calendar"
                    variant="outlined"
                    density="comfortable"
                    placeholder="سال را انتخاب کنید"
                    hint="سال شروع فعالیت شرکت یا فروشگاه (تقویم شمسی)"
                    :rules="yearRules"
                    clearable
                    item-title="label"
                    item-value="value"
                  >
                    <template #item="{ props, item }">
                      <v-list-item v-bind="props" :title="item.raw.label">
                        <template #prepend>
                          <v-icon>mdi-calendar</v-icon>
                        </template>
                      </v-list-item>
                    </template>
                  </v-select>
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
                    hint="تعداد کارمندان شرکت (اختیاری)"
                    :rules="employeeCountRules"
                  ></v-text-field>
                </v-col>

                <v-col cols="12">
                  <v-text-field
                    v-model="formData.video_url"
                    label="لینک ویدیو معرفی (در صورت داشتن)"
                    prepend-icon="mdi-video"
                    variant="outlined"
                    density="comfortable"
                    placeholder="لینک ویدیو از یوتیوب یا آپارات"
                    hint="اگر ویدیوی معرفی شرکت دارید، لینک آن را اینجا وارد کنید (اختیاری)"
                    :rules="videoUrlRules"
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
              <div class="text-body-2 text-medium-emphasis mb-4">
                اگر گواهینامه یا جایزه‌ای دارید، می‌توانید آن‌ها را در این بخش اضافه کنید. این کار به اعتماد بیشتر مشتریان کمک می‌کند.
              </div>
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
                    افزودن گواهینامه جدید
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
                          placeholder="مثال: ISO 9001"
                          hide-details
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="4">
                        <v-text-field
                          v-model="cert.issuer"
                          label="صادرکننده"
                          density="compact"
                          variant="outlined"
                          placeholder="مثال: سازمان استاندارد"
                          hide-details
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="2">
                        <v-text-field
                          v-model="cert.date"
                          label="تاریخ"
                          density="compact"
                          variant="outlined"
                          placeholder="1400"
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
                  <div class="text-subtitle-2 font-weight-bold">جوایز و افتخارات</div>
                  <v-btn
                    size="small"
                    color="primary"
                    prepend-icon="mdi-plus"
                    @click="addAward"
                  >
                    افزودن جایزه جدید
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
                          placeholder="مثال: برترین تولیدکننده سال"
                          hide-details
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="3">
                        <v-text-field
                          v-model="award.issuer"
                          label="اهدا کننده"
                          density="compact"
                          variant="outlined"
                          placeholder="مثال: اتاق بازرگانی"
                          hide-details
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="2">
                        <v-text-field
                          v-model="award.year"
                          label="سال"
                          density="compact"
                          variant="outlined"
                          placeholder="1400"
                          hide-details
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="2">
                        <v-text-field
                          v-model="award.description"
                          label="توضیحات"
                          density="compact"
                          variant="outlined"
                          placeholder="توضیح کوتاه"
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
              صفحات شبکه‌های اجتماعی
            </v-card-title>
            <v-card-text>
              <div class="text-body-2 text-medium-emphasis mb-4">
                اگر در شبکه‌های اجتماعی صفحه‌ای دارید، آدرس آن‌ها را اینجا وارد کنید. مشتریان می‌توانند از این طریق با شما در ارتباط باشند. (همه فیلدها اختیاری هستند)
              </div>
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="socialMedia.linkedin"
                    label="لینکدین (در صورت داشتن)"
                    prepend-icon="mdi-linkedin"
                    variant="outlined"
                    density="comfortable"
                    placeholder="https://linkedin.com/company/..."
                    hint="آدرس صفحه لینکدین شرکت"
                    :rules="socialMediaUrlRules"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="socialMedia.instagram"
                    label="اینستاگرام (در صورت داشتن)"
                    prepend-icon="mdi-instagram"
                    variant="outlined"
                    density="comfortable"
                    placeholder="https://instagram.com/..."
                    hint="آدرس صفحه اینستاگرام"
                    :rules="socialMediaUrlRules"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="socialMedia.telegram"
                    label="تلگرام (در صورت داشتن)"
                    prepend-icon="mdi-telegram"
                    variant="outlined"
                    density="comfortable"
                    placeholder="https://t.me/..."
                    hint="آدرس کانال یا گروه تلگرام"
                    :rules="socialMediaUrlRules"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="socialMedia.whatsapp"
                    label="واتساپ (در صورت داشتن)"
                    prepend-icon="mdi-whatsapp"
                    variant="outlined"
                    density="comfortable"
                    placeholder="https://wa.me/..."
                    hint="لینک واتساپ برای تماس مستقیم"
                    :rules="socialMediaUrlRules"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- SEO Settings -->
          <v-card class="mb-4" elevation="1">
            <v-card-title class="text-subtitle-1 font-weight-bold bg-grey-lighten-4">
              <v-icon size="small" class="me-2">mdi-search-web</v-icon>
              تنظیمات نمایش در گوگل
            </v-card-title>
            <v-card-text>
              <div class="text-body-2 text-medium-emphasis mb-4">
                وقتی کسی در گوگل شما را جستجو می‌کند، چه عنوان و توضیحی نمایش داده شود؟ این بخش برای بهتر پیدا شدن شما در گوگل است. (اختیاری - اگر خالی بگذارید، از نام و توضیحات فروشگاه استفاده می‌شود)
              </div>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="formData.meta_title"
                    label="عنوان نمایش در گوگل"
                    prepend-icon="mdi-format-title"
                    variant="outlined"
                    density="comfortable"
                    counter="60"
                    hint="عنوانی که در نتایج جستجوی گوگل نمایش داده می‌شود (حداکثر 60 حرف)"
                    placeholder="مثال: فروشگاه آنلاین ماشین‌آلات صنعتی"
                    :rules="[v => !v || v.length <= 60 || 'حداکثر 60 کاراکتر']"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-textarea
                    v-model="formData.meta_description"
                    label="توضیحات نمایش در گوگل"
                    prepend-icon="mdi-text"
                    variant="outlined"
                    rows="3"
                    counter="160"
                    hint="توضیح کوتاهی که زیر عنوان در نتایج گوگل نمایش داده می‌شود (حداکثر 160 حرف)"
                    placeholder="مثال: فروشگاه آنلاین انواع ماشین‌آلات صنعتی با بهترین قیمت و کیفیت..."
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
          ذخیره همه تغییرات
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
          مشاهده صفحه فروشگاه
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
            <v-tooltip activator="parent" location="top">کپی آدرس صفحه</v-tooltip>
          </v-btn>
        </ClientOnly>
        <v-spacer></v-spacer>
        <v-btn
          variant="text"
          @click="resetForm"
        >
          بازگشت به تنظیمات قبلی
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
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useSupplierApi } from '~/composables/useSupplierApi'
import { useGamificationStore } from '~/stores/gamification'
import FormQualityScore from '~/components/gamification/FormQualityScore.vue'
import { toJalaali } from 'jalaali-js'

const authStore = useAuthStore()
const supplierApi = useSupplierApi()
const gamificationStore = useGamificationStore()

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
const hasLoadedData = ref(false)

const formData = ref({
  store_name: '',
  description: '',
  contact_email: '',
  contact_phone: '',
  website: '',
  brand_color_primary: '#1976D2',
  brand_color_secondary: '#424242',
  slogan: '',
  year_established: 1405 as number | null,
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
const socialLinksCount = computed(() => Object.values(socialMedia.value).filter(Boolean).length)

// Persian year picker - generate years from 1200 to 1405
const persianYears = computed(() => {
  // Generate years from 1200 to 1405
  const years: Array<{ label: string; value: number }> = []
  const startYear = 1200
  const endYear = 1405
  
  for (let year = endYear; year >= startYear; year--) {
    years.push({
      label: `${year}`,
      value: year
    })
  }
  
  return years
})

// Validation rules
const emailRules = [
  (value: string) => {
    if (!value) return true // Optional field
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return pattern.test(value) || 'ایمیل معتبر نیست (مثال: info@example.com)'
  }
]

const phoneRules = [
  (value: string) => {
    if (!value) return true // Optional field
    // Remove spaces, dashes, and parentheses for validation
    const cleaned = value?.replace(/[\s\-()]/g, '') || ''
    // Check if it starts with a valid Iranian mobile prefix
    // Accept: 09XXXXXXXXX, +98XXXXXXXXXX, 0098XXXXXXXXXX, 98XXXXXXXXXX, 9XXXXXXXXX
    const mobileRegex = /^(\+98|0098|98|0)?9\d{9}$/
    if (!mobileRegex.test(cleaned)) {
      return 'شماره تماس معتبر نیست. لطفاً شماره را صحیح وارد کنید (مثال: 09123456789)'
    }
    // Check minimum length (should be at least 10 digits after cleaning)
    const digitsOnly = cleaned.replace(/\D/g, '')
    if (digitsOnly.length < 10 || digitsOnly.length > 13) {
      return 'شماره تماس باید ۱۱ رقم باشد (مثال: 09123456789)'
    }
    return true
  }
]

const urlRules = [
  (value: string) => {
    if (!value) return true // Optional field
    try {
      // Allow URLs with or without protocol (we'll add https:// automatically if missing)
      const urlPattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/
      if (!urlPattern.test(value)) {
        return 'آدرس معتبر نیست (مثال: example.com یا https://example.com)'
      }
      return true
    } catch {
      return 'آدرس معتبر نیست'
    }
  }
]

const videoUrlRules = [
  (value: string) => {
    if (!value) return true // Optional field
    // Check for YouTube, Aparat, or general URL format (with or without protocol)
    const youtubePattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/
    const aparatPattern = /^(https?:\/\/)?(www\.)?aparat\.com\/.+/
    const generalUrlPattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/
    
    if (youtubePattern.test(value) || aparatPattern.test(value) || generalUrlPattern.test(value)) {
      return true
    }
    return 'لینک ویدیو معتبر نیست. لطفاً لینک یوتیوب یا آپارات وارد کنید (مثال: youtube.com/watch?v=... یا aparat.com/v/...)'
  }
]

const yearRules = [
  (value: number | null) => {
    if (!value) return true // Optional field
    
    if (value < 1200 || value > 1405) {
      return 'سال باید بین ۱۲۰۰ و ۱۴۰۵ باشد'
    }
    return true
  }
]

const employeeCountRules = [
  (value: number | null) => {
    if (!value) return true // Optional field
    if (value < 1) {
      return 'تعداد کارمندان باید حداقل ۱ باشد'
    }
    if (value > 1000000) {
      return 'تعداد کارمندان معتبر نیست'
    }
    return true
  }
]

const socialMediaUrlRules = [
  (value: string) => {
    if (!value) return true // Optional field
    try {
      // Allow URLs with or without protocol (we'll add https:// automatically if missing)
      const urlPattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/
      if (!urlPattern.test(value)) {
        return 'آدرس معتبر نیست (مثال: instagram.com/username یا https://instagram.com/username)'
      }
      return true
    } catch {
      return 'آدرس معتبر نیست'
    }
  }
]

const miniSiteMetrics = computed(() => [
  {
    key: 'banner',
    label: 'بنر و رنگ برند',
    tip: 'یک تصویر عریض از خط تولید یا دستگاه شاخص انتخاب کنید.',
    weight: 0.18,
    passed: Boolean(previewBanner.value)
  },
  {
    key: 'colors',
    label: 'رنگ برند',
    tip: 'رنگ اصلی و دوم را مشخص کنید تا صفحه هماهنگ شود.',
    weight: 0.1,
    passed: Boolean(formData.value.brand_color_primary && formData.value.brand_color_secondary)
  },
  {
    key: 'slogan',
    label: 'شعار کوتاه',
    tip: 'شعاری ۱۰ تا ۲۰۰ کاراکتری درباره ارزش پیشنهادی خود بنویسید.',
    weight: 0.08,
    passed: Boolean(formData.value.slogan && formData.value.slogan.length >= 10)
  },
  {
    key: 'about',
    label: 'معرفی فروشگاه',
    tip: 'حداقل ۲۰۰ کاراکتر درباره تجربه و خدمات خود توضیح دهید.',
    weight: 0.12,
    passed: Boolean(formData.value.description && formData.value.description.length >= 200)
  },
  {
    key: 'contact',
    label: 'راه‌های تماس',
    tip: 'تلفن، واتساپ یا ایمیل پاسخگو را وارد کنید.',
    weight: 0.1,
    passed: Boolean(formData.value.contact_phone || formData.value.contact_email)
  },
  {
    key: 'media',
    label: 'ویدیو یا وب‌سایت',
    tip: 'ویدیو معرفی یا لینک وب‌سایت رسمی را اضافه کنید.',
    weight: 0.07,
    passed: Boolean(formData.value.video_url || formData.value.website)
  },
  {
    key: 'company',
    label: 'سال تاسیس و تیم',
    tip: 'سال شروع فعالیت و تعداد همکاران را بنویسید.',
    weight: 0.05,
    passed: Boolean(formData.value.year_established && formData.value.employee_count)
  },
  {
    key: 'certs',
    label: 'گواهینامه‌ها',
    tip: 'گواهینامه‌هایی مانند ISO یا استاندارد ملی را ثبت کنید.',
    weight: 0.12,
    passed: certifications.value.length > 0
  },
  {
    key: 'awards',
    label: 'جوایز و تقدیرنامه',
    tip: 'حداقل یک نمونه از موفقیت‌های خود را معرفی کنید.',
    weight: 0.08,
    passed: awards.value.length > 0
  },
  {
    key: 'social',
    label: 'شبکه‌های اجتماعی',
    tip: 'حداقل دو لینک شبکه اجتماعی قرار دهید.',
    weight: 0.1,
    passed: socialLinksCount.value >= 2
  },
  {
    key: 'seo',
    label: 'متای سئو',
    tip: 'عنوان و توضیح متای صفحه را تکمیل کنید.',
    weight: 0.1,
    passed: Boolean(formData.value.meta_title && formData.value.meta_description)
  }
])

const miniSiteScore = computed(() => {
  const metrics = miniSiteMetrics.value
  const totalWeight = metrics.reduce((sum, metric) => sum + metric.weight, 0) || 1
  const earned = metrics.reduce((sum, metric) => sum + (metric.passed ? metric.weight : 0), 0)
  return Math.round((earned / totalWeight) * 100)
})

const miniSiteTips = computed(() => miniSiteMetrics.value.filter(metric => !metric.passed).map(metric => metric.tip))

watch(miniSiteScore, (score) => {
  gamificationStore.updateLocalScore('miniWebsite', {
    title: 'miniWebsite',
    score,
    metrics: miniSiteMetrics.value,
    tips: miniSiteTips.value
  })
}, { immediate: true })

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
  // Don't load if already loading
  if (loadingSettings.value) return
  
  loadingSettings.value = true
  try {
    // Always fetch fresh user data to ensure we have complete vendor profile
    // The login endpoint only returns minimal vendor_profile (id, store_name, logo)
    // so we need to fetch from auth/me/ to get all fields
    console.log('Loading settings - fetching fresh user data...')
    let user = authStore.user
    let vendorProfile: any = null
    
    // Always fetch current user to get complete vendor profile data
    try {
      const fetchedUser = await authStore.fetchCurrentUser()
      user = fetchedUser || authStore.user
      console.log('Fetched user data:', user)
      
      if (user?.vendor_profile) {
        vendorProfile = user.vendor_profile
        console.log('Vendor profile from fetched user:', vendorProfile)
      } else if (authStore.vendorProfile) {
        vendorProfile = authStore.vendorProfile
        console.log('Vendor profile from authStore:', vendorProfile)
      }
    } catch (err) {
      console.error('Error fetching current user:', err)
      // Fallback to cached data if fetch fails
      if (authStore.user?.vendor_profile) {
        vendorProfile = authStore.user.vendor_profile
      } else if (authStore.vendorProfile) {
        vendorProfile = authStore.vendorProfile
      }
    }
    
    if (vendorProfile && vendorProfile.id) {
      const profileId = vendorProfile.id
      supplierId.value = profileId
      hasLoadedData.value = true
      console.log('Vendor profile loaded, ID:', profileId, 'Store name:', vendorProfile.store_name)
      console.log('Full vendor profile data:', JSON.stringify(vendorProfile, null, 2))
      
      formData.value = {
        store_name: vendorProfile.store_name || '',
        description: vendorProfile.description || '',
        contact_email: vendorProfile.contact_email || '',
        contact_phone: vendorProfile.contact_phone || '',
        website: vendorProfile.website || '',
        brand_color_primary: vendorProfile.brand_color_primary || '#1976D2',
        brand_color_secondary: vendorProfile.brand_color_secondary || '#424242',
        slogan: vendorProfile.slogan || '',
        year_established: vendorProfile.year_established || 1405,
        employee_count: vendorProfile.employee_count || null,
        video_url: vendorProfile.video_url || '',
        meta_title: vendorProfile.meta_title || '',
        meta_description: vendorProfile.meta_description || ''
      }

      if (vendorProfile.banner_image) {
        // Handle both relative and absolute URLs
        const bannerUrl = vendorProfile.banner_image
        if (bannerUrl.startsWith('http://') || bannerUrl.startsWith('https://')) {
          previewBanner.value = bannerUrl
        } else {
          // Assume it's a relative URL, prepend API base URL if needed
          // For now, use as-is since the backend should return full URLs
          previewBanner.value = bannerUrl
        }
        console.log('Banner image loaded:', previewBanner.value)
      } else {
        previewBanner.value = ''
      }

      certifications.value = Array.isArray(vendorProfile.certifications) 
        ? vendorProfile.certifications 
        : (vendorProfile.certifications ? [vendorProfile.certifications] : [])
      awards.value = Array.isArray(vendorProfile.awards) 
        ? vendorProfile.awards 
        : (vendorProfile.awards ? [vendorProfile.awards] : [])
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

// Helper function to normalize URLs - add https:// if missing
const normalizeUrl = (url: string | null | undefined): string | null => {
  if (!url || !url.trim()) return null
  const trimmed = url.trim()
  // If it already has a protocol, return as is
  if (trimmed.match(/^https?:\/\//i)) {
    return trimmed
  }
  // Otherwise, add https://
  return `https://${trimmed}`
}

const saveSettings = async () => {
  if (!formValid.value) return

  saving.value = true

  try {
    // Normalize URLs before sending (Django URLField requires protocol)
    const normalizedSocialMedia: any = {}
    for (const [key, value] of Object.entries(socialMedia.value)) {
      // Only include non-empty values, and normalize URLs
      if (value && typeof value === 'string' && value.trim()) {
        normalizedSocialMedia[key] = normalizeUrl(value)
      } else {
        normalizedSocialMedia[key] = null
      }
    }
    
    const updateData: any = {
      ...formData.value,
      // Normalize website and video_url
      website: formData.value.website ? normalizeUrl(formData.value.website) : null,
      video_url: formData.value.video_url ? normalizeUrl(formData.value.video_url) : null,
      certifications: certifications.value.filter(c => c.title),
      awards: awards.value.filter(a => a.title),
      social_media: normalizedSocialMedia
    }

    // Handle banner upload if changed
    if (bannerFile.value.length > 0) {
      updateData.banner_image = bannerFile.value[0]
    }

    console.log('Saving settings with data:', updateData)
    
    const response = await supplierApi.updateSupplierProfile(updateData)
    console.log('Save response:', response)
    
    // Refresh user data to get updated vendor_profile
    try {
      const updatedUser = await authStore.fetchCurrentUser()
      console.log('User data refreshed after save:', updatedUser)
      console.log('Vendor profile in refreshed user:', updatedUser?.vendor_profile || authStore.vendorProfile)
      
      // Reload settings to show updated data
      await loadCurrentSettings()
    } catch (err) {
      console.warn('Error refreshing user data:', err)
      // Still try to reload settings even if fetchCurrentUser failed
      await loadCurrentSettings()
    }
    
    // Clear banner file after successful upload
    bannerFile.value = []

    snackbarMessage.value = 'همه تغییرات با موفقیت ذخیره شد'
    snackbarColor.value = 'success'
    snackbar.value = true
  } catch (error: any) {
    console.error('Error saving settings:', error)
    console.error('Error details:', {
      message: error?.message,
      response: error?.response,
      data: error?.data,
      status: error?.status
    })
    
    // Try to get the actual error message from the response
    let errorMessage = 'خطا در ذخیره تنظیمات'
    if (error?.data) {
      console.error('Error data:', error.data)
      if (typeof error.data === 'string') {
        errorMessage = error.data
      } else if (error.data.error) {
        errorMessage = error.data.error
        // If there are validation errors, format them nicely
        if (error.data.vendor_profile_errors) {
          const errors = error.data.vendor_profile_errors
          const errorList: string[] = []
          
          // Map field names to Persian labels
          const fieldLabels: Record<string, string> = {
            website: 'آدرس وب‌سایت',
            video_url: 'لینک ویدیو',
            contact_email: 'ایمیل تماس',
            contact_phone: 'شماره تماس',
            year_established: 'سال تاسیس',
            employee_count: 'تعداد کارمندان',
            store_name: 'نام فروشگاه',
            description: 'توضیحات',
            slogan: 'شعار',
            meta_title: 'عنوان متا',
            meta_description: 'توضیحات متا'
          }
          
          for (const [field, messages] of Object.entries(errors)) {
            const fieldLabel = fieldLabels[field] || field
            const messageArray = Array.isArray(messages) ? messages : [messages]
            messageArray.forEach((msg: string) => {
              errorList.push(`${fieldLabel}: ${msg}`)
            })
          }
          
          if (errorList.length > 0) {
            errorMessage = 'خطا در اعتبارسنجی:\n' + errorList.join('\n')
          }
        }
      } else if (error.data.vendor_profile_errors) {
        const errors = error.data.vendor_profile_errors
        const errorList: string[] = []
        for (const [field, messages] of Object.entries(errors)) {
          const messageArray = Array.isArray(messages) ? messages : [messages]
          errorList.push(`${field}: ${messageArray.join(', ')}`)
        }
        errorMessage = 'خطا در اعتبارسنجی:\n' + errorList.join('\n')
      } else if (typeof error.data === 'object') {
        errorMessage = JSON.stringify(error.data)
      }
    }
    
    snackbarMessage.value = errorMessage
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
      snackbarMessage.value = 'لطفاً ابتدا اطلاعات را ذخیره کنید'
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
      snackbarMessage.value = 'نمی‌توانم صفحه را باز کنم. لطفاً آدرس را کپی کنید: ' + previewUrl.value
      snackbarColor.value = 'error'
      snackbar.value = true
    }
  } else {
    snackbarMessage.value = 'لطفاً ابتدا اطلاعات را ذخیره کنید'
    snackbarColor.value = 'warning'
    snackbar.value = true
  }
}

const copyPreviewUrl = async () => {
  if (previewUrl.value) {
    const fullUrl = window.location.origin + previewUrl.value
    try {
      await navigator.clipboard.writeText(fullUrl)
      snackbarMessage.value = 'آدرس صفحه کپی شد. می‌توانید آن را برای دیگران ارسال کنید.'
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

// Watch for vendor profile changes and reload settings
watch(() => authStore.vendorProfile, (newProfile) => {
  if (newProfile && newProfile.id && isMounted.value) {
    // Only reload if we don't have a supplierId or if the ID changed
    if (!supplierId.value || supplierId.value !== newProfile.id) {
      console.log('Vendor profile changed, reloading settings...', { oldId: supplierId.value, newId: newProfile.id })
      hasLoadedData.value = false
      loadCurrentSettings()
    }
  }
}, { deep: true })

// Watch for user changes
watch(() => authStore.user, (newUser) => {
  if (newUser && newUser.vendor_profile && isMounted.value) {
    const profileId = newUser.vendor_profile?.id
    if (profileId && (!supplierId.value || supplierId.value !== profileId)) {
      console.log('User vendor profile changed, reloading settings...', { oldId: supplierId.value, newId: profileId })
      hasLoadedData.value = false
      loadCurrentSettings()
    }
  }
}, { deep: true })

onMounted(async () => {
  isMounted.value = true
  
  // Wait for auth to be initialized
  if (authStore.token && !authStore.user) {
    try {
      await authStore.initializeAuth()
    } catch (err) {
      console.warn('Error initializing auth:', err)
    }
  }
  
  // Load settings after a short delay to ensure auth is ready
  await nextTick()
  loadCurrentSettings()
})
</script>

<style scoped>
.mini-website-settings {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

