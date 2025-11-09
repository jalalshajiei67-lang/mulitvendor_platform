<template>
  <div dir="rtl" class="admin-dashboard-wrapper">
    <!-- Navigation Drawer (Sidebar) -->
    <v-navigation-drawer
      v-model="drawer"
      :permanent="!isMobile"
      :temporary="isMobile"
      :rail="rail && !isMobile"
      :width="271"
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

        <v-list-group value="products">
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              prepend-icon="mdi-package-variant"
              title="مدیریت محصولات"
            ></v-list-item>
          </template>

          <v-list-item
            prepend-icon="mdi-format-list-bulleted"
            title="لیست محصولات"
            value="products-list"
            :active="activeView === 'products'"
            @click="setActiveView('products')"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-plus-circle"
            title="افزودن محصول"
            value="products-create"
            @click="createNewProduct"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-domain"
            title="مدیریت دپارتمان‌ها"
            value="departments"
            :active="activeView === 'departments'"
            @click.stop="setActiveView('departments')"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-folder"
            title="مدیریت دسته‌بندی‌ها"
            value="categories"
            :active="activeView === 'categories'"
            @click.stop="setActiveView('categories')"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-folder-multiple"
            title="مدیریت زیردسته‌ها"
            value="subcategories"
            :active="activeView === 'subcategories'"
            @click.stop="setActiveView('subcategories')"
          ></v-list-item>
        </v-list-group>

        <v-list-item
          prepend-icon="mdi-history"
          title="گزارش فعالیت‌ها"
          value="activities"
          :active="activeView === 'activities'"
          @click="setActiveView('activities')"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-file-document-edit-outline"
          title="درخواست‌های استعلام قیمت"
          value="rfqs"
          :active="activeView === 'rfqs'"
          @click="setActiveView('rfqs')"
        ></v-list-item>

        <v-list-group value="blog">
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              prepend-icon="mdi-newspaper"
              title="مدیریت وبلاگ"
            ></v-list-item>
          </template>

          <v-list-item
            prepend-icon="mdi-format-list-bulleted"
            title="لیست پست‌ها"
            value="blog-posts"
            :active="activeView === 'blog'"
            @click="setActiveView('blog')"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-plus-circle"
            title="افزودن پست"
            value="blog-create"
            @click="createNewBlogPost"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-tag"
            title="مدیریت دسته‌بندی‌ها"
            value="blog-categories"
            :active="activeView === 'blog-categories'"
            @click="setActiveView('blog-categories')"
          ></v-list-item>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>

    <!-- App Bar (Header) -->
    <v-app-bar
      :elevation="2"
      color="primary"
      class="admin-header"
      fixed
    >
      <!-- Logo (Far Left) -->
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

      <!-- Mobile Hamburger Button (Far Right) -->
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
        paddingLeft: !isMobile && drawer ? (rail ? '64px' : '271px') : '0'
      }"
    >
      <!-- Nested Routes (Product/Blog Forms) -->
      <div v-if="isFormRoute" class="admin-form-wrapper">
        <router-view />
      </div>
      
      <!-- Regular Dashboard Views -->
      <v-container v-else fluid class="pa-4">
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
                    <v-icon color="purple" size="32">mdi-file-document-edit-outline</v-icon>
                  </div>
                  <div class="text-h4 font-weight-bold mb-1">{{ dashboardData.rfqs?.total || 0 }}</div>
                  <div class="text-body-2 text-grey">درخواست‌های استعلام قیمت</div>
                  <div class="text-caption text-grey mt-2">
                    در انتظار: {{ dashboardData.rfqs?.pending || 0 }}
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

        <!-- Products Management View -->
        <div v-if="activeView === 'products'" class="products-view">
          <!-- Summary Cards -->
          <v-row class="mb-4">
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold mb-1">{{ products.length }}</div>
                  <div class="text-caption text-grey">کل محصولات</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold text-success mb-1">
                    {{ products.filter(p => p.is_active).length }}
                  </div>
                  <div class="text-caption text-grey">محصولات فعال</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold text-warning mb-1">
                    {{ products.filter(p => !p.is_active).length }}
                  </div>
                  <div class="text-caption text-grey">محصولات غیرفعال</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold text-info mb-1">
                    {{ selectedProducts.length }}
                  </div>
                  <div class="text-caption text-grey">انتخاب شده</div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Filters and Actions -->
          <v-card class="mb-4" elevation="0" variant="outlined">
            <v-card-text class="pa-4">
              <v-row>
                <v-col cols="12" md="3">
                  <v-text-field
                    v-model="productFilters.search"
                    label="جستجو"
                    prepend-inner-icon="mdi-magnify"
                    density="compact"
                    variant="outlined"
                    clearable
                    @update:model-value="loadProducts"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="2">
                  <v-select
                    v-model="productFilters.is_active"
                    label="وضعیت"
                    :items="productStatusFilterOptions"
                    clearable
                    density="compact"
                    variant="outlined"
                    @update:model-value="loadProducts"
                  ></v-select>
                </v-col>
                <v-col cols="12" md="2">
                  <v-text-field
                    v-model="productFilters.min_price"
                    label="حداقل قیمت"
                    type="number"
                    density="compact"
                    variant="outlined"
                    clearable
                    @update:model-value="loadProducts"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="2">
                  <v-text-field
                    v-model="productFilters.max_price"
                    label="حداکثر قیمت"
                    type="number"
                    density="compact"
                    variant="outlined"
                    clearable
                    @update:model-value="loadProducts"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="3">
                  <div class="d-flex" style="gap: 8px;">
                    <v-btn
                      color="primary"
                      @click="createNewProduct"
                      prepend-icon="mdi-plus"
                    >
                      افزودن محصول
                    </v-btn>
                    <v-menu v-if="selectedProducts.length > 0">
                      <template v-slot:activator="{ props }">
                        <v-btn
                          color="secondary"
                          v-bind="props"
                          prepend-icon="mdi-dots-vertical"
                        >
                          عملیات گروهی
                        </v-btn>
                      </template>
                      <v-list>
                        <v-list-item @click="bulkAction('activate')">
                          <template v-slot:prepend>
                            <v-icon>mdi-check-circle</v-icon>
                          </template>
                          <v-list-item-title>فعال‌سازی</v-list-item-title>
                        </v-list-item>
                        <v-list-item @click="bulkAction('deactivate')">
                          <template v-slot:prepend>
                            <v-icon>mdi-close-circle</v-icon>
                          </template>
                          <v-list-item-title>غیرفعال‌سازی</v-list-item-title>
                        </v-list-item>
                        <v-list-item @click="bulkAction('delete')">
                          <template v-slot:prepend>
                            <v-icon color="error">mdi-delete</v-icon>
                          </template>
                          <v-list-item-title>حذف</v-list-item-title>
                        </v-list-item>
                      </v-list>
                    </v-menu>
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- Products Table -->
          <v-card elevation="0" variant="outlined">
            <v-card-title class="pa-4">لیست محصولات</v-card-title>
            <v-divider></v-divider>
            <v-data-table
              v-model="selectedProducts"
              :headers="productHeaders"
              :items="products"
              :loading="loadingProducts"
              item-value="id"
              show-select
              class="products-table"
            >
              <template v-slot:item.name="{ item }">
                <div class="d-flex align-center">
                  <v-avatar size="40" class="mr-2" rounded>
                    <v-img
                      v-if="item.primary_image || item.image"
                      :src="item.primary_image || item.image"
                      cover
                    ></v-img>
                    <v-icon v-else>mdi-package-variant</v-icon>
                  </v-avatar>
                  <div>
                    <strong>{{ item.name }}</strong>
                    <div class="text-caption text-grey">{{ item.vendor_name }}</div>
                  </div>
                </div>
              </template>
              <template v-slot:item.category_name="{ item }">
                <v-chip size="small">{{ item.category_name || 'بدون دسته‌بندی' }}</v-chip>
              </template>
              <template v-slot:item.price="{ item }">
                {{ formatPrice(item.price) }}
              </template>
              <template v-slot:item.stock="{ item }">
                <v-chip
                  size="small"
                  :color="item.stock > 0 ? 'success' : 'error'"
                >
                  {{ item.stock }}
                </v-chip>
              </template>
              <template v-slot:item.created_at="{ item }">
                {{ formatDate(item.created_at) }}
              </template>
              <template v-slot:item.is_active="{ item }">
                <v-chip
                  size="small"
                  :color="item.is_active ? 'success' : 'warning'"
                >
                  {{ item.is_active ? 'فعال' : 'غیرفعال' }}
                </v-chip>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-menu>
                  <template v-slot:activator="{ props }">
                    <v-btn icon size="small" variant="text" v-bind="props">
                      <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item @click="viewProduct(item)">
                      <template v-slot:prepend>
                        <v-icon>mdi-eye</v-icon>
                      </template>
                      <v-list-item-title>مشاهده</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="editProduct(item.id)">
                      <template v-slot:prepend>
                        <v-icon>mdi-pencil</v-icon>
                      </template>
                      <v-list-item-title>ویرایش</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="toggleProductStatus(item)">
                      <template v-slot:prepend>
                        <v-icon>{{ item.is_active ? 'mdi-close-circle' : 'mdi-check-circle' }}</v-icon>
                      </template>
                      <v-list-item-title>
                        {{ item.is_active ? 'غیرفعال کردن' : 'فعال کردن' }}
                      </v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="deleteProduct(item)">
                      <template v-slot:prepend>
                        <v-icon color="error">mdi-delete</v-icon>
                      </template>
                      <v-list-item-title>حذف</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </template>
            </v-data-table>
          </v-card>
        </div>

        <!-- Departments Management View -->
        <div v-if="activeView === 'departments'" class="departments-view">
          <DepartmentManagement ref="departmentManagementRef" />
        </div>

        <!-- Categories Management View -->
        <div v-if="activeView === 'categories'" class="categories-view">
          <CategoryManagement ref="categoryManagementRef" />
        </div>

        <!-- Subcategories Management View -->
        <div v-if="activeView === 'subcategories'" class="subcategories-view">
          <SubcategoryManagement ref="subcategoryManagementRef" />
        </div>

        <!-- Blog Management View -->
        <div v-if="activeView === 'blog'" class="blog-view">
          <!-- Summary Cards -->
          <v-row class="mb-4">
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold mb-1">{{ blogPosts.length }}</div>
                  <div class="text-caption text-grey">کل پست‌ها</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold text-success mb-1">
                    {{ blogPosts.filter(p => p.status === 'published').length }}
                  </div>
                  <div class="text-caption text-grey">منتشر شده</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold text-warning mb-1">
                    {{ blogPosts.filter(p => p.status === 'draft').length }}
                  </div>
                  <div class="text-caption text-grey">پیش‌نویس</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold text-info mb-1">
                    {{ selectedBlogPosts.length }}
                  </div>
                  <div class="text-caption text-grey">انتخاب شده</div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Filters and Actions -->
          <v-card class="mb-4" elevation="0" variant="outlined">
            <v-card-text class="pa-4">
              <v-row>
                <v-col cols="12" md="3">
                  <v-text-field
                    v-model="blogFilters.search"
                    label="جستجو"
                    prepend-inner-icon="mdi-magnify"
                    density="compact"
                    variant="outlined"
                    clearable
                    @update:model-value="loadBlogPosts"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="2">
                  <v-select
                    v-model="blogFilters.status"
                    label="وضعیت"
                    :items="blogStatusFilterOptions"
                    clearable
                    density="compact"
                    variant="outlined"
                    @update:model-value="loadBlogPosts"
                  ></v-select>
                </v-col>
                <v-col cols="12" md="2">
                  <v-select
                    v-model="blogFilters.category"
                    label="دسته‌بندی"
                    :items="blogCategoryFilterOptions"
                    clearable
                    density="compact"
                    variant="outlined"
                    @update:model-value="loadBlogPosts"
                  ></v-select>
                </v-col>
                <v-col cols="12" md="5">
                  <div class="d-flex" style="gap: 8px;">
                    <v-btn
                      color="primary"
                      @click="createNewBlogPost"
                      prepend-icon="mdi-plus"
                    >
                      افزودن پست
                    </v-btn>
                    <v-menu v-if="selectedBlogPosts.length > 0">
                      <template v-slot:activator="{ props }">
                        <v-btn
                          color="secondary"
                          v-bind="props"
                          prepend-icon="mdi-dots-vertical"
                        >
                          عملیات گروهی
                        </v-btn>
                      </template>
                      <v-list>
                        <v-list-item @click="bulkBlogAction('publish')">
                          <template v-slot:prepend>
                            <v-icon>mdi-publish</v-icon>
                          </template>
                          <v-list-item-title>انتشار</v-list-item-title>
                        </v-list-item>
                        <v-list-item @click="bulkBlogAction('draft')">
                          <template v-slot:prepend>
                            <v-icon>mdi-file-document-edit</v-icon>
                          </template>
                          <v-list-item-title>پیش‌نویس</v-list-item-title>
                        </v-list-item>
                        <v-list-item @click="bulkBlogAction('archive')">
                          <template v-slot:prepend>
                            <v-icon>mdi-archive</v-icon>
                          </template>
                          <v-list-item-title>بایگانی</v-list-item-title>
                        </v-list-item>
                        <v-list-item @click="bulkBlogAction('delete')">
                          <template v-slot:prepend>
                            <v-icon color="error">mdi-delete</v-icon>
                          </template>
                          <v-list-item-title>حذف</v-list-item-title>
                        </v-list-item>
                      </v-list>
                    </v-menu>
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- Blog Posts Table -->
          <v-card elevation="0" variant="outlined">
            <v-card-title class="pa-4">لیست پست‌های وبلاگ</v-card-title>
            <v-divider></v-divider>
            <v-data-table
              v-model="selectedBlogPosts"
              :headers="blogHeaders"
              :items="blogPosts"
              :loading="loadingBlogPosts"
              item-value="slug"
              show-select
              class="blog-table"
            >
              <template v-slot:item.title="{ item }">
                <div class="d-flex align-center">
                  <v-avatar size="40" class="mr-2" rounded>
                    <v-img
                      v-if="item.featured_image"
                      :src="item.featured_image"
                      cover
                    ></v-img>
                    <v-icon v-else>mdi-newspaper</v-icon>
                  </v-avatar>
                  <div>
                    <strong>{{ item.title }}</strong>
                    <div class="text-caption text-grey">{{ item.author_username || 'نامشخص' }}</div>
                  </div>
                </div>
              </template>
              <template v-slot:item.category_name="{ item }">
                <v-chip size="small">{{ item.category_name || 'بدون دسته‌بندی' }}</v-chip>
              </template>
              <template v-slot:item.status="{ item }">
                <v-chip
                  size="small"
                  :color="getBlogStatusColor(item.status)"
                >
                  {{ getBlogStatusText(item.status) }}
                </v-chip>
              </template>
              <template v-slot:item.views="{ item }">
                <div class="d-flex align-center">
                  <v-icon size="small" class="mr-1">mdi-eye</v-icon>
                  {{ item.views || 0 }}
                </div>
              </template>
              <template v-slot:item.comments_count="{ item }">
                <div class="d-flex align-center">
                  <v-icon size="small" class="mr-1">mdi-comment</v-icon>
                  {{ item.comments_count || 0 }}
                </div>
              </template>
              <template v-slot:item.created_at="{ item }">
                {{ formatDate(item.created_at) }}
              </template>
              <template v-slot:item.actions="{ item }">
                <v-menu>
                  <template v-slot:activator="{ props }">
                    <v-btn icon size="small" variant="text" v-bind="props">
                      <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item @click="viewBlogPost(item.slug)">
                      <template v-slot:prepend>
                        <v-icon>mdi-eye</v-icon>
                      </template>
                      <v-list-item-title>مشاهده</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="editBlogPost(item.slug)">
                      <template v-slot:prepend>
                        <v-icon>mdi-pencil</v-icon>
                      </template>
                      <v-list-item-title>ویرایش</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="toggleBlogPostStatus(item)">
                      <template v-slot:prepend>
                        <v-icon>{{ item.status === 'published' ? 'mdi-file-document-edit' : 'mdi-publish' }}</v-icon>
                      </template>
                      <v-list-item-title>
                        {{ item.status === 'published' ? 'تبدیل به پیش‌نویس' : 'انتشار' }}
                      </v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="deleteBlogPost(item)">
                      <template v-slot:prepend>
                        <v-icon color="error">mdi-delete</v-icon>
                      </template>
                      <v-list-item-title>حذف</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </template>
            </v-data-table>
          </v-card>
        </div>

        <!-- RFQs Management View -->
        <div v-if="activeView === 'rfqs'" class="rfqs-view">
          <!-- Summary Cards -->
          <v-row class="mb-4">
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold mb-1">{{ rfqs.length }}</div>
                  <div class="text-caption text-grey">کل درخواست‌ها</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold text-warning mb-1">
                    {{ rfqs.filter(r => r.status === 'pending').length }}
                  </div>
                  <div class="text-caption text-grey">در انتظار بررسی</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold text-success mb-1">
                    {{ rfqs.filter(r => r.status === 'confirmed').length }}
                  </div>
                  <div class="text-caption text-grey">تأیید شده</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-card class="summary-card" elevation="0" variant="outlined">
                <v-card-text class="text-center pa-4">
                  <div class="text-h5 font-weight-bold text-info mb-1">
                    {{ rfqs.filter(r => r.images && r.images.length > 0).length }}
                  </div>
                  <div class="text-caption text-grey">با تصویر</div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Filters -->
          <v-card class="mb-4" elevation="0" variant="outlined">
            <v-card-text class="pa-4">
              <v-row>
                <v-col cols="12" md="3">
                  <v-select
                    v-model="rfqFilters.status"
                    label="فیلتر بر اساس وضعیت"
                    :items="rfqStatusFilterOptions"
                    clearable
                    density="compact"
                    variant="outlined"
                    @update:model-value="loadRFQs"
                  ></v-select>
                </v-col>
                <v-col cols="12" md="9">
                  <v-text-field
                    v-model="rfqFilters.search"
                    label="جستجو (نام، شرکت، محصول)"
                    prepend-inner-icon="mdi-magnify"
                    density="compact"
                    variant="outlined"
                    clearable
                    @update:model-value="loadRFQs"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- RFQs Table -->
          <v-card elevation="0" variant="outlined">
            <v-card-title class="pa-4">لیست درخواست‌های استعلام قیمت</v-card-title>
            <v-divider></v-divider>
            <v-data-table
              :headers="rfqHeaders"
              :items="rfqs"
              :loading="loadingRFQs"
              item-value="id"
              class="rfqs-table"
            >
              <template v-slot:item.order_number="{ item }">
                <strong>{{ item.order_number }}</strong>
              </template>
              <template v-slot:item.buyer_info="{ item }">
                <div>
                  <div class="font-weight-bold">{{ item.first_name }} {{ item.last_name }}</div>
                  <div class="text-caption text-grey">{{ item.company_name }}</div>
                  <div class="text-caption text-grey">{{ item.phone_number }}</div>
                </div>
              </template>
              <template v-slot:item.product_name="{ item }">
                <div>
                  <div class="font-weight-bold">{{ item.product_name || 'نامشخص' }}</div>
                  <div v-if="item.category_name" class="text-caption text-grey">
                    دسته‌بندی: {{ item.category_name }}
                  </div>
                </div>
              </template>
              <template v-slot:item.status="{ item }">
                <v-chip
                  size="small"
                  :color="getRFQStatusColor(item.status)"
                >
                  {{ getRFQStatusText(item.status) }}
                </v-chip>
              </template>
              <template v-slot:item.images="{ item }">
                <div v-if="item.images && item.images.length > 0" class="d-flex align-center">
                  <v-icon size="small" class="mr-1">mdi-image</v-icon>
                  {{ item.images.length }} تصویر
                </div>
                <span v-else class="text-grey">بدون تصویر</span>
              </template>
              <template v-slot:item.created_at="{ item }">
                {{ formatDate(item.created_at) }}
              </template>
              <template v-slot:item.actions="{ item }">
                <v-menu>
                  <template v-slot:activator="{ props }">
                    <v-btn icon size="small" variant="text" v-bind="props">
                      <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item @click="viewRFQDetail(item)">
                      <template v-slot:prepend>
                        <v-icon>mdi-eye</v-icon>
                      </template>
                      <v-list-item-title>مشاهده جزئیات</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="updateRFQStatus(item, 'confirmed')" v-if="item.status === 'pending'">
                      <template v-slot:prepend>
                        <v-icon color="success">mdi-check-circle</v-icon>
                      </template>
                      <v-list-item-title>تأیید</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="updateRFQStatus(item, 'rejected')" v-if="item.status === 'pending'">
                      <template v-slot:prepend>
                        <v-icon color="error">mdi-close-circle</v-icon>
                      </template>
                      <v-list-item-title>رد کردن</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </template>
            </v-data-table>
          </v-card>
        </div>

        <!-- Blog Categories Management View -->
        <div v-if="activeView === 'blog-categories'" class="blog-categories-view">
          <v-card elevation="0" variant="outlined">
            <v-card-title class="pa-4 d-flex justify-space-between align-center">
              <span>مدیریت دسته‌بندی‌های وبلاگ</span>
              <v-btn
                color="primary"
                @click="openBlogCategoryDialog()"
                prepend-icon="mdi-plus"
              >
                افزودن دسته‌بندی
              </v-btn>
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <v-data-table
                :headers="blogCategoryHeaders"
                :items="blogCategories"
                :loading="loadingBlogCategories"
                item-value="slug"
                class="blog-categories-table"
              >
                <template v-slot:item.name="{ item }">
                  <div class="d-flex align-center">
                    <v-icon class="mr-2">mdi-tag</v-icon>
                    <strong>{{ item.name }}</strong>
                  </div>
                </template>
                <template v-slot:item.posts_count="{ item }">
                  {{ item.posts_count || 0 }} پست
                </template>
                <template v-slot:item.actions="{ item }">
                  <v-menu>
                    <template v-slot:activator="{ props }">
                      <v-btn icon size="small" variant="text" v-bind="props">
                        <v-icon>mdi-dots-vertical</v-icon>
                      </v-btn>
                    </template>
                    <v-list>
                      <v-list-item @click="editBlogCategory(item)">
                        <template v-slot:prepend>
                          <v-icon>mdi-pencil</v-icon>
                        </template>
                        <v-list-item-title>ویرایش</v-list-item-title>
                      </v-list-item>
                      <v-list-item @click="deleteBlogCategory(item)">
                        <template v-slot:prepend>
                          <v-icon color="error">mdi-delete</v-icon>
                        </template>
                        <v-list-item-title>حذف</v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </v-menu>
                </template>
              </v-data-table>
            </v-card-text>
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
      <v-btn value="blog">
        <v-icon>mdi-newspaper</v-icon>
        <span>وبلاگ</span>
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

    <!-- Create/Edit Blog Category Dialog -->
    <v-dialog v-model="showCreateBlogCategoryDialog" max-width="500px">
      <v-card>
        <v-card-title>
          {{ editingBlogCategory ? 'ویرایش دسته‌بندی' : 'افزودن دسته‌بندی جدید' }}
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="blogCategoryForm.name"
            label="نام دسته‌بندی"
            variant="outlined"
            density="compact"
            :rules="[v => !!v || 'نام دسته‌بندی الزامی است']"
          ></v-text-field>
          <v-textarea
            v-model="blogCategoryForm.description"
            label="توضیحات"
            variant="outlined"
            density="compact"
            rows="3"
          ></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeBlogCategoryDialog">انصراف</v-btn>
          <v-btn color="primary" @click="saveBlogCategory" :loading="savingBlogCategory">
            {{ editingBlogCategory ? 'ذخیره' : 'افزودن' }}
          </v-btn>
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
import { useRouter, useRoute } from 'vue-router'
import api from '@/services/api'
import DepartmentManagement from '@/components/admin/DepartmentManagement.vue'
import CategoryManagement from '@/components/admin/CategoryManagement.vue'
import SubcategoryManagement from '@/components/admin/SubcategoryManagement.vue'

export default {
  name: 'AdminDashboard',
  components: {
    DepartmentManagement,
    CategoryManagement,
    SubcategoryManagement
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    const { mdAndDown } = useDisplay()
    
    const drawer = ref(!mdAndDown.value)
    const rail = ref(false)
    const isMobile = computed(() => mdAndDown.value)
    const activeView = ref('dashboard')
    const isNavigatingFromForm = ref(false)
    
    // Check if we're on a product or blog form route (admin routes)
    const isProductFormRoute = computed(() => {
      const path = route.path
      return path === '/admin/dashboard/products/new' ||
             /^\/admin\/dashboard\/products\/[^/]+\/edit$/.test(path) ||
             path === '/products/new' ||
             /^\/products\/[^/]+\/edit$/.test(path)
    })
    
    const isBlogFormRoute = computed(() => {
      return route.path === '/admin/dashboard/blog/new' || 
             route.path.match(/^\/admin\/dashboard\/blog\/[^/]+\/edit$/) ||
             route.path === '/blog/new' || 
             route.path.match(/^\/blog\/[^/]+\/edit$/)
    })
    
    const isFormRoute = computed(() => isProductFormRoute.value || isBlogFormRoute.value)
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
    
    // Products state
    const products = ref([])
    const selectedProducts = ref([])
    const loadingProducts = ref(false)
    const productFilters = ref({
      search: null,
      category: null,
      supplier: null,
      is_active: null,
      min_price: null,
      max_price: null
    })
    
    // Blog state
    const blogPosts = ref([])
    const selectedBlogPosts = ref([])
    const loadingBlogPosts = ref(false)
    const blogFilters = ref({
      search: null,
      status: null,
      category: null
    })
    const blogCategories = ref([])
    const loadingBlogCategories = ref(false)
    const showCreateBlogCategoryDialog = ref(false)
    const editingBlogCategory = ref(null)
    const savingBlogCategory = ref(false)
    const blogCategoryForm = ref({
      name: '',
      description: ''
    })

    const departmentManagementRef = ref(null)
    const categoryManagementRef = ref(null)
    const subcategoryManagementRef = ref(null)
    
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
    
    const productStatusFilterOptions = [
      { title: 'فعال', value: 'true' },
      { title: 'غیرفعال', value: 'false' }
    ]
    
    const blogStatusFilterOptions = [
      { title: 'منتشر شده', value: 'published' },
      { title: 'پیش‌نویس', value: 'draft' },
      { title: 'بایگانی', value: 'archived' }
    ]
    
    const blogCategoryFilterOptions = computed(() => {
      return blogCategories.value.map(cat => ({
        title: cat.name,
        value: cat.slug
      }))
    })
    
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
    
    const productHeaders = [
      { title: 'نام محصول', key: 'name', align: 'start' },
      { title: 'دسته‌بندی', key: 'category_name', align: 'start' },
      { title: 'قیمت', key: 'price', align: 'start' },
      { title: 'موجودی', key: 'stock', align: 'center' },
      { title: 'وضعیت', key: 'is_active', align: 'center' },
      { title: 'تاریخ ایجاد', key: 'created_at', align: 'start' },
      { title: 'عملیات', key: 'actions', sortable: false, align: 'center' }
    ]
    
    const blogHeaders = [
      { title: 'عنوان', key: 'title', align: 'start' },
      { title: 'دسته‌بندی', key: 'category_name', align: 'start' },
      { title: 'وضعیت', key: 'status', align: 'center' },
      { title: 'بازدید', key: 'views', align: 'center' },
      { title: 'نظرات', key: 'comments_count', align: 'center' },
      { title: 'تاریخ ایجاد', key: 'created_at', align: 'start' },
      { title: 'عملیات', key: 'actions', sortable: false, align: 'center' }
    ]
    
    const blogCategoryHeaders = [
      { title: 'نام', key: 'name', align: 'start' },
      { title: 'تعداد پست‌ها', key: 'posts_count', align: 'center' },
      { title: 'عملیات', key: 'actions', sortable: false, align: 'center' }
    ]
    
    const rfqHeaders = [
      { title: 'شماره درخواست', key: 'order_number', align: 'start' },
      { title: 'اطلاعات خریدار', key: 'buyer_info', align: 'start' },
      { title: 'محصول', key: 'product_name', align: 'start' },
      { title: 'وضعیت', key: 'status', align: 'center' },
      { title: 'تصاویر', key: 'images', align: 'center' },
      { title: 'تاریخ ایجاد', key: 'created_at', align: 'start' },
      { title: 'عملیات', key: 'actions', sortable: false, align: 'center' }
    ]
    
    const rfqStatusFilterOptions = [
      { title: 'در انتظار', value: 'pending' },
      { title: 'تأیید شده', value: 'confirmed' },
      { title: 'رد شده', value: 'rejected' },
      { title: 'در حال پردازش', value: 'processing' }
    ]
    
    // RFQ state
    const rfqs = ref([])
    const loadingRFQs = ref(false)
    const rfqFilters = ref({
      status: null,
      search: null
    })
    
    // Notifications
    const notifications = computed(() => {
      const notifs = []
      
      // Pending RFQs
      const pendingRFQs = dashboardData.value.rfqs?.pending || 0
      if (pendingRFQs > 0) {
        notifs.push({
          id: 'pending_rfqs',
          title: `${pendingRFQs} درخواست استعلام قیمت در انتظار`,
          subtitle: 'نیاز به بررسی دارند',
          icon: 'mdi-file-document-edit-outline',
          color: 'purple',
          type: 'rfqs'
        })
      }
      
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
      
      if (notification.type === 'rfqs') {
        setActiveView('rfqs')
        rfqFilters.value.status = 'pending'
        loadRFQs()
        scrollToTop()
      } else if (notification.type === 'orders') {
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
      console.log('Setting active view to:', view)
      
      // If we're on a nested route (form route), navigate back to dashboard first
      if (isFormRoute.value) {
        // Set flag to prevent route watcher from overriding
        isNavigatingFromForm.value = true
        // Navigate to dashboard and set view
        router.push('/admin/dashboard').then(() => {
          // Set the view immediately
          activeView.value = view
          if (isMobile.value) {
            drawer.value = false
          }
          scrollToTop()
          // Clear flag after a short delay
          setTimeout(() => {
            isNavigatingFromForm.value = false
          }, 200)
        }).catch(err => {
          console.error('Navigation error:', err)
          // Fallback: just set the view
          activeView.value = view
          if (isMobile.value) {
            drawer.value = false
          }
          isNavigatingFromForm.value = false
        })
      } else {
        // If already on dashboard, just update the view
        activeView.value = view
        if (isMobile.value) {
          drawer.value = false
        }
        scrollToTop()
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
    
    const normalizeCollectionResponse = (data) => {
      if (Array.isArray(data)) {
        return data
      }
      if (Array.isArray(data?.results)) {
        return data.results
      }
      return []
    }
    
    const loadUsers = async () => {
      loadingUsers.value = true
      try {
        const params = {}
        if (userFilters.value.role) params.role = userFilters.value.role
        if (userFilters.value.is_blocked !== null) params.is_blocked = userFilters.value.is_blocked
        if (userFilters.value.is_verified !== null) params.is_verified = userFilters.value.is_verified
        
        const response = await api.getAdminUsers(params)
        users.value = normalizeCollectionResponse(response.data)
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
        activities.value = normalizeCollectionResponse(response.data)
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
    
    // Product Management Methods
    const loadProducts = async () => {
      loadingProducts.value = true
      try {
        const params = {}
        if (productFilters.value.search) params.search = productFilters.value.search
        if (productFilters.value.category) params.category = productFilters.value.category
        if (productFilters.value.supplier) params.supplier = productFilters.value.supplier
        if (productFilters.value.is_active !== null) params.is_active = productFilters.value.is_active
        if (productFilters.value.min_price) params.min_price = productFilters.value.min_price
        if (productFilters.value.max_price) params.max_price = productFilters.value.max_price
        
        const response = await api.getAdminProducts(params)
        products.value = normalizeCollectionResponse(response.data)
      } catch (error) {
        console.error('Failed to load products:', error)
        showSnackbar('خطا در بارگذاری محصولات', 'error')
      } finally {
        loadingProducts.value = false
      }
    }
    
    const createNewProduct = () => {
      router.push('/admin/dashboard/products/new')
    }
    
    const viewProduct = (product) => {
      const slug = typeof product === 'object' ? product.slug : undefined
      const id = typeof product === 'object' ? product.id : product
      if (slug) {
        router.push(`/products/${slug}`)
      } else if (id) {
        router.push(`/products/${id}`)
      }
    }
    
    const editProduct = (productId) => {
      router.push(`/admin/dashboard/products/${productId}/edit`)
    }
    
    const toggleProductStatus = async (product) => {
      const action = product.is_active ? 'deactivate' : 'activate'
      const actionText = product.is_active ? 'غیرفعال' : 'فعال'
      
      try {
        await api.adminProductBulkAction(action, [product.id])
        showSnackbar(`محصول با موفقیت ${actionText} شد`, 'success')
        await loadProducts()
      } catch (error) {
        console.error(`Failed to ${action} product:`, error)
        showSnackbar(`خطا در ${actionText} محصول`, 'error')
      }
    }
    
    const deleteProduct = async (product) => {
      if (confirm(`آیا مطمئن هستید که می‌خواهید محصول "${product.name}" را حذف کنید؟`)) {
        try {
          await api.adminDeleteProduct(product.id)
          showSnackbar('محصول با موفقیت حذف شد', 'success')
          await loadProducts()
        } catch (error) {
          console.error('Failed to delete product:', error)
          showSnackbar('خطا در حذف محصول', 'error')
        }
      }
    }
    
    const bulkAction = async (action) => {
      if (selectedProducts.value.length === 0) {
        showSnackbar('لطفاً حداقل یک محصول را انتخاب کنید', 'warning')
        return
      }
      
      const actionText = {
        activate: 'فعال‌سازی',
        deactivate: 'غیرفعال‌سازی',
        delete: 'حذف'
      }[action]
      
      if (action === 'delete') {
        if (!confirm(`آیا مطمئن هستید که می‌خواهید ${selectedProducts.value.length} محصول را حذف کنید؟`)) {
          return
        }
      }
      
      try {
        const productIds = selectedProducts.value.map(p => typeof p === 'object' ? p.id : p)
        await api.adminProductBulkAction(action, productIds)
        showSnackbar(`${selectedProducts.value.length} محصول با موفقیت ${actionText} شد`, 'success')
        selectedProducts.value = []
        await loadProducts()
      } catch (error) {
        console.error(`Failed to ${action} products:`, error)
        showSnackbar(`خطا در ${actionText} محصولات`, 'error')
      }
    }
    
    const formatPrice = (price) => {
      // Price is in smallest currency unit (no decimals)
      // Convert to formatted string with thousand separators
      return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
    }
    
    // Blog Management Methods
    const loadBlogPosts = async () => {
      loadingBlogPosts.value = true
      try {
        const params = {}
        if (blogFilters.value.search) params.search = blogFilters.value.search
        if (blogFilters.value.status) params.status = blogFilters.value.status
        if (blogFilters.value.category) params.category = blogFilters.value.category
        
        // Try admin endpoint first, fallback to regular endpoint
        let response
        try {
          response = await api.getAdminBlogPosts(params)
        } catch {
          // Fallback to regular blog posts endpoint if admin endpoint doesn't exist
          response = await api.getBlogPosts(params)
        }
        blogPosts.value = normalizeCollectionResponse(response.data)
      } catch (error) {
        console.error('Failed to load blog posts:', error)
        showSnackbar('خطا در بارگذاری پست‌های وبلاگ', 'error')
      } finally {
        loadingBlogPosts.value = false
      }
    }
    
    const loadBlogCategories = async () => {
      loadingBlogCategories.value = true
      try {
        // Try admin endpoint first, fallback to regular endpoint
        let response
        try {
          response = await api.getAdminBlogCategories()
        } catch {
          // Fallback to regular blog categories endpoint
          response = await api.getBlogCategories()
        }
        blogCategories.value = normalizeCollectionResponse(response.data)
      } catch (error) {
        console.error('Failed to load blog categories:', error)
        showSnackbar('خطا در بارگذاری دسته‌بندی‌های وبلاگ', 'error')
      } finally {
        loadingBlogCategories.value = false
      }
    }
    
    const createNewBlogPost = () => {
      router.push('/admin/dashboard/blog/new')
    }
    
    const viewBlogPost = (slug) => {
      router.push(`/blog/${slug}`)
    }
    
    const editBlogPost = (slug) => {
      router.push(`/admin/dashboard/blog/${slug}/edit`)
    }
    
    const toggleBlogPostStatus = async (post) => {
      const newStatus = post.status === 'published' ? 'draft' : 'published'
      const actionText = newStatus === 'published' ? 'انتشار' : 'پیش‌نویس'
      
      try {
        await api.updateBlogPost(post.slug, { status: newStatus })
        showSnackbar(`پست با موفقیت ${actionText} شد`, 'success')
        await loadBlogPosts()
      } catch (error) {
        console.error('Failed to toggle blog post status:', error)
        showSnackbar(`خطا در ${actionText} پست`, 'error')
      }
    }
    
    const deleteBlogPost = async (post) => {
      if (confirm(`آیا مطمئن هستید که می‌خواهید پست "${post.title}" را حذف کنید؟`)) {
        try {
          // Try admin endpoint first, fallback to regular endpoint
          try {
            await api.adminDeleteBlogPost(post.slug)
          } catch {
            await api.deleteBlogPost(post.slug)
          }
          showSnackbar('پست با موفقیت حذف شد', 'success')
          await loadBlogPosts()
        } catch (error) {
          console.error('Failed to delete blog post:', error)
          showSnackbar('خطا در حذف پست', 'error')
        }
      }
    }
    
    const bulkBlogAction = async (action) => {
      if (selectedBlogPosts.value.length === 0) {
        showSnackbar('لطفاً حداقل یک پست را انتخاب کنید', 'warning')
        return
      }
      
      const actionText = {
        publish: 'انتشار',
        draft: 'پیش‌نویس',
        archive: 'بایگانی',
        delete: 'حذف'
      }[action]
      
      if (action === 'delete') {
        if (!confirm(`آیا مطمئن هستید که می‌خواهید ${selectedBlogPosts.value.length} پست را حذف کنید؟`)) {
          return
        }
      }
      
      try {
        const postSlugs = selectedBlogPosts.value.map(p => typeof p === 'object' ? p.slug : p)
        
        // Try admin endpoint first, fallback to individual updates
        try {
          const normalizedAction = action === 'archive' ? 'archived' : action
          await api.adminBlogPostBulkAction(normalizedAction, postSlugs)
        } catch {
          // Fallback to individual updates
          for (const slug of postSlugs) {
            if (action === 'delete') {
              await api.deleteBlogPost(slug)
            } else {
              const normalizedStatus = action === 'archive' ? 'archived' : action
              await api.updateBlogPost(slug, { status: normalizedStatus })
            }
          }
        }
        
        showSnackbar(`${selectedBlogPosts.value.length} پست با موفقیت ${actionText} شد`, 'success')
        selectedBlogPosts.value = []
        await loadBlogPosts()
      } catch (error) {
        console.error(`Failed to ${action} blog posts:`, error)
        showSnackbar(`خطا در ${actionText} پست‌ها`, 'error')
      }
    }
    
    const getBlogStatusColor = (status) => {
      const colors = {
        published: 'success',
        draft: 'warning',
        archived: 'grey'
      }
      return colors[status] || 'grey'
    }
    
    const getBlogStatusText = (status) => {
      const texts = {
        published: 'منتشر شده',
        draft: 'پیش‌نویس',
        archived: 'بایگانی'
      }
      return texts[status] || status
    }
    
    const openBlogCategoryDialog = (category = null) => {
      editingBlogCategory.value = category
      if (category) {
        blogCategoryForm.value = {
          name: category.name,
          description: category.description || ''
        }
      } else {
        blogCategoryForm.value = {
          name: '',
          description: ''
        }
      }
      showCreateBlogCategoryDialog.value = true
    }
    
    const closeBlogCategoryDialog = () => {
      showCreateBlogCategoryDialog.value = false
      editingBlogCategory.value = null
      blogCategoryForm.value = {
        name: '',
        description: ''
      }
    }
    
    const saveBlogCategory = async () => {
      if (!blogCategoryForm.value.name) {
        showSnackbar('نام دسته‌بندی الزامی است', 'error')
        return
      }
      
      savingBlogCategory.value = true
      try {
        if (editingBlogCategory.value) {
          // Try admin endpoint first, fallback to regular endpoint
          try {
            await api.adminUpdateBlogCategory(editingBlogCategory.value.slug, blogCategoryForm.value)
          } catch {
            await api.updateBlogCategory(editingBlogCategory.value.slug, blogCategoryForm.value)
          }
          showSnackbar('دسته‌بندی با موفقیت به‌روزرسانی شد', 'success')
        } else {
          // Try admin endpoint first, fallback to regular endpoint
          try {
            await api.adminCreateBlogCategory(blogCategoryForm.value)
          } catch {
            await api.createBlogCategory(blogCategoryForm.value)
          }
          showSnackbar('دسته‌بندی با موفقیت ایجاد شد', 'success')
        }
        closeBlogCategoryDialog()
        await loadBlogCategories()
      } catch (error) {
        console.error('Failed to save blog category:', error)
        showSnackbar('خطا در ذخیره دسته‌بندی', 'error')
      } finally {
        savingBlogCategory.value = false
      }
    }
    
    const editBlogCategory = (category) => {
      openBlogCategoryDialog(category)
    }
    
    const deleteBlogCategory = async (category) => {
      if (confirm(`آیا مطمئن هستید که می‌خواهید دسته‌بندی "${category.name}" را حذف کنید؟`)) {
        try {
          // Try admin endpoint first, fallback to regular endpoint
          try {
            await api.adminDeleteBlogCategory(category.slug)
          } catch {
            await api.deleteBlogCategory(category.slug)
          }
          showSnackbar('دسته‌بندی با موفقیت حذف شد', 'success')
          await loadBlogCategories()
        } catch (error) {
          console.error('Failed to delete blog category:', error)
          showSnackbar('خطا در حذف دسته‌بندی', 'error')
        }
      }
    }
    
    // Watch for route changes to update activeView
    watch(() => route.path, (newPath) => {
      // Don't override if we're navigating from a form route (user clicked menu item)
      if (isNavigatingFromForm.value) {
        return
      }
      
      if (isProductFormRoute.value) {
        activeView.value = 'products'
      } else if (isBlogFormRoute.value) {
        activeView.value = 'blog'
      } else if (newPath === '/admin/dashboard') {
        // Only reset to dashboard if not navigating from form
        activeView.value = 'dashboard'
      }
    }, { immediate: true })
    
    // RFQ Management Methods
    const loadRFQs = async () => {
      loadingRFQs.value = true
      try {
        const params = {}
        if (rfqFilters.value.status) params.status = rfqFilters.value.status
        if (rfqFilters.value.search) params.search = rfqFilters.value.search
        
        const response = await api.getAdminRFQs(params)
        rfqs.value = normalizeCollectionResponse(response.data)
      } catch (error) {
        console.error('Failed to load RFQs:', error)
        showSnackbar('خطا در بارگذاری درخواست‌های استعلام قیمت', 'error')
      } finally {
        loadingRFQs.value = false
      }
    }
    
    const viewRFQDetail = (rfq) => {
      // Open a dialog or navigate to detail page
      // For now, just show an alert with details
      const detailText = `
        شماره درخواست: ${rfq.order_number}
        نام: ${rfq.first_name} ${rfq.last_name}
        شرکت: ${rfq.company_name}
        تلفن: ${rfq.phone_number}
        محصول: ${rfq.product_name || 'نامشخص'}
        دسته‌بندی: ${rfq.category_name || 'نامشخص'}
        نیازهای خاص: ${rfq.unique_needs || 'ندارد'}
        تصاویر: ${rfq.images?.length || 0} تصویر
      `
      alert(detailText)
    }
    
    const updateRFQStatus = async (rfq, newStatus) => {
      try {
        await api.updateRFQStatus(rfq.id, newStatus)
        showSnackbar('وضعیت درخواست با موفقیت به‌روزرسانی شد', 'success')
        await loadRFQs()
        await loadDashboardData()
      } catch (error) {
        console.error('Failed to update RFQ status:', error)
        showSnackbar('خطا در به‌روزرسانی وضعیت', 'error')
      }
    }
    
    const getRFQStatusColor = (status) => {
      const colors = {
        pending: 'warning',
        confirmed: 'success',
        rejected: 'error',
        processing: 'info'
      }
      return colors[status] || 'grey'
    }
    
    const getRFQStatusText = (status) => {
      const texts = {
        pending: 'در انتظار',
        confirmed: 'تأیید شده',
        rejected: 'رد شده',
        processing: 'در حال پردازش'
      }
      return texts[status] || status
    }

    const departmentStoreFetchSafe = () => {
      if (departmentManagementRef.value?.loadDepartments) {
        departmentManagementRef.value.loadDepartments()
      }
    }

    const categoryStoreFetchSafe = () => {
      if (categoryManagementRef.value?.loadCategories) {
        categoryManagementRef.value.loadCategories()
      }
      if (categoryManagementRef.value?.loadDepartments) {
        categoryManagementRef.value.loadDepartments()
      }
    }

    const subcategoryStoreFetchSafe = () => {
      if (subcategoryManagementRef.value?.loadSubcategories) {
        subcategoryManagementRef.value.loadSubcategories()
      }
      if (subcategoryManagementRef.value?.loadCategories) {
        subcategoryManagementRef.value.loadCategories()
      }
    }
    
    // Watch for activeView changes to load data when needed
    watch(activeView, (newView) => {
      if (newView === 'dashboard') {
        loadDashboardData()
      } else if (newView === 'users') {
        loadUsers()
      } else if (newView === 'activities') {
        loadActivities()
      } else if (newView === 'products') {
        loadProducts()
      } else if (newView === 'departments') {
        departmentStoreFetchSafe()
      } else if (newView === 'categories') {
        categoryStoreFetchSafe()
      } else if (newView === 'subcategories') {
        subcategoryStoreFetchSafe()
      } else if (newView === 'blog') {
        loadBlogPosts()
        loadBlogCategories()
      } else if (newView === 'blog-categories') {
        loadBlogCategories()
      } else if (newView === 'rfqs') {
        loadRFQs()
      }
    })
    
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
      isProductFormRoute,
      isBlogFormRoute,
      isFormRoute,
      showPasswordDialog,
      selectedUser,
      newPassword,
      showNotificationsMenu,
      dashboardData,
      users,
      activities,
      products,
      selectedProducts,
      loading,
      loadingUsers,
      loadingActivities,
      loadingProducts,
      changingPassword,
      userFilters,
      activityFilters,
      productFilters,
      roleFilterOptions,
      statusFilterOptions,
      productStatusFilterOptions,
      blogStatusFilterOptions,
      blogCategoryFilterOptions,
      verificationFilterOptions,
      actionFilterOptions,
      userHeaders,
      activityHeaders,
      productHeaders,
      blogHeaders,
      blogCategoryHeaders,
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
      loadProducts,
      departmentManagementRef,
      categoryManagementRef,
      subcategoryManagementRef,
      createNewProduct,
      viewProduct,
      editProduct,
      toggleProductStatus,
      deleteProduct,
      bulkAction,
      toggleBlockUser,
      toggleVerifyUser,
      openPasswordDialog,
      closePasswordDialog,
      changeUserPassword,
      getRoleColor,
      getActionColor,
      formatDate,
      formatPrice,
      handleLogout,
      // Blog management
      blogPosts,
      selectedBlogPosts,
      loadingBlogPosts,
      blogFilters,
      blogCategories,
      loadingBlogCategories,
      showCreateBlogCategoryDialog,
      editingBlogCategory,
      savingBlogCategory,
      blogCategoryForm,
      loadBlogPosts,
      loadBlogCategories,
      createNewBlogPost,
      viewBlogPost,
      editBlogPost,
      toggleBlogPostStatus,
      deleteBlogPost,
      bulkBlogAction,
      getBlogStatusColor,
      getBlogStatusText,
      openBlogCategoryDialog,
      closeBlogCategoryDialog,
      saveBlogCategory,
      editBlogCategory,
      deleteBlogCategory,
      // RFQ management
      rfqs,
      loadingRFQs,
      rfqFilters,
      rfqHeaders,
      rfqStatusFilterOptions,
      loadRFQs,
      viewRFQDetail,
      updateRFQStatus,
      getRFQStatusColor,
      getRFQStatusText
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
  width: 100%;
}

.admin-header {
  direction: ltr;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  margin-right: 16px;
}

.logo-img {
  max-height: 40px;
}

.hamburger-btn {
  margin-left: 8px;
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
.activities-view,
.products-view,
.departments-view,
.categories-view,
.subcategories-view,
.blog-view,
.blog-categories-view,
.rfqs-view {
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
.activities-table,
.products-table,
.blog-table,
.blog-categories-table,
.rfqs-table {
  direction: rtl;
}

/* Form wrapper styling when forms are shown in admin layout */
.admin-form-wrapper {
  width: 100%;
  height: 100%;
  overflow-y: auto;
}

.admin-form-wrapper :deep(.product-form-container),
.admin-form-wrapper :deep(.blog-form) {
  padding-top: 0;
}

.admin-form-wrapper :deep(.container) {
  max-width: 100%;
  padding: 16px;
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
