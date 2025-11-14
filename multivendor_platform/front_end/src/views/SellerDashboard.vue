<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">
          <v-icon left>mdi-store</v-icon>
          Seller Dashboard
        </h1>
      </v-col>
    </v-row>

    <!-- Stats Cards -->
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <v-card color="primary" dark>
          <v-card-text>
            <div class="text-h6">Total Products</div>
            <div class="text-h3">{{ dashboardData.total_products || 0 }}</div>
            <div class="text-caption">Active: {{ dashboardData.active_products || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="success" dark>
          <v-card-text>
            <div class="text-h6">Total Sales</div>
            <div class="text-h3">${{ parseFloat(dashboardData.total_sales || 0).toFixed(2) }}</div>
            <div class="text-caption">{{ dashboardData.total_orders || 0 }} orders</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="info" dark>
          <v-card-text>
            <div class="text-h6">Product Views</div>
            <div class="text-h3">{{ dashboardData.product_views || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="warning" dark>
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
            <v-tab value="products">
              <v-icon left>mdi-package-variant</v-icon>
              Products
            </v-tab>
            <v-tab value="ads">
              <v-icon left>mdi-bullhorn</v-icon>
              Advertisements
            </v-tab>
            <v-tab value="orders">
              <v-icon left>mdi-cart</v-icon>
              Orders
            </v-tab>
            <v-tab value="reviews">
              <v-icon left>mdi-star</v-icon>
              Customer Reviews
            </v-tab>
            <v-tab value="analytics">
              <v-icon left>mdi-chart-line</v-icon>
              Analytics
            </v-tab>
          </v-tabs>

          <v-card-text>
            <v-window v-model="tab">
              <!-- Profile Tab -->
              <v-window-item value="profile">
                <v-form ref="profileForm" @submit.prevent="updateProfile">
                  <h3 class="text-h6 mb-3">Personal Information</h3>
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
                  
                  <v-divider class="my-4"></v-divider>
                  <h3 class="text-h6 mb-3">Store Information</h3>
                  <v-text-field
                    v-model="profileData.store_name"
                    label="Store Name"
                    prepend-icon="mdi-store"
                  ></v-text-field>
                  <v-textarea
                    v-model="profileData.description"
                    label="Store Description"
                    prepend-icon="mdi-text"
                    rows="3"
                  ></v-textarea>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileData.contact_email"
                        label="Contact Email"
                        prepend-icon="mdi-email-outline"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileData.contact_phone"
                        label="Contact Phone"
                        prepend-icon="mdi-phone-outline"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-text-field
                    v-model="profileData.website"
                    label="Website"
                    prepend-icon="mdi-web"
                  ></v-text-field>
                  <v-btn color="primary" type="submit" :loading="saving">
                    Update Profile
                  </v-btn>
                </v-form>
              </v-window-item>

              <!-- Products Tab -->
              <v-window-item value="products">
                <v-btn color="primary" class="mb-4" @click="$router.push('/products/new')">
                  <v-icon left>mdi-plus</v-icon>
                  Add New Product
                </v-btn>
                <v-btn color="secondary" class="mb-4 ml-2" @click="$router.push('/my-products')">
                  <v-icon left>mdi-eye</v-icon>
                  View All Products
                </v-btn>
              </v-window-item>

              <!-- Ads Tab -->
              <v-window-item value="ads">
                <v-btn color="primary" class="mb-4" @click="showAdDialog = true">
                  <v-icon left>mdi-plus</v-icon>
                  Create New Ad
                </v-btn>
                <v-data-table
                  :headers="adHeaders"
                  :items="ads"
                  :loading="loadingAds"
                  item-value="id"
                >
                  <template v-slot:item.title="{ item }">
                    <strong>{{ item.title }}</strong>
                  </template>
                  <template v-slot:item.is_active="{ item }">
                    <v-chip :color="item.is_active ? 'success' : 'grey'" small>
                      {{ item.is_active ? 'Active' : 'Inactive' }}
                    </v-chip>
                  </template>
                  <template v-slot:item.created_at="{ item }">
                    {{ formatDate(item.created_at) }}
                  </template>
                  <template v-slot:item.actions="{ item }">
                    <v-btn icon size="small" @click="editAd(item)">
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn icon size="small" color="error" @click="deleteAd(item.id)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                </v-data-table>
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
                  <template v-slot:item.created_at="{ item }">
                    {{ formatDate(item.created_at) }}
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
                  <template v-slot:item.buyer="{ item }">
                    {{ item.author?.username || 'Unknown' }}
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

              <!-- Analytics Tab -->
              <v-window-item value="analytics">
                <v-row>
                  <v-col cols="12" md="6">
                    <v-card>
                      <v-card-title>Product Performance</v-card-title>
                      <v-card-text>
                        <div class="text-h4">{{ dashboardData.product_views || 0 }}</div>
                        <div class="text-caption">Total Product Views</div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-card>
                      <v-card-title>Order Statistics</v-card-title>
                      <v-card-text>
                        <div>Total Orders: <strong>{{ dashboardData.total_orders || 0 }}</strong></div>
                        <div>Total Revenue: <strong>${{ parseFloat(dashboardData.total_sales || 0).toFixed(2) }}</strong></div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Ad Dialog -->
    <v-dialog v-model="showAdDialog" max-width="600px">
      <v-card>
        <v-card-title>{{ editingAd ? 'Edit Advertisement' : 'Create New Advertisement' }}</v-card-title>
        <v-card-text>
          <v-form ref="adForm" @submit.prevent="saveAd">
            <v-text-field
              v-model="adData.title"
              label="Title *"
              required
            ></v-text-field>
            <v-textarea
              v-model="adData.description"
              label="Description *"
              rows="4"
              required
            ></v-textarea>
            <v-textarea
              v-model="adData.contact_info"
              label="Contact Information *"
              rows="2"
              required
            ></v-textarea>
            <v-switch
              v-model="adData.is_active"
              label="Active"
              color="primary"
            ></v-switch>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeAdDialog">Cancel</v-btn>
          <v-btn color="primary" @click="saveAd" :loading="savingAd">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

export default {
  name: 'SellerDashboard',
  setup() {
    const authStore = useAuthStore()
    const tab = ref('profile')
    const dashboardData = ref({})
    const orders = ref([])
    const reviews = ref([])
    const ads = ref([])
    const loading = ref(false)
    const loadingOrders = ref(false)
    const loadingReviews = ref(false)
    const loadingAds = ref(false)
    const saving = ref(false)
    const savingAd = ref(false)
    const snackbar = ref(false)
    const snackbarMessage = ref('')
    const snackbarColor = ref('success')
    const showAdDialog = ref(false)
    const editingAd = ref(false)
    
    const profileData = ref({
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      store_name: '',
      description: '',
      contact_email: '',
      contact_phone: '',
      website: ''
    })
    
    const adData = ref({
      title: '',
      description: '',
      contact_info: '',
      is_active: true
    })
    
    const adHeaders = [
      { title: 'Title', key: 'title' },
      { title: 'Status', key: 'is_active' },
      { title: 'Created', key: 'created_at' },
      { title: 'Actions', key: 'actions', sortable: false }
    ]
    
    const orderHeaders = [
      { title: 'Order Number', key: 'order_number' },
      { title: 'Buyer', key: 'buyer_username' },
      { title: 'Status', key: 'status' },
      { title: 'Total', key: 'total_amount' },
      { title: 'Date', key: 'created_at' }
    ]
    
    const reviewHeaders = [
      { title: 'Product', key: 'product' },
      { title: 'Buyer', key: 'buyer' },
      { title: 'Rating', key: 'rating' },
      { title: 'Comment', key: 'comment' },
      { title: 'Date', key: 'created_at' }
    ]
    
    const loadDashboardData = async () => {
      loading.value = true
      try {
        const response = await api.getSellerDashboard()
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
        const response = await api.getSellerOrders()
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
        const response = await api.getSellerReviews()
        reviews.value = response.data
      } catch (error) {
        console.error('Failed to load reviews:', error)
        showSnackbar('Failed to load reviews', 'error')
      } finally {
        loadingReviews.value = false
      }
    }
    
    const loadAds = async () => {
      loadingAds.value = true
      try {
        const response = await api.getSellerAds()
        ads.value = response.data
      } catch (error) {
        console.error('Failed to load ads:', error)
        showSnackbar('Failed to load ads', 'error')
      } finally {
        loadingAds.value = false
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
    
    const saveAd = async () => {
      savingAd.value = true
      try {
        if (editingAd.value) {
          await api.updateSellerAd(adData.value.id, adData.value)
          showSnackbar('Ad updated successfully', 'success')
        } else {
          await api.createSellerAd(adData.value)
          showSnackbar('Ad created successfully', 'success')
        }
        await loadAds()
        closeAdDialog()
      } catch (error) {
        console.error('Failed to save ad:', error)
        showSnackbar('Failed to save ad', 'error')
      } finally {
        savingAd.value = false
      }
    }
    
    const editAd = (ad) => {
      editingAd.value = true
      adData.value = { ...ad }
      showAdDialog.value = true
    }
    
    const deleteAd = async (id) => {
      if (confirm('Are you sure you want to delete this ad?')) {
        try {
          await api.deleteSellerAd(id)
          showSnackbar('Ad deleted successfully', 'success')
          await loadAds()
        } catch (error) {
          console.error('Failed to delete ad:', error)
          showSnackbar('Failed to delete ad', 'error')
        }
      }
    }
    
    const closeAdDialog = () => {
      showAdDialog.value = false
      editingAd.value = false
      adData.value = {
        title: '',
        description: '',
        contact_info: '',
        is_active: true
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
          store_name: authStore.user.vendor_profile?.store_name || '',
          description: authStore.user.vendor_profile?.description || '',
          contact_email: authStore.user.vendor_profile?.contact_email || '',
          contact_phone: authStore.user.vendor_profile?.contact_phone || '',
          website: authStore.user.vendor_profile?.website || ''
        }
      }
      loadDashboardData()
      loadOrders()
      loadReviews()
      loadAds()
    })
    
    return {
      tab,
      dashboardData,
      orders,
      reviews,
      ads,
      loading,
      loadingOrders,
      loadingReviews,
      loadingAds,
      saving,
      savingAd,
      profileData,
      adData,
      adHeaders,
      orderHeaders,
      reviewHeaders,
      snackbar,
      snackbarMessage,
      snackbarColor,
      showAdDialog,
      editingAd,
      updateProfile,
      saveAd,
      editAd,
      deleteAd,
      closeAdDialog,
      getStatusColor,
      formatDate
    }
  }
}
</script>

