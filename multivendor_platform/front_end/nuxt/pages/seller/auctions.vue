<template>
  <v-container fluid dir="rtl" class="seller-auctions-page">
    <v-row>
      <v-col cols="12">
        <v-card elevation="2" rounded="xl">
          <v-card-title class="text-h5 pa-4 pa-md-6">
            <v-icon start>mdi-gavel</v-icon>
            مناقصه‌ها
          </v-card-title>
          <v-divider></v-divider>

          <v-card-text class="pa-4 pa-md-6">
            <v-tabs v-model="activeTab" class="mb-4">
              <v-tab value="active">فعال</v-tab>
              <v-tab value="participated">شرکت کرده‌ام</v-tab>
              <v-tab value="closed">بسته شده</v-tab>
            </v-tabs>

            <v-window v-model="activeTab">
              <v-window-item value="active">
                <div>
                  <v-row v-if="loading" justify="center">
                    <v-col cols="12" class="text-center">
                      <v-progress-circular indeterminate color="primary"></v-progress-circular>
                    </v-col>
                  </v-row>
                  <v-row v-else-if="activeAuctions.length > 0">
                    <v-col
                      v-for="auction in activeAuctions"
                      :key="auction.id"
                      cols="12"
                      md="6"
                      lg="4"
                    >
                      <AuctionCard :auction="auction" user-role="supplier" />
                    </v-col>
                  </v-row>
                  <v-alert v-else type="info" variant="tonal">
                    موردی یافت نشد
                  </v-alert>
                </div>
              </v-window-item>
              <v-window-item value="participated">
                <div>
                  <v-row v-if="loading" justify="center">
                    <v-col cols="12" class="text-center">
                      <v-progress-circular indeterminate color="primary"></v-progress-circular>
                    </v-col>
                  </v-row>
                  <v-row v-else-if="participatedAuctions.length > 0">
                    <v-col
                      v-for="auction in participatedAuctions"
                      :key="auction.id"
                      cols="12"
                      md="6"
                      lg="4"
                    >
                      <AuctionCard :auction="auction" user-role="supplier" />
                    </v-col>
                  </v-row>
                  <v-alert v-else type="info" variant="tonal">
                    موردی یافت نشد
                  </v-alert>
                </div>
              </v-window-item>
              <v-window-item value="closed">
                <div>
                  <v-row v-if="loading" justify="center">
                    <v-col cols="12" class="text-center">
                      <v-progress-circular indeterminate color="primary"></v-progress-circular>
                    </v-col>
                  </v-row>
                  <v-row v-else-if="closedAuctions.length > 0">
                    <v-col
                      v-for="auction in closedAuctions"
                      :key="auction.id"
                      cols="12"
                      md="6"
                      lg="4"
                    >
                      <AuctionCard :auction="auction" user-role="supplier" />
                    </v-col>
                  </v-row>
                  <v-alert v-else type="info" variant="tonal">
                    موردی یافت نشد
                  </v-alert>
                </div>
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuctionApi } from '~/composables/useAuctionApi'
import AuctionCard from '~/components/auction/AuctionCard.vue'

definePageMeta({
  middleware: 'authenticated'
})

const { getAuctions } = useAuctionApi()

const loading = ref(false)
const activeTab = ref('active')
const auctions = ref<any[]>([])

const activeAuctions = computed(() => {
  return auctions.value.filter(a => a.status === 'active' && a.is_invited)
})

const participatedAuctions = computed(() => {
  return auctions.value.filter(a => a.my_bid !== null)
})

const closedAuctions = computed(() => {
  return auctions.value.filter(a => ['closed', 'awarded', 'cancelled'].includes(a.status))
})

const loadAuctions = async () => {
  try {
    loading.value = true
    const response = await getAuctions()
    auctions.value = response.results || response || []
  } catch (error: any) {
    console.error('Error loading auctions:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAuctions()
})
</script>

<style scoped>
.seller-auctions-page {
  min-height: 100vh;
  padding-top: 2rem;
  padding-bottom: 2rem;
}
</style>

