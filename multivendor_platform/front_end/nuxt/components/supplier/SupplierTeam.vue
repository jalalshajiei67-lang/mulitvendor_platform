<template>
  <div class="supplier-team" dir="rtl">
    <v-container>
      <!-- Header -->
      <div class="section-header mb-6">
        <h2 class="text-h4 font-weight-bold">تیم ما</h2>
        <p class="text-body-1 text-medium-emphasis mt-2">
          اعضای تیم حرفه‌ای و با تجربه ما
        </p>
      </div>

      <!-- Loading State -->
      <v-row v-if="loading" justify="center" class="my-8">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      </v-row>

      <!-- Team Grid -->
      <v-row v-else-if="members.length > 0" class="team-grid">
        <v-col
          v-for="(member, index) in members"
          :key="member.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
          class="team-col"
          :style="{ animationDelay: `${index * 0.15}s` }"
        >
          <v-card
            class="team-card animate-in"
            elevation="4"
            hover
            @click="openMemberDialog(member)"
          >
            <!-- Avatar Section -->
            <div class="avatar-section">
              <div class="avatar-container">
                <v-avatar
                  :size="display.xs.value ? 140 : 160"
                  class="team-avatar"
                >
                  <v-img
                    v-if="member.photo"
                    :src="formatImageUrl(member.photo)"
                    cover
                    class="avatar-image"
                  >
                    <template v-slot:placeholder>
                      <v-skeleton-loader type="avatar" />
                    </template>
                  </v-img>
                  <v-icon v-else :size="display.xs.value ? 70 : 80" color="grey-lighten-1">
                    mdi-account-circle
                  </v-icon>
                </v-avatar>

                <!-- Social Links Overlay -->
                <div class="social-overlay">
                  <v-btn
                    v-if="member.linkedin"
                    icon="mdi-linkedin"
                    size="small"
                    variant="text"
                    color="white"
                    :href="member.linkedin"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="social-link"
                    @click.stop
                  ></v-btn>
                  <v-btn
                    v-if="member.email"
                    icon="mdi-email"
                    size="small"
                    variant="text"
                    color="white"
                    :href="`mailto:${member.email}`"
                    class="social-link"
                    @click.stop
                  ></v-btn>
                  <v-btn
                    v-if="member.phone"
                    icon="mdi-phone"
                    size="small"
                    variant="text"
                    color="white"
                    :href="`tel:${member.phone}`"
                    class="social-link"
                    @click.stop
                  ></v-btn>
                </div>
              </div>

              <!-- Experience Badge -->
              <v-chip
                v-if="member.experience_years"
                size="small"
                color="primary"
                variant="elevated"
                class="experience-badge"
              >
                <v-icon start size="x-small">mdi-star</v-icon>
                {{ member.experience_years }} سال تجربه
              </v-chip>
            </div>

            <!-- Card Content -->
            <v-card-text class="text-center pa-4 team-content">
              <div class="member-info">
                <h3 class="member-name text-h6 font-weight-bold mb-1">
                  {{ member.name }}
                </h3>
                <p class="member-position text-subtitle-1 text-primary mb-3 font-weight-medium">
                  {{ member.position }}
                </p>

                <!-- Skills/Chips -->
                <div v-if="member.skills && member.skills.length > 0" class="skills-section mb-3">
                  <div class="skills-chips">
                    <v-chip
                      v-for="skill in member.skills.slice(0, 2)"
                      :key="skill"
                      size="x-small"
                      variant="tonal"
                      color="secondary"
                      class="skill-chip"
                    >
                      {{ skill }}
                    </v-chip>
                    <v-chip
                      v-if="member.skills.length > 2"
                      size="x-small"
                      variant="outlined"
                      color="secondary"
                      class="more-skills-chip"
                    >
                      +{{ member.skills.length - 2 }}
                    </v-chip>
                  </div>
                </div>

                <!-- Bio -->
                <p v-if="member.bio" class="member-bio text-body-2 text-medium-emphasis line-clamp-3 mb-3">
                  {{ member.bio }}
                </p>

                <!-- Action Buttons -->
                <div class="action-buttons">
                  <v-btn
                    variant="outlined"
                    color="primary"
                    size="small"
                    class="view-profile-btn"
                    @click.stop="openMemberDialog(member)"
                  >
                    <v-icon start size="small">mdi-account-eye</v-icon>
                    پروفایل کامل
                  </v-btn>
                </div>
              </div>
            </v-card-text>

            <!-- Hover Effect Indicator -->
            <div class="member-hover-indicator">
              <v-icon color="primary" size="small">mdi-eye</v-icon>
              <span class="text-caption ms-1">مشاهده جزئیات</span>
            </div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Empty State -->
      <v-row v-else justify="center" class="my-8">
        <v-col cols="12" class="text-center">
          <v-icon size="80" color="grey-lighten-2">mdi-account-group</v-icon>
          <h3 class="text-h6 mt-3">عضوی یافت نشد</h3>
          <p class="text-body-2 text-medium-emphasis">
            اطلاعات تیم هنوز به اشتراک گذاشته نشده است
          </p>
        </v-col>
      </v-row>
    </v-container>

    <!-- Member Detail Dialog -->
    <v-dialog v-model="memberDialog" max-width="700" scrollable>
      <v-card v-if="selectedMember" rounded="xl">
        <v-card-title class="d-flex justify-space-between align-center pa-6">
          <h2 class="text-h5 font-weight-bold">پروفایل کامل</h2>
          <v-btn icon="mdi-close" variant="text" @click="memberDialog = false" size="small"></v-btn>
        </v-card-title>
        
        <v-card-text class="text-center pa-6">
          <v-avatar
            :size="display.xs.value ? 120 : 160"
            class="mb-4 member-dialog-avatar"
          >
            <v-img
              v-if="selectedMember.photo"
              :src="formatImageUrl(selectedMember.photo)"
              cover
            ></v-img>
            <v-icon v-else :size="display.xs.value ? 60 : 80" color="grey-lighten-1">
              mdi-account-circle
            </v-icon>
          </v-avatar>
          
          <h2 class="text-h4 font-weight-bold mb-2">{{ selectedMember.name }}</h2>
          <p class="text-h6 text-primary mb-4 font-weight-medium">{{ selectedMember.position }}</p>
          
          <div v-if="selectedMember.experience_years" class="mb-4">
            <v-chip color="primary" variant="tonal" size="large" class="experience-chip-dialog">
              <v-icon start>mdi-star</v-icon>
              {{ selectedMember.experience_years }} سال تجربه
            </v-chip>
          </div>
          
          <div v-if="selectedMember.skills && selectedMember.skills.length > 0" class="mb-4">
            <div class="skills-dialog d-flex flex-wrap justify-center gap-2">
              <v-chip
                v-for="skill in selectedMember.skills"
                :key="skill"
                size="small"
                variant="tonal"
                color="secondary"
                class="skill-chip-dialog"
              >
                {{ skill }}
              </v-chip>
            </div>
          </div>
          
          <v-divider class="my-6"></v-divider>
          
          <div v-if="selectedMember.bio" class="text-body-1 text-start bio-dialog">
            <h3 class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center">
              <v-icon color="primary" class="me-2">mdi-information</v-icon>
              درباره
            </h3>
            <p class="readable-text" style="white-space: pre-line; line-height: 1.8;">{{ selectedMember.bio }}</p>
          </div>

          <!-- Contact Information -->
          <div v-if="selectedMember.email || selectedMember.phone || selectedMember.linkedin" class="mt-6">
            <v-divider class="mb-4"></v-divider>
            <h3 class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center justify-center">
              <v-icon color="primary" class="me-2">mdi-contact-mail</v-icon>
              اطلاعات تماس
            </h3>
            <div class="d-flex flex-wrap justify-center gap-3">
              <v-btn
                v-if="selectedMember.email"
                :href="`mailto:${selectedMember.email}`"
                color="primary"
                variant="outlined"
                prepend-icon="mdi-email"
                rounded="lg"
              >
                ایمیل
              </v-btn>
              <v-btn
                v-if="selectedMember.phone"
                :href="`tel:${selectedMember.phone}`"
                color="success"
                variant="outlined"
                prepend-icon="mdi-phone"
                rounded="lg"
              >
                تماس
              </v-btn>
              <v-btn
                v-if="selectedMember.linkedin"
                :href="selectedMember.linkedin"
                target="_blank"
                rel="noopener noreferrer"
                color="blue-darken-3"
                variant="outlined"
                prepend-icon="mdi-linkedin"
                rounded="lg"
              >
                LinkedIn
              </v-btn>
            </div>
          </div>
        </v-card-text>
        
        <v-card-actions class="pa-6">
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="flat" size="large" rounded="lg" @click="memberDialog = false">
            بستن
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useDisplay } from 'vuetify'
import type { SupplierTeamMember } from '~/composables/useSupplierTeamApi'
import { formatImageUrl } from '~/utils/imageUtils'

interface Props {
  members: SupplierTeamMember[]
  loading?: boolean
}

withDefaults(defineProps<Props>(), {
  loading: false
})

const display = useDisplay()
const memberDialog = ref(false)
const selectedMember = ref<SupplierTeamMember | null>(null)

const openMemberDialog = (member: SupplierTeamMember) => {
  selectedMember.value = member
  memberDialog.value = true
}
</script>

<style scoped>
.section-header {
  text-align: center;
}

/* Team Grid */
.team-grid {
  margin: -16px;
}

.team-grid > .v-col {
  padding: 16px;
}

.team-col {
  opacity: 0;
  animation: fadeInUp 0.6s ease-out forwards;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Team Card */
.team-card {
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 24px;
  text-align: center;
  height: 100%;
  position: relative;
  overflow: hidden;
  background: white;
  border: 1px solid rgba(var(--v-theme-outline), 0.1);
}

.team-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.18) !important;
  border-color: rgba(var(--v-theme-primary), 0.3);
}

.team-card::before {
  content: '';
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.15), rgba(var(--v-theme-secondary, var(--v-theme-primary)), 0.1));
  border-radius: 26px;
  opacity: 0;
  transition: opacity 0.4s ease;
  z-index: -1;
}

.team-card:hover::before {
  opacity: 1;
}

/* Avatar Section */
.avatar-section {
  position: relative;
  padding: 24px 16px 16px;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.05), rgba(var(--v-theme-secondary, var(--v-theme-primary)), 0.02));
}

.avatar-container {
  position: relative;
  display: inline-block;
}

.team-avatar {
  border: 4px solid white;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  background: white;
  transition: all 0.4s ease;
}

.team-card:hover .team-avatar {
  transform: scale(1.05);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

.avatar-image {
  transition: transform 0.4s ease;
}

.team-card:hover .avatar-image {
  transform: scale(1.1);
}

/* Social Overlay */
.social-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  opacity: 0;
  transition: all 0.3s ease;
  border-radius: 50%;
  backdrop-filter: blur(10px);
}

.team-card:hover .social-overlay {
  opacity: 1;
}

.social-link {
  background: rgba(255, 255, 255, 0.2) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.social-link:hover {
  background: rgba(255, 255, 255, 0.3) !important;
  transform: scale(1.1);
}

/* Experience Badge */
.experience-badge {
  position: absolute;
  top: 16px;
  left: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(var(--v-theme-primary), 0.3);
}

/* Team Content */
.team-content {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.9));
  backdrop-filter: blur(10px);
  padding: 20px !important;
}

.member-info {
  position: relative;
}

.member-name {
  color: rgba(var(--v-theme-on-surface), 0.9);
  line-height: 1.4;
  margin-bottom: 4px;
  transition: color 0.3s ease;
}

.team-card:hover .member-name {
  color: rgb(var(--v-theme-primary));
}

.member-position {
  color: rgb(var(--v-theme-primary));
  font-weight: 600;
  margin-bottom: 12px;
  position: relative;
}

.member-position::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background: rgb(var(--v-theme-primary));
  transition: width 0.3s ease;
}

.team-card:hover .member-position::after {
  width: 60px;
}

/* Skills Section */
.skills-section {
  margin: 16px 0;
}

.skills-chips {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 6px;
}

.skill-chip {
  transition: all 0.3s ease;
}

.skill-chip:hover {
  transform: scale(1.05);
}

.more-skills-chip {
  opacity: 0.8;
}

/* Member Bio */
.member-bio {
  line-height: 1.6;
  color: rgba(var(--v-theme-on-surface), 0.7);
  margin-bottom: 16px;
}

/* Action Buttons */
.action-buttons {
  margin-top: 16px;
}

.view-profile-btn {
  border-radius: 12px;
  transition: all 0.3s ease;
  border: 2px solid rgb(var(--v-theme-primary));
}

.view-profile-btn:hover {
  background: rgb(var(--v-theme-primary)) !important;
  color: white !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(var(--v-theme-primary), 0.3);
}

/* Hover Indicator */
.member-hover-indicator {
  position: absolute;
  bottom: 16px;
  left: 16px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  padding: 6px 12px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease;
  border: 1px solid rgba(var(--v-theme-outline), 0.2);
  font-size: 0.75rem;
}

.team-card:hover .member-hover-indicator {
  opacity: 1;
  transform: translateY(0);
}

/* Line Clamping */
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Animations */
.animate-in {
  opacity: 0;
  transform: translateY(20px);
  animation: slideInUp 0.6s ease-out forwards;
}

@keyframes slideInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile optimizations */
@media (max-width: 960px) {
  .team-grid {
    margin: -12px;
  }

  .team-grid > .v-col {
    padding: 12px;
  }

  .team-card:hover {
    transform: translateY(-8px) scale(1.01);
  }

  .social-overlay {
    opacity: 1;
    background: rgba(0, 0, 0, 0.5);
  }

  .member-hover-indicator {
    display: none;
  }
}

/* Member Dialog Styles */
.member-dialog-avatar {
  border: 4px solid rgba(var(--v-theme-primary), 0.2);
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.2);
}

.experience-chip-dialog {
  font-weight: 600;
}

.skill-chip-dialog {
  transition: all 0.3s ease;
}

.skill-chip-dialog:hover {
  transform: scale(1.1);
}

.bio-dialog {
  background: rgba(var(--v-theme-surface-variant), 0.3);
  padding: 20px;
  border-radius: 16px;
}

.readable-text {
  line-height: 1.8;
  color: rgba(var(--v-theme-on-surface), 0.87);
}

@media (max-width: 600px) {
  .avatar-section {
    padding: 20px 12px 12px;
  }

  .team-avatar {
    width: 120px !important;
    height: 120px !important;
  }

  .team-content {
    padding: 16px !important;
  }

  .skills-chips {
    justify-content: center;
  }

  .action-buttons {
    margin-top: 12px;
  }

  .view-profile-btn {
    width: 100%;
  }

  .bio-dialog {
    padding: 16px;
  }
}
</style>

