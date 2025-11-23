<template>
  <div class="supplier-contact" dir="rtl">
    <v-container class="contact-container">
      <!-- Section Header -->
      <div class="section-header text-center mb-8">
        <h2 class="text-h4 font-weight-bold mb-3">با ما در تماس باشید</h2>
        <p class="text-body-1 text-medium-emphasis">
          سوالات خود را بپرسید یا پروژه خود را با ما در میان بگذارید
        </p>
      </div>

      <v-row class="contact-row">
        <!-- Enhanced Contact Form -->
        <v-col cols="12" lg="7" class="form-col">
          <v-card elevation="8" class="contact-form-card glass-card" rounded="xl">
            <v-card-title class="text-h5 font-weight-bold pa-6">
              <div class="title-wrapper">
                <v-icon start color="primary" size="large">mdi-email-edit</v-icon>
                <span>ارسال پیام</span>
              </div>
            </v-card-title>
            <v-card-text class="pa-6">
              <v-form ref="formRef" v-model="formValid" @submit.prevent="submitForm">
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="formData.sender_name"
                      label="نام و نام خانوادگی"
                      prepend-inner-icon="mdi-account"
                      variant="outlined"
                      :rules="[rules.required]"
                      required
                      density="comfortable"
                      class="modern-input"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="formData.sender_email"
                      label="ایمیل"
                      prepend-inner-icon="mdi-email"
                      variant="outlined"
                      type="email"
                      :rules="[rules.required, rules.email]"
                      required
                      density="comfortable"
                      class="modern-input"
                    ></v-text-field>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="formData.sender_phone"
                      label="شماره تماس"
                      prepend-inner-icon="mdi-phone"
                      variant="outlined"
                      density="comfortable"
                      class="modern-input"
                      hint="اختیاری"
                      persistent-hint
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-select
                      v-model="formData.inquiry_type"
                      :items="inquiryTypes"
                      label="نوع درخواست"
                      prepend-inner-icon="mdi-help-circle"
                      variant="outlined"
                      density="comfortable"
                      class="modern-input"
                    ></v-select>
                  </v-col>
                </v-row>

                <v-text-field
                  v-model="formData.subject"
                  label="موضوع"
                  prepend-inner-icon="mdi-text-subject"
                  variant="outlined"
                  :rules="[rules.required]"
                  required
                  density="comfortable"
                  class="modern-input mb-4"
                ></v-text-field>

                <v-textarea
                  v-model="formData.message"
                  label="پیام شما"
                  prepend-inner-icon="mdi-message-text"
                  variant="outlined"
                  rows="6"
                  :rules="[rules.required]"
                  required
                  density="comfortable"
                  class="modern-input mb-6"
                  hint="جزئیات بیشتری درباره درخواست خود بنویسید"
                  persistent-hint
                ></v-textarea>

                <!-- Quick Action Buttons -->
                <div class="quick-actions mb-6">
                  <span class="text-caption text-medium-emphasis mb-2 d-block">یا می‌توانید سریع تماس بگیرید:</span>
                  <div class="action-buttons">
                    <v-btn
                      v-if="supplier.contact_phone"
                      :href="`tel:${supplier.contact_phone}`"
                      color="success"
                      variant="outlined"
                      prepend-icon="mdi-phone"
                      class="quick-btn"
                    >
                      تماس تلفنی
                    </v-btn>
                    <v-btn
                      v-if="supplier.contact_email"
                      :href="`mailto:${supplier.contact_email}`"
                      color="primary"
                      variant="outlined"
                      prepend-icon="mdi-email"
                      class="quick-btn"
                    >
                      ارسال ایمیل
                    </v-btn>
                <v-btn
                  v-if="supplier.social_media?.whatsapp"
                  :href="supplier.social_media.whatsapp"
                  target="_blank"
                  rel="nofollow noopener noreferrer"
                  color="#25D366"
                  variant="outlined"
                  prepend-icon="mdi-whatsapp"
                  class="quick-btn"
                >
                  واتس‌اپ
                </v-btn>
                  </div>
                </div>

                <v-btn
                  type="submit"
                  color="primary"
                  size="x-large"
                  block
                  :loading="submitting"
                  :disabled="!formValid"
                  prepend-icon="mdi-send"
                  class="submit-btn"
                  elevation="4"
                >
                  <span class="submit-text">ارسال پیام</span>
                  <v-icon end class="submit-icon">mdi-chevron-left</v-icon>
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Enhanced Contact Information -->
        <v-col cols="12" lg="5" class="info-col">
          <!-- Contact Info Card -->
          <v-card elevation="8" class="contact-info-card glass-card mb-6" rounded="xl">
            <v-card-title class="text-h5 font-weight-bold pa-6">
              <div class="title-wrapper">
                <v-icon start color="primary" size="large">mdi-card-account-details</v-icon>
                <span>اطلاعات تماس</span>
              </div>
            </v-card-title>
            <v-card-text class="pa-6">
              <div class="contact-items">
                <v-list bg-color="transparent" class="contact-list">
                  <!-- Email -->
                  <v-list-item
                    v-if="supplier.contact_email"
                    class="contact-item"
                    @click="copyToClipboard(supplier.contact_email)"
                  >
                    <template v-slot:prepend>
                      <div class="icon-container email-icon">
                        <v-icon color="primary">mdi-email</v-icon>
                      </div>
                    </template>
                    <v-list-item-title class="contact-title">{{ supplier.contact_email }}</v-list-item-title>
                    <v-list-item-subtitle class="contact-subtitle">ایمیل</v-list-item-subtitle>
                    <template v-slot:append>
                      <v-btn
                        icon="mdi-content-copy"
                        variant="text"
                        size="small"
                        color="primary"
                        class="copy-btn"
                        @click.stop="copyToClipboard(supplier.contact_email)"
                      ></v-btn>
                    </template>
                  </v-list-item>

                  <!-- Phone -->
                  <v-list-item
                    v-if="supplier.contact_phone"
                    class="contact-item"
                    :href="`tel:${supplier.contact_phone}`"
                  >
                    <template v-slot:prepend>
                      <div class="icon-container phone-icon">
                        <v-icon color="success">mdi-phone</v-icon>
                      </div>
                    </template>
                    <v-list-item-title class="contact-title">{{ supplier.contact_phone }}</v-list-item-title>
                    <v-list-item-subtitle class="contact-subtitle">تلفن</v-list-item-subtitle>
                    <template v-slot:append>
                      <v-btn
                        icon="mdi-phone-in-talk"
                        variant="text"
                        size="small"
                        color="success"
                        class="call-btn"
                        :href="`tel:${supplier.contact_phone}`"
                        @click.stop
                      ></v-btn>
                    </template>
                  </v-list-item>

                  <!-- Website -->
                  <v-list-item
                    v-if="supplier.website"
                    class="contact-item"
                    :href="supplier.website"
                    target="_blank"
                    rel="nofollow noopener noreferrer"
                  >
                    <template v-slot:prepend>
                      <div class="icon-container website-icon">
                        <v-icon color="secondary">mdi-web</v-icon>
                      </div>
                    </template>
                    <v-list-item-title class="contact-title">{{ supplier.website }}</v-list-item-title>
                    <v-list-item-subtitle class="contact-subtitle">وب‌سایت</v-list-item-subtitle>
                    <template v-slot:append>
                      <v-btn
                        icon="mdi-open-in-new"
                        variant="text"
                        size="small"
                        color="secondary"
                        class="external-btn"
                        :href="supplier.website"
                        target="_blank"
                        rel="nofollow noopener noreferrer"
                        @click.stop
                      ></v-btn>
                    </template>
                  </v-list-item>

                  <!-- Address -->
                  <v-list-item
                    v-if="supplier.address"
                    class="contact-item"
                    @click="copyToClipboard(supplier.address)"
                  >
                    <template v-slot:prepend>
                      <div class="icon-container address-icon">
                        <v-icon color="info">mdi-map-marker</v-icon>
                      </div>
                    </template>
                    <v-list-item-title class="contact-title">{{ supplier.address }}</v-list-item-title>
                    <v-list-item-subtitle class="contact-subtitle">آدرس</v-list-item-subtitle>
                    <template v-slot:append>
                      <v-btn
                        icon="mdi-content-copy"
                        variant="text"
                        size="small"
                        color="info"
                        class="copy-btn"
                        @click.stop="copyToClipboard(supplier.address)"
                      ></v-btn>
                    </template>
                  </v-list-item>
                </v-list>
              </div>
            </v-card-text>
          </v-card>

          <!-- Enhanced Social Media -->
          <v-card v-if="supplier.social_media" elevation="8" class="social-media-card glass-card mb-6" rounded="xl">
            <v-card-title class="text-h6 font-weight-bold pa-6">
              <div class="title-wrapper">
                <v-icon start color="primary" size="large">mdi-share-variant</v-icon>
                <span>شبکه‌های اجتماعی</span>
              </div>
            </v-card-title>
            <v-card-text class="pa-6">
              <div class="social-grid">
                <v-btn
                  v-if="supplier.social_media.linkedin"
                  icon="mdi-linkedin"
                  size="large"
                  color="blue-darken-3"
                  variant="flat"
                  class="social-btn linkedin-btn"
                  :href="supplier.social_media.linkedin"
                  target="_blank"
                  rel="nofollow noopener noreferrer"
                  :title="'LinkedIn: ' + supplier.store_name"
                >
                  <span class="social-label">LinkedIn</span>
                </v-btn>
                <v-btn
                  v-if="supplier.social_media.instagram"
                  icon="mdi-instagram"
                  size="large"
                  color="#E4405F"
                  variant="flat"
                  class="social-btn instagram-btn"
                  :href="supplier.social_media.instagram"
                  target="_blank"
                  rel="nofollow noopener noreferrer"
                  :title="'Instagram: @' + supplier.store_name"
                >
                  <span class="social-label">Instagram</span>
                </v-btn>
                <v-btn
                  v-if="supplier.social_media.telegram"
                  icon="mdi-telegram"
                  size="large"
                  color="#0088cc"
                  variant="flat"
                  class="social-btn telegram-btn"
                  :href="supplier.social_media.telegram"
                  target="_blank"
                  rel="nofollow noopener noreferrer"
                  :title="'Telegram: ' + supplier.store_name"
                >
                  <span class="social-label">Telegram</span>
                </v-btn>
                <v-btn
                  v-if="supplier.social_media.whatsapp"
                  icon="mdi-whatsapp"
                  size="large"
                  color="#25D366"
                  variant="flat"
                  class="social-btn whatsapp-btn"
                  :href="supplier.social_media.whatsapp"
                  target="_blank"
                  rel="nofollow noopener noreferrer"
                  :title="'WhatsApp: ' + supplier.store_name"
                >
                  <span class="social-label">WhatsApp</span>
                </v-btn>
                <v-btn
                  v-if="supplier.social_media.twitter"
                  icon="mdi-twitter"
                  size="large"
                  color="#1DA1F2"
                  variant="flat"
                  class="social-btn twitter-btn"
                  :href="supplier.social_media.twitter"
                  target="_blank"
                  rel="nofollow noopener noreferrer"
                  :title="'Twitter: @' + supplier.store_name"
                >
                  <span class="social-label">Twitter</span>
                </v-btn>
                <v-btn
                  v-if="supplier.social_media.youtube"
                  icon="mdi-youtube"
                  size="large"
                  color="#FF0000"
                  variant="flat"
                  class="social-btn youtube-btn"
                  :href="supplier.social_media.youtube"
                  target="_blank"
                  rel="nofollow noopener noreferrer"
                  :title="'YouTube: ' + supplier.store_name"
                >
                  <span class="social-label">YouTube</span>
                </v-btn>
              </div>
            </v-card-text>
          </v-card>

          <!-- Business Hours -->
          <v-card v-if="supplier.business_hours" elevation="8" class="business-hours-card glass-card" rounded="xl">
            <v-card-title class="text-h6 font-weight-bold pa-6">
              <div class="title-wrapper">
                <v-icon start color="primary" size="large">mdi-clock-outline</v-icon>
                <span>ساعات کاری</span>
              </div>
            </v-card-title>
            <v-card-text class="pa-6">
              <div class="hours-list">
                <div
                  v-for="(hours, day) in supplier.business_hours"
                  :key="day"
                  class="hours-item"
                >
                  <span class="day-name">{{ day }}</span>
                  <span class="day-hours">{{ hours }}</span>
                </div>
              </div>
            </v-card-text>
          </v-card>

          <!-- Video Section -->
          <v-card v-if="supplier.video_url" elevation="8" class="video-card glass-card mt-6" rounded="xl">
            <v-card-title class="text-h6 font-weight-bold pa-6">
              <div class="title-wrapper">
                <v-icon start color="primary" size="large">mdi-video</v-icon>
                <span>ویدیو معرفی</span>
              </div>
            </v-card-title>
            <v-card-text class="pa-6">
              <div class="video-container">
                <iframe
                  :src="getEmbedUrl(supplier.video_url)"
                  frameborder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowfullscreen
                  class="video-iframe"
                  loading="lazy"
                ></iframe>
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

const inquiryTypes = [
  { title: 'پرسش عمومی', value: 'general' },
  { title: 'درخواست همکاری', value: 'partnership' },
  { title: 'پشتیبانی محصول', value: 'support' },
  { title: 'پیشنهاد پروژه', value: 'project' },
  { title: 'شکایات و پیشنهادات', value: 'feedback' },
  { title: 'سایر', value: 'other' }
]

const formData = ref({
  sender_name: '',
  sender_email: '',
  sender_phone: '',
  inquiry_type: '',
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
/* Contact Container */
.contact-container {
  max-width: 1400px;
}

.section-header {
  margin-bottom: 3rem;
}

.section-header h2 {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)), rgb(var(--v-theme-secondary, var(--v-theme-primary))));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
}

/* Contact Cards */
.contact-form-card,
.contact-info-card,
.social-media-card,
.business-hours-card,
.video-card {
  border-radius: 24px;
  height: fit-content;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.contact-form-card:hover,
.contact-info-card:hover,
.social-media-card:hover,
.business-hours-card:hover,
.video-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12) !important;
}

.title-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.glass-card {
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
}

/* Form Column */
.form-col {
  animation: slideInLeft 0.6s ease-out;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Info Column */
.info-col {
  animation: slideInRight 0.6s ease-out;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Modern Form Inputs */
.modern-input {
  transition: all 0.3s ease;
}

.modern-input:hover {
  transform: translateY(-1px);
}

.modern-input:focus-within {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.15);
}

/* Quick Actions */
.quick-actions {
  padding: 1.5rem;
  background: rgba(var(--v-theme-primary), 0.05);
  border-radius: 12px;
  border: 1px solid rgba(var(--v-theme-primary), 0.1);
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.quick-btn {
  border-radius: 8px;
  transition: all 0.3s ease;
}

.quick-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Submit Button */
.submit-btn {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)), rgb(var(--v-theme-primary-variant, var(--v-theme-primary)))) !important;
  color: white !important;
  border-radius: 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.submit-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.submit-btn:hover::before {
  opacity: 1;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(var(--v-theme-primary), 0.4);
}

.submit-text {
  font-weight: 600;
  letter-spacing: 0.5px;
}

.submit-icon {
  transition: transform 0.3s ease;
}

.submit-btn:hover .submit-icon {
  transform: translateX(-4px);
}

/* Contact Items */
.contact-items {
  position: relative;
}

.contact-list {
  padding: 0;
}

.contact-item {
  border-radius: 12px;
  margin-bottom: 8px;
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid transparent;
}

.contact-item:hover {
  background: rgba(var(--v-theme-surface-variant), 0.5);
  border-color: rgba(var(--v-theme-outline), 0.2);
  transform: translateX(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.icon-container {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.email-icon {
  background: rgba(var(--v-theme-primary), 0.1);
}

.phone-icon {
  background: rgba(76, 175, 80, 0.1);
}

.website-icon {
  background: rgba(var(--v-theme-secondary, var(--v-theme-primary)), 0.1);
}

.address-icon {
  background: rgba(33, 150, 243, 0.1);
}

.contact-title {
  font-weight: 600;
  color: rgba(var(--v-theme-on-surface), 0.9);
}

.contact-subtitle {
  color: rgba(var(--v-theme-on-surface), 0.6);
  font-size: 0.875rem;
}

.copy-btn,
.call-btn,
.external-btn {
  opacity: 0.7;
  transition: all 0.3s ease;
}

.contact-item:hover .copy-btn,
.contact-item:hover .call-btn,
.contact-item:hover .external-btn {
  opacity: 1;
  transform: scale(1.1);
}

/* Social Media Grid */
.social-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
}

.social-btn {
  border-radius: 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.social-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.2);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.social-btn:hover::before {
  opacity: 1;
}

.social-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.social-label {
  font-size: 0.75rem;
  font-weight: 500;
  z-index: 1;
  position: relative;
}

/* Business Hours */
.hours-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.hours-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: rgba(var(--v-theme-surface-variant), 0.3);
  border-radius: 8px;
}

.day-name {
  font-weight: 500;
  color: rgba(var(--v-theme-on-surface), 0.9);
}

.day-hours {
  color: rgba(var(--v-theme-on-surface), 0.7);
  font-size: 0.875rem;
}

/* Video Section */
.video-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  height: 0;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.video-iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 12px;
}

/* Mobile Optimizations */
@media (max-width: 960px) {
  .contact-row {
    gap: 2rem;
  }

  .form-col,
  .info-col {
    order: 1;
  }

  .info-col {
    order: 2;
  }
}

@media (max-width: 600px) {
  .section-header {
    margin-bottom: 2rem;
  }

  .section-header h2 {
    font-size: 1.75rem !important;
  }

  .contact-form-card,
  .contact-info-card,
  .social-media-card,
  .business-hours-card,
  .video-card {
    margin-bottom: 1.5rem;
  }

  .social-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .action-buttons {
    flex-direction: column;
  }

  .quick-btn {
    width: 100%;
  }

  .hours-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
}
</style>

