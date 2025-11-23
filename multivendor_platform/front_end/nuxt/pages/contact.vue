<template>
  <div class="contact-us" dir="rtl">
    <!-- Loading State -->
    <div v-if="pending" class="loading-container">
      <v-container class="text-center py-16">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        <p class="mt-4">در حال بارگذاری...</p>
      </v-container>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <v-container class="text-center py-16">
        <v-alert type="error" variant="tonal" prominent>
          <v-alert-title>خطا در بارگذاری صفحه</v-alert-title>
          <p class="mt-2">{{ error }}</p>
        </v-alert>
      </v-container>
    </div>

    <!-- Content -->
    <template v-else-if="page">
      <!-- Hero Section -->
      <div class="hero-section">
        <v-container class="py-10 text-center text-white">
          <div class="hero-content">
            <h1>{{ page.title_fa || 'تماس با ما' }}</h1>
            <p v-if="page.content_fa" class="hero-subtitle" v-html="getExcerpt(page.content_fa)"></p>
            <p v-else>ما اینجا هستیم تا به شما کمک کنیم</p>
          </div>
        </v-container>
      </div>

      <!-- Content Section -->
      <div v-if="page.content_fa" class="content-section">
        <div class="container">
          <div class="content-wrapper">
            <div class="content-text" v-html="page.content_fa"></div>
          </div>
        </div>
      </div>

      <!-- Contact Information Section -->
      <div class="contact-section">
        <div class="container">
          <h2>اطلاعات تماس</h2>
          <div class="contact-grid">
            <!-- Email -->
            <div v-if="page.email" class="contact-card">
              <div class="contact-icon">
                <v-icon size="48">mdi-email</v-icon>
              </div>
              <h3>ایمیل</h3>
              <a :href="`mailto:${page.email}`" class="contact-link">{{ page.email }}</a>
            </div>

            <!-- Phone -->
            <div v-if="page.phone" class="contact-card">
              <div class="contact-icon">
                <v-icon size="48">mdi-phone</v-icon>
              </div>
              <h3>تلفن</h3>
              <a :href="`tel:${page.phone.replace(/\s/g, '')}`" class="contact-link">{{ page.phone }}</a>
            </div>

            <!-- Address -->
            <div v-if="page.address_fa" class="contact-card">
              <div class="contact-icon">
                <v-icon size="48">mdi-map-marker</v-icon>
              </div>
              <h3>آدرس</h3>
              <div class="contact-text" v-html="page.address_fa"></div>
            </div>

            <!-- Working Hours -->
            <div v-if="page.working_hours_fa" class="contact-card">
              <div class="contact-icon">
                <v-icon size="48">mdi-clock-outline</v-icon>
              </div>
              <h3>ساعات کاری</h3>
              <p class="contact-text">{{ page.working_hours_fa }}</p>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { usePagesApi, type ContactPage } from '~/composables/usePagesApi'

const pagesApi = usePagesApi()

// Fetch contact page data
const { data: page, pending, error } = await useAsyncData<ContactPage>(
  'contact-page',
  async () => {
    try {
      return await pagesApi.getContactPage()
    } catch (err: any) {
      console.error('Error fetching contact page:', err)
      throw new Error(err?.data?.detail || err?.message || 'خطا در بارگذاری صفحه تماس با ما')
    }
  }
)

// Helper function to get excerpt from HTML content
const getExcerpt = (html: string, maxLength: number = 100): string => {
  if (!html) return ''
  // Remove HTML tags
  const text = html.replace(/<[^>]*>/g, '')
  // Return excerpt
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

// Update SEO meta tags (reactive)
useHead({
  title: computed(() => page.value?.meta_title_fa || page.value?.title_fa || 'تماس با ما'),
  meta: computed(() => [
    {
      name: 'description',
      content: page.value?.meta_description_fa || 'راه‌های ارتباط با ما'
    },
    {
      name: 'keywords',
      content: page.value?.meta_keywords_fa || 'تماس، آدرس، تلفن، ایمیل'
    }
  ])
})
</script>

<style scoped>
.contact-us {
  min-height: 100vh;
  direction: rtl;
  text-align: right;
  background-color: rgba(var(--v-theme-surface), 0.97);
  color: rgba(var(--v-theme-on-surface), 0.92);
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.85), rgba(var(--v-theme-secondary), 0.9));
  color: rgba(var(--v-theme-on-primary), 0.98);
  margin: 16px auto 36px;
  max-width: 1440px;
  border-radius: 24px;
  text-align: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.12);
}

.hero-section::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(var(--v-theme-surface), 0.28), transparent 60%);
  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 20px;
  font-weight: 700;
}

.hero-content p {
  font-size: 1.2rem;
  opacity: 0.95;
}

/* About Section */
.about-section {
  padding: 80px 20px;
  background-color: transparent;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.about-content {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.12), rgba(var(--v-theme-secondary), 0.16));
  padding: 50px 40px;
  border-radius: 20px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
  color: rgba(var(--v-theme-on-surface), 0.95);
  text-align: center;
  position: relative;
  overflow: hidden;
}

.about-content::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(var(--v-theme-surface), 0.65), transparent);
  opacity: 0.45;
  pointer-events: none;
}

.about-content h2 {
  font-size: 2rem;
  margin-bottom: 30px;
  font-weight: 700;
  position: relative;
  z-index: 1;
  color: rgba(var(--v-theme-on-surface), 0.98);
}

.about-text {
  font-size: 1.1rem;
  line-height: 2;
  max-width: 900px;
  margin: 0 auto;
  text-align: justify;
  position: relative;
  z-index: 1;
  color: rgba(var(--v-theme-on-surface), 0.9);
}

/* Loading and Error States */
.loading-container,
.error-container {
  min-height: 50vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Content Section */
.content-section {
  padding: 80px 20px;
  background-color: transparent;
}

.content-wrapper {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.12), rgba(var(--v-theme-secondary), 0.16));
  padding: 50px 40px;
  border-radius: 20px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
  color: rgba(var(--v-theme-on-surface), 0.95);
  position: relative;
  overflow: hidden;
}

.content-wrapper::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(var(--v-theme-surface), 0.65), transparent);
  opacity: 0.45;
  pointer-events: none;
}

.content-text {
  font-size: 1.1rem;
  line-height: 2;
  position: relative;
  z-index: 1;
  color: rgba(var(--v-theme-on-surface), 0.9);
  direction: rtl;
  text-align: justify;
}

.content-text :deep(p) {
  margin-bottom: 1rem;
}

.content-text :deep(h1),
.content-text :deep(h2),
.content-text :deep(h3) {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.content-text :deep(ul),
.content-text :deep(ol) {
  margin: 1rem 0;
  padding-right: 2rem;
}

.content-text :deep(li) {
  margin-bottom: 0.5rem;
}

.hero-subtitle {
  font-size: 1.2rem;
  opacity: 0.95;
  max-width: 800px;
  margin: 0 auto;
}

.contact-text {
  color: rgba(var(--v-theme-on-surface), 0.92);
  font-size: 1.1rem;
  line-height: 1.8;
  margin: 0;
  word-break: break-word;
}

/* Contact Section */
.contact-section {
  padding: 80px 20px;
  background-color: transparent;
}

.contact-section h2 {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 60px;
  color: rgba(var(--v-theme-on-surface), 0.98);
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
}

.contact-card {
  background: rgb(var(--v-theme-surface));
  padding: 40px 30px;
  border-radius: 18px;
  text-align: center;
  box-shadow: 0 10px 28px rgba(var(--v-theme-on-surface), 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  color: rgba(var(--v-theme-on-surface), 0.92);
  border: 1px solid rgba(var(--v-theme-primary), 0.12);
}

.contact-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 18px 36px rgba(var(--v-theme-on-surface), 0.12);
  border-color: rgba(var(--v-theme-primary), 0.3);
}

.contact-icon {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  opacity: 0.95;
}

.contact-card h3 {
  font-size: 1.3rem;
  margin-bottom: 15px;
  font-weight: 600;
  color: rgba(var(--v-theme-on-surface), 0.96);
}

.contact-link {
  color: rgb(var(--v-theme-primary));
  text-decoration: none;
  font-size: 1.1rem;
  display: inline-block;
  transition: opacity 0.3s ease;
  word-break: break-word;
}

.contact-link:hover {
  opacity: 0.85;
  text-decoration: underline;
}

.contact-card :deep(.v-icon) {
  color: rgb(var(--v-theme-primary));
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .hero-content p {
    font-size: 1rem;
  }

  .about-content {
    padding: 30px 20px;
  }

  .about-content h2 {
    font-size: 1.6rem;
    margin-bottom: 20px;
  }

  .about-text {
    font-size: 1rem;
    line-height: 1.8;
  }

  .contact-section h2 {
    font-size: 2rem;
    margin-bottom: 40px;
  }

  .contact-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .contact-card {
    padding: 30px 20px;
  }

  .contact-icon {
    margin-bottom: 15px;
  }

  .contact-card h3 {
    font-size: 1.1rem;
  }

  .contact-link {
    font-size: 1rem;
  }

  .content-wrapper {
    padding: 30px 20px;
  }

  .content-text {
    font-size: 1rem;
    line-height: 1.8;
  }
}
</style>

