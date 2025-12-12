<template>
  <div dir="rtl" class="admin-dashboard-wrapper">
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
        </v-row>

        <v-row class="mb-4">
          <v-col cols="12" md="6">
            <v-card elevation="0" variant="outlined" class="pa-4">
              <v-card-title class="d-flex align-center justify-space-between">
                <span>پرچم‌های ضد سوءاستفاده</span>
                <v-chip color="error" size="small" v-if="flagsBadgeCount > 0">
                  {{ flagsBadgeCount }}
                </v-chip>
              </v-card-title>
              <v-card-text class="text-body-2">
                بررسی سریع دعوت‌های مسدود شده و بازبینی‌های پرچم‌دار.
                <div class="mt-4 d-flex gap-3">
                  <v-btn color="primary" prepend-icon="mdi-shield-alert" @click="handleNavigate('flags')">
                    مشاهده پرچم‌ها
                  </v-btn>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>

      <!-- Users Management View -->
      <div v-if="activeView === 'users'" class="users-view">
        <v-card elevation="0" variant="outlined">
          <v-card-title class="pa-4">لیست کاربران</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-data-table
              :headers="userHeaders"
              :items="users"
              :loading="loadingUsers"
              item-value="id"
            >
              <template v-slot:item.username="{ item }">
                <div class="d-flex align-center">
                  <v-avatar size="32" class="mr-2">
                    <v-icon>mdi-account</v-icon>
                  </v-avatar>
                  <strong>{{ item.username }}</strong>
                </div>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn size="small" variant="text" @click="toggleBlockUser(item)">
                  {{ item.profile?.is_blocked ? 'رفع مسدودی' : 'مسدود' }}
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </div>

      <!-- Departments Management View -->
      <div v-if="activeView === 'departments'" class="departments-view">
        <AdminDepartmentManagement />
      </div>

      <!-- Categories Management View -->
      <div v-if="activeView === 'categories'" class="categories-view">
        <AdminCategoryManagement />
      </div>

      <!-- Subcategories Management View -->
      <div v-if="activeView === 'subcategories'" class="subcategories-view">
        <AdminSubcategoryManagement />
      </div>

      <!-- Products Management View -->
      <div v-if="activeView === 'products'" class="products-view">
        <v-card elevation="0" variant="outlined">
          <v-card-title class="pa-4 d-flex justify-space-between align-center">
            <span>مدیریت محصولات</span>
            <v-btn color="primary" :to="'/admin/dashboard/products/new'" prepend-icon="mdi-plus">
              افزودن محصول
            </v-btn>
          </v-card-title>
          <v-divider></v-divider>
          
          <!-- Filters -->
          <v-card-text>
            <v-alert
              type="info"
              variant="tonal"
              color="primary"
              class="mb-4"
              border="start"
              elevation="0"
            >
              اگر روی تصویر یا توضیحات محصول واترمارک یا نام فروشنده می‌بینید، با دکمه «عدم نمایش» محصول را از مارکت‌پلیس مخفی کنید و پیام دوستانه‌ای برای فروشنده بفرستید تا محتوا را تمیز کند.
            </v-alert>
            <v-row class="mb-4">
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="productFilters.search"
                  label="جستجو (نام یا توضیحات)"
                  prepend-inner-icon="mdi-magnify"
                  variant="outlined"
                  density="compact"
                  clearable
                  @update:model-value="loadProducts"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="2">
                <v-select
                  v-model="productFilters.category"
                  :items="filterCategories"
                  item-title="name"
                  item-value="id"
                  label="دسته‌بندی"
                  variant="outlined"
                  density="compact"
                  clearable
                  @update:model-value="loadProducts"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6" md="2">
                <v-select
                  v-model="productFilters.supplier"
                  :items="filterSuppliers"
                  item-title="name"
                  item-value="id"
                  label="تامین‌کننده"
                  variant="outlined"
                  density="compact"
                  clearable
                  @update:model-value="loadProducts"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6" md="2">
                <v-select
                  v-model="productFilters.status"
                  :items="statusOptions"
                  label="وضعیت"
                  variant="outlined"
                  density="compact"
                  clearable
                  @update:model-value="loadProducts"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6" md="2">
                <v-btn
                  color="secondary"
                  variant="outlined"
                  block
                  @click="resetProductFilters"
                  prepend-icon="mdi-refresh"
                >
                  پاک کردن
                </v-btn>
              </v-col>
            </v-row>

            <v-data-table
              :headers="productHeaders"
              :items="products"
              :loading="loadingProducts"
              item-value="id"
              class="elevation-0"
            >
              <template v-slot:item.image="{ item }">
                <v-avatar size="48" rounded>
                  <v-img
                    v-if="item.primary_image || item.image"
                    :src="item.primary_image || item.image"
                    cover
                  ></v-img>
                  <v-icon v-else>mdi-image-off</v-icon>
                </v-avatar>
              </template>
              <template v-slot:item.name="{ item }">
                <div>
                  <div class="font-weight-bold">{{ item.name }}</div>
                  <div v-if="item.slug" class="text-caption text-grey">{{ item.slug }}</div>
                </div>
              </template>
              <template v-slot:item.supplier="{ item }">
                <div>
                  <div class="font-weight-medium">{{ item.supplier?.name || item.vendor_name || 'نامشخص' }}</div>
                </div>
              </template>
              <template v-slot:item.category_path="{ item }">
                <div class="text-caption">
                  {{ item.category_path || 'بدون دسته‌بندی' }}
                </div>
              </template>
              <template v-slot:item.price="{ item }">
                <div class="font-weight-bold">
                  {{ formatPrice(item.price) }}
                </div>
              </template>
              <template v-slot:item.stock="{ item }">
                <v-chip size="small" :color="item.stock > 0 ? 'success' : 'warning'">
                  {{ item.stock || 0 }}
                </v-chip>
              </template>
              <template v-slot:item.is_active="{ item }">
                <v-chip size="small" :color="item.is_active ? 'success' : 'error'">
                  {{ item.is_active ? 'فعال' : 'غیرفعال' }}
                </v-chip>
              </template>
              <template v-slot:item.is_marketplace_hidden="{ item }">
                <v-chip
                  v-if="item.is_marketplace_hidden"
                  size="small"
                  color="warning"
                  variant="tonal"
                  prepend-icon="mdi-eye-off"
                >
                  مخفی شده
                  <v-tooltip activator="parent" location="top">
                    {{ item.marketplace_hide_reason || 'به دلیل واترمارک یا محتوای برنددار مخفی شده است.' }}
                  </v-tooltip>
                </v-chip>
                <v-chip v-else size="small" color="success" variant="tonal" prepend-icon="mdi-shield-check">
                  تمیز
                </v-chip>
              </template>
              <template v-slot:item.created_at="{ item }">
                {{ formatDate(item.created_at) }}
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon
                  size="small"
                  variant="text"
                  @click="viewProductDetail(item)"
                >
                  <v-icon>mdi-eye</v-icon>
                </v-btn>
                <v-btn
                  icon
                  size="small"
                  variant="text"
                  :to="`/admin/dashboard/products/${item.id}/edit`"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn
                  icon
                  size="small"
                  variant="text"
                  @click="toggleProductStatus(item)"
                >
                  <v-icon :color="item.is_active ? 'warning' : 'success'">
                    {{ item.is_active ? 'mdi-eye-off' : 'mdi-eye' }}
                  </v-icon>
                </v-btn>
                <v-btn
                  icon
                  size="small"
                  variant="text"
                  :color="item.is_marketplace_hidden ? 'success' : 'warning'"
                  @click="openHideDialog(item)"
                >
                  <v-icon>
                    {{ item.is_marketplace_hidden ? 'mdi-eye-check-outline' : 'mdi-eye-off-outline' }}
                  </v-icon>
                  <v-tooltip activator="parent" location="top">
                    {{ item.is_marketplace_hidden ? 'بازگردانی به مارکت‌پلیس' : 'عدم نمایش در مارکت‌پلیس' }}
                  </v-tooltip>
                </v-btn>
                <v-btn
                  icon
                  size="small"
                  variant="text"
                  color="error"
                  @click="deleteProduct(item)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </div>

      <!-- Activities View -->
      <div v-if="activeView === 'activities'" class="activities-view">
        <v-card elevation="0" variant="outlined">
          <v-card-title class="pa-4">گزارش فعالیت‌ها</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-data-table
              :headers="activityHeaders"
              :items="activities"
              :loading="loadingActivities"
              item-value="id"
            >
              <template v-slot:item.user_username="{ item }">
                {{ item.user_username || 'نامشخص' }}
              </template>
              <template v-slot:item.action="{ item }">
                <v-chip size="small">{{ item.action_display }}</v-chip>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </div>

      <!-- Flags View -->
      <div v-if="activeView === 'flags'" class="flags-view">
        <v-row>
          <v-col cols="12" md="6">
            <v-card elevation="0" variant="outlined">
              <v-card-title class="pa-4 d-flex justify-space-between align-center">
                <span>بازبینی‌های پرچم‌دار</span>
                <v-chip color="error" size="small" v-if="flaggedProductReviews.length">
                  {{ flaggedProductReviews.length }}
                </v-chip>
              </v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-data-table
                  :headers="flagReviewHeaders"
                  :items="flaggedProductReviews"
                  :loading="loadingFlags"
                  item-value="id"
                  class="mb-4"
                >
                  <template #item.actions="{ item }">
                    <v-btn size="small" variant="text" color="success" @click="clearFlag('product_review', item.id)">
                      تایید و پاک‌کردن پرچم
                    </v-btn>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card elevation="0" variant="outlined">
              <v-card-title class="pa-4 d-flex justify-space-between align-center">
                <span>نظرات فروشنده پرچم‌دار</span>
                <v-chip color="error" size="small" v-if="flaggedSupplierComments.length">
                  {{ flaggedSupplierComments.length }}
                </v-chip>
              </v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-data-table
                  :headers="flagSupplierHeaders"
                  :items="flaggedSupplierComments"
                  :loading="loadingFlags"
                  item-value="id"
                  class="mb-4"
                >
                  <template #item.actions="{ item }">
                    <v-btn size="small" variant="text" color="success" @click="clearFlag('supplier_comment', item.id)">
                      تایید و پاک‌کردن پرچم
                    </v-btn>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12">
            <v-card elevation="0" variant="outlined">
              <v-card-title class="pa-4 d-flex justify-space-between align-center">
                <span>دعوت‌های مسدود شده</span>
                <v-chip color="warning" size="small" v-if="invitationBlocks.length">
                  {{ invitationBlocks.length }}
                </v-chip>
              </v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-data-table
                  :headers="inviteBlockHeaders"
                  :items="invitationBlocks"
                  :loading="loadingFlags"
                  item-value="id"
                >
                  <template #item.actions="{ item }">
                    <v-btn size="small" variant="text" color="primary" @click="clearFlag('invitation_block', item.id)">
                      رسیدگی شد
                    </v-btn>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>

      <!-- Blog Management View -->
      <div v-if="activeView === 'blog'" class="blog-view">
        <v-card elevation="0" variant="outlined">
          <v-card-title class="pa-4">لیست پست‌های وبلاگ</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-data-table
              :headers="blogHeaders"
              :items="blogPosts"
              :loading="loadingBlog"
              item-value="id"
            >
              <template v-slot:item.title="{ item }">
                <strong>{{ item.title }}</strong>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn size="small" variant="text" :to="`/admin/dashboard/blog/${item.slug}/edit`">
                  ویرایش
                </v-btn>
                <v-btn size="small" variant="text" color="error" @click="deleteBlogPost(item)">
                  حذف
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </div>

      <!-- RFQs View -->
      <div v-if="activeView === 'rfqs'" class="rfqs-view">
        <v-card elevation="0" variant="outlined">
          <v-card-title class="pa-4 d-flex justify-space-between align-center">
            <span>درخواست‌های استعلام قیمت</span>
            <v-btn color="primary" @click="showCreateLeadDialog = true">
              <v-icon class="ms-2">mdi-plus</v-icon>
              ثبت لید جدید
            </v-btn>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-data-table
              :headers="rfqHeaders"
              :items="rfqs"
              :loading="loadingRFQs"
              item-value="id"
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
              <template v-slot:item.images="{ item }">
                <div v-if="item.images && item.images.length > 0" class="d-flex gap-2">
                  <v-avatar
                    v-for="(img, idx) in item.images.slice(0, 3)"
                    :key="idx"
                    size="40"
                    @click="viewImage(img.image_url || img.image)"
                  >
                    <v-img :src="img.image_url || img.image" cover></v-img>
                  </v-avatar>
                  <v-chip v-if="item.images.length > 3" size="small" color="primary">
                    +{{ item.images.length - 3 }}
                  </v-chip>
                </div>
                <span v-else class="text-grey">بدون تصویر</span>
              </template>
              <template v-slot:item.status="{ item }">
                <v-chip size="small" :color="getRFQStatusColor(item.status)">
                  {{ getRFQStatusText(item.status) }}
                </v-chip>
              </template>
              <template v-slot:item.created_at="{ item }">
                {{ formatDate(item.created_at) }}
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon
                  size="small"
                  variant="text"
                  @click="viewRFQDetail(item)"
                >
                  <v-icon>mdi-eye</v-icon>
                </v-btn>
                <v-menu>
                  <template v-slot:activator="{ props }">
                    <v-btn icon size="small" variant="text" v-bind="props">
                      <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item @click="updateRFQStatus(item, 'confirmed')">
                      <v-list-item-title>تأیید</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="updateRFQStatus(item, 'rejected')">
                      <v-list-item-title>رد</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="updateRFQStatus(item, 'processing')">
                      <v-list-item-title>در حال پردازش</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </div>

      <!-- RFQ Detail Dialog -->
      <v-dialog v-model="showRFQDetailDialog" max-width="900px" scrollable>
        <v-card v-if="selectedRFQ">
          <v-card-title class="d-flex justify-space-between align-center pa-4" style="background: rgb(var(--v-theme-primary)); color: white;">
            <div>
              <div class="text-h6">جزئیات درخواست استعلام قیمت</div>
              <div class="text-caption">{{ selectedRFQ.order_number }}</div>
            </div>
            <v-btn icon variant="text" color="white" @click="showRFQDetailDialog = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>

          <v-divider></v-divider>

          <v-card-text class="pa-6">
            <v-row>
              <!-- Buyer Information -->
              <v-col cols="12" md="6">
                <v-card variant="outlined" class="pa-4">
                  <div class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-2">
                    <v-icon color="primary">mdi-account</v-icon>
                    اطلاعات خریدار
                  </div>
                  <v-list density="compact">
                    <v-list-item>
                      <v-list-item-title>نام و نام خانوادگی</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedRFQ.first_name }} {{ selectedRFQ.last_name }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>نام شرکت</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedRFQ.company_name }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>شماره تماس</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedRFQ.phone_number }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item v-if="selectedRFQ.buyer_username">
                      <v-list-item-title>نام کاربری</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedRFQ.buyer_username }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-col>

              <!-- Order Information -->
              <v-col cols="12" md="6">
                <v-card variant="outlined" class="pa-4">
                  <div class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-2">
                    <v-icon color="primary">mdi-information</v-icon>
                    اطلاعات درخواست
                  </div>
                  <v-list density="compact">
                    <v-list-item>
                      <v-list-item-title>وضعیت</v-list-item-title>
                      <v-list-item-subtitle>
                        <v-chip size="small" :color="getRFQStatusColor(selectedRFQ.status)">
                          {{ getRFQStatusText(selectedRFQ.status) }}
                        </v-chip>
                      </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>تاریخ ایجاد</v-list-item-title>
                      <v-list-item-subtitle>{{ formatDate(selectedRFQ.created_at) }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item v-if="selectedRFQ.product_name">
                      <v-list-item-title>محصول</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedRFQ.product_name }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item v-if="selectedRFQ.category_name">
                      <v-list-item-title>دسته‌بندی</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedRFQ.category_name }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-col>

              <!-- Description -->
              <v-col cols="12">
                <v-card variant="outlined" class="pa-4">
                  <div class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-2">
                    <v-icon color="primary">mdi-text-box</v-icon>
                    نیازهای خاص
                  </div>
                  <p class="text-body-1">{{ selectedRFQ.unique_needs || 'توضیحی ارائه نشده است' }}</p>
                </v-card>
              </v-col>

              <!-- Images -->
              <v-col cols="12" v-if="selectedRFQ.images && selectedRFQ.images.length > 0">
                <v-card variant="outlined" class="pa-4">
                  <div class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-2">
                    <v-icon color="primary">mdi-image</v-icon>
                    تصاویر ({{ selectedRFQ.images.length }})
                  </div>
                  <v-row>
                    <v-col
                      v-for="(img, idx) in selectedRFQ.images"
                      :key="idx"
                      cols="6"
                      sm="4"
                      md="3"
                    >
                      <v-card
                        class="image-card"
                        @click="viewImage(img.image_url || img.image)"
                      >
                        <v-img
                          :src="img.image_url || img.image"
                          aspect-ratio="1"
                          cover
                          class="cursor-pointer"
                        >
                          <template v-slot:placeholder>
                            <div class="d-flex align-center justify-center fill-height">
                              <v-progress-circular
                                indeterminate
                                color="primary"
                              ></v-progress-circular>
                            </div>
                          </template>
                        </v-img>
                        <v-card-actions class="pa-2">
                          <v-btn
                            icon
                            size="small"
                            variant="text"
                            @click.stop="viewImage(img.image_url || img.image)"
                          >
                            <v-icon>mdi-magnify</v-icon>
                          </v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions class="pa-4">
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="showRFQDetailDialog = false">
              بستن
            </v-btn>
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn color="primary" v-bind="props">
                  تغییر وضعیت
                  <v-icon class="ms-2">mdi-menu-down</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item @click="updateRFQStatus(selectedRFQ, 'confirmed')">
                  <v-list-item-title>تأیید</v-list-item-title>
                </v-list-item>
                <v-list-item @click="updateRFQStatus(selectedRFQ, 'rejected')">
                  <v-list-item-title>رد</v-list-item-title>
                </v-list-item>
                <v-list-item @click="updateRFQStatus(selectedRFQ, 'processing')">
                  <v-list-item-title>در حال پردازش</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Product Detail Dialog -->
      <v-dialog v-model="showProductDetailDialog" max-width="900px" scrollable>
        <v-card v-if="selectedProduct">
          <v-card-title class="d-flex justify-space-between align-center pa-4" style="background: rgb(var(--v-theme-primary)); color: white;">
            <div>
              <div class="text-h6">جزئیات محصول</div>
              <div class="text-caption">{{ selectedProduct.name }}</div>
            </div>
            <v-btn icon variant="text" color="white" @click="showProductDetailDialog = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>

          <v-divider></v-divider>

          <v-card-text v-if="loadingProductDetail" class="pa-6">
            <div class="d-flex justify-center align-center" style="min-height: 200px;">
              <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
            </div>
          </v-card-text>

          <v-card-text v-else class="pa-6">
            <v-row>
              <!-- Product Image -->
              <v-col cols="12" md="4">
                <v-card variant="outlined" class="pa-4">
                  <div class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-2">
                    <v-icon color="primary">mdi-image</v-icon>
                    تصویر محصول
                  </div>
                  <v-img
                    v-if="selectedProduct.primary_image || selectedProduct.image"
                    :src="selectedProduct.primary_image || selectedProduct.image"
                    aspect-ratio="1"
                    cover
                    class="rounded-lg"
                  ></v-img>
                  <div v-else class="text-center text-grey pa-8">
                    <v-icon size="64">mdi-image-off</v-icon>
                    <div class="mt-2">بدون تصویر</div>
                  </div>
                </v-card>
              </v-col>

              <!-- Product Information -->
              <v-col cols="12" md="8">
                <v-card variant="outlined" class="pa-4 mb-4">
                  <div class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-2">
                    <v-icon color="primary">mdi-information</v-icon>
                    اطلاعات محصول
                  </div>
                  <v-list density="compact">
                    <v-list-item>
                      <v-list-item-title>نام محصول</v-list-item-title>
                      <v-list-item-subtitle class="font-weight-bold">{{ selectedProduct.name }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item v-if="selectedProduct.slug">
                      <v-list-item-title>Slug</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedProduct.slug }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>قیمت</v-list-item-title>
                      <v-list-item-subtitle class="font-weight-bold">{{ formatPrice(selectedProduct.price) }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>موجودی</v-list-item-title>
                      <v-list-item-subtitle>
                        <v-chip size="small" :color="selectedProduct.stock > 0 ? 'success' : 'warning'">
                          {{ selectedProduct.stock || 0 }}
                        </v-chip>
                      </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>وضعیت</v-list-item-title>
                      <v-list-item-subtitle>
                        <v-chip size="small" :color="selectedProduct.is_active ? 'success' : 'error'">
                          {{ selectedProduct.is_active ? 'فعال' : 'غیرفعال' }}
                        </v-chip>
                      </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>نمایش در مارکت‌پلیس</v-list-item-title>
                      <v-list-item-subtitle>
                        <v-chip
                          size="small"
                          :color="selectedProduct.is_marketplace_hidden ? 'warning' : 'success'"
                          variant="tonal"
                          prepend-icon="mdi-shield-check-outline"
                        >
                          {{ selectedProduct.is_marketplace_hidden ? 'مخفی شده (فقط مینی‌وبسایت/داشبورد)' : 'نمایش داده می‌شود' }}
                        </v-chip>
                      </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item v-if="selectedProduct.marketplace_hide_reason">
                      <v-list-item-title>یادداشت به فروشنده</v-list-item-title>
                      <v-list-item-subtitle class="text-body-2">
                        {{ selectedProduct.marketplace_hide_reason }}
                      </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item v-if="selectedProduct.category_path">
                      <v-list-item-title>دسته‌بندی</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedProduct.category_path }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item v-if="selectedProduct.supplier?.name || selectedProduct.vendor_name">
                      <v-list-item-title>تامین‌کننده</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedProduct.supplier?.name || selectedProduct.vendor_name }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>تاریخ ایجاد</v-list-item-title>
                      <v-list-item-subtitle>{{ formatDate(selectedProduct.created_at) }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card>

                <!-- Description -->
                <v-card v-if="selectedProduct.description" variant="outlined" class="pa-4">
                  <div class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-2">
                    <v-icon color="primary">mdi-text-box</v-icon>
                    توضیحات
                  </div>
                  <div v-html="selectedProduct.description" class="text-body-1"></div>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions class="pa-4">
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="showProductDetailDialog = false">
              بستن
            </v-btn>
            <v-btn
              color="primary"
              :to="`/admin/dashboard/products/${selectedProduct.id}/edit`"
              @click="showProductDetailDialog = false"
            >
              ویرایش محصول
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Hide Product Dialog -->
      <v-dialog v-model="showHideDialog" max-width="520">
        <v-card>
          <v-card-title class="d-flex align-center justify-space-between">
            <div class="d-flex align-center gap-2">
              <v-icon color="warning">mdi-eye-off-outline</v-icon>
              <span class="text-subtitle-1">
                {{ productToHide?.is_marketplace_hidden ? 'بازگردانی نمایش محصول' : 'عدم نمایش در مارکت‌پلیس' }}
              </span>
            </div>
            <v-btn icon="mdi-close" variant="text" @click="closeHideDialog"></v-btn>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <p class="text-body-2 text-medium-emphasis mb-3">
              محصول «{{ productToHide?.name || '...' }}»
              {{ productToHide?.is_marketplace_hidden ? 'به‌زودی دوباره در مارکت‌پلیس نمایش داده می‌شود.' : 'از مارکت‌پلیس مخفی می‌شود اما در مینی‌وبسایت و داشبورد فروشنده قابل مشاهده می‌ماند.' }}
            </p>
            <v-alert
              type="info"
              variant="tonal"
              color="primary"
              class="mb-4"
              border="start"
              elevation="0"
            >
              یک یادداشت دوستانه برای فروشنده بگذارید تا تصویر و توضیحات را بدون واترمارک یا اطلاعات برند اصلاح کند.
            </v-alert>
            <v-textarea
              v-model="hideReason"
              label="پیام به فروشنده"
              rows="3"
              auto-grow
              variant="outlined"
              color="primary"
              :disabled="productToHide?.is_marketplace_hidden && !hideReason"
            ></v-textarea>
          </v-card-text>
          <v-card-actions class="pa-4">
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="closeHideDialog">
              انصراف
            </v-btn>
            <v-btn
              :color="productToHide?.is_marketplace_hidden ? 'success' : 'warning'"
              :loading="hidingProduct"
              @click="confirmHideProduct"
            >
              {{ productToHide?.is_marketplace_hidden ? 'بازگردانی به مارکت‌پلیس' : 'عدم نمایش و ارسال پیام' }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Create Lead Dialog -->
      <v-dialog v-model="showCreateLeadDialog" max-width="800px" scrollable persistent>
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center pa-4" style="background: rgb(var(--v-theme-primary)); color: white;">
            <div class="text-h6">ثبت لید جدید</div>
            <v-btn icon variant="text" color="white" @click="closeCreateLeadDialog">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>

          <v-divider></v-divider>

          <v-card-text class="pa-6">
            <v-form ref="createLeadForm" v-model="createLeadFormValid">
              <v-row>
                <!-- Lead Source -->
                <v-col cols="12" md="6">
                  <v-select
                    v-model="createLeadData.lead_source"
                    :items="leadSourceOptions"
                    label="منبع لید *"
                    required
                    :rules="[v => !!v || 'لطفاً منبع لید را انتخاب کنید']"
                  ></v-select>
                </v-col>

                <!-- Category -->
                <v-col cols="12" md="6">
                  <v-select
                    v-model="createLeadData.category_id"
                    :items="leadCategories"
                    item-title="name"
                    item-value="id"
                    label="دسته‌بندی *"
                    required
                    :rules="[v => !!v || 'لطفاً دسته‌بندی را انتخاب کنید']"
                    :loading="loadingLeadCategories"
                    @update:model-value="onCategoryChange"
                  ></v-select>
                </v-col>

                <!-- Product (Optional) -->
                <v-col cols="12" md="6">
                  <v-select
                    v-model="createLeadData.product_id"
                    :items="leadProducts"
                    item-title="name"
                    item-value="id"
                    label="محصول (اختیاری)"
                    :loading="loadingLeadProducts"
                    clearable
                    @update:model-value="onProductChange"
                  ></v-select>
                </v-col>

                <!-- First Name -->
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="createLeadData.first_name"
                    label="نام *"
                    required
                    :rules="[v => !!v || 'لطفاً نام را وارد کنید']"
                  ></v-text-field>
                </v-col>

                <!-- Last Name -->
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="createLeadData.last_name"
                    label="نام خانوادگی *"
                    required
                    :rules="[v => !!v || 'لطفاً نام خانوادگی را وارد کنید']"
                  ></v-text-field>
                </v-col>

                <!-- Company Name -->
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="createLeadData.company_name"
                    label="نام شرکت *"
                    required
                    :rules="[v => !!v || 'لطفاً نام شرکت را وارد کنید']"
                  ></v-text-field>
                </v-col>

                <!-- Phone Number -->
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="createLeadData.phone_number"
                    label="شماره تماس *"
                    required
                    :rules="[v => !!v || 'لطفاً شماره تماس را وارد کنید']"
                  ></v-text-field>
                </v-col>

                <!-- Email -->
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="createLeadData.email"
                    label="ایمیل"
                    type="email"
                  ></v-text-field>
                </v-col>

                <!-- Unique Needs -->
                <v-col cols="12">
                  <v-textarea
                    v-model="createLeadData.unique_needs"
                    label="نیازهای خاص"
                    rows="3"
                  ></v-textarea>
                </v-col>

                <!-- Auto-matched Suppliers -->
                <v-col cols="12" v-if="autoMatchedSuppliers.length > 0">
                  <v-card variant="outlined" class="pa-4">
                    <div class="text-subtitle-1 font-weight-bold mb-3">
                      تامین‌کنندگان پیشنهادی (بر اساس دسته‌بندی/محصول)
                    </div>
                    <v-chip-group v-model="selectedAutoSuppliers" multiple>
                      <v-chip
                        v-for="supplier in autoMatchedSuppliers"
                        :key="supplier.id"
                        :value="supplier.id"
                      >
                        {{ supplier.name }}
                      </v-chip>
                    </v-chip-group>
                  </v-card>
                </v-col>

                <!-- Manual Supplier Selection -->
                <v-col cols="12">
                  <v-card variant="outlined" class="pa-4">
                    <div class="text-subtitle-1 font-weight-bold mb-3">
                      انتخاب دستی تامین‌کنندگان
                    </div>
                    <v-select
                      v-model="createLeadData.supplier_ids"
                      :items="allSuppliers"
                      item-title="name"
                      item-value="id"
                      label="تامین‌کنندگان"
                      multiple
                      chips
                      :loading="loadingSuppliers"
                    ></v-select>
                  </v-card>
                </v-col>

                <!-- Image Upload -->
                <v-col cols="12">
                  <v-card variant="outlined" class="pa-4">
                    <div class="text-subtitle-1 font-weight-bold mb-3">تصاویر (حداکثر 10 تصویر)</div>
                    <v-file-input
                      v-model="createLeadImages"
                      label="انتخاب تصاویر"
                      multiple
                      accept="image/*"
                      prepend-icon="mdi-camera"
                      show-size
                      :rules="[v => !v || v.length <= 10 || 'حداکثر 10 تصویر مجاز است']"
                    ></v-file-input>
                    <div v-if="createLeadImages && createLeadImages.length > 0" class="mt-4">
                      <v-row>
                        <v-col
                          v-for="(file, idx) in createLeadImages"
                          :key="idx"
                          cols="6"
                          sm="4"
                          md="3"
                        >
                          <v-card>
                            <v-img
                              :src="getImagePreview(file)"
                              aspect-ratio="1"
                              cover
                            ></v-img>
                            <v-card-actions>
                              <v-btn
                                icon
                                size="small"
                                variant="text"
                                color="error"
                                @click="removeImage(idx)"
                              >
                                <v-icon>mdi-delete</v-icon>
                              </v-btn>
                            </v-card-actions>
                          </v-card>
                        </v-col>
                      </v-row>
                    </div>
                  </v-card>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions class="pa-4">
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="closeCreateLeadDialog">
              انصراف
            </v-btn>
            <v-btn
              color="primary"
              :loading="submittingLead"
              :disabled="!createLeadFormValid"
              @click="submitLead"
            >
              ثبت لید
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const adminApi = useAdminApi()
const categoryApi = useCategoryApi()
const productApi = useProductApi()
const supplierApi = useSupplierApi()

const activeView = ref((route.query.view as string) || 'dashboard')
const dashboardData = ref<any>({})
const users = ref<any[]>([])
const activities = ref<any[]>([])
const blogPosts = ref<any[]>([])
const rfqs = ref<any[]>([])
const products = ref<any[]>([])
const flaggedSupplierComments = ref<any[]>([])
const flaggedProductReviews = ref<any[]>([])
const invitationBlocks = ref<any[]>([])
const flagsBadgeCount = computed(() =>
  flaggedSupplierComments.value.length + flaggedProductReviews.value.length + invitationBlocks.value.length
)

const loading = ref(false)
const loadingFlags = ref(false)
const loadingUsers = ref(false)
const loadingActivities = ref(false)
const loadingBlog = ref(false)
const loadingRFQs = ref(false)
const loadingProducts = ref(false)
const showRFQDetailDialog = ref(false)
const selectedRFQ = ref<any>(null)
const loadingRFQDetail = ref(false)
const showProductDetailDialog = ref(false)
const selectedProduct = ref<any>(null)
const loadingProductDetail = ref(false)
const showHideDialog = ref(false)
const productToHide = ref<any>(null)
const hidingProduct = ref(false)
const defaultHideMessage =
  'این محصول شامل واترمارک یا اطلاعات فروشنده است. لطفاً نسخه تمیز و بدون برند را بارگذاری کنید تا دوباره در مارکت‌پلیس نمایش داده شود.'
const hideReason = ref(defaultHideMessage)

// Product filters
const productFilters = ref({
  search: '',
  category: null as number | null,
  supplier: null as number | null,
  status: null as string | null
})
const filterCategories = ref<any[]>([])
const filterSuppliers = ref<any[]>([])
const statusOptions = [
  { title: 'فعال', value: 'true' },
  { title: 'غیرفعال', value: 'false' }
]

// Create Lead Dialog
const showCreateLeadDialog = ref(false)
const createLeadFormValid = ref(false)
const createLeadForm = ref<any>(null)
const submittingLead = ref(false)
const createLeadData = ref({
  lead_source: '',
  category_id: null as number | null,
  product_id: null as number | null,
  first_name: '',
  last_name: '',
  company_name: '',
  phone_number: '',
  email: '',
  unique_needs: '',
  supplier_ids: [] as number[]
})
const createLeadImages = ref<File[]>([])
const leadCategories = ref<any[]>([])
const leadProducts = ref<any[]>([])
const allSuppliers = ref<any[]>([])
const autoMatchedSuppliers = ref<any[]>([])
const selectedAutoSuppliers = ref<number[]>([])
const loadingLeadCategories = ref(false)
const loadingLeadProducts = ref(false)
const loadingSuppliers = ref(false)

const leadSourceOptions = [
  { title: 'تلفن', value: 'phone' },
  { title: 'واتساپ', value: 'whatsapp' },
  { title: 'اینستاگرام', value: 'instagram' }
]

const userHeaders = [
  { title: 'نام کاربری', key: 'username' },
  { title: 'ایمیل', key: 'email' },
  { title: 'نقش', key: 'role' },
  { title: 'عملیات', key: 'actions' }
]

const activityHeaders = [
  { title: 'کاربر', key: 'user_username' },
  { title: 'عملیات', key: 'action' },
  { title: 'تاریخ', key: 'created_at' }
]

const blogHeaders = [
  { title: 'عنوان', key: 'title' },
  { title: 'وضعیت', key: 'status' },
  { title: 'تاریخ', key: 'created_at' },
  { title: 'عملیات', key: 'actions' }
]

const rfqHeaders = [
  { title: 'شماره درخواست', key: 'order_number' },
  { title: 'اطلاعات خریدار', key: 'buyer_info' },
  { title: 'محصول', key: 'product_name' },
  { title: 'تصاویر', key: 'images' },
  { title: 'وضعیت', key: 'status' },
  { title: 'تاریخ', key: 'created_at' },
  { title: 'عملیات', key: 'actions' }
]

const productHeaders = [
  { title: 'تصویر', key: 'image', sortable: false },
  { title: 'نام محصول', key: 'name' },
  { title: 'تامین‌کننده', key: 'supplier' },
  { title: 'دسته‌بندی', key: 'category_path' },
  { title: 'قیمت', key: 'price' },
  { title: 'موجودی', key: 'stock' },
  { title: 'وضعیت', key: 'is_active' },
  { title: 'پاکیزگی محتوا', key: 'is_marketplace_hidden' },
  { title: 'تاریخ ایجاد', key: 'created_at' },
  { title: 'عملیات', key: 'actions', sortable: false }
]

const flagReviewHeaders = [
  { title: 'محصول', key: 'product' },
  { title: 'فروشنده', key: 'vendor_name' },
  { title: 'امتیاز', key: 'rating' },
  { title: 'متن', key: 'comment' },
  { title: 'دلیل', key: 'flag_reason' },
  { title: 'عملیات', key: 'actions', sortable: false }
]

const flagSupplierHeaders = [
  { title: 'فروشنده', key: 'vendor_name' },
  { title: 'کاربر', key: 'reviewer' },
  { title: 'امتیاز', key: 'rating' },
  { title: 'متن', key: 'comment' },
  { title: 'دلیل', key: 'flag_reason' },
  { title: 'عملیات', key: 'actions', sortable: false }
]

const inviteBlockHeaders = [
  { title: 'فروشنده', key: 'vendor_name' },
  { title: 'ایمیل', key: 'invitee_email' },
  { title: 'تلفن', key: 'invitee_phone' },
  { title: 'دلیل', key: 'reason' },
  { title: 'عملیات', key: 'actions', sortable: false }
]

const loadDashboardData = async () => {
  loading.value = true
  try {
    const data = await adminApi.getDashboard()
    dashboardData.value = data
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  } finally {
    loading.value = false
  }
}

const loadUsers = async () => {
  loadingUsers.value = true
  try {
    const data = await adminApi.getUsers()
    users.value = Array.isArray(data) ? data : data.results || []
  } catch (error) {
    console.error('Failed to load users:', error)
  } finally {
    loadingUsers.value = false
  }
}

const loadActivities = async () => {
  loadingActivities.value = true
  try {
    const data = await adminApi.getActivities()
    activities.value = Array.isArray(data) ? data : data.results || []
  } catch (error) {
    console.error('Failed to load activities:', error)
  } finally {
    loadingActivities.value = false
  }
}

const loadFlags = async () => {
  loadingFlags.value = true
  try {
    const data = await adminApi.getGamificationFlags()
    flaggedSupplierComments.value = data.flagged_supplier_comments || []
    flaggedProductReviews.value = data.flagged_product_reviews || []
    invitationBlocks.value = data.invitation_blocks || []
  } catch (error) {
    console.error('Failed to load flags:', error)
  } finally {
    loadingFlags.value = false
  }
}

const clearFlag = async (objectType: string, id: number) => {
  try {
    await adminApi.clearGamificationFlag({ object_type: objectType, id })
    await loadFlags()
    await loadDashboardData()
  } catch (error) {
    console.error('Failed to clear flag:', error)
  }
}

const loadBlogPosts = async () => {
  loadingBlog.value = true
  try {
    const data = await adminApi.getAdminBlogPosts()
    blogPosts.value = Array.isArray(data) ? data : data.results || []
  } catch (error) {
    console.error('Failed to load blog posts:', error)
  } finally {
    loadingBlog.value = false
  }
}

const loadRFQs = async () => {
  loadingRFQs.value = true
  try {
    const data = await adminApi.getRFQs()
    const normalized = Array.isArray(data) ? data : (data as any)?.results || []
    rfqs.value = normalized
    console.log('Loaded RFQs:', rfqs.value)
  } catch (error) {
    console.error('Failed to load RFQs:', error)
  } finally {
    loadingRFQs.value = false
  }
}

const loadProducts = async () => {
  loadingProducts.value = true
  try {
    const params: any = {}
    if (productFilters.value.search) {
      params.search = productFilters.value.search
    }
    if (productFilters.value.category) {
      params.category = productFilters.value.category
    }
    if (productFilters.value.supplier) {
      params.supplier = productFilters.value.supplier
    }
    if (productFilters.value.status !== null) {
      params.is_active = productFilters.value.status === 'true'
    }
    
    const data = await adminApi.getAdminProducts(params)
    products.value = Array.isArray(data) ? data : data.results || []
  } catch (error) {
    console.error('Failed to load products:', error)
  } finally {
    loadingProducts.value = false
  }
}

const loadFilterData = async () => {
  try {
    // Load categories for filter
    const categoriesResponse = await categoryApi.getCategories()
    filterCategories.value = Array.isArray(categoriesResponse) ? categoriesResponse : categoriesResponse.results || []
    
    // Load suppliers for filter
    filterSuppliers.value = await supplierApi.getSuppliers()
  } catch (error) {
    console.error('Failed to load filter data:', error)
  }
}

const resetProductFilters = () => {
  productFilters.value = {
    search: '',
    category: null,
    supplier: null,
    status: null
  }
  loadProducts()
}

const toggleBlockUser = async (user: any) => {
  try {
    await adminApi.blockUser(user.id, !user.profile?.is_blocked)
    await loadUsers()
  } catch (error) {
    console.error('Failed to toggle block user:', error)
  }
}

const deleteBlogPost = async (post: any) => {
  if (confirm(`آیا مطمئن هستید که می‌خواهید پست "${post.title}" را حذف کنید؟`)) {
    try {
      await adminApi.deleteBlogPost(post.slug)
      await loadBlogPosts()
    } catch (error) {
      console.error('Failed to delete blog post:', error)
    }
  }
}

const viewProductDetail = async (product: any) => {
  loadingProductDetail.value = true
  try {
    // Try to get full product detail from API
    const detail = await adminApi.getAdminProductDetail(product.id)
    selectedProduct.value = detail
  } catch (error) {
    console.error('Failed to load product detail:', error)
    // Fallback to using the data we already have
    selectedProduct.value = product
  } finally {
    loadingProductDetail.value = false
    showProductDetailDialog.value = true
  }
}

const openHideDialog = (product: any) => {
  productToHide.value = product
  hideReason.value = product.marketplace_hide_reason || defaultHideMessage
  showHideDialog.value = true
}

const closeHideDialog = () => {
  showHideDialog.value = false
  productToHide.value = null
  hideReason.value = defaultHideMessage
}

const confirmHideProduct = async () => {
  if (!productToHide.value) return
  hidingProduct.value = true
  try {
    const hideFlag = !productToHide.value.is_marketplace_hidden
    const reasonToSend = hideFlag ? hideReason.value : ''
    await adminApi.hideProduct(productToHide.value.id, {
      hide: hideFlag,
      reason: reasonToSend
    })
    await loadProducts()
    if (selectedProduct.value && selectedProduct.value.id === productToHide.value.id) {
      selectedProduct.value.is_marketplace_hidden = hideFlag
      selectedProduct.value.marketplace_hide_reason = reasonToSend
    }
    closeHideDialog()
  } catch (error) {
    console.error('Failed to update marketplace visibility:', error)
    alert('خطا در تغییر وضعیت نمایش محصول')
  } finally {
    hidingProduct.value = false
  }
}

const toggleProductStatus = async (product: any) => {
  try {
    await adminApi.updateProductStatus(product.id, !product.is_active)
    await loadProducts()
    await loadDashboardData()
  } catch (error) {
    console.error('Failed to toggle product status:', error)
    alert('خطا در تغییر وضعیت محصول')
  }
}

const deleteProduct = async (product: any) => {
  if (confirm(`آیا مطمئن هستید که می‌خواهید محصول "${product.name}" را حذف کنید؟`)) {
    try {
      await adminApi.deleteProduct(product.id)
      await loadProducts()
      await loadDashboardData()
    } catch (error) {
      console.error('Failed to delete product:', error)
      alert('خطا در حذف محصول')
    }
  }
}

const getRFQStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    pending: 'warning',
    confirmed: 'success',
    rejected: 'error',
    processing: 'info'
  }
  return colors[status] || 'grey'
}

const getRFQStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: 'در انتظار',
    confirmed: 'تأیید شده',
    rejected: 'رد شده',
    processing: 'در حال پردازش'
  }
  return texts[status] || status
}

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const formatPrice = (price: number) => {
  if (!price) return '0'
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

const viewRFQDetail = async (rfq: any) => {
  loadingRFQDetail.value = true
  try {
    // Fetch full details from API
    const detail = await adminApi.getRFQDetail(rfq.id)
    selectedRFQ.value = detail
    showRFQDetailDialog.value = true
  } catch (error) {
    console.error('Failed to load RFQ detail:', error)
    // Fallback to using the data we already have
    selectedRFQ.value = rfq
    showRFQDetailDialog.value = true
  } finally {
    loadingRFQDetail.value = false
  }
}

const viewImage = (imageUrl: string) => {
  // Open image in a new window or dialog
  window.open(imageUrl, '_blank')
}

const updateRFQStatus = async (rfq: any, newStatus: string) => {
  try {
    await adminApi.updateRFQStatus(rfq.id, newStatus)
    // Update the selected RFQ if dialog is open
    if (selectedRFQ.value && selectedRFQ.value.id === rfq.id) {
      selectedRFQ.value.status = newStatus
    }
    await loadRFQs()
    await loadDashboardData()
  } catch (error) {
    console.error('Failed to update RFQ status:', error)
  }
}

const handleNavigate = (view: string) => {
  activeView.value = view
  navigateTo({
    path: '/admin/dashboard',
    query: { view }
  })
}

watch(activeView, (newView) => {
  if (newView === 'dashboard') {
    loadDashboardData()
  } else if (newView === 'users') {
    loadUsers()
  } else if (newView === 'activities') {
    loadActivities()
  } else if (newView === 'blog') {
    loadBlogPosts()
  } else if (newView === 'rfqs') {
    loadRFQs()
  } else if (newView === 'products') {
    loadFilterData()
    loadProducts()
  } else if (newView === 'flags') {
    loadFlags()
  }
})

watch(() => route.query.view, (newView) => {
  if (typeof newView === 'string') {
    activeView.value = newView
  }
})

// Create Lead Methods
const loadLeadCategories = async () => {
  loadingLeadCategories.value = true
  try {
    const response = await categoryApi.getCategories()
    leadCategories.value = Array.isArray(response) ? response : response.results || []
  } catch (error) {
    console.error('Failed to load categories:', error)
  } finally {
    loadingLeadCategories.value = false
  }
}

const loadLeadProducts = async (categoryId?: number) => {
  loadingLeadProducts.value = true
  try {
    const params: any = {}
    if (categoryId) {
      params.category = categoryId
    }
    const response = await productApi.getProducts(params)
    leadProducts.value = Array.isArray(response) ? response : response.results || []
  } catch (error) {
    console.error('Failed to load products:', error)
  } finally {
    loadingLeadProducts.value = false
  }
}

const loadSuppliers = async () => {
  loadingSuppliers.value = true
  try {
    allSuppliers.value = await supplierApi.getSuppliers()
  } catch (error) {
    console.error('Failed to load suppliers:', error)
  } finally {
    loadingSuppliers.value = false
  }
}

const onCategoryChange = async (categoryId: number) => {
  if (categoryId) {
    await loadLeadProducts(categoryId)
    await findAutoMatchedSuppliers()
  } else {
    leadProducts.value = []
    autoMatchedSuppliers.value = []
  }
}

const onProductChange = async (productId: number | null) => {
  if (productId) {
    await findAutoMatchedSuppliers()
  } else {
    await findAutoMatchedSuppliers()
  }
}

const findAutoMatchedSuppliers = async () => {
  autoMatchedSuppliers.value = []
  selectedAutoSuppliers.value = []
  
  if (createLeadData.value.product_id) {
    // If product is selected, get supplier from product
    try {
      const product = leadProducts.value.find(p => p.id === createLeadData.value.product_id)
      if (product && product.supplier) {
        autoMatchedSuppliers.value = [product.supplier]
        selectedAutoSuppliers.value = [product.supplier.id]
      }
    } catch (error) {
      console.error('Failed to find supplier from product:', error)
    }
  } else if (createLeadData.value.category_id) {
    // If only category is selected, find all suppliers with products in this category
    try {
      const categoryProducts = await productApi.getProducts({ category: createLeadData.value.category_id })
      const productsList = Array.isArray(categoryProducts) ? categoryProducts : categoryProducts.results || []
      const suppliersMap = new Map()
      productsList.forEach((product: any) => {
        if (product.supplier && product.supplier.id) {
          suppliersMap.set(product.supplier.id, product.supplier)
        }
      })
      autoMatchedSuppliers.value = Array.from(suppliersMap.values())
      selectedAutoSuppliers.value = Array.from(suppliersMap.keys())
    } catch (error) {
      console.error('Failed to find suppliers from category:', error)
    }
  }
}

const getImagePreview = (file: File) => {
  return URL.createObjectURL(file)
}

const removeImage = (index: number) => {
  createLeadImages.value.splice(index, 1)
}

const closeCreateLeadDialog = () => {
  showCreateLeadDialog.value = false
  createLeadForm.value?.reset()
  createLeadData.value = {
    lead_source: '',
    category_id: null,
    product_id: null,
    first_name: '',
    last_name: '',
    company_name: '',
    phone_number: '',
    email: '',
    unique_needs: '',
    supplier_ids: []
  }
  createLeadImages.value = []
  autoMatchedSuppliers.value = []
  selectedAutoSuppliers.value = []
}

const submitLead = async () => {
  if (!createLeadForm.value?.validate()) {
    return
  }

  submittingLead.value = true
  try {
    const formData = new FormData()
    
    // Add form fields
    formData.append('lead_source', createLeadData.value.lead_source)
    formData.append('category_id', String(createLeadData.value.category_id!))
    if (createLeadData.value.product_id) {
      formData.append('product_id', String(createLeadData.value.product_id))
    }
    formData.append('first_name', createLeadData.value.first_name)
    formData.append('last_name', createLeadData.value.last_name)
    formData.append('company_name', createLeadData.value.company_name)
    formData.append('phone_number', createLeadData.value.phone_number)
    if (createLeadData.value.email) {
      formData.append('email', createLeadData.value.email)
    }
    if (createLeadData.value.unique_needs) {
      formData.append('unique_needs', createLeadData.value.unique_needs)
    }
    
    // Combine auto-selected and manually selected suppliers
    const allSelectedSuppliers = [
      ...selectedAutoSuppliers.value,
      ...createLeadData.value.supplier_ids
    ].filter((id, index, self) => self.indexOf(id) === index) // Remove duplicates
    
    if (allSelectedSuppliers.length > 0) {
      allSelectedSuppliers.forEach(supplierId => {
        formData.append('supplier_ids', String(supplierId))
      })
    }
    
    // Add images
    createLeadImages.value.forEach((image, index) => {
      formData.append(`images`, image)
    })
    
    await adminApi.createRFQ(formData)
    
    // Show success message
    alert('لید با موفقیت ثبت شد')
    
    // Close dialog and reload RFQs
    closeCreateLeadDialog()
    await loadRFQs()
    await loadDashboardData()
  } catch (error: any) {
    console.error('Failed to create lead:', error)
    alert(`خطا در ثبت لید: ${error.message || 'خطای نامشخص'}`)
  } finally {
    submittingLead.value = false
  }
}

watch(showCreateLeadDialog, (isOpen) => {
  if (isOpen) {
    loadLeadCategories()
    loadSuppliers()
  }
})

onMounted(() => {
  if (activeView.value === 'dashboard') {
    loadDashboardData()
  } else if (activeView.value === 'users') {
    loadUsers()
  } else if (activeView.value === 'activities') {
    loadActivities()
  } else if (activeView.value === 'blog') {
    loadBlogPosts()
  } else if (activeView.value === 'rfqs') {
    loadRFQs()
  } else if (activeView.value === 'products') {
    loadFilterData()
    loadProducts()
  } else if (activeView.value === 'flags') {
    loadFlags()
  }
})
</script>

<style scoped>
.admin-dashboard-wrapper {
  min-height: 100vh;
  padding-top: 80px;
}

@media (max-width: 960px) {
  .admin-dashboard-wrapper {
    padding-top: 72px;
  }
}

@media (max-width: 600px) {
  .admin-dashboard-wrapper {
    padding-top: 72px;
  }
}

.stat-card {
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.image-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.image-card:hover {
  transform: scale(1.05);
}

.cursor-pointer {
  cursor: pointer;
}
</style>

