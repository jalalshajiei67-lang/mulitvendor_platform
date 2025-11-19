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
              @click.stop
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
                  ></v-text-field>
                </v-col>
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
                    hint="سال شروع فعالیت شرکت یا فروشگاه"
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
                    hint="تعداد کارمندان شرکت (اختیاری)"
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
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useSupplierApi } from '~/composables/useSupplierApi'
import { useGamificationStore } from '~/stores/gamification'
import FormQualityScore from '~/components/gamification/FormQualityScore.vue'

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

const formData = ref({
  store_name: '',
  description: '',
  contact_email: '',
  contact_phone: '',
  website: '',
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
const socialLinksCount = computed(() => Object.values(socialMedia.value).filter(Boolean).length)

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
  loadingSettings.value = true
  try {
    let user = authStore.user
    let vendorProfile: any = null
    
    // Try to get vendor profile from user object
    if (user?.vendor_profile) {
      vendorProfile = user.vendor_profile
    } else if (authStore.vendorProfile) {
      vendorProfile = authStore.vendorProfile
    } else {
      // If vendor profile is not available, fetch current user data
      console.log('Vendor profile not found, fetching current user...')
      try {
        await authStore.fetchCurrentUser()
        user = authStore.user
        if (user?.vendor_profile) {
          vendorProfile = user.vendor_profile
        } else if (authStore.vendorProfile) {
          vendorProfile = authStore.vendorProfile
        }
      } catch (err) {
        console.error('Error fetching current user:', err)
      }
    }
    
    if (vendorProfile && vendorProfile.id) {
      supplierId.value = vendorProfile.id
      console.log('Vendor profile loaded, ID:', vendorProfile.id, 'Store name:', vendorProfile.store_name)
      
      formData.value = {
        store_name: vendorProfile.store_name || '',
        description: vendorProfile.description || '',
        contact_email: vendorProfile.contact_email || '',
        contact_phone: vendorProfile.contact_phone || '',
        website: vendorProfile.website || '',
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

    snackbarMessage.value = 'همه تغییرات با موفقیت ذخیره شد'
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

