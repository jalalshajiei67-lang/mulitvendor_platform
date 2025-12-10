<template>
  <v-container fluid dir="rtl" class="seller-dashboard">
    <!-- Main Content Tabs -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="0" class="bg-transparent">
          <!-- Responsive Navigation Tabs -->
          <v-card elevation="2" rounded="xl" class="mb-6 overflow-visible">
            <v-tabs
              v-model="tab"
              bg-color="surface"
              color="primary"
              align-tabs="start"
              class="border-b"
              height="64"
              show-arrows
            >
              <!-- Visible Tabs (Dynamic based on screen size) -->
              <v-tab
                v-for="item in visibleTabs"
                :key="item.value"
                :value="item.value"
                :data-tour="item.tour"
                class="text-body-1 font-weight-medium"
              >
                <!-- Badge handling for 'chats' -->
                <template v-if="item.value === 'chats'">
                  <v-badge
                    v-if="unreadChatsCount > 0"
                    :content="unreadChatsCount"
                    color="error"
                    offset-x="-5"
                    offset-y="5"
                  >
                    <v-icon start>mdi-chat-processing-outline</v-icon>
                  </v-badge>
                  <v-icon v-else start>mdi-chat-outline</v-icon>
                </template>
                
                <!-- Standard Icon -->
                <v-icon v-else start>{{ item.icon }}</v-icon>
                {{ item.label }}
              </v-tab>

              <!-- 3-Dot Overflow Menu (Visible only on Mobile) -->
              <v-menu v-if="overflowTabs.length > 0">
                <template v-slot:activator="{ props }">
                  <v-btn
                    variant="text"
                    class="align-self-center ms-2"
                    icon="mdi-dots-vertical"
                    v-bind="props"
                    color="medium-emphasis"
                  ></v-btn>
                </template>
                <v-list elevation="3" rounded="lg" density="comfortable">
                  <v-list-item
                    v-for="item in overflowTabs"
                    :key="item.value"
                    :value="item.value"
                    @click="tab = item.value"
                    :active="tab === item.value"
                    color="primary"
                  >
                    <template v-slot:prepend>
                      <!-- Badge handling inside menu -->
                      <v-badge
                        v-if="item.value === 'chats' && unreadChatsCount > 0"
                        dot
                        color="error"
                        location="bottom start"
                        offset-x="2"
                        offset-y="2"
                      >
                        <v-icon>{{ item.icon }}</v-icon>
                      </v-badge>
                      <v-icon v-else>{{ item.icon }}</v-icon>
                    </template>
                    <v-list-item-title>{{ item.label }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-tabs>
          </v-card>

          <v-window v-model="tab">
            <!-- Home Tab -->
            <v-window-item value="home">
              <div class="py-2">
                <!-- Low score banner -->
                <LowScoreBanner
                  :status="lowScoreStatus"
                  :loading="lowScoreLoading"
                  @improve-profile="navigateTo('/seller/profile')"
                  @upgrade-premium="navigateTo('/pricing')"
                />

                <!-- Endorsement CTA -->
                <EndorsementCTA />
                
                <!-- Hero Section: Benefits & Rank or Setup Progress -->
                <v-row class="mb-4">
                  <v-col cols="12">
                    <BenefitsRankWidget v-if="!showSetupWidget" :loading="gamificationStore.loading" />
                    <SetupProgressWidget
                      v-else
                      :progress-percent="Math.min(100, Math.round((tourProgress / tourTotalSteps) * 100))"
                      :steps-completed="tourProgress"
                      :total-steps="tourTotalSteps"
                      @resume="resumeTour"
                    />
                  </v-col>
                </v-row>

                <TierNudge
                  :tier="gamificationStore.userTier"
                  :engagement="gamificationStore.engagement"
                  :is-premium="lowScoreStatus.is_premium"
                  class="mb-4"
                  @cta-primary="navigateTo('/seller/profile')"
                  @cta-secondary="navigateTo('/seller/profile')"
                />

                <!-- Quick Stats Row (Smaller, Secondary) -->
                <v-row class="mb-6">
                  <v-col cols="6" sm="4" md="3">
                    <v-card
                      class="h-100"
                      elevation="0"
                      rounded="lg"
                      color="primary"
                      variant="tonal"
                      :loading="loading"
                    >
                      <v-card-text class="pa-4">
                        <div class="d-flex align-center justify-space-between">
                          <div>
                            <div class="text-caption mb-1">محصولات</div>
                            <div class="text-h5 font-weight-bold">
                              {{ dashboardData.total_products || 0 }}
                            </div>
                            <div class="text-caption opacity-70">
                              {{ dashboardData.active_products || 0 }} فعال
                            </div>
                          </div>
                          <v-icon size="32" color="primary">mdi-package-variant</v-icon>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="6" sm="4" md="3">
                    <v-card
                      class="h-100"
                      elevation="0"
                      rounded="lg"
                      color="info"
                      variant="tonal"
                      :loading="loading"
                    >
                      <v-card-text class="pa-4">
                        <div class="d-flex align-center justify-space-between">
                          <div>
                            <div class="text-caption mb-1">سفارشات</div>
                            <div class="text-h5 font-weight-bold">
                              {{ dashboardData.total_orders || 0 }}
                            </div>
                            <div class="text-caption opacity-70">
                              کل سفارشات
                            </div>
                          </div>
                          <v-icon size="32" color="info">mdi-shopping-outline</v-icon>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="6" sm="4" md="3">
                    <v-card
                      class="h-100"
                      elevation="0"
                      rounded="lg"
                      color="success"
                      variant="tonal"
                      :loading="loading"
                    >
                      <v-card-text class="pa-4">
                        <div class="d-flex align-center justify-space-between">
                          <div>
                            <div class="text-caption mb-1">بازدیدها</div>
                            <div class="text-h5 font-weight-bold">
                              {{ dashboardData.product_views || 0 }}
                            </div>
                            <div class="text-caption opacity-70">
                              بازدید محصولات
                            </div>
                          </div>
                          <v-icon size="32" color="success">mdi-eye-outline</v-icon>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="6" sm="4" md="3">
                    <v-card
                      class="h-100"
                      elevation="0"
                      rounded="lg"
                      color="warning"
                      variant="tonal"
                      :loading="loading"
                    >
                      <v-card-text class="pa-4">
                        <div class="d-flex align-center justify-space-between">
                          <div>
                            <div class="text-caption mb-1">نظرات</div>
                            <div class="text-h5 font-weight-bold">
                              {{ dashboardData.total_reviews || 0 }}
                            </div>
                            <div class="text-caption opacity-70">
                              کل نظرات
                            </div>
                          </div>
                          <v-icon size="32" color="warning">mdi-star-outline</v-icon>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>

                <!-- Gamification Status Section -->
                <v-row class="mb-6">
                  <v-col cols="12" md="6">
                    <v-card elevation="2" rounded="xl" class="pa-4">
                      <v-card-title class="text-h6 font-weight-bold mb-4">
                        <v-icon start color="primary">mdi-chart-line</v-icon>
                        امتیاز بخش‌ها
                      </v-card-title>
                      <v-card-text>
                        <div v-if="gamificationStore.scores.product" class="mb-4">
                          <div class="d-flex justify-space-between align-center mb-2">
                            <span class="text-body-1 font-weight-medium">محصول</span>
                            <v-chip
                              :color="getScoreColor(gamificationStore.scores.product.score)"
                              size="small"
                              variant="flat"
                            >
                              {{ gamificationStore.scores.product.score }}%
                            </v-chip>
                          </div>
                          <v-progress-linear
                            :model-value="gamificationStore.scores.product.score"
                            :color="getScoreColor(gamificationStore.scores.product.score)"
                            height="8"
                            rounded
                          ></v-progress-linear>
                        </div>
                        <div v-if="gamificationStore.scores.profile" class="mb-4">
                          <div class="d-flex justify-space-between align-center mb-2">
                            <span class="text-body-1 font-weight-medium">پروفایل</span>
                            <v-chip
                              :color="getScoreColor(gamificationStore.scores.profile.score)"
                              size="small"
                              variant="flat"
                            >
                              {{ gamificationStore.scores.profile.score }}%
                            </v-chip>
                          </div>
                          <v-progress-linear
                            :model-value="gamificationStore.scores.profile.score"
                            :color="getScoreColor(gamificationStore.scores.profile.score)"
                            height="8"
                            rounded
                          ></v-progress-linear>
                        </div>
                        <div v-if="gamificationStore.scores.miniWebsite" class="mb-4">
                          <div class="d-flex justify-space-between align-center mb-2">
                            <span class="text-body-1 font-weight-medium">فروشگاه</span>
                            <v-chip
                              :color="getScoreColor(gamificationStore.scores.miniWebsite.score)"
                              size="small"
                              variant="flat"
                            >
                              {{ gamificationStore.scores.miniWebsite.score }}%
                            </v-chip>
                          </div>
                          <v-progress-linear
                            :model-value="gamificationStore.scores.miniWebsite.score"
                            :color="getScoreColor(gamificationStore.scores.miniWebsite.score)"
                            height="8"
                            rounded
                          ></v-progress-linear>
                        </div>
                        <v-btn
                          block
                          color="primary"
                          variant="tonal"
                          @click="tab = 'miniwebsite'"
                          class="mt-2"
                        >
                          بهبود امتیازها
                          <v-icon end>mdi-arrow-left</v-icon>
                        </v-btn>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-card elevation="2" rounded="xl" class="pa-4">
                      <v-card-title class="text-h6 font-weight-bold mb-4">
                        <v-icon start color="primary">mdi-lightning-bolt</v-icon>
                        اقدامات سریع
                      </v-card-title>
                      <v-card-text>
                        <v-list density="comfortable">
                          <v-list-item
                            @click="tab = 'miniwebsite'; miniWebsiteTab = 'products'; openProductForm()"
                            class="mb-2 rounded-lg"
                            data-tour="add-product-btn"
                          >
                            <template v-slot:prepend>
                              <v-avatar color="primary" variant="tonal" size="40">
                                <v-icon>mdi-plus</v-icon>
                              </v-avatar>
                            </template>
                            <v-list-item-title class="font-weight-medium">افزودن محصول جدید</v-list-item-title>
                            <v-list-item-subtitle>امتیاز +20</v-list-item-subtitle>
                          </v-list-item>
                          <v-list-item
                            @click="tab = 'miniwebsite'; miniWebsiteTab = 'profile'"
                            class="mb-2 rounded-lg"
                          >
                            <template v-slot:prepend>
                              <v-avatar color="secondary" variant="tonal" size="40">
                                <v-icon>mdi-account-edit</v-icon>
                              </v-avatar>
                            </template>
                            <v-list-item-title class="font-weight-medium">تکمیل پروفایل</v-list-item-title>
                            <v-list-item-subtitle>افزایش امتیاز پروفایل</v-list-item-subtitle>
                          </v-list-item>
                          <v-list-item
                            @click="tab = 'miniwebsite'; miniWebsiteTab = 'settings'"
                            class="mb-2 rounded-lg"
                          >
                            <template v-slot:prepend>
                              <v-avatar color="success" variant="tonal" size="40">
                                <v-icon>mdi-web</v-icon>
                              </v-avatar>
                            </template>
                            <v-list-item-title class="font-weight-medium">بهبود فروشگاه</v-list-item-title>
                            <v-list-item-subtitle>افزایش امتیاز فروشگاه</v-list-item-subtitle>
                          </v-list-item>
                        </v-list>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>

                <!-- Additional Gamification Widgets -->
                <v-row class="mb-6">
                  <v-col cols="12" md="4">
                    <EngagementWidget
                      :engagement="gamificationStore.engagement"
                      :loading="gamificationStore.loading"
                      @cta="openProductForm"
                    />
                  </v-col>
                  <v-col cols="12" md="4">
                    <BadgeDisplay
                      :badges="gamificationStore.badges.slice(0, 4)"
                      title="نشان‌های پیش رو"
                    />
                  </v-col>
                  <v-col cols="12" md="4">
                    <LeaderboardWidget 
                      :entries="gamificationStore.leaderboard" 
                      title="برترین‌های این هفته"
                    />
                  </v-col>
                </v-row>

                <!-- Recent Orders Section -->
                <v-row class="mb-4" v-if="recentOrders.length > 0">
                  <v-col cols="12">
                    <v-card elevation="2" rounded="xl" class="pa-2">
                      <v-card-title class="d-flex align-center justify-space-between px-4 pt-4">
                        <span class="text-h6 font-weight-bold">سفارشات اخیر</span>
                        <v-btn
                          variant="text"
                          color="primary"
                          class="px-2"
                          @click="tab = 'orders'"
                        >
                          مشاهده همه
                          <v-icon end>mdi-arrow-left</v-icon>
                        </v-btn>
                      </v-card-title>
                      <v-card-text>
                        <v-list lines="two">
                          <v-list-item
                            v-for="order in recentOrders"
                            :key="order.id"
                            class="rounded-lg mb-2"
                            rounded="lg"
                          >
                            <template v-slot:prepend>
                              <v-avatar color="primary" variant="tonal" rounded="lg">
                                <v-icon>mdi-basket-outline</v-icon>
                              </v-avatar>
                            </template>
                            
                            <v-list-item-title class="font-weight-bold">
                              سفارش {{ order.order_number }}
                            </v-list-item-title>
                            <v-list-item-subtitle>
                              {{ order.buyer_username || 'کاربر مهمان' }} • <span class="text-high-emphasis">{{ formatPrice(order.total_amount) }}</span>
                            </v-list-item-subtitle>

                            <template v-slot:append>
                              <v-chip
                                :color="getStatusColor(order.status)"
                                size="small"
                                variant="tonal"
                                label
                              >
                                {{ getStatusLabel(order.status) }}
                              </v-chip>
                            </template>
                          </v-list-item>
                        </v-list>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </div>
            </v-window-item>


            <!-- Orders Tab -->
            <v-window-item value="orders">
              <v-card elevation="2" rounded="xl" class="pa-4 mt-4">
                <div class="d-flex align-center justify-space-between mb-6">
                  <h3 class="text-h6 font-weight-bold">سفارشات</h3>
                  <v-btn
                    variant="text"
                    color="primary"
                    prepend-icon="mdi-refresh"
                    @click="loadOrders"
                    :loading="loadingOrders"
                  >
                    به‌روزرسانی
                  </v-btn>
                </div>
                
                <v-progress-linear v-if="loadingOrders" indeterminate color="primary" class="mb-4"></v-progress-linear>
                
                <v-data-table
                  v-if="!loadingOrders && orders.length > 0"
                  :headers="orderHeaders"
                  :items="orders"
                  :items-per-page="10"
                  class="elevation-0"
                  no-data-text="سفارشی یافت نشد"
                >
                  <template v-slot:item.order_number="{ item }">
                    <span class="font-weight-bold">{{ item.order_number }}</span>
                  </template>
                  <template v-slot:item.buyer_username="{ item }">
                    {{ item.buyer_username || 'کاربر مهمان' }}
                  </template>
                  <template v-slot:item.total_amount="{ item }">
                    <span class="font-weight-bold text-primary">{{ formatPrice(item.total_amount) }} تومان</span>
                  </template>
                  <template v-slot:item.status="{ item }">
                    <v-chip
                      :color="getStatusColor(item.status)"
                      size="small"
                      variant="tonal"
                      label
                    >
                      {{ getStatusLabel(item.status) }}
                    </v-chip>
                  </template>
                  <template v-slot:item.created_at="{ item }">
                    {{ formatDate(item.created_at) }}
                  </template>
                </v-data-table>
                
                <v-card v-else-if="!loadingOrders && orders.length === 0" elevation="1" class="text-center pa-8">
                  <v-icon size="80" color="grey-lighten-1">mdi-shopping-outline</v-icon>
                  <p class="text-h6 mt-4 mb-2">هنوز سفارشی دریافت نکرده‌اید</p>
                  <p class="text-body-2 text-grey">سفارشات شما در اینجا نمایش داده می‌شوند</p>
                </v-card>
              </v-card>
            </v-window-item>

            <!-- Reviews Tab -->
            <v-window-item value="reviews">
              <v-card elevation="2" rounded="xl" class="pa-4 mt-4">
                <div class="d-flex align-center justify-space-between mb-6">
                  <h3 class="text-h6 font-weight-bold">نظرات محصولات</h3>
                  <v-btn
                    variant="text"
                    color="primary"
                    prepend-icon="mdi-refresh"
                    @click="loadReviews"
                    :loading="loadingReviews"
                  >
                    به‌روزرسانی
                  </v-btn>
                </div>
                
                <v-progress-linear v-if="loadingReviews" indeterminate color="primary" class="mb-4"></v-progress-linear>
                
                <v-list v-if="!loadingReviews && reviews.length > 0" lines="three">
                  <v-list-item
                    v-for="review in reviews"
                    :key="review.id"
                    class="mb-4 rounded-lg border"
                  >
                    <template v-slot:prepend>
                      <v-avatar color="primary" variant="tonal" size="48">
                        <v-icon>mdi-star</v-icon>
                      </v-avatar>
                    </template>
                    
                    <v-list-item-title class="font-weight-bold mb-2">
                      {{ review.product?.name || 'محصول' }}
                    </v-list-item-title>
                    
                    <v-list-item-subtitle>
                      <div class="d-flex align-center gap-2 mb-2">
                        <v-rating
                          :model-value="review.rating"
                          readonly
                          size="small"
                          color="warning"
                          density="compact"
                        ></v-rating>
                        <span class="text-caption text-medium-emphasis">
                          توسط {{ review.author?.username || 'کاربر' }}
                        </span>
                      </div>
                      <p class="text-body-2 mt-2">{{ review.comment }}</p>
                      <span class="text-caption text-disabled">{{ formatDate(review.created_at) }}</span>
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
                
                <v-card v-else-if="!loadingReviews && reviews.length === 0" elevation="1" class="text-center pa-8">
                  <v-icon size="80" color="grey-lighten-1">mdi-star-outline</v-icon>
                  <p class="text-h6 mt-4 mb-2">هنوز نظری دریافت نکرده‌اید</p>
                  <p class="text-body-2 text-grey">نظرات مشتریان در اینجا نمایش داده می‌شوند</p>
                </v-card>
              </v-card>
            </v-window-item>

            <!-- Invite & Earn Tab -->
            <v-window-item value="invite">
              <v-card elevation="2" rounded="xl" class="pa-6 mt-4 text-center">
                <v-icon size="56" color="primary" class="mb-4">mdi-share-variant</v-icon>
                <h3 class="text-h6 font-weight-bold mb-2">دعوت و امتیاز</h3>
                <p class="text-body-2 text-medium-emphasis mb-6">
                  دوستان خود را دعوت کنید و برای هر ثبت‌نام موفق ۱۰۰ امتیاز دریافت کنید.
                </p>
                <v-btn
                  color="primary"
                  size="large"
                  rounded="lg"
                  prepend-icon="mdi-open-in-new"
                  @click="navigateTo('/vendor/invite')"
                >
                  رفتن به صفحه دعوت
                </v-btn>
              </v-card>
            </v-window-item>

            <!-- Miniwebsite Tab -->
            <v-window-item value="miniwebsite">
              <div class="py-4">
                <v-tabs v-model="miniWebsiteTab" bg-color="surface" class="mb-4">
                  <v-tab value="profile">پروفایل</v-tab>
                  <v-tab value="products">محصولات من</v-tab>
                  <v-tab value="settings">تنظیمات فروشگاه</v-tab>
                  <v-tab value="portfolio">نمونه کارها</v-tab>
                  <v-tab value="team">تیم ما</v-tab>
                  <v-tab value="messages">پیام‌ها و تماس‌ها</v-tab>
                </v-tabs>
                
                <v-window v-model="miniWebsiteTab">
                  <v-window-item value="profile">
                    <v-card elevation="2" rounded="xl" class="pa-6 mt-4">
                      <div class="d-flex align-center mb-6">
                        <v-avatar color="primary" variant="tonal" size="48" class="ml-4 rounded-lg">
                          <v-icon color="primary">mdi-account-cog</v-icon>
                        </v-avatar>
                        <h3 class="text-h5 font-weight-bold">اطلاعات شخصی</h3>
                      </div>
                      
                      <v-row>
                        <v-col cols="12" lg="4">
                          <FormQualityScore
                            title="امتیاز پروفایل"
                            caption="تکمیل پروفایل = اعتماد بیشتر خریدار"
                            :score="profileScore"
                            :metrics="profileMetrics"
                            :tips="profileTips"
                          />
                        </v-col>
                        <v-col cols="12" lg="8">
                          <v-form ref="profileForm" @submit.prevent="updateProfile">
                            <v-row>
                              <v-col cols="12" md="6">
                                <v-text-field
                                  v-model="profileData.first_name"
                                  label="نام"
                                  variant="outlined"
                                  density="comfortable"
                                  color="primary"
                                ></v-text-field>
                              </v-col>
                              <v-col cols="12" md="6">
                                <v-text-field
                                  v-model="profileData.last_name"
                                  label="نام خانوادگی"
                                  variant="outlined"
                                  density="comfortable"
                                  color="primary"
                                ></v-text-field>
                              </v-col>
                            </v-row>
                            <v-row>
                              <v-col cols="12" md="6">
                                <v-text-field
                                  v-model="profileData.email"
                                  label="ایمیل"
                                  prepend-inner-icon="mdi-email-outline"
                                  type="email"
                                  variant="outlined"
                                  density="comfortable"
                                  color="primary"
                                ></v-text-field>
                              </v-col>
                              <v-col cols="12" md="6">
                                <v-text-field
                                  v-model="profileData.phone"
                                  label="تلفن"
                                  prepend-inner-icon="mdi-phone-outline"
                                  variant="outlined"
                                  density="comfortable"
                                  color="primary"
                                ></v-text-field>
                              </v-col>
                            </v-row>
                            <div class="d-flex justify-end mt-4">
                              <v-btn
                                color="primary"
                                type="submit"
                                :loading="saving"
                                size="large"
                                elevation="2"
                                rounded="lg"
                              >
                                <v-icon start>mdi-content-save-outline</v-icon>
                                ذخیره تغییرات
                              </v-btn>
                            </div>
                          </v-form>
                        </v-col>
                      </v-row>
                    </v-card>
                  </v-window-item>
                  
                  <v-window-item value="products">
                    <v-card elevation="2" rounded="xl" class="pa-4 mt-4">
                      <div v-if="showProductForm">
                        <div class="d-flex align-center mb-6 border-b pb-4">
                          <v-btn icon="mdi-arrow-right" variant="text" @click="closeProductForm" class="ml-2"></v-btn>
                          <h3 class="text-h6 font-weight-bold text-primary">
                            {{ editingProduct ? 'ویرایش محصول' : 'افزودن محصول جدید' }}
                          </h3>
                        </div>
                        <SupplierProductForm
                          :product-data="editingProduct"
                          :edit-mode="!!editingProduct"
                          @saved="onProductSaved"
                          @cancel="closeProductForm"
                        />
                      </div>
                      <SupplierProductList
                        v-else
                        ref="productListRef"
                        @add-product="openProductForm"
                        @edit-product="openEditProductForm"
                      />
                    </v-card>
                  </v-window-item>
                  
                  <v-window-item value="settings">
                    <MiniWebsiteSettings />
                  </v-window-item>
                  <v-window-item value="portfolio">
                    <PortfolioManager />
                  </v-window-item>
                  <v-window-item value="team">
                    <TeamManager />
                  </v-window-item>
                  <v-window-item value="messages">
                    <ContactMessagesInbox />
                  </v-window-item>
                </v-window>
              </div>
            </v-window-item>

            <!-- Chats Tab -->
            <v-window-item value="chats">
              <div class="py-4">
                <v-row>
                  <!-- Chat Queue -->
                  <v-col cols="12" md="4">
                    <v-card elevation="2" rounded="xl" height="650" class="d-flex flex-column">
                      <div class="pa-4 bg-grey-lighten-5 border-b">
                        <div class="d-flex justify-space-between align-center">
                          <span class="font-weight-bold text-primary">پیام‌ها</span>
                          <div class="d-flex align-center gap-2">
                            <v-btn
                              icon="mdi-refresh"
                              size="small"
                              variant="text"
                              @click="loadChatRooms"
                              :loading="loadingChats"
                            ></v-btn>
                            <v-chip
                              v-if="unreadChatsCount > 0"
                              size="small"
                              color="error"
                              variant="flat"
                            >
                              {{ unreadChatsCount }} جدید
                            </v-chip>
                          </div>
                        </div>
                      </div>
                      
                      <v-progress-linear v-if="loadingChats" indeterminate color="primary"></v-progress-linear>
                      
                      <v-list v-if="!loadingChats" class="flex-grow-1 overflow-y-auto py-0">
                        <v-list-item
                          v-for="room in chatRooms"
                          :key="room.room_id"
                          @click="selectChatRoom(room)"
                          :class="{
                            'bg-primary-lighten-5': selectedChatRoom?.room_id === room.room_id,
                            'bg-surface': selectedChatRoom?.room_id !== room.room_id
                          }"
                          lines="two"
                          class="py-3 border-b"
                        >
                          <template #prepend>
                            <v-badge dot color="success" location="bottom end" :model-value="room.unread_count > 0">
                                <v-avatar color="secondary" variant="tonal">
                                {{ getChatInitials(room.other_participant) }}
                                </v-avatar>
                            </v-badge>
                          </template>
                          
                          <v-list-item-title class="font-weight-bold text-body-2 mb-1">
                            {{ room.other_participant?.username || 'مشتری' }}
                          </v-list-item-title>
                          
                          <v-list-item-subtitle class="text-caption">
                            <span v-if="room.last_message?.content" :class="room.unread_count > 0 ? 'text-high-emphasis font-weight-medium' : ''">
                                {{ room.last_message.content.length > 35 ? room.last_message.content.substring(0, 35) + '...' : room.last_message.content }}
                            </span>
                            <span v-else class="text-disabled">هیچ پیامی وجود ندارد</span>
                          </v-list-item-subtitle>
                          
                          <template #append>
                            <div class="d-flex flex-column align-end">
                                <span class="text-caption text-disabled mb-1">{{ formatChatTime(room.updated_at) }}</span>
                                <v-chip v-if="room.product_name" size="x-small" variant="outlined" color="grey">
                                    {{ room.product_name }}
                                </v-chip>
                            </div>
                          </template>
                        </v-list-item>
                      </v-list>
                      
                      <v-card v-else-if="!loadingChats && chatRooms.length === 0" elevation="0" class="flex-grow-1 d-flex align-center justify-center">
                        <div class="text-center text-medium-emphasis">
                          <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-chat-outline</v-icon>
                          <div class="text-body-1">هیچ گفتگویی وجود ندارد</div>
                        </div>
                      </v-card>
                    </v-card>
                  </v-col>

                  <!-- Chat Conversation -->
                  <v-col cols="12" md="8">
                    <v-card v-if="selectedChatRoom" elevation="2" rounded="xl" height="650" class="d-flex flex-column">
                      <v-toolbar density="compact" color="surface" class="border-b pr-4">
                         <v-avatar size="32" color="secondary" variant="tonal" class="ml-3">
                            {{ getChatInitials(selectedChatRoom.other_participant) }}
                         </v-avatar>
                         <div class="d-flex flex-column">
                             <span class="font-weight-bold text-body-2">{{ selectedChatRoom.other_participant?.username || 'مشتری' }}</span>
                             <span v-if="selectedChatRoom.product_name" class="text-caption text-medium-emphasis">
                                درباره: {{ selectedChatRoom.product_name }}
                             </span>
                         </div>
                         <v-spacer></v-spacer>
                         <v-btn
                            v-if="selectedChatRoom.product_id"
                            variant="tonal"
                            color="primary"
                            size="small"
                            class="ml-2"
                            :to="`/products/${selectedChatRoom.product_id}`"
                            target="_blank"
                          >
                            مشاهده محصول
                            <v-icon end size="small">mdi-open-in-new</v-icon>
                         </v-btn>
                      </v-toolbar>
                      
                      <div class="flex-grow-1 position-relative">
                        <ChatRoom :room-id="selectedChatRoom.room_id" @back="() => {}" />
                      </div>
                    </v-card>
                    
                    <v-card v-else elevation="2" rounded="xl" height="650" class="d-flex align-center justify-center bg-grey-lighten-5">
                      <div class="text-center text-medium-emphasis">
                        <v-icon size="80" color="grey-lighten-1" class="mb-4">mdi-chat-processing-outline</v-icon>
                        <div class="text-h6">یک گفتگو را انتخاب کنید</div>
                      </div>
                    </v-card>
                  </v-col>
                </v-row>
              </div>
            </v-window-item>
          </v-window>
        </v-card>
      </v-col>
    </v-row>

    <!-- Dialogs and Extras -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000" location="top" rounded="pill">
      {{ snackbarMessage }}
    </v-snackbar>

    <OnboardingTour
      :force-show="forceTour"
      @tour-started="handleTourStarted"
      @tour-completed="handleTourCompleted"
      @tour-dismissed="handleTourDismissed"
    />
  </v-container>
</template>

<script setup lang="ts">
// Script remains exactly the same as provided, logic is preserved.
// Only template visual classes were updated.
import { ref, computed, onMounted, watch } from 'vue'
import { useDisplay } from 'vuetify'
import { useAuthStore } from '~/stores/auth'
import { useSellerApi } from '~/composables/useSellerApi'
import type { SellerOrder, SellerReview } from '~/composables/useSellerApi'
import MiniWebsiteSettings from '~/components/supplier/MiniWebsiteSettings.vue'
import PortfolioManager from '~/components/supplier/PortfolioManager.vue'
import TeamManager from '~/components/supplier/TeamManager.vue'
import ContactMessagesInbox from '~/components/supplier/ContactMessagesInbox.vue'
import SupplierProductForm from '~/components/supplier/ProductForm.vue'
import SupplierProductList from '~/components/supplier/ProductList.vue'
import ChatRoom from '~/components/chat/ChatRoom.vue'
import FormQualityScore from '~/components/gamification/FormQualityScore.vue'
import EngagementWidget from '~/components/gamification/EngagementWidget.vue'
import BadgeDisplay from '~/components/gamification/BadgeDisplay.vue'
import LeaderboardWidget from '~/components/gamification/LeaderboardWidget.vue'
import BenefitsRankWidget from '~/components/gamification/BenefitsRankWidget.vue'
import EndorsementCTA from '~/components/gamification/EndorsementCTA.vue'
import SetupProgressWidget from '~/components/gamification/SetupProgressWidget.vue'
import LowScoreBanner from '~/components/gamification/LowScoreBanner.vue'
import TierNudge from '~/components/gamification/TierNudge.vue'
import OnboardingTour from '~/components/supplier/OnboardingTour.vue'
import { useGamificationStore } from '~/stores/gamification'
import { useSupplierOnboarding } from '~/composables/useSupplierOnboarding'

definePageMeta({
  middleware: 'authenticated',
  layout: 'dashboard'
})

const authStore = useAuthStore()
const sellerApi = useSellerApi()
const gamificationStore = useGamificationStore()
const onboarding = useSupplierOnboarding()
const route = useRoute()
const { mdAndUp } = useDisplay()
const lowScoreStatus = computed(() => gamificationStore.lowScoreStatus)
const lowScoreLoading = computed(() => gamificationStore.loading)

// Define Menu Structure
const menuItems = [
  { value: 'home', label: 'صفحه اصلی', icon: 'mdi-home-outline', tour: 'welcome' },
  { value: 'miniwebsite', label: 'فروشگاه من', icon: 'mdi-web', tour: 'products-tab' },
  { value: 'chats', label: 'گفتگوها', icon: 'mdi-chat-processing-outline', tour: '' },
  { value: 'orders', label: 'سفارشات', icon: 'mdi-shopping-outline', tour: '' },
  { value: 'reviews', label: 'نظرات', icon: 'mdi-star-outline', tour: '' },
  { value: 'invite', label: 'دعوت و امتیاز', icon: 'mdi-share-variant', tour: '' },
]

// Computed Logic for "3-Dot" Breakpoint
const visibleTabs = computed(() => {
  // On Desktop (mdAndUp): Show all tabs
  if (mdAndUp.value) return menuItems
  
  // On Mobile/Tablet: Show only first 3, put rest in menu
  return menuItems.slice(0, 3)
})

const overflowTabs = computed(() => {
  if (mdAndUp.value) return []
  return menuItems.slice(3)
})

const tabQuery = computed(() => route.query.tab as string || 'home')
const tab = ref(tabQuery.value)
const miniWebsiteTab = ref('profile')
const showSetupWidget = ref(false)
const tourProgress = ref(0)
const tourTotalSteps = ref(onboarding.getInteractiveTourSteps().length || 1)
const forceTour = ref(false)

watch(() => route.query.tab, (newTab) => {
  if (newTab && typeof newTab === 'string') {
    tab.value = newTab
  }
})

// Watch tab changes to update URL
watch(tab, (newTab) => {
  if (newTab === 'invite') {
    return navigateTo('/vendor/invite')
  }
  navigateTo(`/seller/dashboard?tab=${newTab}`, { replace: true })
})

const dashboardData = ref({
  total_products: 0,
  active_products: 0,
  total_sales: '0',
  total_orders: 0,
  product_views: 0,
  total_reviews: 0
})

// Helper functions
const getUserFullName = () => {
  const user = authStore.user
  if (!user) return 'کاربر'
  const firstName = user.first_name || ''
  const lastName = user.last_name || ''
  if (firstName || lastName) {
    return `${firstName} ${lastName}`.trim() || user.username || 'کاربر'
  }
  return user.username || 'کاربر'
}

const formatPrice = (price: string | number) => {
  if (!price) return '0'
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  if (isNaN(numPrice)) return '0'
  return new Intl.NumberFormat('fa-IR').format(numPrice)
}

const getScoreColor = (score: number) => {
  if (score >= 70) return 'success'
  if (score >= 40) return 'warning'
  return 'error'
}

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    pending: 'warning',
    confirmed: 'info',
    processing: 'primary',
    shipped: 'pink',
    delivered: 'success',
    cancelled: 'error',
    rejected: 'error',
    completed: 'success'
  }
  return colors[status] || 'grey'
}

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    pending: 'در انتظار',
    confirmed: 'تایید شده',
    processing: 'در حال پردازش',
    shipped: 'ارسال شده',
    delivered: 'تحویل داده شده',
    cancelled: 'لغو شده',
    rejected: 'رد شده',
    completed: 'تکمیل شده'
  }
  return labels[status] || status
}

const getChatInitials = (user: any) => {
  if (!user) return '?'
  const username = user.username || user.first_name || 'U'
  return username.charAt(0).toUpperCase()
}

const formatChatTime = (timestamp: string) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return 'الان'
  if (minutes < 60) return `${minutes} دقیقه پیش`
  if (hours < 24) return `${hours} ساعت پیش`
  if (days < 7) return `${days} روز پیش`
  
  return date.toLocaleDateString('fa-IR')
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

const openProductForm = () => {
  showProductForm.value = true
  editingProduct.value = null
}

const closeProductForm = () => {
  showProductForm.value = false
  editingProduct.value = null
}

const onProductSaved = () => {
  closeProductForm()
  if (productListRef.value && typeof productListRef.value.loadProducts === 'function') {
    productListRef.value.loadProducts()
  }
  loadDashboardData()
  // Refresh gamification state after product save
  gamificationStore.hydrate().catch(() => {})
  showSnackbar('محصول با موفقیت ذخیره شد', 'success')
}

const openEditProductForm = (product: any) => {
  editingProduct.value = product
  showProductForm.value = true
}

const selectChatRoom = (room: any) => {
  selectedChatRoom.value = room
}

const handleTourStarted = () => {
  refreshTourState()
}

const handleTourCompleted = () => {
  refreshTourState()
}

const handleTourDismissed = () => {
  refreshTourState()
}

const TOUR_COMPLETED_KEY = 'supplier_tour_completed'
const TOUR_DISMISSED_KEY = 'supplier_tour_dismissed'

const tourCompleted = () => {
  if (typeof window === 'undefined') return false
  return localStorage.getItem(TOUR_COMPLETED_KEY) === 'true'
}

const tourDismissed = () => {
  if (typeof window === 'undefined') return false
  return localStorage.getItem(TOUR_DISMISSED_KEY) === 'true'
}

const refreshTourState = () => {
  if (typeof window === 'undefined') return
  tourProgress.value = onboarding.getTourProgress()
  showSetupWidget.value = !tourCompleted() && (tourProgress.value > 0 || tourDismissed() || onboarding.shouldShowTour())
}

const resumeTour = () => {
  onboarding.startTour(
    () => {
      refreshTourState()
    },
    () => {
      refreshTourState()
    }
  )
}

const updateProfile = async () => {
  saving.value = true
  try {
    await authStore.updateProfile(profileData.value)
    showSnackbar('پروفایل با موفقیت به‌روزرسانی شد', 'success')
    // Refresh user data
    await authStore.fetchCurrentUser()
    // Update profile data from store
    loadProfileData()
    // Calculate profile score
    calculateProfileScore()
    // Award profile section and refresh gamification
    try {
      await useApiFetch('gamification/award-section/', {
        method: 'POST',
        body: { section: 'profile' }
      })
      await gamificationStore.hydrate()
    } catch (e) {
      console.warn('Failed to award profile section', e)
    }
  } catch (error: any) {
    console.error('Failed to update profile:', error)
    showSnackbar(error?.message || 'خطا در به‌روزرسانی پروفایل', 'error')
  } finally {
    saving.value = false
  }
}

const showSnackbar = (message: string, color = 'success') => {
  snackbarMessage.value = message
  snackbarColor.value = color
  snackbar.value = true
}

const orders = ref<SellerOrder[]>([])
const reviews = ref<SellerReview[]>([])
const recentOrders = ref<any[]>([]) 
const chatRooms = ref<any[]>([])
const selectedChatRoom = ref<any>(null)
const unreadChatsCount = ref(0)
const activeTodayCount = ref(0)
const profileScore = ref(0)
const profileMetrics = ref([])
const profileTips = ref([])
const profileData = ref({ first_name: '', last_name: '', email: '', phone: '' })
const loading = ref(false)
const loadingOrders = ref(false)
const loadingReviews = ref(false)
const loadingChats = ref(false)
const saving = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')
const showProductForm = ref(false)
const editingProduct = ref<any>(null)
const productListRef = ref<any>(null)
const orderHeaders = ref([
  { title: 'شماره سفارش', key: 'order_number', align: 'start' },
  { title: 'خریدار', key: 'buyer_username', align: 'start' },
  { title: 'مبلغ', key: 'total_amount', align: 'start' },
  { title: 'وضعیت', key: 'status', align: 'start' },
  { title: 'تاریخ', key: 'created_at', align: 'start' }
])

const reviewHeaders = ref([
  { title: 'محصول', key: 'product.name', align: 'start' },
  { title: 'امتیاز', key: 'rating', align: 'start' },
  { title: 'نظر', key: 'comment', align: 'start' },
  { title: 'تاریخ', key: 'created_at', align: 'start' }
])

// Data loading functions
const loadDashboardData = async () => {
  loading.value = true
  try {
    const data = await sellerApi.getSellerDashboard()
    dashboardData.value = {
      total_products: data.total_products || 0,
      active_products: data.active_products || 0,
      total_sales: String(data.total_sales || '0'),
      total_orders: data.total_orders || 0,
      product_views: data.product_views || 0,
      total_reviews: data.total_reviews || 0
    }
    // Set recent orders from dashboard data
    if (data.recent_orders && Array.isArray(data.recent_orders)) {
      recentOrders.value = data.recent_orders
    }
  } catch (error: any) {
    console.error('Failed to load dashboard data:', error)
    showSnackbar('خطا در بارگذاری اطلاعات داشبورد', 'error')
  } finally {
    loading.value = false
    forceTour.value = (dashboardData.value.total_products || 0) === 0 && !tourCompleted()
    refreshTourState()
  }
}

const loadOrders = async () => {
  loadingOrders.value = true
  try {
    const data = await sellerApi.getSellerOrders()
    orders.value = Array.isArray(data) ? data : []
  } catch (error: any) {
    console.error('Failed to load orders:', error)
    showSnackbar('خطا در بارگذاری سفارشات', 'error')
  } finally {
    loadingOrders.value = false
  }
}

const loadReviews = async () => {
  loadingReviews.value = true
  try {
    const data = await sellerApi.getSellerReviews()
    reviews.value = Array.isArray(data) ? data : []
  } catch (error: any) {
    console.error('Failed to load reviews:', error)
    showSnackbar('خطا در بارگذاری نظرات', 'error')
  } finally {
    loadingReviews.value = false
  }
}

const loadChatRooms = async () => {
  loadingChats.value = true
  try {
    const data = await useApiFetch<any[]>('chat/vendor/rooms/')
    chatRooms.value = Array.isArray(data) ? data : []
    // Calculate unread count
    unreadChatsCount.value = chatRooms.value.reduce((sum, room) => sum + (room.unread_count || 0), 0)
  } catch (error: any) {
    console.error('Failed to load chat rooms:', error)
    showSnackbar('خطا در بارگذاری گفتگوها', 'error')
  } finally {
    loadingChats.value = false
  }
}

const loadProfileData = () => {
  const user = authStore.user
  if (user) {
    profileData.value = {
      first_name: user.first_name || '',
      last_name: user.last_name || '',
      email: user.email || '',
      phone: user.profile?.phone || ''
    }
  }
}

const calculateProfileScore = () => {
  const user = authStore.user
  if (!user) {
    profileScore.value = 0
    profileMetrics.value = []
    profileTips.value = []
    return
  }

  let score = 0
  const metrics: any[] = []
  const tips: string[] = []

  // Check first name (25 points)
  if (user.first_name) {
    score += 25
    metrics.push({ label: 'نام', completed: true })
  } else {
    metrics.push({ label: 'نام', completed: false })
    tips.push('نام خود را تکمیل کنید')
  }

  // Check last name (25 points)
  if (user.last_name) {
    score += 25
    metrics.push({ label: 'نام خانوادگی', completed: true })
  } else {
    metrics.push({ label: 'نام خانوادگی', completed: false })
    tips.push('نام خانوادگی خود را تکمیل کنید')
  }

  // Check email (25 points)
  if (user.email) {
    score += 25
    metrics.push({ label: 'ایمیل', completed: true })
  } else {
    metrics.push({ label: 'ایمیل', completed: false })
    tips.push('ایمیل خود را تکمیل کنید')
  }

  // Check phone (25 points)
  if (user.profile?.phone) {
    score += 25
    metrics.push({ label: 'تلفن', completed: true })
  } else {
    metrics.push({ label: 'تلفن', completed: false })
    tips.push('شماره تلفن خود را تکمیل کنید')
  }

  profileScore.value = score
  profileMetrics.value = metrics
  profileTips.value = tips
}

// Watch tab changes to load data when needed
watch(tab, async (newTab) => {
  if (newTab === 'orders' && orders.value.length === 0 && !loadingOrders.value) {
    await loadOrders()
  } else if (newTab === 'reviews' && reviews.value.length === 0 && !loadingReviews.value) {
    await loadReviews()
  } else if (newTab === 'chats' && chatRooms.value.length === 0 && !loadingChats.value) {
    await loadChatRooms()
  }
})

// Gamification: Hydrate store on mount
onMounted(async () => {
  try {
    await gamificationStore.hydrate()
  } catch (error) {
    console.warn('Failed to load gamification data', error)
  }
  
  // Load initial data
  await Promise.all([
    loadDashboardData(),
    loadProfileData()
  ])
  
  // Calculate profile score after loading profile data
  calculateProfileScore()
  
  // Load chat rooms if on chats tab
  if (tab.value === 'chats') {
    await loadChatRooms()
  }
})

// Gamification: Sync profile score with store
watch(profileScore, (score) => {
  if (score > 0) {
    gamificationStore.updateLocalScore('profile', {
      title: 'profile',
      score,
      metrics: profileMetrics.value,
      tips: profileTips.value
    })
  }
}, { immediate: true })
</script>

<style scoped>
.seller-dashboard {
  padding-top: 96px !important;
  padding-bottom: 32px;
}

.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.stat-card { transition: transform 0.2s; }
.stat-card:hover { transform: translateY(-2px); }

/* Responsive spacing adjustments */
@media (max-width: 960px) {
  .seller-dashboard {
    padding-top: 88px !important;
  }
}

@media (max-width: 600px) {
  .seller-dashboard {
    padding-top: 80px !important;
    padding-bottom: 24px;
  }
}
</style>

