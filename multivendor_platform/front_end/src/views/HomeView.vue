<template>
  <div class="home" dir="rtl">
    <div class="hero-section">
      <div class="hero-content">
        <h1>{{ t('home.welcomeTitle') }}</h1>
        <p>{{ t('home.welcomeSubtitle') }}</p>
        <div class="hero-actions">
          <router-link to="/products" class="btn btn-primary">{{ t('home.browseProducts') }}</router-link>
          <router-link v-if="!authStore.isAuthenticated" to="/register" class="btn btn-secondary">{{ t('home.joinAsSeller') }}</router-link>
          <router-link v-else to="/my-products" class="btn btn-secondary">{{ t('nav.myProducts') }}</router-link>
        </div>
      </div>
    </div>
    
    <div class="features-section">
      <div class="container">
        <h2>{{ t('home.whyChooseUs') }}</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">🏪</div>
            <h3>{{ t('home.multipleVendors') }}</h3>
            <p>{{ t('home.multipleVendorsDesc') }}</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">⚙️</div>
            <h3>{{ t('home.easyManagement') }}</h3>
            <p>{{ t('home.easyManagementDesc') }}</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <h3>{{ t('home.securePlatform') }}</h3>
            <p>{{ t('home.securePlatformDesc') }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'

export default {
  name: 'HomeView',
  setup() {
    let authStore
    let i18n
    
    try {
      authStore = useAuthStore()
    } catch (error) {
      console.error('Failed to initialize auth store:', error)
      authStore = { isAuthenticated: false }
    }
    
    try {
      i18n = useI18n()
    } catch (error) {
      console.error('Failed to initialize i18n:', error)
      i18n = null
    }
    
    // Safe translation function with fallback
    const safeTranslate = (key, fallback = '') => {
      // If i18n is not available, return fallback or key
      if (!i18n || !i18n.t) {
        return fallback || key
      }
      
      try {
        const translated = i18n.t(key)
        // If translation returns the key itself (meaning not found), use fallback
        if (translated === key && fallback) {
          return fallback
        }
        // Return translated value if it exists, otherwise fallback, otherwise key
        return translated || fallback || key
      } catch (error) {
        console.warn(`Translation error for key: ${key}`, error)
        return fallback || key
      }
    }
    
    return {
      authStore: authStore || { isAuthenticated: false },
      t: safeTranslate
    }
  }
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  direction: rtl;
  text-align: right;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 20px;
  text-align: center;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 20px;
  font-weight: 700;
}

.hero-content p {
  font-size: 1.2rem;
  margin-bottom: 40px;
  opacity: 0.9;
}

.hero-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  flex-direction: row-reverse;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-block;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-primary:hover {
  background-color: #45a049;
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: transparent;
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background-color: white;
  color: #667eea;
  transform: translateY(-2px);
}

.features-section {
  padding: 80px 20px;
  background-color: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.features-section h2 {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 60px;
  color: #333;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
}

.feature-card {
  background: white;
  padding: 40px 30px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #333;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

.feature-icon {
  font-size: 64px;
  margin-bottom: 20px;
  display: block;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .hero-content p {
    font-size: 1rem;
  }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .features-section h2 {
    font-size: 2rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
