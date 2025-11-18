<template>
  <div class="supplier-certifications" dir="rtl">
    <v-container>
      <!-- Certifications Section -->
      <div v-if="certifications && certifications.length > 0" class="mb-12">
        <div class="section-header mb-6">
          <h2 class="text-h4 font-weight-bold">گواهینامه‌ها</h2>
          <p class="text-body-1 text-medium-emphasis mt-2">
            گواهینامه‌ها و مجوزهای رسمی ما
          </p>
        </div>

        <v-row>
          <v-col
            v-for="(cert, index) in certifications"
            :key="index"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card class="cert-card" elevation="4" hover>
              <v-card-text class="pa-4">
                <v-icon color="success" size="large" class="mb-3">
                  mdi-certificate
                </v-icon>
                <h3 class="text-h6 font-weight-bold mb-2">
                  {{ cert.title || cert.name || cert }}
                </h3>
                <p v-if="cert.issuer" class="text-body-2 text-medium-emphasis mb-1">
                  <v-icon size="small" class="me-1">mdi-domain</v-icon>
                  {{ cert.issuer }}
                </p>
                <p v-if="cert.date" class="text-caption text-medium-emphasis">
                  <v-icon size="x-small" class="me-1">mdi-calendar</v-icon>
                  {{ cert.date }}
                </p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>

      <!-- Awards Section -->
      <div v-if="awards && awards.length > 0">
        <div class="section-header mb-6">
          <h2 class="text-h4 font-weight-bold">جوایز و افتخارات</h2>
          <p class="text-body-1 text-medium-emphasis mt-2">
            جوایز و دستاوردهای ما
          </p>
        </div>

        <v-timeline
          align="start"
          side="end"
          :density="display.xs.value ? 'compact' : 'default'"
        >
          <v-timeline-item
            v-for="(award, index) in awards"
            :key="index"
            dot-color="amber"
            size="small"
          >
            <template v-slot:icon>
              <v-icon color="white">mdi-trophy</v-icon>
            </template>
            <v-card class="award-card" elevation="2">
              <v-card-text>
                <div class="d-flex align-start">
                  <v-icon color="amber" size="large" class="me-3">mdi-trophy-award</v-icon>
                  <div>
                    <h3 class="text-h6 font-weight-bold mb-1">
                      {{ award.title || award.name || award }}
                    </h3>
                    <p v-if="award.issuer" class="text-body-2 mb-1">
                      <span class="font-weight-medium">اهدا شده توسط:</span> {{ award.issuer }}
                    </p>
                    <p v-if="award.description" class="text-body-2 text-medium-emphasis mb-2">
                      {{ award.description }}
                    </p>
                    <v-chip v-if="award.year" size="small" variant="tonal" color="amber">
                      {{ award.year }}
                    </v-chip>
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </v-timeline-item>
        </v-timeline>
      </div>

      <!-- Empty State -->
      <div v-if="(!certifications || certifications.length === 0) && (!awards || awards.length === 0)">
        <v-row justify="center" class="my-8">
          <v-col cols="12" class="text-center">
            <v-icon size="80" color="grey-lighten-2">mdi-certificate-outline</v-icon>
            <h3 class="text-h6 mt-3">گواهینامه یا جایزه‌ای یافت نشد</h3>
            <p class="text-body-2 text-medium-emphasis">
              اطلاعات گواهینامه‌ها و جوایز هنوز به اشتراک گذاشته نشده است
            </p>
          </v-col>
        </v-row>
      </div>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { useDisplay } from 'vuetify'

interface Props {
  certifications?: any[]
  awards?: any[]
}

withDefaults(defineProps<Props>(), {
  certifications: () => [],
  awards: () => []
})

const display = useDisplay()
</script>

<style scoped>
.section-header {
  text-align: center;
}

.cert-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
  height: 100%;
}

.cert-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
}

.award-card {
  border-radius: 12px;
}
</style>

