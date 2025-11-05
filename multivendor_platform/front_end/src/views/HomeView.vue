<template>
  <div class="home" dir="rtl">
    <!-- Hero Section with Large Search -->
    <v-container fluid class="hero-section pa-0">
      <v-row no-gutters justify="center" align="center" class="hero-content">
        <v-col cols="12" md="10" lg="8" class="pa-4 pa-md-8">
          <!-- Large Search Box -->
          <v-card 
            elevation="8" 
            rounded="xl" 
            class="search-card pa-4 pa-md-6 mb-4"
            color="surface"
          >
            <v-card-text class="pa-0">
              <v-text-field
                v-model="searchQuery"
                placeholder="چه دستگاهی نیاز دارید؟"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                rounded="lg"
                hide-details
                class="home-search-input"
                density="comfortable"
                @click="handleSearchClick"
                readonly
              >
                <template v-slot:append-inner>
                  <v-btn
                    color="primary"
                    size="large"
                    rounded="lg"
                    elevation="2"
                    @click="handleSearchClick"
                    class="search-button"
                  >
                    جستجو
                  </v-btn>
                </template>
              </v-text-field>
            </v-card-text>
          </v-card>

          <!-- Subtitle -->
          <p class="search-subtitle text-center text-body-1 text-md-h6">
            از بین تولیدات بهترین تولید کنندگان ماشین آلات نیاز خود را جستجو کنید
          </p>
        </v-col>
      </v-row>
    </v-container>

    <!-- Indexo for Buyers Section -->
    <v-container class="buyers-section py-8 py-md-12">
      <v-card 
        elevation="4" 
        rounded="xl" 
        class="section-card buyers-card"
        color="info"
      >
        <v-card-title class="section-title text-h4 text-md-h3 text-center pa-6 pa-md-8">
          <v-icon size="large" class="ml-2">mdi-account-group</v-icon>
          ایندکسو برای خریداران
        </v-card-title>

        <v-card-text class="pa-4 pa-md-6">
          <!-- Advantages Grid -->
          <v-row class="advantages-grid mb-6">
            <v-col 
              v-for="(advantage, index) in buyerAdvantages" 
              :key="index"
              cols="12" 
              sm="6" 
              md="4"
              class="d-flex justify-center"
            >
              <v-card 
                elevation="2" 
                rounded="lg" 
                class="advantage-card pa-4 pa-md-6 text-center"
                color="surface"
              >
                <v-icon 
                  :icon="advantage.icon" 
                  size="64" 
                  :color="advantage.color"
                  class="mb-4"
                ></v-icon>
                <h3 class="text-h6 text-md-h5 font-weight-bold mb-3">
                  {{ advantage.title }}
                </h3>
                <p class="text-body-2 text-md-body-1 text-medium-emphasis">
                  {{ advantage.description }}
                </p>
              </v-card>
            </v-col>
          </v-row>

          <!-- CTA Section -->
          <v-card 
            elevation="2" 
            rounded="lg" 
            class="cta-card pa-4 pa-md-6 mb-4"
            color="surface"
          >
            <v-row align="center" no-gutters>
              <v-col cols="12" md="8" class="pa-2 pa-md-4">
                <p class="text-body-1 text-md-h6 mb-0">
                  همین الان درخواست خودت را ثبت کن و منتظر تماس تامین کنندگان معتبر باش
                </p>
              </v-col>
              <v-col cols="12" md="4" class="pa-2 pa-md-4 text-center text-md-end">
                <v-btn
                  color="primary"
                  size="large"
                  rounded="lg"
                  elevation="2"
                  prepend-icon="mdi-file-document-edit"
                  @click="handleBuyerCTA"
                  block
                  class="cta-button"
                >
                  ثبت درخواست
                </v-btn>
              </v-col>
            </v-row>
          </v-card>
        </v-card-text>
      </v-card>
    </v-container>

    <!-- Indexo for Sellers Section -->
    <v-container class="sellers-section py-8 py-md-12">
      <v-card 
        elevation="4" 
        rounded="xl" 
        class="section-card sellers-card"
        color="success"
      >
        <v-card-title class="section-title text-h4 text-md-h3 text-center pa-6 pa-md-8">
          <v-icon size="large" class="ml-2">mdi-store</v-icon>
          ایندکسو برای فروشندگان
        </v-card-title>

        <v-card-text class="pa-4 pa-md-6">
          <!-- Advantages Grid -->
          <v-row class="advantages-grid mb-6">
            <v-col 
              v-for="(advantage, index) in sellerAdvantages" 
              :key="index"
              cols="12" 
              sm="6" 
              md="4"
              class="d-flex justify-center"
            >
              <v-card 
                elevation="2" 
                rounded="lg" 
                class="advantage-card pa-4 pa-md-6 text-center"
                color="surface"
              >
                <v-icon 
                  :icon="advantage.icon" 
                  size="64" 
                  :color="advantage.color"
                  class="mb-4"
                ></v-icon>
                <h3 class="text-h6 text-md-h5 font-weight-bold mb-3">
                  {{ advantage.title }}
                </h3>
                <p class="text-body-2 text-md-body-1 text-medium-emphasis">
                  {{ advantage.description }}
                </p>
              </v-card>
            </v-col>
          </v-row>

          <!-- CTA Section -->
          <v-card 
            elevation="2" 
            rounded="lg" 
            class="cta-card pa-4 pa-md-6 mb-4"
            color="surface"
          >
            <v-row align="center" no-gutters>
              <v-col cols="12" md="8" class="pa-2 pa-md-4">
                <p class="text-body-1 text-md-h6 mb-0">
                  برای شروع همکاری و بهره بردن از امکانات ایندکسو ثبت نام کنید
                </p>
              </v-col>
              <v-col cols="12" md="4" class="pa-2 pa-md-4 text-center text-md-end">
                <v-btn
                  color="primary"
                  size="large"
                  rounded="lg"
                  elevation="2"
                  prepend-icon="mdi-account-plus"
                  @click="handleSellerCTA"
                  block
                  class="cta-button"
                >
                  ثبت نام بعنوان تامین کننده
                </v-btn>
              </v-col>
            </v-row>
          </v-card>
        </v-card-text>
      </v-card>
    </v-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchQuery = ref('')

// Buyer Advantages
const buyerAdvantages = [
  {
    icon: 'mdi-account-switch',
    title: 'ارتباط مستقیم',
    description: 'بدون واسطه و اصطکاک، مستقیماً با تامین‌کنندگان معتبر در ارتباط باشید',
    color: 'info'
  },
  {
    icon: 'mdi-shield-check',
    title: 'تامین‌کنندگان معتبر',
    description: 'از بین بهترین تولیدکنندگان ماشین‌آلات، تامین‌کننده مناسب خود را پیدا کنید',
    color: 'success'
  },
  {
    icon: 'mdi-lightning-bolt',
    title: 'مسیر کوتاه خرید',
    description: 'فرآیند خرید را کوتاه کرده و سریع‌تر به محصول مورد نظر خود برسید',
    color: 'warning'
  }
]

// Seller Advantages
const sellerAdvantages = [
  {
    icon: 'mdi-cash',
    title: 'هزینه کم',
    description: 'با حداقل هزینه، محصولات خود را به خریداران هدف معرفی کنید',
    color: 'success'
  },
  {
    icon: 'mdi-chart-line',
    title: 'فروش آسان',
    description: 'مدل کسب‌وکار بدون زحمت و با حداقل تلاش برای افزایش فروش',
    color: 'primary'
  },
  {
    icon: 'mdi-handshake',
    title: 'دسترسی به خریداران',
    description: 'مستقیماً با خریداران واقعی در صنعت ماشین‌آلات ارتباط برقرار کنید',
    color: 'info'
  }
]

const handleSearchClick = () => {
  // Placeholder - no action needed
  console.log('Search clicked')
}

const handleBuyerCTA = () => {
  // Navigate to # as placeholder
  window.location.href = '#'
}

const handleSellerCTA = () => {
  // Navigate to register page
  router.push('/register')
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  direction: rtl;
  background-color: #FAFAFA;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #1976D2 0%, #2196F3 100%);
  min-height: 400px;
  display: flex;
  align-items: center;
  padding: 60px 20px;
}

@media (min-width: 960px) {
  .hero-section {
    min-height: 500px;
  }
}

.hero-content {
  width: 100%;
}

.search-card {
  max-width: 100%;
  margin: 0 auto;
}

.home-search-input :deep(.v-field) {
  font-size: 1.125rem;
  padding: 12px 16px;
}

@media (min-width: 960px) {
  .home-search-input :deep(.v-field) {
    font-size: 1.25rem;
    padding: 16px 20px;
  }
}

.home-search-input :deep(.v-field__input) {
  min-height: 56px;
}

@media (min-width: 960px) {
  .home-search-input :deep(.v-field__input) {
    min-height: 64px;
  }
}

.search-button {
  min-width: 120px;
}

@media (min-width: 960px) {
  .search-button {
    min-width: 140px;
  }
}

.search-subtitle {
  color: white;
  opacity: 0.95;
  font-weight: 400;
  margin-top: 24px;
}

/* Section Cards */
.section-card {
  max-width: 1200px;
  margin: 0 auto;
}

.buyers-card {
  background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
}

.sellers-card {
  background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
}

.section-title {
  color: #1C1B1F;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Advantages Grid */
.advantages-grid {
  margin-top: 24px;
}

.advantage-card {
  height: 100%;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.advantage-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15) !important;
}

/* CTA Cards */
.cta-card {
  background: white;
}

.cta-button {
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* Mobile Responsive */
@media (max-width: 959px) {
  .hero-section {
    padding: 40px 16px;
    min-height: 350px;
  }

  .search-card {
    padding: 16px !important;
  }

  .section-title {
    font-size: 1.75rem !important;
    flex-direction: column;
    gap: 8px;
  }

  .advantage-card {
    margin-bottom: 16px;
  }

  .cta-card .v-row {
    flex-direction: column-reverse;
  }

  .cta-card .v-col {
    text-align: center !important;
  }
}

/* RTL Support */
:deep(.v-field__prepend-inner) {
  padding-left: 12px;
  padding-right: 0;
}

:deep(.v-field__append-inner) {
  padding-right: 12px;
  padding-left: 0;
}
</style>
