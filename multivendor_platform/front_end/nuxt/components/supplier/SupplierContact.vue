<template>
  <div class="supplier-contact" dir="rtl">
    <v-container>
      <v-row>
        <!-- Contact Form -->
        <v-col cols="12" md="6">
          <v-card elevation="4" class="contact-form-card">
            <v-card-title class="text-h5 font-weight-bold">
              تماس با ما
            </v-card-title>
            <v-card-text>
              <v-form ref="formRef" v-model="formValid" @submit.prevent="submitForm">
                <v-text-field
                  v-model="formData.sender_name"
                  label="نام و نام خانوادگی"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  :rules="[rules.required]"
                  required
                  class="mb-2"
                ></v-text-field>

                <v-text-field
                  v-model="formData.sender_email"
                  label="ایمیل"
                  prepend-inner-icon="mdi-email"
                  variant="outlined"
                  type="email"
                  :rules="[rules.required, rules.email]"
                  required
                  class="mb-2"
                ></v-text-field>

                <v-text-field
                  v-model="formData.sender_phone"
                  label="شماره تماس (اختیاری)"
                  prepend-inner-icon="mdi-phone"
                  variant="outlined"
                  class="mb-2"
                ></v-text-field>

                <v-text-field
                  v-model="formData.subject"
                  label="موضوع"
                  prepend-inner-icon="mdi-text-subject"
                  variant="outlined"
                  :rules="[rules.required]"
                  required
                  class="mb-2"
                ></v-text-field>

                <v-textarea
                  v-model="formData.message"
                  label="پیام"
                  prepend-inner-icon="mdi-message-text"
                  variant="outlined"
                  rows="5"
                  :rules="[rules.required]"
                  required
                  class="mb-2"
                ></v-textarea>

                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  block
                  :loading="submitting"
                  :disabled="!formValid"
                  prepend-icon="mdi-send"
                >
                  ارسال پیام
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Contact Information -->
        <v-col cols="12" md="6">
          <v-card elevation="4" class="contact-info-card">
            <v-card-title class="text-h5 font-weight-bold">
              اطلاعات تماس
            </v-card-title>
            <v-card-text>
              <v-list bg-color="transparent">
                <v-list-item
                  v-if="supplier.contact_email"
                  prepend-icon="mdi-email"
                  :title="supplier.contact_email"
                  subtitle="ایمیل"
                >
                  <template v-slot:append>
                    <v-btn
                      icon="mdi-content-copy"
                      variant="text"
                      size="small"
                      @click="copyToClipboard(supplier.contact_email)"
                    ></v-btn>
                  </template>
                </v-list-item>

                <v-list-item
                  v-if="supplier.contact_phone"
                  prepend-icon="mdi-phone"
                  :title="supplier.contact_phone"
                  subtitle="تلفن"
                >
                  <template v-slot:append>
                    <v-btn
                      icon="mdi-content-copy"
                      variant="text"
                      size="small"
                      @click="copyToClipboard(supplier.contact_phone)"
                    ></v-btn>
                  </template>
                </v-list-item>

                <v-list-item
                  v-if="supplier.website"
                  prepend-icon="mdi-web"
                  :title="supplier.website"
                  subtitle="وب‌سایت"
                  :href="supplier.website"
                  target="_blank"
                ></v-list-item>

                <v-list-item
                  v-if="supplier.address"
                  prepend-icon="mdi-map-marker"
                  :title="supplier.address"
                  subtitle="آدرس"
                >
                  <template v-slot:append>
                    <v-btn
                      icon="mdi-content-copy"
                      variant="text"
                      size="small"
                      @click="copyToClipboard(supplier.address)"
                    ></v-btn>
                  </template>
                </v-list-item>
              </v-list>

              <!-- Social Media -->
              <div v-if="supplier.social_media" class="social-media mt-4">
                <h3 class="text-subtitle-1 font-weight-bold mb-3">شبکه‌های اجتماعی</h3>
                <div class="d-flex flex-wrap gap-2">
                  <v-btn
                    v-if="supplier.social_media.linkedin"
                    icon="mdi-linkedin"
                    color="blue-darken-3"
                    :href="supplier.social_media.linkedin"
                    target="_blank"
                  ></v-btn>
                  <v-btn
                    v-if="supplier.social_media.instagram"
                    icon="mdi-instagram"
                    color="pink"
                    :href="supplier.social_media.instagram"
                    target="_blank"
                  ></v-btn>
                  <v-btn
                    v-if="supplier.social_media.telegram"
                    icon="mdi-telegram"
                    color="blue"
                    :href="supplier.social_media.telegram"
                    target="_blank"
                  ></v-btn>
                  <v-btn
                    v-if="supplier.social_media.whatsapp"
                    icon="mdi-whatsapp"
                    color="green"
                    :href="supplier.social_media.whatsapp"
                    target="_blank"
                  ></v-btn>
                  <v-btn
                    v-if="supplier.social_media.twitter"
                    icon="mdi-twitter"
                    color="blue-lighten-1"
                    :href="supplier.social_media.twitter"
                    target="_blank"
                  ></v-btn>
                </div>
              </div>

              <!-- Video -->
              <div v-if="supplier.video_url" class="mt-6">
                <h3 class="text-subtitle-1 font-weight-bold mb-3">ویدیو معرفی</h3>
                <div class="video-container">
                  <iframe
                    :src="getEmbedUrl(supplier.video_url)"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen
                    class="video-iframe"
                  ></iframe>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Success Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000" location="top">
      {{ snackbarMessage }}
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Supplier } from '~/composables/useSupplierApi'
import { useSupplierContactApi, type SupplierContactMessage } from '~/composables/useSupplierContactApi'

interface Props {
  supplier: Supplier
}

const props = defineProps<Props>()
const contactApi = useSupplierContactApi()

const formRef = ref()
const formValid = ref(false)
const submitting = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const formData = ref({
  sender_name: '',
  sender_email: '',
  sender_phone: '',
  subject: '',
  message: ''
})

const rules = {
  required: (value: string) => !!value || 'این فیلد الزامی است',
  email: (value: string) => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return pattern.test(value) || 'ایمیل معتبر نیست'
  }
}

const submitForm = async () => {
  if (!formValid.value) return

  submitting.value = true

  try {
    await contactApi.createContactMessage({
      vendor_profile: props.supplier.id,
      ...formData.value
    })

    snackbarMessage.value = 'پیام شما با موفقیت ارسال شد'
    snackbarColor.value = 'success'
    snackbar.value = true

    // Reset form
    formData.value = {
      sender_name: '',
      sender_email: '',
      sender_phone: '',
      subject: '',
      message: ''
    }
    formRef.value?.reset()
  } catch (error) {
    console.error('Error submitting contact form:', error)
    snackbarMessage.value = 'خطا در ارسال پیام. لطفاً دوباره تلاش کنید'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    submitting.value = false
  }
}

const copyToClipboard = (text: string) => {
  navigator.clipboard.writeText(text).then(() => {
    snackbarMessage.value = 'کپی شد'
    snackbarColor.value = 'success'
    snackbar.value = true
  })
}

const getEmbedUrl = (url: string) => {
  // Convert YouTube URL to embed format
  if (url.includes('youtube.com') || url.includes('youtu.be')) {
    const videoId = url.match(/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/)?.[1]
    return videoId ? `https://www.youtube.com/embed/${videoId}` : url
  }
  // Convert Aparat URL to embed format
  if (url.includes('aparat.com')) {
    const videoId = url.match(/aparat\.com\/v\/([^"&?\/\s]+)/)?.[1]
    return videoId ? `https://www.aparat.com/video/video/embed/videohash/${videoId}/vt/frame` : url
  }
  return url
}
</script>

<style scoped>
.contact-form-card,
.contact-info-card {
  border-radius: 16px;
  height: 100%;
}

.social-media .v-btn {
  margin: 4px;
}

.video-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  height: 0;
  overflow: hidden;
  border-radius: 12px;
}

.video-iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>

