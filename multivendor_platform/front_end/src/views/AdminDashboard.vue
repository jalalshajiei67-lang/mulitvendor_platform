<template>
  <div dir="rtl" class="admin-dashboard-wrapper">
    <!-- Navigation Drawer (Sidebar) -->
    <v-navigation-drawer
      v-model="drawer"
      :permanent="!isMobile"
      :temporary="isMobile"
      :rail="rail && !isMobile"
      location="right"
      class="admin-sidebar"
      fixed
      dir="rtl"
    >
      <div class="sidebar-header">
        <v-list-item
          v-if="!rail || isMobile"
          prepend-avatar="/indexo.jpg"
          :title="authStore.user?.username || 'Admin'"
          :subtitle="authStore.user?.email || ''"
        ></v-list-item>
        <v-btn
          v-if="!isMobile"
          icon
          variant="text"
          @click="rail = !rail"
          class="rail-toggle"
        >
          <v-icon>{{ rail ? 'mdi-chevron-right' : 'mdi-chevron-left' }}</v-icon>
        </v-btn>
      </div>

      <v-divider class="sidebar-divider"></v-divider>

      <v-list density="compact" nav class="sidebar-menu-list">
        <v-list-item
          prepend-icon="mdi-view-dashboard"
          title="داشبورد"
          value="dashboard"
          :active="activeView === 'dashboard'"
          @click="setActiveView('dashboard')"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-account-multiple"
          title="مدیریت کاربران"
          value="users"
          :active="activeView === 'users'"
          @click="setActiveView('users')"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-history"
          title="گزارش فعالیت‌ها"
          value="activities"
          :active="activeView === 'activities'"
          @click="setActiveView('activities')"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- App Bar (Header) -->
    <v-app-bar
      :elevation="2"
      color="primary"
      class="admin-header"
      fixed
      dir="rtl"
    >
      <!-- Logo (Visual Left) -->
      <router-link to="/" class="logo-link">
        <v-img
          src="/indexo.jpg"
          alt="Logo"
          max-height="40"
          max-width="120"
          contain
          class="logo-img"
        ></v-img>
      </router-link>

      <v-spacer></v-spacer>

      <!-- Mobile Hamburger Button (Visual Right) -->
      <v-app-bar-nav-icon
        v-if="isMobile"
        @click="drawer = !drawer"
        class="hamburger-btn"
      ></v-app-bar-nav-icon>

      <!-- Notifications Bell -->
      <v-menu
        v-model="showNotificationsMenu"
        location="bottom end"
        offset="10"
      >
        <template v-slot:activator="{ props }">
          <v-btn
            icon
            v-bind="props"
            variant="text"
            class="notification-btn"
          >
            <v-badge
              :content="notificationCount"
              :model-value="notificationCount > 0"
              color="error"
              overlap
            >
              <v-icon>mdi-bell</v-icon>
            </v-badge>
          </v-btn>
        </template>

        <v-card min-width="300" max-width="400">
          <v-card-title class="d-flex align-center justify-space-between">
            <span>اعلان‌ها</span>
            <v-btn
              icon
              size="small"
              variant="text"
              @click="showNotificationsMenu = false"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>
          <v-divider></v-divider>
          <v-list>
            <v-list-item
              v-if="notifications.length === 0"
              class="text-center py-4"
            >
              <v-list-item-title class="text-grey">هیچ اعلانی وجود ندارد</v-list-item-title>
            </v-list-item>
            <v-list-item
              v-for="notification in notifications"
              :key="notification.id"
              @click="handleNotificationClick(notification)"
              class="notification-item"
            >
              <template v-slot:prepend>
                <v-icon :color="notification.color">{{ notification.icon }}</v-icon>
              </template>
              <v-list-item-title>{{ notification.title }}</v-list-item-title>
              <v-list-item-subtitle>{{ notification.subtitle }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card>
      </v-menu>

      <!-- User Menu -->
      <v-menu location="bottom end">
        <template v-slot:activator="{ props }">
          <v-btn
            icon
            v-bind="props"
            variant="text"
          >
            <v-avatar size="32">
              <v-icon>mdi-account</v-icon>
            </v-avatar>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="handleLogout">
            <template v-slot:prepend>
              <v-icon>mdi-logout</v-icon>
            </template>
            <v-list-item-title>خروج</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <!-- Main Content -->
    <div 
      class="admin-main"
      :style="{
        paddingLeft: !isMobile && drawer ? (rail ? '64px' : '256px') : '0'
      }"
    >
      <v-container fluid class="pa-4">
        <!-- Dashboard View -->
        <div v-if="activeView === 'dashboard'" class="dashboard-view">
          <!-- Stats Cards -->
          <v-row class="mb-6">
            <v-col cols="12" sm="6" md="3">
              <v-card class="stat-card" elevation="0" variant="outlined">
                <v-card-text class="pa-4">
                  <div class="d-flex align-center justify-space-between mb-2">
                    <v-icon color="primary" size="32">mdi-account-group</v-icon>
                  </div>
                  <div class="text-h4 font-weight-bold mb-1">{{ dashboardData.users?.total || 0 }}</div>
                  <div class="text-body-2 text-grey">کل کاربران</div>
                  <div class="text-caption text-grey mt-2">
                    خریدار: {{ dashboardData.users?.buyers || 0 }} | فروشنده: {{ dashboardData.users?.sellers || 0 }}
                  </div>
                </v-card-text>
              </v-card>
            </v-col>

            <v-col cols="12" sm="6" md="3">
              <v-card class="stat-card" elevation="0" variant="outlined">
                <v-card-text class="pa-4">
                  <div class="d-flex align-center justify-space-between mb-2">
                    <v-icon color="success" size="32">mdi-package-variant</v-icon>
                  </div>
                  <div class="text-h4 font-weight-bold mb-1">{{ dashboardData.products?.total || 0 }}</div>
                  <div class="text-body-2 text-grey">کل محصولات</div>
                  <div class="text-caption text-grey mt-2">
                    فعال: {{ dashboardData.products?.active || 0 }}
                  </div>
                </v-card-text>
              </v-card>
            </v-col>

            <v-col cols="12" sm="6" md="3">
              <v-card class="stat-card" elevation="0" variant="outlined">
                <v-card-text class="pa-4">
                  <div class="d-flex align-center justify-space-between mb-2">
                    <v-icon color="info" size="32">mdi-cart</v-icon>
                  </div>
                  <div class="text-h4 font-weight-bold mb-1">{{ dashboardData.orders?.total || 0 }}</div>
                  <div class="text-body-2 text-grey">کل سفارشات</div>
                  <div class="text-caption text-grey mt-2">
                    در انتظار: {{ dashboardData.orders?.pending || 0 }}
                  </div>
                </v-card-text>
              </v-card>
            </v-col>

            <v-col cols="12" sm="6" md="3">
              <v-card class="stat-card" elevation="0" variant="outlined">
                <v-card-text class="pa-4">
                  <div class="d-flex align-center justify-space-between mb-2">
                    <v-icon color="warning" size="32">mdi-alert</v-icon>
                  </div>
                  <div class="text-h4 font-weight-bold mb-1">
                    {{ (dashboardData.users?.blocked || 0) + (dashboardData.users?.unverified || 0) }}
                  </div>
                  <div class="text-body-2 text-grey">هشدارها</div>
                  <div class="text-caption text-grey mt-2">
                    مسدود: {{ dashboardData.users?.blocked || 0 }} | تأیید نشده: {{ dashboardData.users?.unverified || 0 }}
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Quick Summary Cards -->
          <v-row>
            <v-col cols="12">
              <v-card elevation="0" variant="outlined">
                <v-card-title class="text-h6 pa-4">خلاصه فعالیت‌ها</v-card-title>
                <v-divider></v-divider>
                <v-card-text class="pa-4">
                  <v-row>
                    <v-col cols="12" md="4">
                      <div class="summary-item">
                        <v-icon color="primary" class="mb-2">mdi-account-plus</v-icon>
                        <div class="text-h6">{{ dashboardData.users?.total || 0 }}</div>
                        <div class="text-caption text-grey">کاربران جدید این ماه</div>
                      </div>
                    </v-col>
                    <v-col cols="12" md="4">
                      <div class="summary-item">
                        <v-icon color="success" class="mb-2">mdi-cart-plus</v-icon>
                        <div class="text-h6">{{ dashboardData.orders?.total || 0 }}</div>
                        <div class="text-caption text-grey">سفارشات این ماه</div>
                      </div>
                    </v-col>
                    <v-col cols="12" md="4">
                      <div class="summary-item">
                        <v-icon color="info" class="mb-2">mdi-chart-line</v-icon>
                        <div class="text-h6">{{ dashboardData.products?.active || 0 }}</div>
                        <div class="text-caption text-grey">محصولات فعال</div>
                      </div>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </div>

        <!-- Users Management View -->
        <div v-if="activeView === 'users'" class="users-view">
          <!-- Summary Cards -->
          <v-row class="mb-4">
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold mb-1">{{ users.length }}</div>
                  <div class="text-caption text-grey">کل کاربران</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold text-success mb-1">
                    {{ users.filter(u => !u.profile?.is_blocked).length }}
                  </div>
                  <div class="text-caption text-grey">کاربران فعال</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold text-error mb-1">
                    {{ users.filter(u => u.profile?.is_blocked).length }}
                  </div>
                  <div class="text-caption text-grey">کاربران مسدود</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold text-warning mb-1">
                    {{ users.filter(u => !u.profile?.is_verified).length }}
                  </div>
                  <div class="text-caption text-grey">تأیید نشده</div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Filters -->
          <v-card class="mb-4" elevation="0" variant="outlined">
            <v-card-text class="pa-4">
              <v-row>
                <v-col cols="12" md="4">
                  <v-select
                    v-model="userFilters.role"
                    label="فیلتر بر اساس نقش"
                    :items="roleFilterOptions"
                    clearable
                    density="compact"
                    variant="outlined"
                    @update:model-value="loadUsers"
                  ></v-select>
                </v-col>
                <v-col cols="12" md="4">
                  <v-select
                    v-model="userFilters.is_blocked"
                    label="فیلتر بر اساس وضعیت"
                    :items="statusFilterOptions"
                    clearable
                    density="compact"
                    variant="outlined"
                    @update:model-value="loadUsers"
                  ></v-select>
                </v-col>
                <v-col cols="12" md="4">
                  <v-select
                    v-model="userFilters.is_verified"
                    label="فیلتر بر اساس تأیید"
                    :items="verificationFilterOptions"
                    clearable
                    density="compact"
                    variant="outlined"
                    @update:model-value="loadUsers"
                  ></v-select>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- Users Table -->
          <v-card elevation="0" variant="outlined">
            <v-card-title class="pa-4">لیست کاربران</v-card-title>
            <v-divider></v-divider>
            <v-data-table
              :headers="userHeaders"
              :items="users"
              :loading="loadingUsers"
              item-value="id"
              class="users-table"
            >
              <template v-slot:item.username="{ item }">
                <div class="d-flex align-center">
                  <v-avatar size="32" class="mr-2">
                    <v-icon>mdi-account</v-icon>
                  </v-avatar>
                  <strong>{{ item.username }}</strong>
                </div>
              </template>
              <template v-slot:item.role="{ item }">
                <v-chip size="small" :color="getRoleColor(item.profile?.role)">
                  {{ item.profile?.role === 'buyer' ? 'خریدار' : item.profile?.role === 'seller' ? 'فروشنده' : 'N/A' }}
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
                    <v-btn icon size="small" variant="text" v-bind="props">
                      <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item @click="toggleBlockUser(item)">
                      <template v-slot:prepend>
                        <v-icon>{{ item.profile?.is_blocked ? 'mdi-lock-open' : 'mdi-lock' }}</v-icon>
                      </template>
                      <v-list-item-title>
                        {{ item.profile?.is_blocked ? 'رفع مسدودی' : 'مسدود کردن' }}
                      </v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="toggleVerifyUser(item)">
                      <template v-slot:prepend>
                        <v-icon>{{ item.profile?.is_verified ? 'mdi-close-circle' : 'mdi-check-circle' }}</v-icon>
                      </template>
                      <v-list-item-title>
                        {{ item.profile?.is_verified ? 'لغو تأیید' : 'تأیید کاربر' }}
                      </v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="openPasswordDialog(item)">
                      <template v-slot:prepend>
                        <v-icon>mdi-key</v-icon>
                      </template>
                      <v-list-item-title>تغییر رمز عبور</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </template>
            </v-data-table>
          </v-card>
        </div>

        <!-- Activities View -->
        <div v-if="activeView === 'activities'" class="activities-view">
          <!-- Summary Cards -->
          <v-row class="mb-4">
            <v-col cols="12" sm="6" md="4">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold mb-1">{{ activities.length }}</div>
                  <div class="text-caption text-grey">کل فعالیت‌ها</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold text-success mb-1">
                    {{ activities.filter(a => a.action === 'login' || a.action === 'register').length }}
                  </div>
                  <div class="text-caption text-grey">ورود/ثبت‌نام</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold text-info mb-1">
                    {{ activities.filter(a => a.action?.includes('order')).length }}
                  </div>
                  <div class="text-caption text-grey">سفارشات</div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Filters -->
          <v-card class="mb-4" elevation="0" variant="outlined">
            <v-card-text class="pa-4">
              <v-select
                v-model="activityFilters.action"
                label="فیلتر بر اساس عملیات"
                :items="actionFilterOptions"
                clearable
                density="compact"
                variant="outlined"
                @update:model-value="loadActivities"
              ></v-select>
            </v-card-text>
          </v-card>

          <!-- Activities Table -->
          <v-card elevation="0" variant="outlined">
            <v-card-title class="pa-4">گزارش فعالیت‌ها</v-card-title>
            <v-divider></v-divider>
            <v-data-table
              :headers="activityHeaders"
              :items="activities"
              :loading="loadingActivities"
              item-value="id"
              class="activities-table"
            >
              <template v-slot:item.user_username="{ item }">
                <div class="d-flex align-center">
                  <v-avatar size="32" class="mr-2">
                    <v-icon>mdi-account</v-icon>
                  </v-avatar>
                  <strong>{{ item.user_username || 'نامشخص' }}</strong>
                </div>
              </template>
              <template v-slot:item.action="{ item }">
                <v-chip size="small" :color="getActionColor(item.action)">
                  {{ item.action_display }}
                </v-chip>
              </template>
              <template v-slot:item.created_at="{ item }">
                {{ formatDate(item.created_at) }}
              </template>
            </v-data-table>
          </v-card>
        </div>
      </v-container>
    </div>

    <!-- Mobile Bottom Navigation -->
    <v-bottom-navigation
      v-if="isMobile"
      :model-value="activeView"
      @update:model-value="setActiveView"
      color="primary"
      class="mobile-bottom-nav"
    >
      <v-btn value="dashboard" @click="scrollToTop">
        <v-icon>mdi-view-dashboard</v-icon>
        <span>داشبورد</span>
      </v-btn>
      <v-btn value="users">
        <v-icon>mdi-account-multiple</v-icon>
        <span>کاربران</span>
      </v-btn>
      <v-btn value="activities">
        <v-icon>mdi-history</v-icon>
        <span>فعالیت‌ها</span>
      </v-btn>
      <v-btn @click="showNotificationsMenu = true">
        <v-badge
          :content="notificationCount"
          :model-value="notificationCount > 0"
          color="error"
          overlap
        >
          <v-icon>mdi-bell</v-icon>
        </v-badge>
        <span>اعلان‌ها</span>
      </v-btn>
    </v-bottom-navigation>

    <!-- Password Change Dialog -->
    <v-dialog v-model="showPasswordDialog" max-width="400px">
      <v-card>
        <v-card-title>تغییر رمز عبور کاربر</v-card-title>
        <v-card-text>
          <p class="mb-4">تغییر رمز عبور برای: <strong>{{ selectedUser?.username }}</strong></p>
          <v-text-field
            v-model="newPassword"
            label="رمز عبور جدید"
            type="password"
            variant="outlined"
            density="compact"
            :rules="[v => !!v || 'رمز عبور الزامی است', v => v.length >= 6 || 'رمز عبور باید حداقل 6 کاراکتر باشد']"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closePasswordDialog">انصراف</v-btn>
          <v-btn color="primary" @click="changeUserPassword" :loading="changingPassword">تغییر رمز</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000" location="top">
      {{ snackbarMessage }}
    </v-snackbar>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useDisplay } from 'vuetify'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/services/api'

export default {
  name: 'AdminDashboard',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const { mdAndDown } = useDisplay()
    
    const drawer = ref(!mdAndDown.value)
    const rail = ref(false)
    const isMobile = computed(() => mdAndDown.value)
    const activeView = ref('dashboard')
    const showPasswordDialog = ref(false)
    const selectedUser = ref(null)
    const newPassword = ref('')
    const showNotificationsMenu = ref(false)
    
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
    
    const userFilters = ref({
      role: null,
      is_blocked: null,
      is_verified: null
    })
    
    const activityFilters = ref({
      action: null
    })
    
    // Watch for mobile changes
    watch(isMobile, (newVal) => {
      drawer.value = !newVal
    })
    
    const roleFilterOptions = [
      { title: 'خریدار', value: 'buyer' },
      { title: 'فروشنده', value: 'seller' },
      { title: 'هر دو', value: 'both' }
    ]
    
    const statusFilterOptions = [
      { title: 'مسدود شده', value: 'true' },
      { title: 'فعال', value: 'false' }
    ]
    
    const verificationFilterOptions = [
      { title: 'تأیید شده', value: 'true' },
      { title: 'تأیید نشده', value: 'false' }
    ]
    
    const actionFilterOptions = [
      { title: 'ورود', value: 'login' },
      { title: 'خروج', value: 'logout' },
      { title: 'ثبت‌نام', value: 'register' },
      { title: 'ایجاد محصول', value: 'create_product' },
      { title: 'به‌روزرسانی محصول', value: 'update_product' },
      { title: 'حذف محصول', value: 'delete_product' },
      { title: 'ایجاد سفارش', value: 'create_order' },
      { title: 'به‌روزرسانی سفارش', value: 'update_order' }
    ]
    
    const userHeaders = [
      { title: 'نام کاربری', key: 'username', align: 'start' },
      { title: 'ایمیل', key: 'email', align: 'start' },
      { title: 'نقش', key: 'role', align: 'center' },
      { title: 'تأیید شده', key: 'is_verified', align: 'center' },
      { title: 'وضعیت', key: 'is_blocked', align: 'center' },
      { title: 'عملیات', key: 'actions', sortable: false, align: 'center' }
    ]
    
    const activityHeaders = [
      { title: 'کاربر', key: 'user_username', align: 'start' },
      { title: 'عملیات', key: 'action', align: 'center' },
      { title: 'توضیحات', key: 'description', align: 'start' },
      { title: 'آدرس IP', key: 'ip_address', align: 'start' },
      { title: 'تاریخ', key: 'created_at', align: 'start' }
    ]
    
    // Notifications
    const notifications = computed(() => {
      const notifs = []
      
      // Pending orders
      const pendingOrders = dashboardData.value.orders?.pending || 0
      if (pendingOrders > 0) {
        notifs.push({
          id: 'pending_orders',
          title: `${pendingOrders} سفارش در انتظار`,
          subtitle: 'نیاز به بررسی دارند',
          icon: 'mdi-cart',
          color: 'warning',
          type: 'orders'
        })
      }
      
      // Recent comments (from activities)
      const recentComments = activities.value.filter(a => 
        a.action?.includes('comment') || a.description?.includes('comment')
      ).slice(0, 5)
      
      if (recentComments.length > 0) {
        notifs.push({
          id: 'recent_comments',
          title: `${recentComments.length} نظر جدید`,
          subtitle: 'نیاز به بررسی دارند',
          icon: 'mdi-comment',
          color: 'info',
          type: 'comments'
        })
      }
      
      // Blocked users
      const blockedUsers = dashboardData.value.users?.blocked || 0
      if (blockedUsers > 0) {
        notifs.push({
          id: 'blocked_users',
          title: `${blockedUsers} کاربر مسدود`,
          subtitle: 'نیاز به بررسی دارند',
          icon: 'mdi-account-off',
          color: 'error',
          type: 'users'
        })
      }
      
      return notifs
    })
    
    const notificationCount = computed(() => {
      return notifications.value.length
    })
    
    const handleNotificationClick = (notification) => {
      showNotificationsMenu.value = false
      
      if (notification.type === 'orders') {
        setActiveView('activities')
        activityFilters.value.action = 'create_order'
        loadActivities()
        scrollToTop()
      } else if (notification.type === 'comments') {
        setActiveView('activities')
        // Filter activities to show comments
        scrollToTop()
      } else if (notification.type === 'users') {
        setActiveView('users')
        userFilters.value.is_blocked = 'true'
        loadUsers()
        scrollToTop()
      }
    }
    
    const setActiveView = (view) => {
      activeView.value = view
      if (isMobile.value) {
        drawer.value = false
      }
    }
    
    const scrollToTop = () => {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
    
    const loadDashboardData = async () => {
      loading.value = true
      try {
        const response = await api.getAdminDashboard()
        dashboardData.value = response.data
      } catch (error) {
        console.error('Failed to load dashboard data:', error)
        showSnackbar('خطا در بارگذاری اطلاعات داشبورد', 'error')
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
        showSnackbar('خطا در بارگذاری کاربران', 'error')
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
        showSnackbar('خطا در بارگذاری فعالیت‌ها', 'error')
      } finally {
        loadingActivities.value = false
      }
    }
    
    const toggleBlockUser = async (user) => {
      const action = user.profile?.is_blocked ? 'unblock' : 'block'
      const actionText = user.profile?.is_blocked ? 'رفع مسدودی' : 'مسدود کردن'
      if (confirm(`آیا مطمئن هستید که می‌خواهید این کاربر را ${actionText} کنید؟`)) {
        try {
          await api.adminBlockUser(user.id, !user.profile?.is_blocked)
          showSnackbar(`کاربر با موفقیت ${actionText} شد`, 'success')
          await loadUsers()
          await loadDashboardData()
        } catch (error) {
          console.error(`Failed to ${action} user:`, error)
          showSnackbar(`خطا در ${actionText} کاربر`, 'error')
        }
      }
    }
    
    const toggleVerifyUser = async (user) => {
      const action = user.profile?.is_verified ? 'unverify' : 'verify'
      const actionText = user.profile?.is_verified ? 'لغو تأیید' : 'تأیید'
      if (confirm(`آیا مطمئن هستید که می‌خواهید این کاربر را ${actionText} کنید؟`)) {
        try {
          await api.adminVerifyUser(user.id, !user.profile?.is_verified)
          showSnackbar(`کاربر با موفقیت ${actionText} شد`, 'success')
          await loadUsers()
          await loadDashboardData()
        } catch (error) {
          console.error(`Failed to ${action} user:`, error)
          showSnackbar(`خطا در ${actionText} کاربر`, 'error')
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
        showSnackbar('رمز عبور باید حداقل 6 کاراکتر باشد', 'error')
        return
      }
      
      changingPassword.value = true
      try {
        await api.adminChangePassword(selectedUser.value.id, newPassword.value)
        showSnackbar('رمز عبور با موفقیت تغییر یافت', 'success')
        closePasswordDialog()
      } catch (error) {
        console.error('Failed to change password:', error)
        showSnackbar('خطا در تغییر رمز عبور', 'error')
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
      return date.toLocaleDateString('fa-IR') + ' ' + date.toLocaleTimeString('fa-IR', { hour: '2-digit', minute: '2-digit' })
    }
    
    const showSnackbar = (message, color = 'success') => {
      snackbarMessage.value = message
      snackbarColor.value = color
      snackbar.value = true
    }
    
    const handleLogout = async () => {
      try {
        await authStore.logout()
        router.push('/')
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
    
    onMounted(() => {
      loadDashboardData()
      loadUsers()
      loadActivities()
    })
    
    return {
      authStore,
      drawer,
      rail,
      isMobile,
      activeView,
      showPasswordDialog,
      selectedUser,
      newPassword,
      showNotificationsMenu,
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
      notifications,
      notificationCount,
      snackbar,
      snackbarMessage,
      snackbarColor,
      setActiveView,
      scrollToTop,
      handleNotificationClick,
      loadUsers,
      loadActivities,
      toggleBlockUser,
      toggleVerifyUser,
      openPasswordDialog,
      closePasswordDialog,
      changeUserPassword,
      getRoleColor,
      getActionColor,
      formatDate,
      handleLogout
    }
  }
}
</script>

<style scoped>
.admin-sidebar {
  direction: rtl;
  right: 0 !important;
  left: auto !important;
}

.sidebar-header {
  position: relative;
  padding: 8px;
}

.rail-toggle {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  margin-bottom: 10px;
}

.sidebar-divider {
  margin-bottom: 10px;
}

.sidebar-menu-list {
  margin-top: 10px;
}

.admin-header {
  direction: rtl;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  margin-left: 16px;
  order: -1;
}

.logo-img {
  max-height: 40px;
}

.hamburger-btn {
  margin-right: 8px;
  order: 1;
}

.notification-btn {
  margin-left: 8px;
}

.admin-dashboard-wrapper {
  min-height: 100vh;
  background-color: rgb(var(--v-theme-background));
}

.admin-main {
  min-height: 100vh;
  background-color: rgb(var(--v-theme-background));
  padding-top: 64px;
  transition: padding-right 0.3s ease;
}

.dashboard-view,
.users-view,
.activities-view {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stat-card {
  transition: all 0.3s ease;
  border-radius: 8px;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.summary-card {
  border-radius: 8px;
  transition: all 0.3s ease;
}

.summary-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.summary-item {
  text-align: center;
  padding: 16px;
}

.notification-item {
  cursor: pointer;
  transition: background-color 0.2s;
}

.notification-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.mobile-bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  direction: rtl;
}

.users-table,
.activities-table {
  direction: rtl;
}

/* Mobile adjustments */
@media (max-width: 960px) {
  .admin-main {
    padding-bottom: 80px !important;
  }
  
  .stat-card .text-h4 {
    font-size: 1.75rem !important;
  }
}
</style>
