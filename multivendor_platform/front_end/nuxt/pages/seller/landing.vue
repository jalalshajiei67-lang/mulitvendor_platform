<template>
  <div class="seller-landing" dir="rtl">
    <!-- Hero Section with Value Proposition -->
    <section class="hero-section">
      <div class="hero-background">
        <div class="gradient-overlay"></div>
      </div>
      
      <v-container class="hero-container">
        <div class="hero-content">
          <!-- Main Headline -->
          <div class="headline-wrapper">
            <h1 class="main-headline">
              <span class="highlight">۲۰ تا ۵۰ مشتری رایگان</span>
              <br />
              <span class="sub-headline">هر روز برای شما!</span>
            </h1>
          </div>

          <!-- Value Proposition -->
          <div class="value-proposition">
            <div class="value-card">
              <v-icon size="48" color="success" class="value-icon">mdi-gift</v-icon>
              <h2 class="value-title">مشتری رایگان روزانه</h2>
              <p class="value-description">
                ما هر روز بین ۲۰ تا ۵۰ مشتری آماده خرید را مستقیماً به شما معرفی می‌کنیم
              </p>
            </div>
          </div>

          <!-- Benefits List -->
          <div class="benefits-section">
            <div class="benefit-item">
              <v-icon size="32" color="success">mdi-check-circle</v-icon>
              <span>بدون هزینه - کاملاً رایگان</span>
            </div>
            <div class="benefit-item">
              <v-icon size="32" color="success">mdi-check-circle</v-icon>
              <span>مشتریان واقعی و آماده خرید</span>
            </div>
            <div class="benefit-item">
              <v-icon size="32" color="success">mdi-check-circle</v-icon>
              <span>ارائه روزانه و مداوم</span>
            </div>
            <div class="benefit-item">
              <v-icon size="32" color="success">mdi-check-circle</v-icon>
              <span>بدون نیاز به تبلیغات پولی</span>
            </div>
          </div>

          <!-- CTA Section -->
          <div class="cta-section">
            <p class="cta-text">
              همین حالا ثبت‌نام کنید و این مشتریان را ببینید!
            </p>
            <v-btn
              size="x-large"
              color="success"
              rounded="xl"
              class="cta-button"
              block
              @click="goToSignup"
            >
              <v-icon start>mdi-account-plus</v-icon>
              ثبت‌نام رایگان
            </v-btn>
            <p class="cta-note">
              فقط چند ثانیه زمان می‌برد و کاملاً رایگان است
            </p>
          </div>

          <!-- Social Proof -->
          <div class="social-proof">
            <div class="proof-item">
              <v-icon size="24" color="primary">mdi-account-group</v-icon>
              <span>صدها فروشنده فعال</span>
            </div>
            <div class="proof-item">
              <v-icon size="24" color="primary">mdi-star</v-icon>
              <span>رتبه ۵ ستاره</span>
            </div>
          </div>
        </div>
      </v-container>
    </section>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'blank',
  title: 'فروشنده شوید - مشتری رایگان روزانه'
})

useSeoMeta({
  title: 'فروشنده شوید - ۲۰ تا ۵۰ مشتری رایگان روزانه',
  description: 'هر روز ۲۰ تا ۵۰ مشتری آماده خرید را مستقیماً به شما معرفی می‌کنیم. کاملاً رایگان و بدون نیاز به تبلیغات.',
  ogTitle: 'فروشنده شوید - مشتری رایگان روزانه',
  ogDescription: 'هر روز ۲۰ تا ۵۰ مشتری آماده خرید را مستقیماً به شما معرفی می‌کنیم. کاملاً رایگان و بدون نیاز به تبلیغات.',
  ogImage: '/favicon.ico',
  ogType: 'website'
})

const router = useRouter()

const goToSignup = () => {
  router.push('/register?role=seller')
}
</script>

<style scoped>
.seller-landing {
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
}

.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px 0;
  background: linear-gradient(135deg, #4CAF50 0%, #388E3C 50%, #2E7D32 100%);
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #4CAF50 0%, #388E3C 50%, #2E7D32 100%);
  z-index: 0;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
  z-index: 1;
}

.hero-container {
  position: relative;
  z-index: 2;
  max-width: 600px;
}

.hero-content {
  text-align: center;
  color: white;
}

.headline-wrapper {
  margin-bottom: 32px;
}

.main-headline {
  font-size: 2rem;
  font-weight: 900;
  line-height: 1.3;
  margin: 0;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.highlight {
  color: #FFD700;
  display: inline-block;
  animation: pulse 2s ease-in-out infinite;
}

.sub-headline {
  font-size: 1.5rem;
  font-weight: 700;
  opacity: 0.95;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.value-proposition {
  margin: 40px 0;
}

.value-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 32px 24px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.value-icon {
  margin-bottom: 16px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.value-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 16px 0 12px;
  color: white;
}

.value-description {
  font-size: 1.1rem;
  line-height: 1.6;
  opacity: 0.95;
  margin: 0;
}

.benefits-section {
  margin: 32px 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.benefit-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  border-radius: 16px;
  padding: 16px;
  font-size: 1.1rem;
  font-weight: 600;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.cta-section {
  margin: 48px 0 32px;
}

.cta-text {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 24px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.cta-button {
  font-size: 1.2rem;
  font-weight: 700;
  padding: 20px;
  height: auto;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
}

.cta-note {
  margin-top: 16px;
  font-size: 0.95rem;
  opacity: 0.9;
}

.social-proof {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 32px;
  flex-wrap: wrap;
}

.proof-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  border-radius: 12px;
  padding: 12px 20px;
  font-size: 0.95rem;
  font-weight: 600;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

/* Mobile Responsive */
@media (min-width: 600px) {
  .main-headline {
    font-size: 2.5rem;
  }
  
  .sub-headline {
    font-size: 1.8rem;
  }
  
  .value-card {
    padding: 40px 32px;
  }
  
  .benefit-item {
    font-size: 1.2rem;
    padding: 20px;
  }
  
  .cta-text {
    font-size: 1.5rem;
  }
  
  .cta-button {
    font-size: 1.3rem;
    padding: 24px;
  }
}

@media (min-width: 960px) {
  .hero-container {
    max-width: 700px;
  }
  
  .main-headline {
    font-size: 3rem;
  }
  
  .sub-headline {
    font-size: 2rem;
  }
  
  .value-title {
    font-size: 1.8rem;
  }
  
  .value-description {
    font-size: 1.2rem;
  }
}
</style>

