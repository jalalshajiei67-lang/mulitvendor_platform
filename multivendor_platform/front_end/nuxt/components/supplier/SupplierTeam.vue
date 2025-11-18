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
          v-for="member in members"
          :key="member.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <v-card
            class="team-card"
            elevation="4"
            hover
            @click="openMemberDialog(member)"
          >
            <v-avatar
              :size="display.xs.value ? 150 : 180"
              class="team-avatar mx-auto mt-6"
            >
              <v-img
                v-if="member.photo"
                :src="formatImageUrl(member.photo)"
                cover
              >
                <template v-slot:placeholder>
                  <v-skeleton-loader type="avatar" />
                </template>
              </v-img>
              <v-icon v-else :size="display.xs.value ? 75 : 90" color="grey-lighten-1">
                mdi-account-circle
              </v-icon>
            </v-avatar>

            <v-card-text class="text-center pa-4">
              <h3 class="text-h6 font-weight-bold mb-1">
                {{ member.name }}
              </h3>
              <p class="text-subtitle-2 text-primary mb-2">
                {{ member.position }}
              </p>
              <p v-if="member.bio" class="text-caption text-medium-emphasis line-clamp-3">
                {{ member.bio }}
              </p>
              <v-btn
                v-if="member.bio"
                variant="text"
                color="primary"
                size="small"
                class="mt-2"
                @click.stop="openMemberDialog(member)"
              >
                مشاهده بیشتر
              </v-btn>
            </v-card-text>
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
    <v-dialog v-model="memberDialog" max-width="600">
      <v-card v-if="selectedMember">
        <v-card-title class="d-flex justify-space-between align-center">
          <span></span>
          <v-btn icon="mdi-close" variant="text" @click="memberDialog = false"></v-btn>
        </v-card-title>
        
        <v-card-text class="text-center">
          <v-avatar
            :size="display.xs.value ? 120 : 150"
            class="mb-4"
          >
            <v-img
              v-if="selectedMember.photo"
              :src="formatImageUrl(selectedMember.photo)"
              cover
            ></v-img>
            <v-icon v-else :size="display.xs.value ? 60 : 75" color="grey-lighten-1">
              mdi-account-circle
            </v-icon>
          </v-avatar>
          
          <h2 class="text-h5 font-weight-bold mb-2">{{ selectedMember.name }}</h2>
          <p class="text-h6 text-primary mb-4">{{ selectedMember.position }}</p>
          
          <v-divider class="my-4"></v-divider>
          
          <div v-if="selectedMember.bio" class="text-body-1 text-start">
            <h3 class="text-subtitle-1 font-weight-bold mb-2">درباره</h3>
            <p style="white-space: pre-line;">{{ selectedMember.bio }}</p>
          </div>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="memberDialog = false">
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

.team-grid {
  margin: -12px;
}

.team-grid > .v-col {
  padding: 12px;
}

.team-card {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 16px;
  text-align: center;
}

.team-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15) !important;
}

.team-avatar {
  border: 4px solid rgb(var(--v-theme-surface));
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

