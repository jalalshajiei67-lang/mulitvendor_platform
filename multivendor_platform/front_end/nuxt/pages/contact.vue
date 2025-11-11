<template>
  <div class="contact-us" dir="rtl">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1>تماس با ما</h1>
        <p>ما اینجا هستیم تا به شما کمک کنیم</p>
      </div>
    </div>

    <!-- About Us Section -->
    <div class="about-section">
      <div class="container">
        <div class="about-content">
          <h2>داستان ما</h2>
          <p class="about-text">
            همه چیز از یک ایده ساده شروع شد؛ دو کارآفرین جوان که چالش‌های موجود در صنعت ماشین‌آلات را به چشم دیدند و تصمیم گرفتند راه‌حلی نوآورانه ارائه دهند. آن‌ها متوجه شدند که خریداران و فروشندگان ماشین‌آلات با مشکلات متعددی روبرو هستند: عدم دسترسی به اطلاعات دقیق، نبود بستر مناسب برای ارتباط، و فرآیندهای پیچیده و زمان‌بر. با همین انگیزه، پلتفرم چند فروشنده ایندکسو متولد شد تا با استفاده از تکنولوژی‌های پیشرفته، تحولی شگرف در صنعت ماشین‌آلات ایجاد کند. این پلتفرم با ایجاد بستری امن و کارآمد، هم برای خریداران و هم برای فروشندگان، فرصت‌های جدیدی برای رشد و توسعه کسب‌وکارها فراهم کرده است. امروز ایندکسو به عنوان یک محصول تحول‌آفرین و اختلال‌گر در صنعت، راه‌حل‌های جامعی برای ارتباط بهتر، معاملات سریع‌تر و دسترسی آسان‌تر به محصولات و خدمات ارائه می‌دهد.
          </p>
        </div>
      </div>
    </div>

    <!-- Contact Information Section -->
    <div class="contact-section">
      <div class="container">
        <h2>اطلاعات تماس</h2>
        <div class="contact-grid">
          <!-- Email -->
          <div class="contact-card">
            <div class="contact-icon">
              <v-icon size="48">mdi-email</v-icon>
            </div>
            <h3>ایمیل</h3>
            <a href="mailto:info@indexo.ir" class="contact-link">info@indexo.ir</a>
          </div>

          <!-- Phone -->
          <div class="contact-card">
            <div class="contact-icon">
              <v-icon size="48">mdi-phone</v-icon>
            </div>
            <h3>تلفن ثابت</h3>
            <a href="tel:+982188311001" class="contact-link">021-88311001</a>
          </div>

          <!-- Mobile -->
          <div class="contact-card">
            <div class="contact-icon">
              <v-icon size="48">mdi-cellphone</v-icon>
            </div>
            <h3>موبایل</h3>
            <a href="tel:+989123456789" class="contact-link">0912-345-6789</a>
          </div>

          <!-- WhatsApp -->
          <div class="contact-card">
            <div class="contact-icon">
              <v-icon size="48">mdi-whatsapp</v-icon>
            </div>
            <h3>واتساپ</h3>
            <a href="https://wa.me/989123456789" target="_blank" rel="noopener noreferrer" class="contact-link">0912-345-6789</a>
          </div>

          <!-- Telegram -->
          <div class="contact-card">
            <div class="contact-icon">
              <v-icon size="48">mdi-send</v-icon>
            </div>
            <h3>تلگرام</h3>
            <a href="https://t.me/indexo_support" target="_blank" rel="noopener noreferrer" class="contact-link">@indexo_support</a>
          </div>

          <!-- Instagram -->
          <div class="contact-card">
            <div class="contact-icon">
              <v-icon size="48">mdi-instagram</v-icon>
            </div>
            <h3>اینستاگرام</h3>
            <a href="https://instagram.com/indexo.ir" target="_blank" rel="noopener noreferrer" class="contact-link">@indexo.ir</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: 'تماس با ما',
  meta: [
    {
      name: 'description',
      content: 'راه‌های ارتباط با تیم ایندکسو - ایمیل، تلفن، واتساپ، تلگرام و اینستاگرام'
    }
  ]
})
</script>

<style scoped>
.contact-us {
  min-height: 100vh;
  direction: rtl;
  text-align: right;
  background-color: #f8fafc;
  color: rgba(var(--v-theme-on-surface), 0.92);
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.85), rgba(var(--v-theme-secondary), 0.9));
  color: rgba(var(--v-theme-on-primary), 0.98);
  padding: 80px 20px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.hero-section::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top left, rgba(255, 255, 255, 0.18), transparent 55%);
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
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.65), transparent);
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
  background: white;
  padding: 40px 30px;
  border-radius: 18px;
  text-align: center;
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  color: rgba(var(--v-theme-on-surface), 0.92);
  border: 1px solid rgba(var(--v-theme-primary), 0.12);
}

.contact-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 18px 36px rgba(15, 23, 42, 0.12);
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
}
</style>

