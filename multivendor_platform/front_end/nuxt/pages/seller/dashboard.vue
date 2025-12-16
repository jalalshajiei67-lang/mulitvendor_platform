<template>
  <v-container fluid dir="rtl" class="seller-dashboard">
    <!-- Main Content -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="0" class="bg-transparent">
          <v-window v-model="tab">
            <!-- Home Tab -->
            <v-window-item value="home">
              <div class="py-2">
                <!-- NEW: Simplified Gamification Section -->
                <v-row class="mb-6">
                  <v-col cols="12" data-tour="stat-section">
                    <StatusCard
                      v-if="dashboardGamification"
                      :tier="dashboardGamification.status.tier"
                      :tier-display="dashboardGamification.status.tier_display"
                      :tier-color="dashboardGamification.status.tier_color"
                      :rank="dashboardGamification.status.rank"
                      :total-points="dashboardGamification.status.total_points"
                      :reputation-score="dashboardGamification.status.reputation_score"
                      :streak-days="dashboardGamification.status.current_streak_days"
                      :avg-response-minutes="dashboardGamification.status.avg_response_minutes"
                      :overall-percentage="dashboardGamification.progress.overall_percentage"
                      :milestones="dashboardGamification.progress.milestones"
                      :required-steps-completed="dashboardGamification.progress.required_steps_completed"
                      :total-required-steps="dashboardGamification.progress.total_required_steps"
                    />
                  </v-col>
                </v-row>

                <v-row class="mb-6">
                  <v-col cols="12" data-tour="quest-box">
                    <CurrentTaskCard
                      :task="dashboardGamification?.current_task || null"
                      @action="handleTaskAction"
                    />
                  </v-col>
                </v-row>

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
                            <div class="text-caption mb-1">محصولات شما</div>
                            <div class="text-h5 font-weight-bold">
                              {{ dashboardData.total_products || 0 }}
                            </div>
                            <div class="text-caption opacity-70">
                              {{ dashboardData.active_products || 0 }} فعال در سایت
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
                      :color="hasProductsUnderThreshold ? 'info' : 'grey'"
                      variant="tonal"
                      :loading="loading"
                    >
                      <v-card-text class="pa-4">
                        <div class="d-flex align-center justify-space-between">
                          <div>
                            <div class="text-caption mb-1 d-flex align-center gap-1">
                              سفارشات
                              <v-icon v-if="!hasProductsUnderThreshold" size="14" color="warning">mdi-lock</v-icon>
                            </div>
                            <div class="text-h5 font-weight-bold">
                              {{ hasProductsUnderThreshold ? (dashboardData.total_orders || 0) : '--' }}
                            </div>
                            <div class="text-caption opacity-70">
                              {{ hasProductsUnderThreshold ? 'کل سفارشات' : 'قفل شده' }}
                            </div>
                          </div>
                          <v-icon size="32" :color="hasProductsUnderThreshold ? 'info' : 'grey'">
                            {{ hasProductsUnderThreshold ? 'mdi-shopping-outline' : 'mdi-lock' }}
                          </v-icon>
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
                            <div class="text-caption mb-1">بازدید مشتریان</div>
                            <div class="text-h5 font-weight-bold">
                              {{ dashboardData.product_views || 0 }}
                            </div>
                            <div class="text-caption opacity-70">
                              تعداد بازدید از محصولات
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
                            <div class="text-caption mb-1">نظرات خریداران</div>
                            <div class="text-h5 font-weight-bold">
                              {{ dashboardData.total_reviews || 0 }}
                            </div>
                            <div class="text-caption opacity-70">
                              مجموع نظرات ثبت شده
                            </div>
                          </div>
                          <v-icon size="32" color="warning">mdi-star-outline</v-icon>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="6" sm="4" md="3">
                    <v-card
                      class="h-100 cursor-pointer"
                      elevation="0"
                      rounded="lg"
                      color="amber"
                      variant="tonal"
                      @click="tab = 'payments'"
                    >
                      <v-card-text class="pa-4">
                        <div class="d-flex align-center justify-space-between">
                          <div>
                            <div class="text-caption mb-1">پرداخت‌ها</div>
                            <div class="text-h5 font-weight-bold">
                              --
                            </div>
                            <div class="text-caption opacity-70">
                              تاریخچه و فاکتورها
                            </div>
                          </div>
                          <v-icon size="32" color="amber-darken-2">mdi-credit-card-outline</v-icon>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>

                <!-- Customer Pool Preview -->
                <v-row class="mb-6">
                  <v-col cols="12">
                    <v-card elevation="2" rounded="xl" class="pa-4">
                      <div class="d-flex align-center justify-space-between mb-4">
                        <div>
                          <div class="text-h6 font-weight-bold">مشتریان منتظر شما (۳ فرصت اخیر)</div>
                          <div class="text-body-2 text-medium-emphasis">
                            این افراد به دنبال محصولاتی هستند که شما می‌فروشید. با آنها تماس بگیرید.
                          </div>
                        </div>
                        <v-btn
                          variant="text"
                          color="primary"
                          prepend-icon="mdi-arrow-left"
                          @click="tab = 'customerPool'"
                        >
                          مشاهده همه
                        </v-btn>
                      </div>

                      <v-progress-linear
                        v-if="loadingCustomerPool"
                        indeterminate
                        color="primary"
                        class="mb-4"
                      ></v-progress-linear>

                      <v-alert
                        v-else-if="!loadingCustomerPool && customerPoolPreview.length === 0"
                        type="info"
                        variant="tonal"
                        class="mb-0"
                      >
                        هنوز درخواستی ثبت نشده است. با تکمیل محصولات، شانس دیده شدن خود را افزایش دهید.
                      </v-alert>

                      <v-row v-else class="gy-4">
                        <v-col
                          v-for="lead in customerPoolPreview"
                          :key="lead.id"
                          cols="12"
                          md="4"
                        >
                          <v-card rounded="xl" elevation="1" class="pa-4 h-100 d-flex flex-column gap-3">
                            <div class="d-flex align-center justify-space-between">
                              <div class="d-flex align-center gap-3">
                                <v-avatar color="primary" variant="tonal" size="44">
                                  <v-icon>mdi-account-heart</v-icon>
                                </v-avatar>
                                <div>
                                  <div class="text-body-1 font-weight-bold">
                                    {{ getLeadName(lead) }}
                                  </div>
                                  <div class="text-caption text-medium-emphasis">
                                    {{ lead.company_name || 'مشتری' }}
                                  </div>
                                </div>
                              </div>
                              <v-chip
                                :color="lead.is_free ? 'success' : 'primary'"
                                size="small"
                                variant="flat"
                                class="ml-2"
                              >
                                {{ getLeadCategoryLabel(lead) }}
                              </v-chip>
                            </div>

                            <div class="text-body-2 text-high-emphasis">
                              {{ lead.unique_needs || 'جزئیات نیاز مشتری ثبت نشده است.' }}
                            </div>
                          </v-card>
                        </v-col>
                      </v-row>
                    </v-card>
                  </v-col>
                </v-row>

                <!-- Leaderboard Section -->
                <v-row class="mb-6">
                  <v-col cols="12">
                    <LeaderboardSection
                      v-if="leaderboardData"
                      :leaderboard="leaderboardData"
                      :user-rank="dashboardGamification?.leaderboard_position || null"
                    />
                  </v-col>
                </v-row>

                <!-- Recent Orders Section -->
                <v-row class="mb-4" v-if="hasProductsUnderThreshold && recentOrders.length > 0">
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


            <!-- Customer Pool Tab -->
            <v-window-item value="customerPool">
              <div class="py-2">
                <v-row class="mb-4">
                  <v-col cols="12">
                    <v-card elevation="2" rounded="xl" class="pa-4">
                      <div class="d-flex align-center justify-space-between mb-4">
                        <div>
                          <div class="text-h6 font-weight-bold">مشتریان بالقوه</div>
                          <div class="text-body-2 text-medium-emphasis">
                            لیست خریدارانی که به دنبال محصولات شما هستند. پاسخگویی سریع = اعتماد بیشتر.
                          </div>
                        </div>
                        <v-btn
                          variant="text"
                          color="primary"
                          prepend-icon="mdi-refresh"
                          @click="loadCustomerPool"
                          :loading="loadingCustomerPool"
                        >
                          به‌روزرسانی
                        </v-btn>
                      </div>

                      <v-progress-linear
                        v-if="loadingCustomerPool"
                        indeterminate
                        color="primary"
                        class="mb-4"
                      ></v-progress-linear>

                      <v-alert
                        v-else-if="!loadingCustomerPool && customerPool.length === 0"
                        type="info"
                        variant="tonal"
                        class="mb-0"
                      >
                        هنوز درخواستی موجود نیست. با تکمیل محصولات خود، به مشتریان کمک کنید شما را پیدا کنند.
                      </v-alert>

                      <v-row v-else class="gy-4">
                        <v-col
                          v-for="lead in customerPool"
                          :key="lead.id"
                          cols="12"
                          md="6"
                          lg="4"
                        >
                          <v-card rounded="xl" elevation="1" class="pa-4 h-100 d-flex flex-column gap-3">
                            <div class="d-flex align-center justify-space-between">
                              <div class="d-flex align-center gap-3">
                                <v-avatar color="primary" variant="tonal" size="44">
                                  <v-icon>mdi-account-heart</v-icon>
                                </v-avatar>
                                <div>
                                  <div class="text-body-1 font-weight-bold">
                                    {{ getLeadName(lead) }}
                                  </div>
                                  <div class="text-caption text-medium-emphasis">
                                    {{ lead.company_name || 'مشتری' }}
                                  </div>
                                </div>
                              </div>
                              <v-chip
                                :color="lead.is_free ? 'success' : 'primary'"
                                size="small"
                                variant="flat"
                                class="ml-2"
                              >
                                {{ getLeadCategoryLabel(lead) }}
                              </v-chip>
                            </div>

                            <div class="text-body-2 text-high-emphasis">
                              {{ lead.unique_needs || 'جزئیات نیاز مشتری ثبت نشده است.' }}
                            </div>

                            <div v-if="lead.images && lead.images.length" class="d-flex align-center gap-2">
                              <v-avatar
                                v-for="image in lead.images.slice(0, 4)"
                                :key="image.id"
                                size="64"
                                rounded="lg"
                                variant="tonal"
                              >
                                <v-img :src="image.image_url" cover></v-img>
                              </v-avatar>
                              <v-chip
                                v-if="lead.images.length > 4"
                                size="small"
                                variant="tonal"
                              >
                                +{{ lead.images.length - 4 }}
                              </v-chip>
                            </div>

                            <v-sheet color="surface-variant" class="pa-3 rounded-lg">
                              <div class="text-caption text-medium-emphasis mb-1">شماره تماس</div>
                              <div class="text-body-1 font-weight-bold">
                                {{ lead.contact_revealed ? lead.phone_number : (lead.phone_number || 'برای نمایش، دکمه زیر را بزنید') }}
                              </div>
                            </v-sheet>

                            <v-btn
                              color="primary"
                              variant="flat"
                              block
                              :loading="revealingContact[lead.id]"
                              :disabled="lead.contact_revealed"
                              @click="revealLeadContact(lead.id)"
                            >
                              {{ lead.contact_revealed ? 'اطلاعات نمایش داده شد' : 'دریافت شماره تماس خریدار' }}
                            </v-btn>
                          </v-card>
                        </v-col>
                      </v-row>
                    </v-card>
                  </v-col>
                </v-row>
              </div>
            </v-window-item>

            <!-- Orders Tab -->
            <v-window-item value="orders">
              <v-card elevation="2" rounded="xl" class="pa-4 mt-4">
                <div v-if="!hasProductsUnderThreshold" class="text-center pa-12">
                  <v-icon size="96" color="warning" class="mb-4">mdi-lock</v-icon>
                  <h3 class="text-h5 font-weight-bold mb-4">بخش سفارشات قفل است</h3>
                  <p class="text-body-1 text-medium-emphasis mb-6">
                    برای دسترسی به بخش سفارشات، باید حداقل یک محصول با قیمت کمتر از ۱۰۰,۰۰۰,۰۰۰ تومان داشته باشید.
                  </p>
                  <v-btn
                    color="primary"
                    variant="flat"
                    size="large"
                    prepend-icon="mdi-package-variant"
                    @click="tab = 'miniwebsite'; miniWebsiteTab = 'products'"
                  >
                    افزودن محصول جدید
                  </v-btn>
                </div>
                <div v-else>
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
                    <p class="text-h6 mt-4 mb-2">هنوز سفارشی ثبت نشده است</p>
                    <p class="text-body-2 text-grey">با تکمیل پروفایل و محصولات، اعتماد خریداران را جلب کنید تا اولین سفارش ثبت شود.</p>
                  </v-card>
                </div>
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
                  <p class="text-h6 mt-4 mb-2">هنوز نظری ثبت نشده است</p>
                  <p class="text-body-2 text-grey">نظرات مثبت مشتریان، بزرگترین سرمایه شما برای فروش‌های بعدی است.</p>
                </v-card>
              </v-card>
            </v-window-item>

            <!-- Insights Tab -->
            <v-window-item value="insights">
              <div class="py-2">
                <InsightsFeed
                  :insights="insights"
                  :loading="insightsLoading"
                  :creating="creatingInsight"
                  :error="insightsError"
                  :comments="insightComments"
                  :comments-loading="insightCommentsLoading"
                  :comments-error="insightCommentsError"
                  @refresh="loadInsights"
                  @submit="handleCreateInsight"
                  @like="handleLikeInsight"
                  @load-comments="loadInsightComments"
                  @submit-comment="handleCreateInsightComment"
                />
              </div>
            </v-window-item>

            <!-- Invite & Earn Tab -->
            <v-window-item value="invite">
              <v-card elevation="2" rounded="xl" class="pa-6 mt-4 text-center">
                <div v-if="!hasGoldTierOrAbove">
                  <v-icon size="96" color="warning" class="mb-4">mdi-lock</v-icon>
                  <h3 class="text-h5 font-weight-bold mb-4">بخش دعوت قفل است</h3>
                  <p class="text-body-1 text-medium-emphasis mb-6">
                    برای دسترسی به بخش دعوت و کسب امتیاز، باید به رتبه طلا یا الماس دست یابید.
                  </p>
                  <p class="text-body-2 text-medium-emphasis mb-6">
                    برای دستیابی به رتبه طلا نیاز به حداقل ۵۰۰ امتیاز و امتیاز اعتبار ۶۰+ دارید.
                  </p>
                  <v-btn
                    color="primary"
                    variant="flat"
                    size="large"
                    prepend-icon="mdi-trophy"
                    @click="tab = 'home'"
                  >
                    مشاهده داشبورد
                  </v-btn>
                </div>
                <div v-else>
                  <v-icon size="56" color="primary" class="mb-4">mdi-share-variant</v-icon>
                  <h3 class="text-h6 font-weight-bold mb-2">همکاران خود را دعوت کنید</h3>
                  <p class="text-body-2 text-medium-emphasis mb-6">
                    از همکاران معتبر خود دعوت کنید تا شما را تائید نمایند، با اینکار به آنها هدیه می دهید و باعث افزایش اعتبار شرکت خود می شوید.
                  </p>
                  <v-btn
                    color="primary"
                    size="large"
                    rounded="lg"
                    prepend-icon="mdi-open-in-new"
                    to="/vendor/invite"
                  >
                    رفتن به صفحه دعوت
                  </v-btn>
                </div>
              </v-card>
            </v-window-item>

            <!-- Miniwebsite Tab -->
            <v-window-item value="miniwebsite">
              <div class="py-4">
                <v-tabs v-model="miniWebsiteTab" bg-color="surface" class="mb-4">
                  <v-tab value="profile">پروفایل</v-tab>
                  <v-tab value="products">محصولات من</v-tab>
                  <v-tab value="settings">رزومه شرکت</v-tab>
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
                            title="میزان اعتماد پروفایل"
                            caption="پروفایل کامل = فروش راحت‌تر"
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
                    <MiniWebsiteSettings @saved="onMiniWebsiteSaved" />
                  </v-window-item>
                  <v-window-item value="portfolio">
                    <PortfolioManager @item-added="onPortfolioItemAdded" />
                  </v-window-item>
                  <v-window-item value="team">
                    <TeamManager @member-added="onTeamMemberAdded" />
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

            <!-- CRM Tab -->
            <v-window-item value="crm">
              <div class="py-2">
                <CrmManager />
              </div>
            </v-window-item>

            <!-- Payments Tab -->
            <v-window-item value="payments">
              <div class="py-2">
                <v-card elevation="2" rounded="xl">
                  <v-card-title class="d-flex align-center justify-space-between pa-6">
                    <div class="d-flex align-center gap-2">
                      <v-icon size="28" color="primary">mdi-credit-card-outline</v-icon>
                      <span class="text-h6 font-weight-bold">تاریخچه پرداخت‌ها</span>
                    </div>
                    <v-btn
                      color="amber-darken-2"
                      variant="flat"
                      prepend-icon="mdi-crown"
                      to="/seller/pricing"
                    >
                      ارتقاء پلن
                    </v-btn>
                  </v-card-title>
                  <v-divider />
                  <v-card-text class="pa-0">
                    <PaymentHistorySection />
                  </v-card-text>
                </v-card>
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

    <!-- Celebration Overlay -->
    <CelebrationOverlay
      :show="showCelebration"
      :points="celebrationPoints"
      :message="celebrationMessage"
      @close="showCelebration = false"
    />

    <!-- Welcome Onboarding Tour -->
    <WelcomeOnboardingTour @tour-completed="handleTourCompleted" />
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useSellerApi } from '~/composables/useSellerApi'
import type { SellerOrder, SellerReview } from '~/composables/useSellerApi'
import { useRfqApi } from '~/composables/useRfqApi'
import { useCrmApi } from '~/composables/useCrmApi'
import MiniWebsiteSettings from '~/components/supplier/MiniWebsiteSettings.vue'
import PortfolioManager from '~/components/supplier/PortfolioManager.vue'
import TeamManager from '~/components/supplier/TeamManager.vue'
import ContactMessagesInbox from '~/components/supplier/ContactMessagesInbox.vue'
import SupplierProductForm from '~/components/supplier/ProductForm.vue'
import SupplierProductList from '~/components/supplier/ProductList.vue'
import ChatRoom from '~/components/chat/ChatRoom.vue'
import FormQualityScore from '~/components/gamification/FormQualityScore.vue'
// NEW: Simplified Gamification Components
import StatusCard from '~/components/gamification/StatusCard.vue'
import CurrentTaskCard from '~/components/gamification/CurrentTaskCard.vue'
import CelebrationOverlay from '~/components/gamification/CelebrationOverlay.vue'
import LeaderboardSection from '~/components/gamification/LeaderboardSection.vue'
import InsightsFeed from '~/components/gamification/InsightsFeed.vue'
import WelcomeOnboardingTour from '~/components/gamification/WelcomeOnboardingTour.vue'
import CrmManager from '~/components/crm/CrmManager.vue'
import PaymentHistorySection from '~/components/seller/PaymentHistorySection.vue'
import { useGamificationStore } from '~/stores/gamification'
import { useGamificationApi, type SellerInsight } from '~/composables/useGamification'
import { useGamificationDashboard, type DashboardData, type CurrentTask } from '~/composables/useGamificationDashboard'

interface CustomerLead {
  id: number
  is_free: boolean
  category_name?: string | null
  product_name?: string | null
  first_name?: string | null
  last_name?: string | null
  company_name?: string | null
  phone_number?: string | null
  unique_needs?: string | null
  images?: Array<{ id: number; image_url?: string }>
  contact_revealed?: boolean
}

interface ProfileMetric {
  key: string
  label: string
  tip: string
  weight: number
  passed: boolean
}

definePageMeta({
  middleware: 'authenticated',
  layout: 'dashboard'
})

const authStore = useAuthStore()
const sellerApi = useSellerApi()
const rfqApi = useRfqApi()
const crmApi = useCrmApi()
const gamificationStore = useGamificationStore()
const gamificationApi = useGamificationApi()
const dashboardApi = useGamificationDashboard()
const route = useRoute()

// NEW: Simplified Gamification State
const dashboardGamification = ref<DashboardData | null>(null)
const leaderboardData = ref<any[]>([])
const showCelebration = ref(false)
const celebrationPoints = ref(0)
const celebrationMessage = ref('')

const tabQuery = computed(() => route.query.tab as string || 'home')
const tab = ref(tabQuery.value)
const miniWebsiteTab = ref('profile')

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

const getLeadName = (lead: CustomerLead) => {
  const name = `${lead.first_name || ''} ${lead.last_name || ''}`.trim()
  return name || lead.company_name || 'مشتری'
}

const getLeadCategoryLabel = (lead: CustomerLead) => {
  if (lead.is_free) return 'رایگان'
  return lead.category_name || 'مرتبط با محصولات شما'
}

const normalizeLead = (lead: any): CustomerLead => ({
  id: lead.id,
  is_free: !!lead.is_free,
  category_name: lead.category_name || null,
  product_name: lead.product_name || null,
  first_name: lead.first_name || null,
  last_name: lead.last_name || null,
  company_name: lead.company_name || null,
  phone_number: lead.phone_number || null,
  unique_needs: lead.unique_needs || null,
  images: Array.isArray(lead.images) ? lead.images : [],
  contact_revealed: false
})

const customerPoolPreview = computed(() => customerPool.value.slice(0, 3))

const openProductForm = () => {
  showProductForm.value = true
  editingProduct.value = null
}

const closeProductForm = () => {
  showProductForm.value = false
  editingProduct.value = null
}

const onProductSaved = async () => {
  closeProductForm()
  if (productListRef.value && typeof productListRef.value.loadProducts === 'function') {
    productListRef.value.loadProducts()
  }
  loadDashboardData()
  // Recheck products threshold after adding/editing product
  await checkSellerProducts()
  // NEW: Complete task and celebrate
  try {
    await completeTaskAndCelebrate('products')
  } catch (e) {
    console.warn('Failed to complete products task', e)
  }
  showSnackbar('محصول با موفقیت ذخیره شد', 'success')
}

const onMiniWebsiteSaved = async () => {
  // Mini website settings saved
  try {
    await completeTaskAndCelebrate('mini_website')
  } catch (e) {
    console.warn('Failed to complete mini_website task', e)
  }
}

const onPortfolioItemAdded = async () => {
  // Portfolio item added
  try {
    await completeTaskAndCelebrate('portfolio')
  } catch (e) {
    console.warn('Failed to complete portfolio task', e)
  }
}

const onTeamMemberAdded = async () => {
  // Team member added
  try {
    await completeTaskAndCelebrate('team')
  } catch (e) {
    console.warn('Failed to complete team task', e)
  }
}

const openEditProductForm = (product: any) => {
  editingProduct.value = product
  showProductForm.value = true
}

const selectChatRoom = (room: any) => {
  selectedChatRoom.value = room
}

// NEW: Dashboard Gamification Data Loading
const loadDashboardGamification = async () => {
  try {
    console.log('[Dashboard] Loading gamification data...')
    const result = await dashboardApi.fetchDashboardData()
    if (result.error.value) {
      console.error('[Dashboard] Failed to load dashboard gamification:', result.error.value)
      // Set empty data to prevent null access errors
      dashboardGamification.value = {
        status: {
          tier: 'inactive',
          tier_display: 'غیرفعال',
          tier_color: 'grey',
          rank: null,
          total_points: 0,
          reputation_score: 0,
          current_streak_days: 0,
          avg_response_minutes: 0
        },
        progress: {
          overall_percentage: 0,
          milestones: [],
          required_steps_completed: 0,
          total_required_steps: 5
        },
        current_task: null,
        leaderboard_position: null
      }
      return
    }
    if (result.data.value) {
      console.log('[Dashboard] Gamification data loaded:', result.data.value)
      dashboardGamification.value = result.data.value
      // Also load leaderboard for the section
      await loadLeaderboard()
    }
  } catch (error) {
    console.error('[Dashboard] Error loading dashboard gamification:', error)
    // Set empty data to prevent null access errors
    dashboardGamification.value = {
      status: {
        tier: 'inactive',
        tier_display: 'غیرفعال',
        tier_color: 'grey',
        rank: null,
        total_points: 0,
        reputation_score: 0,
        current_streak_days: 0,
        avg_response_minutes: 0
      },
      progress: {
        overall_percentage: 0,
        milestones: [],
        required_steps_completed: 0,
        total_required_steps: 5
      },
      current_task: null,
      leaderboard_position: null
    }
  }
}

const loadLeaderboard = async () => {
  try {
    const data = await gamificationApi.fetchLeaderboard({ limit: 10 })
    leaderboardData.value = data.overall || []
  } catch (error) {
    console.error('Error loading leaderboard:', error)
  }
}

const handleTaskAction = async (task: CurrentTask | null) => {
  // Guard against null task
  if (!task) {
    console.warn('[Dashboard] handleTaskAction called with null task')
    return
  }

  // Navigate to the appropriate tab based on task actionUrl
  const tabMap: Record<string, string> = {
    'profile': 'miniwebsite',
    'mini_website': 'miniwebsite',
    'products': 'miniwebsite',
    'team': 'miniwebsite',
    'portfolio': 'miniwebsite',
    'insights': 'insights',
    'invite': 'invite'
  }

  const targetTab = tabMap[task.type] || task.action_url

  // Set the appropriate sub-tab for miniwebsite
  if (task.type === 'profile') {
    miniWebsiteTab.value = 'profile'
  } else if (task.type === 'mini_website') {
    miniWebsiteTab.value = 'settings'
  } else if (task.type === 'products') {
    miniWebsiteTab.value = 'products'
  } else if (task.type === 'team') {
    miniWebsiteTab.value = 'team'
  } else if (task.type === 'portfolio') {
    miniWebsiteTab.value = 'portfolio'
  }

  // Navigate to tab
  tab.value = targetTab
}

const completeTaskAndCelebrate = async (taskType: string, metadata: Record<string, any> = {}) => {
  try {
    const result = await dashboardApi.completeTask(taskType, metadata)
    if (result.error.value) {
      console.error('Failed to complete task:', result.error.value)
      return
    }
    
    if (result.data.value && result.data.value.celebration) {
      // Show celebration
      celebrationPoints.value = result.data.value.points_awarded || 0
      celebrationMessage.value = result.data.value.message || 'عالی! یک قدم به موفقیت نزدیک‌تر شدید.'
      showCelebration.value = true
      
      // Refresh dashboard data after celebration
      setTimeout(() => {
        loadDashboardGamification()
      }, 500)
    }
  } catch (error) {
    console.error('Error completing task:', error)
  }
}

const handleTourCompleted = () => {
  // Tour completed - refresh dashboard to show updated quest status
  loadDashboardGamification()
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
    // Load profile score from backend
    await loadProfileScore()
    // NEW: Complete task and celebrate
    try {
      await completeTaskAndCelebrate('profile')
    } catch (e) {
      console.warn('Failed to complete profile task', e)
    }
    // Refresh gamification data
    await loadDashboardGamification()
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
const insights = ref<SellerInsight[]>([])
const insightsLoading = ref(false)
const insightsLoaded = ref(false)
const creatingInsight = ref(false)
const insightsError = ref<string | null>(null)
const insightComments = ref<Record<number, any[]>>({})
const insightCommentsLoading = ref<Record<number, boolean>>({})
const insightCommentsError = ref<Record<number, string | null>>({})
const recentOrders = ref<any[]>([]) 
const chatRooms = ref<any[]>([])
const selectedChatRoom = ref<any>(null)
const unreadChatsCount = ref(0)
const activeTodayCount = ref(0)
const profileScore = ref(0)
const profileMetrics = ref<ProfileMetric[]>([])
const profileTips = ref<string[]>([])
const profileData = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: ''
})
const customerPool = ref<CustomerLead[]>([])
const loadingCustomerPool = ref(false)
const revealingContact = ref<Record<number, boolean>>({})
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

// Check if seller has products under 100,000,000 toman
const hasProductsUnderThreshold = ref<boolean>(false)
const PRICE_THRESHOLD = 100000000 // 100,000,000 toman

// Check if seller has gold tier or above (gold/diamond)
const hasGoldTierOrAbove = computed(() => {
  const tier = dashboardGamification.value?.status?.tier || gamificationStore.userTier
  return tier === 'gold' || tier === 'diamond'
})

const checkSellerProducts = async () => {
  if (!authStore.isSeller) {
    hasProductsUnderThreshold.value = true
    return
  }

  try {
    const { useProductApi } = await import('~/composables/useProductApi')
    const productApi = useProductApi()
    const response = await productApi.getMyProducts({ page_size: 100 })

    const products = Array.isArray(response) ? response : response.results || []
    
    // Check if any product has valid price (not null, not 0, and less than threshold)
    hasProductsUnderThreshold.value = products.some((product: any) => {
      if (!product.price) return false // No price
      const price = parseFloat(product.price)
      if (isNaN(price) || price <= 0) return false // Invalid or zero price
      return price < PRICE_THRESHOLD // Must be less than 100,000,000
    })
  } catch (error) {
    console.error('Failed to check seller products:', error)
    // Default to false (locked) if we can't check
    hasProductsUnderThreshold.value = false
  }
}
const orderHeaders = ref([
  { title: 'شماره سفارش', key: 'order_number', align: 'start' as const },
  { title: 'خریدار', key: 'buyer_username', align: 'start' as const },
  { title: 'مبلغ', key: 'total_amount', align: 'start' as const },
  { title: 'وضعیت', key: 'status', align: 'start' as const },
  { title: 'تاریخ', key: 'created_at', align: 'start' as const }
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
    const data = await sellerApi.getSellerDashboard() as SellerDashboardData & { recent_orders?: SellerOrder[] }
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

const loadInsights = async () => {
  insightsLoading.value = true
  insightsError.value = null
  try {
    const data = await gamificationApi.fetchSellerInsights()
    const results = (data as any)?.results || []
    insights.value = Array.isArray(results) ? results : []
    insightsLoaded.value = true
  } catch (error: any) {
    console.error('Failed to load insights:', error)
    insightsError.value = error?.message || 'خطا در بارگذاری بینش‌ها'
    showSnackbar('خطا در بارگذاری بینش‌ها', 'error')
  } finally {
    insightsLoading.value = false
  }
}

const handleCreateInsight = async (payload: { title: string; content: string }) => {
  creatingInsight.value = true
  try {
    const created = await gamificationApi.createSellerInsight(payload)
    const newInsight: SellerInsight = {
      id: (created as any)?.id || Date.now(),
      title: (created as any)?.title || payload.title,
      content: (created as any)?.content || payload.content,
      author_name: (created as any)?.author_name || getUserFullName(),
      created_at: (created as any)?.created_at || new Date().toISOString(),
      likes_count: (created as any)?.likes_count || 0,
      liked_by_me: false,
      comments_count: (created as any)?.comments_count || 0
    }
    insights.value = [newInsight, ...insights.value]
    showSnackbar('نکته شما به صورت عمومی منتشر شد و برای خریداران قابل مشاهده است', 'success')
    
    // NEW: Complete task and celebrate
    try {
      await completeTaskAndCelebrate('insights', { insight_id: newInsight.id })
    } catch (e) {
      console.warn('Failed to complete insights task', e)
    }
  } catch (error: any) {
    console.error('Failed to create insight:', error)
    showSnackbar(error?.message || 'ثبت نکته تخصصی ناموفق بود', 'error')
  } finally {
    creatingInsight.value = false
  }
}

const updateInsightState = (insightId: number, patch: Partial<SellerInsight>) => {
  const idx = insights.value.findIndex((item) => item.id === insightId)
  if (idx !== -1) {
    insights.value.splice(idx, 1, { ...insights.value[idx], ...patch })
  }
}

const handleLikeInsight = async (insightId: number) => {
  try {
    const res = await gamificationApi.likeSellerInsight(insightId)
    updateInsightState(insightId, {
      liked_by_me: (res as any)?.liked,
      likes_count: (res as any)?.likes_count ?? 0
    })
  } catch (error: any) {
    console.error('Failed to like insight:', error)
    showSnackbar(error?.message || 'خطا در ثبت لایک', 'error')
  }
}

const loadInsightComments = async (insightId: number) => {
  if (insightCommentsLoading.value[insightId]) return
  insightCommentsLoading.value = { ...insightCommentsLoading.value, [insightId]: true }
  insightCommentsError.value = { ...insightCommentsError.value, [insightId]: null }
  try {
    const data = await gamificationApi.fetchSellerInsightComments(insightId)
    const results = (data as any)?.results || []
    insightComments.value = { ...insightComments.value, [insightId]: Array.isArray(results) ? results : [] }
  } catch (error: any) {
    console.error('Failed to load insight comments:', error)
    insightCommentsError.value = {
      ...insightCommentsError.value,
      [insightId]: error?.message || 'خطا در بارگذاری دیدگاه‌ها'
    }
  } finally {
    insightCommentsLoading.value = { ...insightCommentsLoading.value, [insightId]: false }
  }
}

const handleCreateInsightComment = async (payload: { id: number; content: string }) => {
  const { id, content } = payload
  insightCommentsLoading.value = { ...insightCommentsLoading.value, [id]: true }
  insightCommentsError.value = { ...insightCommentsError.value, [id]: null }
  try {
    const created = await gamificationApi.createSellerInsightComment(id, content)
    const newComment = {
      id: (created as any)?.id || Date.now(),
      content: (created as any)?.content || content,
      author_name: (created as any)?.author_name || getUserFullName(),
      created_at: (created as any)?.created_at || new Date().toISOString()
    }
    const existing = insightComments.value[id] || []
    insightComments.value = { ...insightComments.value, [id]: [...existing, newComment] }
    updateInsightState(id, {
      comments_count: (existing.length + 1)
    })
    showSnackbar('نظر شما به صورت عمومی ثبت شد', 'success')
  } catch (error: any) {
    console.error('Failed to add comment:', error)
    insightCommentsError.value = {
      ...insightCommentsError.value,
      [id]: error?.message || 'ثبت نظر ناموفق بود'
    }
  } finally {
    insightCommentsLoading.value = { ...insightCommentsLoading.value, [id]: false }
  }
}

const loadCustomerPool = async () => {
  loadingCustomerPool.value = true
  try {
    const data = await rfqApi.getVendorPool()
    customerPool.value = (Array.isArray(data) ? data : []).map(normalizeLead)
  } catch (error: any) {
    console.error('Failed to load customer pool:', error)
    showSnackbar('خطا در بارگذاری درخواست های خرید رایگان', 'error')
  } finally {
    loadingCustomerPool.value = false
  }
}

const revealLeadContact = async (leadId: number) => {
  revealingContact.value[leadId] = true
  try {
    // Reveal contact info from RFQ
    const data = await rfqApi.revealRFQContact(leadId)
    const normalizedLead = normalizeLead(data)
    
    // Check if contact already exists in CRM by phone number (only if phone exists)
    if (normalizedLead.phone_number) {
      const existingContacts = await crmApi.getContacts(normalizedLead.phone_number)
      const existingContact = existingContacts.find(
        (contact) => contact.phone === normalizedLead.phone_number
      )
      
      if (existingContact) {
        // Contact already exists in CRM
        const idx = customerPool.value.findIndex((lead) => lead.id === leadId)
        if (idx !== -1) {
          customerPool.value.splice(idx, 1)
        }
        showSnackbar('این مخاطب قبلاً در CRM شما ثبت شده است، برای مشاهده به CRM مراجعه کنید.', 'هشدار')
        return
      }
    }
    
    // Add to CRM
    try {
      await crmApi.createContact({
        first_name: normalizedLead.first_name || '',
        last_name: normalizedLead.last_name || '',
        company_name: normalizedLead.company_name || null,
        phone: normalizedLead.phone_number || '',
        notes: normalizedLead.unique_needs || null,
        source_order: leadId
      })
      
      // Remove from customer pool
      const idx = customerPool.value.findIndex((lead) => lead.id === leadId)
      if (idx !== -1) {
        customerPool.value.splice(idx, 1)
      }
      
      showSnackbar('اطلاعات با موفقیت به CRM اضافه شد. برای مشاهده به تب CRM مراجعه کنید.', 'success')
    } catch (crmError: any) {
      console.error('Failed to add contact to CRM:', crmError)
      // Don't show contact info if CRM add fails
      showSnackbar('خطا در افزودن به CRM. لطفاً دوباره تلاش کنید.', 'error')
    }
  } catch (error: any) {
    console.error('Failed to reveal contact:', error)
    
    // Extract error message from response
    const statusCode = error?.statusCode || error?.status || error?.response?.status
    let errorMessage = 'دسترسی به این مشتری ممکن نیست'
    
    // Handle 429 rate limit error specifically
    if (statusCode === 429) {
      errorMessage = error?.data?.detail || 'شما به حد مجاز روزانه برای مشاهده مشتریهای جدید رسیده‌اید. لطفاً بعداً تلاش کنید.'
    } else if (error?.data?.detail) {
      errorMessage = error.data.detail
    } else if (error?.message) {
      errorMessage = error.message
    }
    
    // Don't show contact info if reveal fails - just show error message
    showSnackbar(errorMessage, 'error')
  } finally {
    revealingContact.value[leadId] = false
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

const buildProfileGamificationMetrics = (): ProfileMetric[] => {
  const emailValue = (profileData.value.email || '').trim()
  const phoneDigits = (profileData.value.phone || '').replace(/\D/g, '')
  const hasFirstName = !!profileData.value.first_name?.trim()
  const hasLastName = !!profileData.value.last_name?.trim()
  const hasValidEmail = emailValue.includes('@') && emailValue.split('@')[1]?.includes('.')
  const hasReachablePhone = phoneDigits.length >= 10

  return [
    {
      key: 'first_name',
      label: 'نام',
      tip: 'نامتان را وارد کنید؛ خریداران دوست دارند بدانند طرف معامله‌شان چه کسی است.',
      weight: 0.25,
      passed: hasFirstName
    },
    {
      key: 'last_name',
      label: 'نام خانوادگی',
      tip: 'نام خانوادگی نشان‌دهنده هویت واقعی شماست و باعث اطمینان خریدار می‌شود.',
      weight: 0.25,
      passed: hasLastName
    },
    {
      key: 'email',
      label: 'ایمیل',
      tip: 'ثبت ایمیل در آینده به تسهیل ارتباط شما با مشتریان خارجی کمک می کند.',
      weight: 0.25,
      passed: hasValidEmail
    },
    {
      key: 'phone',
      label: 'شماره تماس',
      tip: 'شماره تماس صحیح، راه ارتباطی مشتریان با شماست. در دسترس بودن = فروش بیشتر.',
      weight: 0.25,
      passed: hasReachablePhone
    }
  ]
}

const applyLocalProfileGamification = () => {
  const metrics = buildProfileGamificationMetrics()
  const score = metrics.reduce((total, metric) => {
    return total + (metric.passed ? metric.weight * 100 : 0)
  }, 0)

  profileMetrics.value = metrics
  profileScore.value = Math.round(score)
  profileTips.value = metrics.filter((metric) => !metric.passed).map((metric) => metric.tip)
}

const loadProfileScore = async () => {
  try {
    const scores = await gamificationApi.fetchScores()
    // Always compute local metrics based on the four profile fields
    applyLocalProfileGamification()

    // If backend provides extra tips, merge them without losing local ones
    if (scores?.profile?.tips?.length) {
      const mergedTips = [...profileTips.value]
      scores.profile.tips.forEach((tip: string) => {
        if (!mergedTips.includes(tip)) {
          mergedTips.push(tip)
        }
      })
      profileTips.value = mergedTips
    }
  } catch (error) {
    console.error('Failed to load profile score:', error)
    // Fall back to local evaluation when backend is unavailable
    applyLocalProfileGamification()
  }
}

// Watch tab changes to load data when needed
watch(tab, async (newTab) => {
  if (newTab === 'orders') {
    // Recheck products threshold when accessing orders tab
    await checkSellerProducts()
    if (hasProductsUnderThreshold.value && orders.value.length === 0 && !loadingOrders.value) {
      await loadOrders()
    }
  } else if (newTab === 'reviews' && reviews.value.length === 0 && !loadingReviews.value) {
    await loadReviews()
  } else if (newTab === 'insights' && !insightsLoaded.value && !insightsLoading.value) {
    await loadInsights()
  } else if (newTab === 'chats' && chatRooms.value.length === 0 && !loadingChats.value) {
    await loadChatRooms()
  } else if (newTab === 'miniwebsite' && miniWebsiteTab.value === 'profile') {
    // Load profile score when profile tab is accessed
    await loadProfileScore()
  }
})

// Watch miniWebsiteTab to load profile score when profile tab is selected
watch(miniWebsiteTab, async (newTab) => {
  if (newTab === 'profile') {
    await loadProfileScore()
  }
})

// Gamification: Hydrate store on mount
onMounted(async () => {
  try {
    await loadDashboardGamification()
  } catch (error) {
    console.warn('Failed to load gamification data', error)
  }
  
  // Check if seller has products under threshold
  await checkSellerProducts()
  
  // Load initial data
  await Promise.all([
    loadDashboardData(),
    loadProfileData(),
    loadCustomerPool()
  ])
  
  // Load profile score from backend after loading profile data
  await loadProfileScore()
  
  // Load chat rooms if on chats tab
  if (tab.value === 'chats') {
    await loadChatRooms()
  }
  if (tab.value === 'insights') {
    await loadInsights()
  }
  // Load profile score if on miniwebsite profile tab
  if (tab.value === 'miniwebsite' && miniWebsiteTab.value === 'profile') {
    await loadProfileScore()
  }
})

// Gamification: Sync profile score with store
watch(profileScore, (score) => {
  if (score >= 0) {
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
  padding-top: 140px !important;
  padding-bottom: 32px;
}

.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.stat-card { transition: transform 0.2s; }
.stat-card:hover { transform: translateY(-2px); }

/* Responsive spacing adjustments */
@media (max-width: 960px) {
  .seller-dashboard {
    padding-top: 120px !important;
  }
}

@media (max-width: 600px) {
  .seller-dashboard {
    padding-top: 112px !important;
    padding-bottom: 24px;
  }
}
</style>

