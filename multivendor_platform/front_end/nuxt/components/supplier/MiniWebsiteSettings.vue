<template>
  <div class="mini-website-settings" dir="rtl">
    <v-card elevation="2" rounded="lg">
      <!-- Header Section - Simplified -->
      <v-card-title class="text-h4 font-weight-bold d-flex align-center gap-3 pa-6 bg-green-lighten-5">
        <v-icon size="40" color="primary">mdi-palette</v-icon>
        <div>
          <div>تنظیمات صفحه فروشگاه شما</div>
          <div class="text-caption text-medium-emphasis mt-2">اطلاعات کسب‌وکار و ظاهر صفحه را تنظیم کنید</div>
        </div>
      </v-card-title>

      <v-card-text class="pa-6">
        <!-- Quality Score - Prominent -->
        <FormQualityScore
          class="mb-8"
          title="میزان تکمیل اطلاعات"
          caption="برای دیدن صفحه حرفه‌ای، اطلاعات زیر را کامل کنید"
          :score="miniSiteScore"
          :metrics="miniSiteMetrics"
          :tips="miniSiteTips"
        />

        <v-form ref="formRef" v-model="formValid">
          <!-- SECTION 1: Store Identity - Core Information -->
          <v-card class="mb-8" elevation="1" rounded="lg" outlined>
            <v-card-title class="text-h6 font-weight-bold pa-5 bg-green-lighten-5">
              <v-icon size="28" class="me-3">mdi-store</v-icon>
              مشخصات فروشگاه
            </v-card-title>
            <v-card-text class="pa-6">
              <div class="text-body-1 text-medium-emphasis mb-6 line-height-lg">
                اطلاعات پایه‌ای فروشگاه خود را وارد کنید. این اطلاعات را مشتریان می‌بینند.
              </div>

              <!-- Store Name - Most Important -->
              <div class="mb-6">
                <v-text-field
                  v-model="formData.store_name"
                  label="نام فروشگاه یا شرکت"
                  variant="outlined"
                  density="comfortable"
                  size="large"
                  class="text-input-large"
                  hint="مثال: فروشگاه آرتا برای صنایع"
                  :rules="[v => !!v || 'لطفاً نام فروشگاه را وارد کنید']"
                  data-tour="store-name-input"
                >
                  <template #prepend>
                    <v-icon color="primary" size="24">mdi-store</v-icon>
                  </template>
                </v-text-field>
              </div>

              <!-- Description - Important -->
              <div class="mb-6">
                <div class="text-body-2 font-weight-bold mb-2">توضیحات درباره فروشگاه</div>
                <div class="text-caption text-medium-emphasis mb-3">
                  چند جمله درباره کسب‌وکار، تجربه و محصولات خود بنویسید
                </div>
                <v-textarea
                  v-model="formData.description"
                  rows="5"
                  variant="outlined"
                  density="comfortable"
                  hint="مثال: ما برای بیش از ۲۰ سال تولید ماشین‌آلات صنعتی می‌کنیم... (حداقل ۲۰۰ حرف)"
                  counter="500"
                  :rules="descriptionRules"
                  data-tour="store-description-input"
                >
                  <template #prepend>
                    <v-icon color="primary" size="24">mdi-text</v-icon>
                  </template>
                </v-textarea>
              </div>

              <!-- Slogan - Brand Statement -->
              <div>
                <v-text-field
                  v-model="formData.slogan"
                  label="شعار یا جمله‌ی معرفی شرکت"
                  variant="outlined"
                  density="comfortable"
                  hint="مثال: بهترین کیفیت، بهترین قیمت"
                  counter="100"
                  :rules="[v => !v || v.length <= 100 || 'حداکثر 100 حرف']"
                >
                  <template #prepend>
                    <v-icon color="primary" size="24">mdi-star</v-icon>
                  </template>
                </v-text-field>
              </div>
            </v-card-text>
          </v-card>

          <!-- SECTION 2: Visual Identity - Design & Colors -->
          <v-card class="mb-8" elevation="1" rounded="lg" outlined>
            <v-card-title class="text-h6 font-weight-bold pa-5 bg-green-lighten-5">
              <v-icon size="28" class="me-3">mdi-palette</v-icon>
              رنگ و ظاهر صفحه فروشگاه
            </v-card-title>
            <v-card-text class="pa-6">
              <div class="text-body-1 text-medium-emphasis mb-6 line-height-lg">
                یک تصویر زیبا برای بالای صفحه انتخاب کنید و رنگ‌های مناسب انتخاب کنید.
              </div>

              <!-- Banner Image -->
              <div class="mb-8">
                <div class="text-subtitle-1 font-weight-bold mb-3">تصویر بالای صفحه</div>
                <div class="text-body-2 text-medium-emphasis mb-4">
                  یک تصویر عریض از محصولات یا فابریکه خود انتخاب کنید
                </div>

                <!-- Banner Preview -->
                <v-card
                  v-if="previewBanner"
                  class="mb-4 position-relative"
                  elevation="1"
                  rounded="lg"
                >
                  <v-img :src="previewBanner" height="250" cover>
                    <v-btn
                      icon="mdi-close"
                      size="large"
                      color="error"
                      class="ma-3"
                      @click="removeBanner"
                      elevation="2"
                    ></v-btn>
                  </v-img>
                  <div class="pa-3 text-caption text-medium-emphasis">
                    تصویر انتخابی (برای حذف بر روی X کلیک کنید)
                  </div>
                </v-card>

                <!-- File Upload -->
                <v-file-input
                  v-model="bannerFile"
                  label="انتخاب تصویر از کامپیوتر"
                  accept="image/*"
                  @change="onBannerChange"
                  variant="outlined"
                  density="comfortable"
                  class="file-input-large"
                  hint="تصاویر JPG یا PNG"
                >
                  <template #prepend>
                    <v-icon color="primary" size="24">mdi-image</v-icon>
                  </template>
                </v-file-input>
              </div>

              <!-- Colors Section -->
              <div class="mb-8">
                <div class="text-subtitle-1 font-weight-bold mb-4">انتخاب رنگ برند</div>
                <v-row>
                  <v-col cols="12" md="6">
                    <div class="text-body-2 font-weight-bold mb-3">رنگ اصلی</div>
                    <div class="d-flex gap-3">
                      <v-text-field
                        v-model="formData.brand_color_primary"
                        type="color"
                        variant="outlined"
                        density="comfortable"
                        hide-details
                        class="color-input"
                      ></v-text-field>
                      <v-card
                        :style="{ backgroundColor: formData.brand_color_primary }"
                        class="flex-grow-1 rounded-lg"
                        min-height="56"
                      ></v-card>
                    </div>
                    <div class="text-caption text-medium-emphasis mt-2">
                      این رنگ در دکمه‌ها و بخش‌های مهم نمایش داده می‌شود
                    </div>
                  </v-col>
                  <v-col cols="12" md="6">
                    <div class="text-body-2 font-weight-bold mb-3">رنگ دوم</div>
                    <div class="d-flex gap-3">
                      <v-text-field
                        v-model="formData.brand_color_secondary"
                        type="color"
                        variant="outlined"
                        density="comfortable"
                        hide-details
                        class="color-input"
                      ></v-text-field>
                      <v-card
                        :style="{ backgroundColor: formData.brand_color_secondary }"
                        class="flex-grow-1 rounded-lg"
                        min-height="56"
                      ></v-card>
                    </div>
                    <div class="text-caption text-medium-emphasis mt-2">
                      رنگ مکمل برای طراحی زیباتر
                    </div>
                  </v-col>
                </v-row>
              </div>
            </v-card-text>
          </v-card>

          <!-- SECTION 3: Contact Information -->
          <v-card class="mb-8" elevation="1" rounded="lg" outlined>
            <v-card-title class="text-h6 font-weight-bold pa-5 bg-green-lighten-5">
              <v-icon size="28" class="me-3">mdi-phone</v-icon>
              راه‌های تماس با شما
            </v-card-title>
            <v-card-text class="pa-6">
              <div class="text-body-1 text-medium-emphasis mb-6 line-height-lg">
                راه‌های تماس خود را وارد کنید تا مشتریان بتوانند با شما ارتباط برقرار کنند
              </div>

              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.contact_phone"
                    label="شماره تلفن"
                    variant="outlined"
                    density="comfortable"
                    hint="مثال: 09123456789"
                    :rules="phoneRules"
                  >
                    <template #prepend>
                      <v-icon color="primary" size="24">mdi-phone</v-icon>
                    </template>
                  </v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.contact_email"
                    label="ایمیل تماس"
                    type="email"
                    variant="outlined"
                    density="comfortable"
                    hint="مثال: info@example.com"
                    :rules="emailRules"
                  >
                    <template #prepend>
                      <v-icon color="primary" size="24">mdi-email</v-icon>
                    </template>
                  </v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- SECTION 4: Company Details -->
          <v-card class="mb-8" elevation="1" rounded="lg" outlined>
            <v-card-title class="text-h6 font-weight-bold pa-5 bg-green-lighten-5">
              <v-icon size="28" class="me-3">mdi-information</v-icon>
              اطلاعات شرکت
            </v-card-title>
            <v-card-text class="pa-6">
              <div class="text-body-1 text-medium-emphasis mb-6 line-height-lg">
                اطلاعات تاریخی و سازمانی درباره شرکت
              </div>

              <v-row>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="formData.year_established"
                    :items="persianYears"
                    label="سال تاسیس"
                    variant="outlined"
                    density="comfortable"
                    hint="سال شروع کسب‌وکار"
                    clearable
                    item-title="label"
                    item-value="value"
                  >
                    <template #prepend>
                      <v-icon color="primary" size="24">mdi-calendar</v-icon>
                    </template>
                  </v-select>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model.number="formData.employee_count"
                    label="تعداد کارمندان"
                    type="number"
                    variant="outlined"
                    density="comfortable"
                    hint="مثال: 50"
                    :min="1"
                    :rules="employeeCountRules"
                  >
                    <template #prepend>
                      <v-icon color="primary" size="24">mdi-account-group</v-icon>
                    </template>
                  </v-text-field>
                </v-col>

                <v-col cols="12">
                  <v-text-field
                    v-model="formData.website"
                    label="آدرس وب‌سایت (اختیاری)"
                    variant="outlined"
                    density="comfortable"
                    hint="مثال: example.com"
                    :rules="urlRules"
                  >
                    <template #prepend>
                      <v-icon color="primary" size="24">mdi-web</v-icon>
                    </template>
                  </v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- SECTION 5: Certifications & Awards (Simplified) -->
          <v-card class="mb-8" elevation="1" rounded="lg" outlined>
            <v-card-title class="text-h6 font-weight-bold pa-5 bg-green-lighten-5">
              <v-icon size="28" class="me-3">mdi-trophy</v-icon>
              گواهینامه‌ها و جوایز
            </v-card-title>
            <v-card-text class="pa-6">
              <div class="text-body-1 text-medium-emphasis mb-6 line-height-lg">
                گواهینامه‌ها و جوایز خود را معرفی کنید تا مشتریان اعتماد بیشتری پیدا کنند
              </div>

              <!-- Certifications -->
              <div class="mb-8">
                <div class="d-flex align-center justify-space-between mb-4">
                  <div class="text-subtitle-1 font-weight-bold">گواهینامه‌ها</div>
                  <v-btn
                    size="small"
                    color="primary"
                    prepend-icon="mdi-plus"
                    @click="addCertification"
                    variant="outlined"
                  >
                    افزودن
                  </v-btn>
                </div>
                <v-card
                  v-for="(cert, index) in certifications"
                  :key="`cert-${index}`"
                  class="mb-3"
                  variant="outlined"
                  rounded="lg"
                >
                  <v-card-text class="pa-4">
                    <v-row dense>
                      <v-col cols="12" md="5">
                        <v-text-field
                          v-model="cert.title"
                          label="عنوان گواهینامه"
                          density="compact"
                          variant="outlined"
                          hint="مثال: ISO 9001"
                          persistent-hint
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="4">
                        <v-text-field
                          v-model="cert.issuer"
                          label="سازمان صادرکننده"
                          density="compact"
                          variant="outlined"
                          hint="مثال: سازمان استاندارد"
                          persistent-hint
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="2">
                        <v-text-field
                          v-model="cert.date"
                          label="سال"
                          density="compact"
                          variant="outlined"
                          hint="مثال: 1400"
                          persistent-hint
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="1" class="d-flex align-center justify-center">
                        <v-btn
                          icon="mdi-trash-can"
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
                <div class="d-flex align-center justify-space-between mb-4">
                  <div class="text-subtitle-1 font-weight-bold">جوایز</div>
                  <v-btn
                    size="small"
                    color="primary"
                    prepend-icon="mdi-plus"
                    @click="addAward"
                    variant="outlined"
                  >
                    افزودن
                  </v-btn>
                </div>
                <v-card
                  v-for="(award, index) in awards"
                  :key="`award-${index}`"
                  class="mb-3"
                  variant="outlined"
                  rounded="lg"
                >
                  <v-card-text class="pa-4">
                    <v-row dense>
                      <v-col cols="12" md="4">
                        <v-text-field
                          v-model="award.title"
                          label="عنوان جایزه"
                          density="compact"
                          variant="outlined"
                          hint="مثال: برترین تولیدکننده"
                          persistent-hint
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="3">
                        <v-text-field
                          v-model="award.issuer"
                          label="اهدا کننده"
                          density="compact"
                          variant="outlined"
                          hint="مثال: اتاق بازرگانی"
                          persistent-hint
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="2">
                        <v-text-field
                          v-model="award.year"
                          label="سال"
                          density="compact"
                          variant="outlined"
                          hint="مثال: 1400"
                          persistent-hint
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="2">
                        <v-text-field
                          v-model="award.description"
                          label="توضیح"
                          density="compact"
                          variant="outlined"
                          hide-details
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="1" class="d-flex align-center justify-center">
                        <v-btn
                          icon="mdi-trash-can"
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

          <!-- SECTION 6: Social Media (Simplified) -->
          <v-card class="mb-8" elevation="1" rounded="lg" outlined>
            <v-card-title class="text-h6 font-weight-bold pa-5 bg-green-lighten-5">
              <v-icon size="28" class="me-3">mdi-share-variant</v-icon>
              شبکه‌های اجتماعی
            </v-card-title>
            <v-card-text class="pa-6">
              <div class="text-body-1 text-medium-emphasis mb-6 line-height-lg">
                صفحه‌های خود را در شبکه‌های اجتماعی معرفی کنید (همه اختیاری هستند)
              </div>

              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="socialMedia.instagram"
                    label="اینستاگرام"
                    variant="outlined"
                    density="comfortable"
                    hint="مثال: https://instagram.com/store"
                  >
                    <template #prepend>
                      <v-icon color="primary" size="24">mdi-instagram</v-icon>
                    </template>
                  </v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="socialMedia.telegram"
                    label="تلگرام"
                    variant="outlined"
                    density="comfortable"
                    hint="مثال: https://t.me/store"
                  >
                    <template #prepend>
                      <v-icon color="primary" size="24">mdi-telegram</v-icon>
                    </template>
                  </v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="socialMedia.whatsapp"
                    label="واتساپ"
                    variant="outlined"
                    density="comfortable"
                    hint="مثال: https://wa.me/989123456789"
                  >
                    <template #prepend>
                      <v-icon color="primary" size="24">mdi-whatsapp</v-icon>
                    </template>
                  </v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="socialMedia.linkedin"
                    label="لینکدین"
                    variant="outlined"
                    density="comfortable"
                    hint="مثال: https://linkedin.com/company/store"
                  >
                    <template #prepend>
                      <v-icon color="primary" size="24">mdi-linkedin</v-icon>
                    </template>
                  </v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- SECTION 7: SEO (Optional - Collapsed) -->
          <v-expansion-panels>
            <v-expansion-panel rounded="lg" elevation="1">
              <template #title>
                <v-icon size="24" class="me-3" color="primary">mdi-search-web</v-icon>
                <span class="text-subtitle-1 font-weight-bold">تنظیمات نمایش در گوگل (اختیاری)</span>
              </template>

              <v-card-text class="pa-6">
                <div class="text-body-1 text-medium-emphasis mb-6 line-height-lg">
                  وقتی کسی شما را در گوگل جستجو می‌کند، چه نمایش داده شود؟
                </div>

                <v-row>
                  <v-col cols="12">
                    <v-text-field
                      v-model="formData.meta_title"
                      label="عنوان نمایش در گوگل"
                      variant="outlined"
                      density="comfortable"
                      counter="60"
                      hint="مثال: فروشگاه آنلاین ماشین‌آلات"
                      :rules="[v => !v || v.length <= 60 || 'حداکثر 60 حرف']"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-textarea
                      v-model="formData.meta_description"
                      label="توضیح نمایش در گوگل"
                      variant="outlined"
                      rows="3"
                      counter="160"
                      hint="مثال: فروشگاه آنلاین انواع ماشین‌آلات با بهترین کیفیت و قیمت"
                      :rules="[v => !v || v.length <= 160 || 'حداکثر 160 حرف']"
                    ></v-textarea>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-form>
      </v-card-text>

      <!-- Action Buttons - Large and Clear -->
      <v-card-actions class="pa-6 gap-3 flex-wrap">
        <v-btn
          color="primary"
          size="x-large"
          prepend-icon="mdi-content-save"
          :loading="saving"
          :disabled="!formValid"
          @click="saveSettings"
          class="flex-grow-1"
          min-width="200"
          data-tour="settings-save-button"
        >
          ذخیره همه تغییرات
        </v-btn>

        <v-btn
          color="secondary"
          size="x-large"
          variant="outlined"
          prepend-icon="mdi-eye"
          :disabled="!supplierId"
          :loading="loadingSettings"
          @click="previewWebsite"
          class="flex-grow-1"
          min-width="200"
          data-tour="preview-website"
        >
          دیدن صفحه فروشگاه
        </v-btn>

        <v-btn
          color="error"
          size="large"
          variant="text"
          prepend-icon="mdi-refresh"
          @click="resetForm"
          class="ms-auto"
        >
          بازگشت
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Preview URL Info Card -->
    <v-card v-if="supplierId" class="mt-6" elevation="1" rounded="lg" outlined>
      <v-card-text class="pa-6 d-flex align-center gap-4">
        <v-icon size="32" color="primary">mdi-link</v-icon>
        <div class="flex-grow-1">
          <div class="text-body-2 text-medium-emphasis mb-2">آدرس صفحه فروشگاه شما:</div>
          <div class="text-body-1 font-weight-bold text-primary">{{ fullPreviewUrl }}</div>
        </div>
        <v-btn
          icon="mdi-content-copy"
          size="large"
          color="primary"
          variant="outlined"
          @click="copyPreviewUrl"
        >
          <v-icon>mdi-content-copy</v-icon>
          <v-tooltip activator="parent" location="top">کپی کردن آدرس</v-tooltip>
        </v-btn>
      </v-card-text>
    </v-card>

    <!-- Success Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="4000" location="top">
      <div class="text-body-1">{{ snackbarMessage }}</div>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useSupplierApi } from '~/composables/useSupplierApi'
import { useGamificationStore } from '~/stores/gamification'
import FormQualityScore from '~/components/gamification/FormQualityScore.vue'

const authStore = useAuthStore()
const supplierApi = useSupplierApi()
const gamificationStore = useGamificationStore()

// State management
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

// Form data - simplified and organized
const formData = ref({
  store_name: '',
  description: '',
  contact_email: '',
  contact_phone: '',
  website: '',
  brand_color_primary: '#4CAF50',
  brand_color_secondary: '#388E3C',
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

// Computed properties
const socialLinksCount = computed(() => 
  Object.values(socialMedia.value).filter(Boolean).length
)

const persianYears = computed(() => {
  const years: Array<{ label: string; value: number }> = []
  const endYear = 1405
  const startYear = 1250
  
  for (let year = endYear; year >= startYear; year--) {
    years.push({
      label: `${year}`,
      value: year
    })
  }
  return years
})

// Validation Rules - Simplified
const descriptionRules = [
  (v: string) => !!v || 'لطفاً توضیحات را وارد کنید',
  (v: string) => (v && v.length >= 50) || 'حداقل 50 حرف لازم است'
]

const emailRules = [
  (value: string) => {
    if (!value) return true
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return pattern.test(value) || 'ایمیل معتبر نیست'
  }
]

const phoneRules = [
  (value: string) => {
    if (!value) return true
    const cleaned = value.replace(/[\s\-()]/g, '')
    const mobileRegex = /^(\+98|0098|98|0)?9\d{9}$/
    return mobileRegex.test(cleaned) || 'شماره معتبر نیست'
  }
]

const urlRules = [
  (value: string) => {
    if (!value) return true
    const urlPattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/
    return urlPattern.test(value) || 'آدرس معتبر نیست'
  }
]

const yearRules = [
  (value: number | null) => {
    if (!value) return true
    return (value >= 1250 && value <= 1405) || 'سال نامعتبر'
  }
]

const employeeCountRules = [
  (value: number | null) => {
    if (!value) return true
    return (value >= 1 && value <= 100000) || 'تعداد نامعتبر'
  }
]

// Gamification Metrics
const miniSiteMetrics = computed(() => [
  {
    key: 'name',
    label: 'نام فروشگاه',
    tip: 'نام فروشگاه را وارد کنید',
    weight: 0.15,
    passed: Boolean(formData.value.store_name)
  },
  {
    key: 'about',
    label: 'توضیحات فروشگاه',
    tip: 'درباره شرکت خود بنویسید',
    weight: 0.15,
    passed: Boolean(formData.value.description && formData.value.description.length >= 50)
  },
  {
    key: 'banner',
    label: 'تصویر صفحه',
    tip: 'یک تصویر عریض انتخاب کنید',
    weight: 0.15,
    passed: Boolean(previewBanner.value)
  },
  {
    key: 'colors',
    label: 'رنگ‌های برند',
    tip: 'رنگ‌های مناسب انتخاب کنید',
    weight: 0.10,
    passed: Boolean(formData.value.brand_color_primary && formData.value.brand_color_secondary)
  },
  {
    key: 'contact',
    label: 'راه‌های تماس',
    tip: 'تلفن یا ایمیل بگذارید',
    weight: 0.15,
    passed: Boolean(formData.value.contact_phone || formData.value.contact_email)
  },
  {
    key: 'company',
    label: 'اطلاعات شرکت',
    tip: 'سال تاسیس و تعداد کارمندان',
    weight: 0.10,
    passed: Boolean(formData.value.year_established && formData.value.employee_count)
  },
  {
    key: 'social',
    label: 'شبکه‌های اجتماعی',
    tip: 'حداقل یک شبکه اجتماعی',
    weight: 0.10,
    passed: socialLinksCount.value >= 1
  },
  {
    key: 'certs',
    label: 'گواهینامه‌ها',
    tip: 'گواهینامه‌های خود را معرفی کنید',
    weight: 0.10,
    passed: certifications.value.length > 0
  }
])

const miniSiteScore = computed(() => {
  const metrics = miniSiteMetrics.value
  const totalWeight = metrics.reduce((sum, m) => sum + m.weight, 0) || 1
  const earned = metrics.reduce((sum, m) => sum + (m.passed ? m.weight : 0), 0)
  return Math.round((earned / totalWeight) * 100)
})

const miniSiteTips = computed(() => 
  miniSiteMetrics.value.filter(m => !m.passed).map(m => m.tip)
)

const previewUrl = computed(() => 
  supplierId.value ? `/suppliers/${supplierId.value}` : null
)

const fullPreviewUrl = computed(() => {
  if (!previewUrl.value) return '#'
  if (import.meta.client && typeof window !== 'undefined') {
    return window.location.origin + previewUrl.value
  }
  return previewUrl.value
})

// Watch gamification score
watch(miniSiteScore, (score) => {
  gamificationStore.updateLocalScore('miniWebsite', {
    title: 'miniWebsite',
    score,
    metrics: miniSiteMetrics.value,
    tips: miniSiteTips.value
  })
}, { immediate: true })

// Methods
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

const onBannerChange = (event: Event) => {
  const files = (event.target as HTMLInputElement).files
  if (files?.[0]) {
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

const normalizeUrl = (url: string | null | undefined): string | null => {
  if (!url?.trim()) return null
  const trimmed = url.trim()
  if (trimmed.match(/^https?:\/\//i)) return trimmed
  return `https://${trimmed}`
}

const loadCurrentSettings = async () => {
  if (loadingSettings.value) return
  
  loadingSettings.value = true
  try {
    // Use single source of truth from store
    let vendorProfile = authStore.vendorProfile

    if (!vendorProfile?.id) {
      try {
        await authStore.fetchCurrentUser()
        vendorProfile = authStore.vendorProfile
      } catch (err) {
        console.error('Error fetching user:', err)
      }
    }

    if (vendorProfile?.id) {
      supplierId.value = vendorProfile.id
      hasLoadedData.value = true

      formData.value = {
        store_name: vendorProfile.store_name || '',
        description: vendorProfile.description || '',
        contact_email: vendorProfile.contact_email || '',
        contact_phone: vendorProfile.contact_phone || '',
        website: vendorProfile.website || '',
        brand_color_primary: vendorProfile.brand_color_primary || '#4CAF50',
        brand_color_secondary: vendorProfile.brand_color_secondary || '#388E3C',
        slogan: vendorProfile.slogan || '',
        year_established: vendorProfile.year_established || null,
        employee_count: vendorProfile.employee_count || null,
        video_url: vendorProfile.video_url || '',
        meta_title: vendorProfile.meta_title || '',
        meta_description: vendorProfile.meta_description || ''
      }

      previewBanner.value = vendorProfile.banner_image || ''
      certifications.value = Array.isArray(vendorProfile.certifications) 
        ? vendorProfile.certifications 
        : []
      awards.value = Array.isArray(vendorProfile.awards) 
        ? vendorProfile.awards 
        : []
      socialMedia.value = vendorProfile.social_media || {
        linkedin: '',
        instagram: '',
        telegram: '',
        whatsapp: ''
      }
    } else {
      snackbarMessage.value = 'پروفایل یافت نشد'
      snackbarColor.value = 'warning'
      snackbar.value = true
    }
  } catch (error) {
    console.error('Error loading settings:', error)
    snackbarMessage.value = 'خطا در بارگذاری'
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
    const normalizedSocialMedia: any = {}
    for (const [key, value] of Object.entries(socialMedia.value)) {
      normalizedSocialMedia[key] = value && typeof value === 'string' 
        ? normalizeUrl(value) 
        : null
    }

    const updateData: any = {
      ...formData.value,
      website: formData.value.website ? normalizeUrl(formData.value.website) : null,
      video_url: formData.value.video_url ? normalizeUrl(formData.value.video_url) : null,
      certifications: certifications.value.filter(c => c.title),
      awards: awards.value.filter(a => a.title),
      social_media: normalizedSocialMedia
    }

    if (bannerFile.value.length > 0) {
      updateData.banner_image = bannerFile.value[0]
    }

    await supplierApi.updateSupplierProfile(updateData)
    const awarded = await awardMiniWebsite()
    if (awarded > 0) {
      snackbarMessage.value = `تغییرات ذخیره شد (+${awarded} امتیاز)`
      try {
        await gamificationStore.hydrate()
      } catch (e) {
        console.warn('Failed to hydrate gamification after mini site update', e)
      }
    }
    
    try {
      await authStore.fetchCurrentUser()
    } catch (err) {
      console.warn('Error refreshing user:', err)
    }

    bannerFile.value = []
    snackbarMessage.value = 'تغییرات ذخیره شد'
    snackbarColor.value = 'success'
    snackbar.value = true
  } catch (error: any) {
    console.error('Error saving:', error)
    snackbarMessage.value = error?.data?.error || 'خطا در ذخیره‌سازی'
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
  if (!supplierId.value) {
    await loadCurrentSettings()
  }

  if (previewUrl.value) {
    const fullUrl = window.location.origin + previewUrl.value
    window.open(fullUrl, '_blank', 'noopener,noreferrer')
  }
}

const copyPreviewUrl = async () => {
  if (previewUrl.value) {
    try {
      await navigator.clipboard.writeText(window.location.origin + previewUrl.value)
      snackbarMessage.value = 'آدرس کپی شد'
      snackbarColor.value = 'success'
      snackbar.value = true
    } catch {
      snackbarMessage.value = 'خطا در کپی‌کردن'
      snackbarColor.value = 'error'
      snackbar.value = true
    }
  }
}

const awardMiniWebsite = async (): Promise<number> => {
  try {
    const { useApiFetch } = await import('~/composables/useApiFetch')
    const resp = await useApiFetch<{ points?: number }>('gamification/award-section/', {
      method: 'POST',
      body: { section: 'miniWebsite' }
    })
    await gamificationStore.fetchScores()
    return resp?.points || 0
  } catch (e) {
    console.warn('Failed to award miniWebsite section', e)
    return 0
  }
}

// Lifecycle
watch(() => authStore.vendorProfile, (newProfile) => {
  if (newProfile?.id && isMounted.value && !supplierId.value) {
    loadCurrentSettings()
  }
}, { deep: true })

onMounted(async () => {
  isMounted.value = true
  if (authStore.token && !authStore.user) {
    try {
      await authStore.initializeAuth()
    } catch (err) {
      console.warn('Auth error:', err)
    }
  }
  await nextTick()
  loadCurrentSettings()
})
</script>

<style scoped>
.mini-website-settings {
  max-width: 1000px;
  margin: 0 auto;
}

/* Larger text inputs for older users */
.text-input-large :deep(.v-field__input) {
  font-size: 16px !important;
  padding: 12px !important;
}

/* Color picker styling */
.color-input {
  max-width: 100px;
}

/* Line height for better readability */
.line-height-lg {
  line-height: 1.8;
}

/* Button spacing */
.gap-3 {
  gap: 12px;
}

.gap-4 {
  gap: 16px;
}

/* Card hover effects - subtle */
:deep(.v-card) {
  transition: box-shadow 0.2s ease;
}

:deep(.v-card:hover) {
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.1);
}
</style>