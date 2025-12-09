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
                <!-- Welcome Section -->
                <v-row class="mb-6">
                  <v-col cols="12">
                    <div class="d-flex align-center justify-space-between flex-wrap gap-3" data-tour="welcome">
                      <div>
                        <h2 class="text-h4 font-weight-bold mb-1 text-high-emphasis">
                          خوش آمدید، <span class="text-primary">{{ getUserFullName() }}</span>
                        </h2>
                        <p class="text-body-1 text-medium-emphasis">
                          گزارش عملکرد فروشگاه شما در یک نگاه
                        </p>
                      </div>

                      <!-- Quick Actions -->
                      <div class="d-flex gap-3 flex-wrap">
                        <v-btn
                          color="primary"
                          elevation="2"
                          rounded="lg"
                          prepend-icon="mdi-plus"
                          @click="tab = 'products'; openProductForm()"
                          size="large"
                          data-tour="add-product-btn"
                        >
                          افزودن محصول
                        </v-btn>
                        <v-btn
                          color="secondary"
                          variant="tonal"
                          rounded="lg"
                          prepend-icon="mdi-package-variant"
                          @click="tab = 'products'"
                          size="large"
                        >
                          مدیریت محصولات
                        </v-btn>
                      </div>
                    </div>
                  </v-col>
                </v-row>

                <!-- Enhanced Stats Cards (Tonal Variants) -->
                <v-row class="mb-6">
                  <v-col cols="12" sm="6" md="3">
                    <v-card
                      class="h-100"
                      elevation="0"
                      rounded="xl"
                      color="primary"
                      variant="tonal"
                      :loading="loading"
                    >
                      <v-card-text class="pa-6">
                        <div class="d-flex align-start justify-space-between">
                          <div>
                            <div class="text-subtitle-2 mb-2">کل محصولات</div>
                            <div class="text-h3 font-weight-bold mb-1">
                              {{ dashboardData.total_products || 0 }}
                            </div>
                            <div class="text-caption font-weight-medium opacity-70">
                              {{ dashboardData.active_products || 0 }} فعال
                            </div>
                          </div>
                          <v-avatar size="48" color="primary" variant="flat" class="rounded-lg">
                            <v-icon color="white">mdi-package-variant</v-icon>
                          </v-avatar>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>

                  <v-col cols="12" sm="6" md="3">
                    <v-card
                      class="h-100"
                      elevation="0"
                      rounded="xl"
                      color="secondary"
                      variant="tonal"
                      :loading="loading"
                    >
                      <v-card-text class="pa-6">
                        <div class="d-flex align-start justify-space-between">
                          <div>
                            <div class="text-subtitle-2 mb-2">فروش کل</div>
                            <div class="text-h3 font-weight-bold mb-1">
                              {{ formatPrice(dashboardData.total_sales || 0) }}
                            </div>
                            <div class="text-caption font-weight-medium opacity-70">
                              {{ dashboardData.total_orders || 0 }} سفارش موفق
                            </div>
                          </div>
                          <v-avatar size="48" color="secondary" variant="flat" class="rounded-lg">
                            <v-icon color="white">mdi-cash-multiple</v-icon>
                          </v-avatar>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>

                  <v-col cols="12" sm="6" md="3">
                    <v-card
                      class="h-100"
                      elevation="0"
                      rounded="xl"
                      color="info"
                      variant="tonal"
                      :loading="loading"
                    >
                      <v-card-text class="pa-6">
                        <div class="d-flex align-start justify-space-between">
                          <div>
                            <div class="text-subtitle-2 mb-2">بازدیدها</div>
                            <div class="text-h3 font-weight-bold mb-1">
                              {{ dashboardData.product_views || 0 }}
                            </div>
                            <div class="text-caption font-weight-medium opacity-70">
                              بازدید از محصولات
                            </div>
                          </div>
                          <v-avatar size="48" color="info" variant="flat" class="rounded-lg">
                            <v-icon color="white">mdi-eye-outline</v-icon>
                          </v-avatar>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>

                  <v-col cols="12" sm="6" md="3">
                    <v-card
                      class="h-100"
                      elevation="0"
                      rounded="xl"
                      color="warning"
                      variant="tonal"
                      :loading="loading"
                    >
                      <v-card-text class="pa-6">
                        <div class="d-flex align-start justify-space-between">
                          <div>
                            <div class="text-subtitle-2 mb-2">نظرات</div>
                            <div class="text-h3 font-weight-bold mb-1">
                              {{ dashboardData.total_reviews || 0 }}
                            </div>
                            <div class="text-caption font-weight-medium opacity-70">
                              نظر ثبت شده
                            </div>
                          </div>
                          <v-avatar size="48" color="warning" variant="flat" class="rounded-lg">
                            <v-icon color="white">mdi-star-outline</v-icon>
                          </v-avatar>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>

                <!-- Gamification Section -->
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
                <v-row class="mb-4" v-if="recentOrders && recentOrders.length > 0">
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

            <!-- Profile Tab -->
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

            <!-- Products Tab (Preserved Logic, Updated UI container) -->
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

            <!-- Orders Tab -->
            <v-window-item value="orders">
              <v-card elevation="2" rounded="xl" class="pa-4 mt-4">
                <div class="d-flex align-center justify-space-between mb-6">
                  <h3 class="text-h6 font-weight-bold">سفارشات من</h3>
                  <v-chip v-if="orders.length > 0" color="primary" variant="tonal">
                    {{ orders.length }} سفارش
                  </v-chip>
                </div>

                <v-progress-linear v-if="loadingOrders" indeterminate color="primary" class="mb-4"></v-progress-linear>

                <v-card v-if="orders.length === 0 && !loadingOrders" elevation="1" class="text-center pa-8">
                  <v-icon size="80" color="grey-lighten-1">mdi-shopping-outline</v-icon>
                  <p class="text-h6 mt-4 mb-2">هنوز سفارشی دریافت نکرده‌اید</p>
                  <p class="text-body-2 text-grey">سفارشات شما در اینجا نمایش داده می‌شوند</p>
                </v-card>

                <v-data-table
                  v-else
                  :headers="orderHeaders"
                  :items="orders"
                  :loading="loadingOrders"
                  item-value="id"
                  class="elevation-0"
                >
                  <template v-slot:item.order_number="{ item }">
                    <span class="font-weight-bold text-primary">#{{ item.order_number }}</span>
                  </template>

                  <template v-slot:item.buyer_username="{ item }">
                    {{ item.buyer_username || 'کاربر مهمان' }}
                  </template>

                  <template v-slot:item.total_amount="{ item }">
                    <span class="font-weight-medium">{{ formatPrice(item.total_amount) }} تومان</span>
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
                    <span class="text-caption">{{ formatDate(item.created_at) }}</span>
                  </template>
                </v-data-table>
              </v-card>
            </v-window-item>

            <!-- Reviews Tab -->
            <v-window-item value="reviews">
              <v-card elevation="2" rounded="xl" class="pa-4 mt-4">
                <div class="d-flex align-center justify-space-between mb-6">
                  <h3 class="text-h6 font-weight-bold">نظرات محصولات</h3>
                  <v-chip v-if="reviews.length > 0" color="primary" variant="tonal">
                    {{ reviews.length }} نظر
                  </v-chip>
                </div>

                <v-progress-linear v-if="loadingReviews" indeterminate color="primary" class="mb-4"></v-progress-linear>

                <v-card v-if="reviews.length === 0 && !loadingReviews" elevation="1" class="text-center pa-8">
                  <v-icon size="80" color="grey-lighten-1">mdi-star-outline</v-icon>
                  <p class="text-h6 mt-4 mb-2">هنوز نظری دریافت نکرده‌اید</p>
                  <p class="text-body-2 text-grey">نظرات مشتریان در اینجا نمایش داده می‌شوند</p>
                </v-card>

                <v-data-table
                  v-else
                  :headers="reviewHeaders"
                  :items="reviews"
                  :loading="loadingReviews"
                  item-value="id"
                  class="elevation-0"
                >
                  <template v-slot:item.product="{ item }">
                    <span class="font-weight-medium">{{ item.product?.name || 'محصول حذف شده' }}</span>
                  </template>

                  <template v-slot:item.author="{ item }">
                    {{ item.author?.username || 'کاربر مهمان' }}
                  </template>

                  <template v-slot:item.rating="{ item }">
                    <div class="d-flex align-center">
                      <v-rating
                        :model-value="item.rating"
                        readonly
                        size="small"
                        color="warning"
                        density="compact"
                      ></v-rating>
                      <span class="text-caption mr-2">({{ item.rating }})</span>
                    </div>
                  </template>

                  <template v-slot:item.comment="{ item }">
                    <span class="text-caption">{{ item.comment?.substring(0, 50) }}{{ item.comment?.length > 50 ? '...' : '' }}</span>
                  </template>

                  <template v-slot:item.created_at="{ item }">
                    <span class="text-caption">{{ formatDate(item.created_at) }}</span>
                  </template>
                </v-data-table>
              </v-card>
            </v-window-item>

            <!-- Mini Website Tab -->
            <v-window-item value="miniwebsite">
              <v-card elevation="2" rounded="xl" class="pa-4 mt-4">
                <v-tabs v-model="miniWebsiteTab" bg-color="surface" color="primary" class="mb-4">
                  <v-tab value="settings">
                    <v-icon start>mdi-cog-outline</v-icon>
                    تنظیمات
                  </v-tab>
                  <v-tab value="portfolio">
                    <v-icon start>mdi-briefcase-outline</v-icon>
                    نمونه کارها
                  </v-tab>
                  <v-tab value="team">
                    <v-icon start>mdi-account-group-outline</v-icon>
                    تیم
                  </v-tab>
                  <v-tab value="messages">
                    <v-icon start>mdi-email-outline</v-icon>
                    پیام‌ها
                  </v-tab>
                </v-tabs>

                <v-window v-model="miniWebsiteTab">
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
              </v-card>
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
                      
                      <v-list class="flex-grow-1 overflow-y-auto py-0">
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
                            <span v-if="room.last_message" :class="room.unread_count > 0 ? 'text-high-emphasis font-weight-medium' : ''">
                                {{ room.last_message.content?.substring(0, 35) || '' }}{{ room.last_message.content?.length > 35 ? '...' : '' }}
                            </span>
                            <span v-else class="text-disabled">پیامی وجود ندارد</span>
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
import { useApiFetch } from '~/composables/useApiFetch'
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
import OnboardingTour from '~/components/supplier/OnboardingTour.vue'
import { useGamificationStore } from '~/stores/gamification'

definePageMeta({
  middleware: 'authenticated',
  layout: 'dashboard'
})

const authStore = useAuthStore()
const sellerApi = useSellerApi()
const gamificationStore = useGamificationStore()
const route = useRoute()
const { mdAndUp } = useDisplay()

// Define Menu Structure
const menuItems = [
  { value: 'home', label: 'صفحه اصلی', icon: 'mdi-home-outline', tour: '' },
  { value: 'profile', label: 'پروفایل', icon: 'mdi-account-outline', tour: 'profile-tab' },
  { value: 'products', label: 'محصولات', icon: 'mdi-package-variant-closed', tour: 'products-tab' },
  { value: 'orders', label: 'سفارشات', icon: 'mdi-shopping-outline', tour: '' },
  { value: 'reviews', label: 'نظرات', icon: 'mdi-star-outline', tour: '' },
  { value: 'miniwebsite', label: 'وب‌سایت مینی', icon: 'mdi-web', tour: 'miniwebsite-tab' },
  { value: 'chats', label: 'گفتگوها', icon: 'mdi-chat-processing-outline', tour: '' },
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
const miniWebsiteTab = ref('settings')

watch(() => route.query.tab, (newTab) => {
  if (newTab && typeof newTab === 'string') {
    tab.value = newTab
  }
})

// Watch tab changes to update URL
watch(tab, (newTab) => {
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
  if (authStore.user) {
    const firstName = authStore.user.first_name || ''
    const lastName = authStore.user.last_name || ''
    return `${firstName} ${lastName}`.trim() || authStore.user.username || 'کاربر'
  }
  return 'کاربر'
}

const formatPrice = (price: string | number) => {
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  if (isNaN(numPrice)) return '0'
  return new Intl.NumberFormat('fa-IR').format(numPrice)
}

const getStatusColor = (status: string) => {
  const statusColors: Record<string, string> = {
    'pending': 'warning',
    'confirmed': 'info',
    'processing': 'primary',
    'shipped': 'secondary',
    'delivered': 'success',
    'cancelled': 'error',
    'completed': 'success'
  }
  return statusColors[status?.toLowerCase()] || 'grey'
}

const getStatusLabel = (status: string) => {
  const statusLabels: Record<string, string> = {
    'pending': 'در انتظار',
    'confirmed': 'تایید شده',
    'processing': 'در حال پردازش',
    'shipped': 'ارسال شده',
    'delivered': 'تحویل داده شده',
    'cancelled': 'لغو شده',
    'completed': 'تکمیل شده'
  }
  return statusLabels[status?.toLowerCase()] || status
}

const getChatInitials = (user: any) => {
  if (!user) return 'م'
  const username = user.username || ''
  if (username.length > 0) {
    return username.charAt(0).toUpperCase()
  }
  return 'م'
}

const formatChatTime = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'همین الان'
  if (diffMins < 60) return `${diffMins} دقیقه پیش`
  if (diffHours < 24) return `${diffHours} ساعت پیش`
  if (diffDays < 7) return `${diffDays} روز پیش`
  
  return new Intl.DateTimeFormat('fa-IR', {
    month: 'short',
    day: 'numeric'
  }).format(date)
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
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
  if (productListRef.value?.loadProducts) {
    productListRef.value.loadProducts()
  }
  loadDashboardData()
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
  // Tour started handler
}

const handleTourCompleted = () => {
  // Tour completed handler
}

const handleTourDismissed = () => {
  // Tour dismissed handler
}

const orders = ref<SellerOrder[]>([])
const reviews = ref<SellerReview[]>([])
const recentOrders = computed(() => {
  return orders.value.slice(0, 5)
}) 
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
  { title: 'شماره سفارش', key: 'order_number', sortable: true },
  { title: 'خریدار', key: 'buyer_username', sortable: true },
  { title: 'مبلغ', key: 'total_amount', sortable: true },
  { title: 'وضعیت', key: 'status', sortable: true },
  { title: 'تاریخ', key: 'created_at', sortable: true }
])

const reviewHeaders = ref([
  { title: 'محصول', key: 'product', sortable: true },
  { title: 'نویسنده', key: 'author', sortable: true },
  { title: 'امتیاز', key: 'rating', sortable: true },
  { title: 'نظر', key: 'comment', sortable: false },
  { title: 'تاریخ', key: 'created_at', sortable: true }
])

// Data loading functions
const loadDashboardData = async () => {
  loading.value = true
  try {
    const response = await sellerApi.getSellerDashboard()
    dashboardData.value = response
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
    showSnackbar('خطا در بارگذاری اطلاعات داشبورد', 'error')
  } finally {
    loading.value = false
  }
}

const loadOrders = async () => {
  loadingOrders.value = true
  try {
    const response = await sellerApi.getSellerOrders()
    orders.value = response
    recentOrders.value = response.slice(0, 5)
  } catch (error) {
    console.error('Failed to load orders:', error)
    showSnackbar('خطا در بارگذاری سفارشات', 'error')
  } finally {
    loadingOrders.value = false
  }
}

const loadReviews = async () => {
  loadingReviews.value = true
  try {
    const response = await sellerApi.getSellerReviews()
    reviews.value = response
  } catch (error) {
    console.error('Failed to load reviews:', error)
    showSnackbar('خطا در بارگذاری نظرات', 'error')
  } finally {
    loadingReviews.value = false
  }
}

const loadChatRooms = async () => {
  loadingChats.value = true
  try {
    const response = await useApiFetch<any[]>('chat/vendor/rooms/')
    chatRooms.value = response || []
    unreadChatsCount.value = chatRooms.value.reduce((sum, room) => sum + (room.unread_count || 0), 0)
  } catch (error) {
    console.error('Failed to load chat rooms:', error)
    showSnackbar('خطا در بارگذاری گفتگوها', 'error')
  } finally {
    loadingChats.value = false
  }
}

const updateProfile = async () => {
  saving.value = true
  try {
    await authStore.updateProfile(profileData.value)
    showSnackbar('پروفایل با موفقیت به‌روزرسانی شد', 'success')
    // Recalculate profile score after update
    calculateProfileScore()
  } catch (error: any) {
    console.error('Failed to update profile:', error)
    showSnackbar(error?.message || 'خطا در به‌روزرسانی پروفایل', 'error')
  } finally {
    saving.value = false
  }
}

const calculateProfileScore = () => {
  let score = 0
  const metrics: any[] = []
  const tips: string[] = []

  if (profileData.value.first_name) {
    score += 10
    metrics.push({ label: 'نام', completed: true })
  } else {
    metrics.push({ label: 'نام', completed: false })
    tips.push('نام خود را وارد کنید')
  }

  if (profileData.value.last_name) {
    score += 10
    metrics.push({ label: 'نام خانوادگی', completed: true })
  } else {
    metrics.push({ label: 'نام خانوادگی', completed: false })
    tips.push('نام خانوادگی خود را وارد کنید')
  }

  if (profileData.value.email) {
    score += 20
    metrics.push({ label: 'ایمیل', completed: true })
  } else {
    metrics.push({ label: 'ایمیل', completed: false })
    tips.push('ایمیل خود را وارد کنید')
  }

  if (profileData.value.phone) {
    score += 20
    metrics.push({ label: 'تلفن', completed: true })
  } else {
    metrics.push({ label: 'تلفن', completed: false })
    tips.push('شماره تلفن خود را وارد کنید')
  }

  profileScore.value = score
  profileMetrics.value = metrics
  profileTips.value = tips
}

const showSnackbar = (message: string, color = 'success') => {
  snackbarMessage.value = message
  snackbarColor.value = color
  snackbar.value = true
}

// Watch tab changes to load data
watch(tab, (newTab) => {
  navigateTo(`/seller/dashboard?tab=${newTab}`, { replace: true })
  
  if (newTab === 'orders' && orders.value.length === 0) {
    loadOrders()
  } else if (newTab === 'reviews' && reviews.value.length === 0) {
    loadReviews()
  } else if (newTab === 'chats' && chatRooms.value.length === 0) {
    loadChatRooms()
  }
})

// Gamification: Hydrate store on mount
onMounted(async () => {
  // Load user profile data
  if (authStore.user) {
    profileData.value = {
      first_name: authStore.user.first_name || '',
      last_name: authStore.user.last_name || '',
      email: authStore.user.email || '',
      phone: authStore.user.profile?.phone || ''
    }
    calculateProfileScore()
  }

  // Load dashboard data
  await loadDashboardData()
  await loadOrders()
  await loadReviews()
  await loadChatRooms()

  // Load gamification data
  try {
    await gamificationStore.hydrate()
  } catch (error) {
    console.warn('Failed to load gamification data', error)
  }

  // Auto-refresh chat rooms every 30 seconds
  setInterval(() => {
    if (tab.value === 'chats') {
      loadChatRooms()
    }
  }, 30000)
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

