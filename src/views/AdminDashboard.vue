<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">
          <v-icon left>mdi-shield-crown</v-icon>
          Admin Dashboard
        </h1>
      </v-col>
    </v-row>

    <!-- Stats Cards -->
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <v-card color="primary" dark>
          <v-card-text>
            <div class="text-h6">Total Users</div>
            <div class="text-h3">{{ dashboardData.users?.total || 0 }}</div>
            <div class="text-caption">
              Buyers: {{ dashboardData.users?.buyers || 0 }} | Sellers: {{ dashboardData.users?.sellers || 0 }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="success" dark>
          <v-card-text>
            <div class="text-h6">Total Products</div>
            <div class="text-h3">{{ dashboardData.products?.total || 0 }}</div>
            <div class="text-caption">Active: {{ dashboardData.products?.active || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="info" dark>
          <v-card-text>
            <div class="text-h6">Total Orders</div>
            <div class="text-h3">{{ dashboardData.orders?.total || 0 }}</div>
            <div class="text-caption">Pending: {{ dashboardData.orders?.pending || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="warning" dark>
          <v-card-text>
            <div class="text-h6">Alerts</div>
            <div class="text-h3">{{ (dashboardData.users?.blocked || 0) + (dashboardData.users?.unverified || 0) }}</div>
            <div class="text-caption">Blocked: {{ dashboardData.users?.blocked || 0 }} | Unverified: {{ dashboardData.users?.unverified || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Tabs -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-tabs v-model="tab" bg-color="primary">
            <v-tab value="users">
              <v-icon left>mdi-account-multiple</v-icon>
              User Management
            </v-tab>
            <v-tab value="activities">
              <v-icon left>mdi-history</v-icon>
              Activity Logs
            </v-tab>
          </v-tabs>

          <v-card-text>
            <v-window v-model="tab">
              <!-- Users Tab -->
              <v-window-item value="users">
                <v-row class="mb-4">
                  <v-col cols="12" md="3">
                    <v-select
                      v-model="userFilters.role"
                      label="Filter by Role"
                      :items="roleFilterOptions"
                      clearable
                      @update:model-value="loadUsers"
                    ></v-select>
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-select
                      v-model="userFilters.is_blocked"
                      label="Filter by Status"
                      :items="statusFilterOptions"
                      clearable
                      @update:model-value="loadUsers"
                    ></v-select>
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-select
                      v-model="userFilters.is_verified"
                      label="Filter by Verification"
                      :items="verificationFilterOptions"
                      clearable
                      @update:model-value="loadUsers"
                    ></v-select>
                  </v-col>
                </v-row>

                <v-data-table
                  :headers="userHeaders"
                  :items="users"
                  :loading="loadingUsers"
                  item-value="id"
                >
                  <template v-slot:item.username="{ item }">
                    <strong>{{ item.username }}</strong>
                  </template>
                  <template v-slot:item.role="{ item }">
                    <v-chip small :color="getRoleColor(item.profile?.role)">
                      {{ item.profile?.role || 'N/A' }}
                    </v-chip>
                  </template>
                  <template v-slot:item.is_verified="{ item }">
                    <v-icon :color="item.profile?.is_verified ? 'success' : 'grey'">
                      {{ item.profile?.is_verified ? 'mdi-check-circle' : 'mdi-close-circle' }}
                    </v-icon>
                  </template>
                  <template v-slot:item.is_blocked="{ item }">
                    <v-icon :color="item.profile?.is_blocked ? 'error' : 'success'">
                      {{ item.profile?.is_blocked ? 'mdi-block-helper' : 'mdi-check' }}
                    </v-icon>
                  </template>
                  <template v-slot:item.actions="{ item }">
                    <v-menu>
                      <template v-slot:activator="{ props }">
                        <v-btn icon size="small" v-bind="props">
                          <v-icon>mdi-dots-vertical</v-icon>
                        </v-btn>
                      </template>
                      <v-list>
                        <v-list-item @click="toggleBlockUser(item)">
                          <v-list-item-title>
                            <v-icon left>{{ item.profile?.is_blocked ? 'mdi-lock-open' : 'mdi-lock' }}</v-icon>
                            {{ item.profile?.is_blocked ? 'Unblock' : 'Block' }}
                          </v-list-item-title>
                        </v-list-item>
                        <v-list-item @click="toggleVerifyUser(item)">
                          <v-list-item-title>
                            <v-icon left>{{ item.profile?.is_verified ? 'mdi-close-circle' : 'mdi-check-circle' }}</v-icon>
                            {{ item.profile?.is_verified ? 'Unverify' : 'Verify' }}
                          </v-list-item-title>
                        </v-list-item>
                        <v-list-item @click="openPasswordDialog(item)">
                          <v-list-item-title>
                            <v-icon left>mdi-key</v-icon>
                            Change Password
                          </v-list-item-title>
                        </v-list-item>
                      </v-list>
                    </v-menu>
                  </template>
                </v-data-table>
              </v-window-item>

              <!-- Activities Tab -->
              <v-window-item value="activities">
                <v-row class="mb-4">
                  <v-col cols="12" md="4">
                    <v-select
                      v-model="activityFilters.action"
                      label="Filter by Action"
                      :items="actionFilterOptions"
                      clearable
                      @update:model-value="loadActivities"
                    ></v-select>
                  </v-col>
                </v-row>

                <v-data-table
                  :headers="activityHeaders"
                  :items="activities"
                  :loading="loadingActivities"
                  item-value="id"
                >
                  <template v-slot:item.user_username="{ item }">
                    <strong>{{ item.user_username || 'Unknown' }}</strong>
                  </template>
                  <template v-slot:item.action="{ item }">
                    <v-chip small :color="getActionColor(item.action)">
                      {{ item.action_display }}
                    </v-chip>
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

    <!-- Password Change Dialog -->
    <v-dialog v-model="showPasswordDialog" max-width="400px">
      <v-card>
        <v-card-title>Change User Password</v-card-title>
        <v-card-text>
          <p class="mb-4">Changing password for: <strong>{{ selectedUser?.username }}</strong></p>
          <v-text-field
            v-model="newPassword"
            label="New Password"
            type="password"
            :rules="[v => !!v || 'Password is required', v => v.length >= 6 || 'Password must be at least 6 characters']"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closePasswordDialog">Cancel</v-btn>
          <v-btn color="primary" @click="changeUserPassword" :loading="changingPassword">Change Password</v-btn>
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
import api from '@/services/api'

export default {
  name: 'AdminDashboard',
  setup() {
    const tab = ref('users')
    const dashboardData = ref({})
    const users = ref([])
    const activities = ref([])
    const loading = ref(false)
    const loadingUsers = ref(false)
    const loadingActivities = ref(false)
    const changingPassword = ref(false)
    const snackbar = ref(false)
    const snackbarMessage = ref('')
    const snackbarColor = ref('success')
    const showPasswordDialog = ref(false)
    const selectedUser = ref(null)
    const newPassword = ref('')
    
    const userFilters = ref({
      role: null,
      is_blocked: null,
      is_verified: null
    })
    
    const activityFilters = ref({
      action: null
    })
    
    const roleFilterOptions = [
      { title: 'Buyer', value: 'buyer' },
      { title: 'Seller', value: 'seller' },
      { title: 'Both', value: 'both' }
    ]
    
    const statusFilterOptions = [
      { title: 'Blocked', value: 'true' },
      { title: 'Active', value: 'false' }
    ]
    
    const verificationFilterOptions = [
      { title: 'Verified', value: 'true' },
      { title: 'Unverified', value: 'false' }
    ]
    
    const actionFilterOptions = [
      { title: 'Login', value: 'login' },
      { title: 'Logout', value: 'logout' },
      { title: 'Register', value: 'register' },
      { title: 'Create Product', value: 'create_product' },
      { title: 'Update Product', value: 'update_product' },
      { title: 'Delete Product', value: 'delete_product' },
      { title: 'Create Order', value: 'create_order' },
      { title: 'Update Order', value: 'update_order' }
    ]
    
    const userHeaders = [
      { title: 'Username', key: 'username' },
      { title: 'Email', key: 'email' },
      { title: 'Role', key: 'role' },
      { title: 'Verified', key: 'is_verified' },
      { title: 'Status', key: 'is_blocked' },
      { title: 'Actions', key: 'actions', sortable: false }
    ]
    
    const activityHeaders = [
      { title: 'User', key: 'user_username' },
      { title: 'Action', key: 'action' },
      { title: 'Description', key: 'description' },
      { title: 'IP Address', key: 'ip_address' },
      { title: 'Date', key: 'created_at' }
    ]
    
    const loadDashboardData = async () => {
      loading.value = true
      try {
        const response = await api.getAdminDashboard()
        dashboardData.value = response.data
      } catch (error) {
        console.error('Failed to load dashboard data:', error)
        showSnackbar('Failed to load dashboard data', 'error')
      } finally {
        loading.value = false
      }
    }
    
    const loadUsers = async () => {
      loadingUsers.value = true
      try {
        const params = {}
        if (userFilters.value.role) params.role = userFilters.value.role
        if (userFilters.value.is_blocked !== null) params.is_blocked = userFilters.value.is_blocked
        if (userFilters.value.is_verified !== null) params.is_verified = userFilters.value.is_verified
        
        const response = await api.getAdminUsers(params)
        users.value = response.data
      } catch (error) {
        console.error('Failed to load users:', error)
        showSnackbar('Failed to load users', 'error')
      } finally {
        loadingUsers.value = false
      }
    }
    
    const loadActivities = async () => {
      loadingActivities.value = true
      try {
        const params = {}
        if (activityFilters.value.action) params.action = activityFilters.value.action
        
        const response = await api.getAdminActivities(params)
        activities.value = response.data
      } catch (error) {
        console.error('Failed to load activities:', error)
        showSnackbar('Failed to load activities', 'error')
      } finally {
        loadingActivities.value = false
      }
    }
    
    const toggleBlockUser = async (user) => {
      const action = user.profile?.is_blocked ? 'unblock' : 'block'
      if (confirm(`Are you sure you want to ${action} this user?`)) {
        try {
          await api.adminBlockUser(user.id, !user.profile?.is_blocked)
          showSnackbar(`User ${action}ed successfully`, 'success')
          await loadUsers()
          await loadDashboardData()
        } catch (error) {
          console.error(`Failed to ${action} user:`, error)
          showSnackbar(`Failed to ${action} user`, 'error')
        }
      }
    }
    
    const toggleVerifyUser = async (user) => {
      const action = user.profile?.is_verified ? 'unverify' : 'verify'
      if (confirm(`Are you sure you want to ${action} this user?`)) {
        try {
          await api.adminVerifyUser(user.id, !user.profile?.is_verified)
          showSnackbar(`User ${action === 'verify' ? 'verified' : 'unverified'} successfully`, 'success')
          await loadUsers()
          await loadDashboardData()
        } catch (error) {
          console.error(`Failed to ${action} user:`, error)
          showSnackbar(`Failed to ${action} user`, 'error')
        }
      }
    }
    
    const openPasswordDialog = (user) => {
      selectedUser.value = user
      newPassword.value = ''
      showPasswordDialog.value = true
    }
    
    const closePasswordDialog = () => {
      showPasswordDialog.value = false
      selectedUser.value = null
      newPassword.value = ''
    }
    
    const changeUserPassword = async () => {
      if (!newPassword.value || newPassword.value.length < 6) {
        showSnackbar('Password must be at least 6 characters', 'error')
        return
      }
      
      changingPassword.value = true
      try {
        await api.adminChangePassword(selectedUser.value.id, newPassword.value)
        showSnackbar('Password changed successfully', 'success')
        closePasswordDialog()
      } catch (error) {
        console.error('Failed to change password:', error)
        showSnackbar('Failed to change password', 'error')
      } finally {
        changingPassword.value = false
      }
    }
    
    const getRoleColor = (role) => {
      const colors = {
        buyer: 'primary',
        seller: 'success',
        both: 'info'
      }
      return colors[role] || 'grey'
    }
    
    const getActionColor = (action) => {
      const colors = {
        login: 'success',
        logout: 'info',
        register: 'primary',
        create_product: 'success',
        update_product: 'warning',
        delete_product: 'error',
        create_order: 'success',
        update_order: 'warning'
      }
      return colors[action] || 'grey'
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
      loadDashboardData()
      loadUsers()
      loadActivities()
    })
    
    return {
      tab,
      dashboardData,
      users,
      activities,
      loading,
      loadingUsers,
      loadingActivities,
      changingPassword,
      userFilters,
      activityFilters,
      roleFilterOptions,
      statusFilterOptions,
      verificationFilterOptions,
      actionFilterOptions,
      userHeaders,
      activityHeaders,
      snackbar,
      snackbarMessage,
      snackbarColor,
      showPasswordDialog,
      selectedUser,
      newPassword,
      loadUsers,
      loadActivities,
      toggleBlockUser,
      toggleVerifyUser,
      openPasswordDialog,
      closePasswordDialog,
      changeUserPassword,
      getRoleColor,
      getActionColor,
      formatDate
    }
  }
}
</script>

