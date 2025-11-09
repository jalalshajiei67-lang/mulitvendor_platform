<template>
  <v-navigation-drawer
    v-model="drawerProxy"
    :permanent="!isMobile"
    :temporary="isMobile"
    :rail="drawerRail"
    :width="271"
    location="right"
    class="admin-sidebar"
    fixed
    dir="rtl"
  >
    <div class="sidebar-header">
      <v-list-item
        v-if="!drawerRail || isMobile"
        prepend-avatar="/indexo.jpg"
        :title="user?.username || 'Admin'"
        :subtitle="user?.email || ''"
      ></v-list-item>
      <v-btn
        v-if="!isMobile"
        icon
        variant="text"
        @click="toggleRail"
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
        @click="handleNavigate('dashboard')"
      ></v-list-item>

      <v-list-item
        prepend-icon="mdi-account-multiple"
        title="مدیریت کاربران"
        value="users"
        :active="activeView === 'users'"
        @click="handleNavigate('users')"
      ></v-list-item>

      <v-list-group value="products">
        <template #activator="{ props }">
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
          @click="handleNavigate('products')"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-plus-circle"
          title="افزودن محصول"
          value="products-create"
          @click="handleCreateProduct"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-domain"
          title="مدیریت دپارتمان‌ها"
          value="departments"
          :active="activeView === 'departments'"
          @click.stop="handleNavigate('departments')"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-folder"
          title="مدیریت دسته‌بندی‌ها"
          value="categories"
          :active="activeView === 'categories'"
          @click.stop="handleNavigate('categories')"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-folder-multiple"
          title="مدیریت زیردسته‌ها"
          value="subcategories"
          :active="activeView === 'subcategories'"
          @click.stop="handleNavigate('subcategories')"
        ></v-list-item>
      </v-list-group>

      <v-list-item
        prepend-icon="mdi-history"
        title="گزارش فعالیت‌ها"
        value="activities"
        :active="activeView === 'activities'"
        @click="handleNavigate('activities')"
      ></v-list-item>

      <v-list-item
        prepend-icon="mdi-file-document-edit-outline"
        title="درخواست‌های استعلام قیمت"
        value="rfqs"
        :active="activeView === 'rfqs'"
        @click="handleNavigate('rfqs')"
      ></v-list-item>

      <v-list-group value="blog">
        <template #activator="{ props }">
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
          @click="handleNavigate('blog')"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-plus-circle"
          title="افزودن پست"
          value="blog-create"
          @click="handleCreateBlogPost"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-tag"
          title="مدیریت دسته‌بندی‌ها"
          value="blog-categories"
          :active="activeView === 'blog-categories'"
          @click="handleNavigate('blog-categories')"
        ></v-list-item>
      </v-list-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  drawer: {
    type: Boolean,
    default: true
  },
  rail: {
    type: Boolean,
    default: false
  },
  isMobile: {
    type: Boolean,
    default: false
  },
  activeView: {
    type: String,
    default: ''
  },
  user: {
    type: Object,
    default: null
  }
})

const emit = defineEmits([
  'update:drawer',
  'update:rail',
  'navigate',
  'create-product',
  'create-blog-post'
])

const drawerProxy = computed({
  get: () => props.drawer,
  set: (value) => emit('update:drawer', value)
})

const drawerRail = computed(() => (props.rail && !props.isMobile) || false)

const toggleRail = () => {
  emit('update:rail', !props.rail)
}

const handleNavigate = (view) => {
  emit('navigate', view)
}

const handleCreateProduct = () => {
  emit('create-product')
}

const handleCreateBlogPost = () => {
  emit('create-blog-post')
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
</style>

