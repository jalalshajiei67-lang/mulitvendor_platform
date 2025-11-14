<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">
          <v-icon left>mdi-view-dashboard</v-icon>
          Buyer Dashboard
        </h1>
      </v-col>
    </v-row>

    <!-- Stats Cards -->
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <v-card color="primary" dark>
          <v-card-text>
            <div class="text-h6">Total Orders</div>
            <div class="text-h3">{{ dashboardData.total_orders || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="warning" dark>
          <v-card-text>
            <div class="text-h6">Pending Orders</div>
            <div class="text-h3">{{ dashboardData.pending_orders || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="success" dark>
          <v-card-text>
            <div class="text-h6">Completed Orders</div>
            <div class="text-h3">{{ dashboardData.completed_orders || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="info" dark>
          <v-card-text>
            <div class="text-h6">Total Reviews</div>
            <div class="text-h3">{{ dashboardData.total_reviews || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Tabs -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-tabs v-model="tab" bg-color="primary">
            <v-tab value="profile">
              <v-icon left>mdi-account</v-icon>
              Profile
            </v-tab>
            <v-tab value="orders">
              <v-icon left>mdi-package-variant</v-icon>
              Order History
            </v-tab>
            <v-tab value="payments">
              <v-icon left>mdi-credit-card</v-icon>
              Payment Records
            </v-tab>
            <v-tab value="reviews">
              <v-icon left>mdi-comment-text</v-icon>
              My Reviews
            </v-tab>
          </v-tabs>

          <v-card-text>
            <v-window v-model="tab">
              <!-- Profile Tab -->
              <v-window-item value="profile">
                <v-form ref="profileForm" @submit.prevent="updateProfile">
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileData.first_name"
                        label="First Name"
                        prepend-icon="mdi-account"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileData.last_name"
                        label="Last Name"
                        prepend-icon="mdi-account"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileData.email"
                        label="Email"
                        prepend-icon="mdi-email"
                        type="email"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileData.phone"
                        label="Phone"
                        prepend-icon="mdi-phone"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-textarea
                    v-model="profileData.address"
                    label="Address"
                    prepend-icon="mdi-map-marker"
                    rows="3"
                  ></v-textarea>
                  <v-btn color="primary" type="submit" :loading="saving">
                    Update Profile
                  </v-btn>
                </v-form>
              </v-window-item>

              <!-- Orders Tab -->
              <v-window-item value="orders">
                <v-data-table
                  :headers="orderHeaders"
                  :items="orders"
                  :loading="loadingOrders"
                  item-value="id"
                >
                  <template v-slot:item.order_number="{ item }">
                    <strong>{{ item.order_number }}</strong>
                  </template>
                  <template v-slot:item.status="{ item }">
                    <v-chip :color="getStatusColor(item.status)" small>
                      {{ item.status }}
                    </v-chip>
                  </template>
                  <template v-slot:item.total_amount="{ item }">
                    ${{ parseFloat(item.total_amount).toFixed(2) }}
                  </template>
                  <template v-slot:item.is_paid="{ item }">
                    <v-icon :color="item.is_paid ? 'success' : 'error'">
                      {{ item.is_paid ? 'mdi-check-circle' : 'mdi-close-circle' }}
                    </v-icon>
                  </template>
                  <template v-slot:item.created_at="{ item }">
                    {{ formatDate(item.created_at) }}
                  </template>
                </v-data-table>
              </v-window-item>

              <!-- Payments Tab -->
              <v-window-item value="payments">
                <v-data-table
                  :headers="paymentHeaders"
                  :items="paymentRecords"
                  :loading="loadingOrders"
                  item-value="id"
                >
                  <template v-slot:item.order_number="{ item }">
                    <strong>{{ item.order_number }}</strong>
                  </template>
                  <template v-slot:item.total_amount="{ item }">
                    ${{ parseFloat(item.total_amount).toFixed(2) }}
                  </template>
                  <template v-slot:item.payment_method="{ item }">
                    <v-chip small>{{ item.payment_method || 'N/A' }}</v-chip>
                  </template>
                  <template v-slot:item.payment_date="{ item }">
                    {{ item.payment_date ? formatDate(item.payment_date) : 'N/A' }}
                  </template>
                </v-data-table>
              </v-window-item>

              <!-- Reviews Tab -->
              <v-window-item value="reviews">
                <v-data-table
                  :headers="reviewHeaders"
                  :items="reviews"
                  :loading="loadingReviews"
                  item-value="id"
                >
                  <template v-slot:item.product="{ item }">
                    {{ item.product?.name || 'Product deleted' }}
                  </template>
                  <template v-slot:item.rating="{ item }">
                    <v-rating
                      :model-value="item.rating"
                      readonly
                      size="small"
                      density="compact"
                    ></v-rating>
                  </template>
                  <template v-slot:item.created_at="{ item }">
                    {{ formatDate(item.created_at) }}
                  </template>
                </v-data-table>
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Success Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

export default {
  name: 'BuyerDashboard',
  setup() {
    const authStore = useAuthStore()
    const tab = ref('profile')
    const dashboardData = ref({})
    const orders = ref([])
    const reviews = ref([])
    const loading = ref(false)
    const loadingOrders = ref(false)
    const loadingReviews = ref(false)
    const saving = ref(false)
    const snackbar = ref(false)
    const snackbarMessage = ref('')
    const snackbarColor = ref('success')
    
    const profileData = ref({
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      address: ''
    })
    
    const orderHeaders = [
      { title: 'Order Number', key: 'order_number' },
      { title: 'Status', key: 'status' },
      { title: 'Total Amount', key: 'total_amount' },
      { title: 'Paid', key: 'is_paid' },
      { title: 'Date', key: 'created_at' }
    ]
    
    const paymentHeaders = [
      { title: 'Order Number', key: 'order_number' },
      { title: 'Amount', key: 'total_amount' },
      { title: 'Payment Method', key: 'payment_method' },
      { title: 'Payment Date', key: 'payment_date' }
    ]
    
    const reviewHeaders = [
      { title: 'Product', key: 'product' },
      { title: 'Rating', key: 'rating' },
      { title: 'Comment', key: 'comment' },
      { title: 'Date', key: 'created_at' }
    ]
    
    const paymentRecords = computed(() => {
      return orders.value.filter(order => order.is_paid)
    })
    
    const loadDashboardData = async () => {
      loading.value = true
      try {
        const response = await api.getBuyerDashboard()
        dashboardData.value = response.data
      } catch (error) {
        console.error('Failed to load dashboard data:', error)
        showSnackbar('Failed to load dashboard data', 'error')
      } finally {
        loading.value = false
      }
    }
    
    const loadOrders = async () => {
      loadingOrders.value = true
      try {
        const response = await api.getBuyerOrders()
        orders.value = response.data
      } catch (error) {
        console.error('Failed to load orders:', error)
        showSnackbar('Failed to load orders', 'error')
      } finally {
        loadingOrders.value = false
      }
    }
    
    const loadReviews = async () => {
      loadingReviews.value = true
      try {
        const response = await api.getBuyerReviews()
        reviews.value = response.data
      } catch (error) {
        console.error('Failed to load reviews:', error)
        showSnackbar('Failed to load reviews', 'error')
      } finally {
        loadingReviews.value = false
      }
    }
    
    const updateProfile = async () => {
      saving.value = true
      try {
        await authStore.updateProfile(profileData.value)
        showSnackbar('Profile updated successfully', 'success')
      } catch (error) {
        console.error('Failed to update profile:', error)
        showSnackbar('Failed to update profile', 'error')
      } finally {
        saving.value = false
      }
    }
    
    const getStatusColor = (status) => {
      const colors = {
        pending: 'warning',
        confirmed: 'info',
        processing: 'primary',
        shipped: 'pink',
        delivered: 'success',
        cancelled: 'error',
        rejected: 'error'
      }
      return colors[status] || 'grey'
    }
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    }
    
    const showSnackbar = (message, color = 'success') => {
      snackbarMessage.value = message
      snackbarColor.value = color
      snackbar.value = true
    }
    
    onMounted(() => {
      if (authStore.user) {
        profileData.value = {
          first_name: authStore.user.first_name || '',
          last_name: authStore.user.last_name || '',
          email: authStore.user.email || '',
          phone: authStore.user.profile?.phone || '',
          address: authStore.user.profile?.address || ''
        }
      }
      loadDashboardData()
      loadOrders()
      loadReviews()
    })
    
    return {
      tab,
      dashboardData,
      orders,
      reviews,
      loading,
      loadingOrders,
      loadingReviews,
      saving,
      profileData,
      orderHeaders,
      paymentHeaders,
      reviewHeaders,
      paymentRecords,
      snackbar,
      snackbarMessage,
      snackbarColor,
      updateProfile,
      getStatusColor,
      formatDate
    }
  }
}
</script>

