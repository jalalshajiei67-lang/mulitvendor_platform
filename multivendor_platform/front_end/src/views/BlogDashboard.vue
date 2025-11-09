<template>
  <div dir="rtl" class="blog-admin-dashboard-wrapper">
    <AdminSidebar
      :drawer="drawer"
      :rail="rail"
      :is-mobile="isMobile"
      :active-view="sidebarActiveView"
      :user="authStore.user"
      @update:drawer="drawer = $event"
      @update:rail="rail = $event"
      @navigate="handleSidebarAction"
      @create-product="() => handleSidebarAction('products-create')"
      @create-blog-post="() => handleSidebarAction('blog-create')"
    />

    <v-app-bar
      :elevation="2"
      color="primary"
      class="admin-header"
      fixed
    >
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

      <v-app-bar-nav-icon
        v-if="isMobile"
        @click="drawer = !drawer"
        class="hamburger-btn"
      ></v-app-bar-nav-icon>

      <v-menu location="bottom end">
        <template #activator="{ props }">
          <v-btn icon v-bind="props" variant="text">
            <v-avatar size="32">
              <v-icon>mdi-account</v-icon>
            </v-avatar>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="handleLogout">
            <template #prepend>
              <v-icon>mdi-logout</v-icon>
            </template>
            <v-list-item-title>خروج</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <div
      class="blog-admin-main"
      :style="mainContentStyle"
    >
      <v-container fluid class="pa-4">
        <div class="blog-dashboard-content">
          <div class="blog-dashboard" dir="rtl">
            <div class="container">
              <!-- Dashboard Header -->
              <div class="dashboard-header">
                <h1>{{ t('blog') }} {{ t('dashboard') }}</h1>
                <div class="header-actions">
                  <button @click="createNewPost" class="btn btn-primary">
                    <i class="fas fa-plus"></i>
                    {{ t('newPost') }}
                  </button>
                  <button @click="showCreateCategory = true" class="btn btn-secondary">
                    <i class="fas fa-tag"></i>
                    {{ t('newCategory') }}
                  </button>
                </div>
              </div>

              <!-- Dashboard Stats -->
              <div class="dashboard-stats">
                <div class="stat-card">
                  <div class="stat-icon">
                    <i class="fas fa-newspaper"></i>
                  </div>
                  <div class="stat-content">
                    <h3>{{ myPosts.length }}</h3>
                    <p>{{ t('totalPosts') }}</p>
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-icon">
                    <i class="fas fa-eye"></i>
                  </div>
                  <div class="stat-content">
                    <h3>{{ totalViews }}</h3>
                    <p>{{ t('totalViews') }}</p>
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-icon">
                    <i class="fas fa-comment"></i>
                  </div>
                  <div class="stat-content">
                    <h3>{{ totalComments }}</h3>
                    <p>{{ t('totalComments') }}</p>
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-icon">
                    <i class="fas fa-tag"></i>
                  </div>
                  <div class="stat-content">
                    <h3>{{ categories.length }}</h3>
                    <p>{{ t('categories') }}</p>
                  </div>
                </div>
              </div>

              <!-- Dashboard Tabs -->
              <div class="dashboard-tabs">
                <button 
                  @click="activeTab = 'posts'"
                  :class="['tab-btn', { active: activeTab === 'posts' }]"
                >
                  <i class="fas fa-newspaper"></i>
                  {{ t('myPosts') }}
                </button>
                <button 
                  @click="activeTab = 'categories'"
                  :class="['tab-btn', { active: activeTab === 'categories' }]"
                >
                  <i class="fas fa-tag"></i>
                  {{ t('categories') }}
                </button>
              </div>

              <!-- Posts Tab -->
              <div v-if="activeTab === 'posts'" class="tab-content">
                <div class="posts-header">
                  <h2>{{ t('myPosts') }}</h2>
                  <div class="posts-filters">
                    <select v-model="postFilter" @change="filterPosts">
                      <option value="all">{{ t('allPosts') }}</option>
                      <option value="published">{{ t('published') }}</option>
                      <option value="draft">{{ t('draft') }}</option>
                      <option value="archived">{{ t('archived') }}</option>
                    </select>
                    <input 
                      v-model="searchQuery" 
                      @input="searchPosts"
                      type="text" 
                      :placeholder="t('search') + '...'"
                      class="search-input"
                    />
                  </div>
                </div>

                <!-- Loading State -->
                <div v-if="loading" class="loading-state">
                  <div class="spinner"></div>
                  <p>{{ t('loadingPosts') }}</p>
                </div>

                <!-- Posts Table -->
                <div v-else class="posts-table">
                  <div class="table-header">
                    <div class="col-title">{{ t('postTitle') }}</div>
                    <div class="col-category">{{ t('category') }}</div>
                    <div class="col-status">{{ t('status') }}</div>
                    <div class="col-stats">{{ t('views') }}</div>
                    <div class="col-date">{{ t('date') }}</div>
                    <div class="col-actions">{{ t('actions') }}</div>
                  </div>
                  
                  <div v-if="filteredPosts.length > 0" class="table-body">
                    <div 
                      v-for="post in filteredPosts" 
                      :key="post.id"
                      class="table-row"
                    >
                      <div class="col-title">
                        <div class="post-title">
                          <h4>{{ post.title }}</h4>
                          <p class="post-excerpt">{{ post.excerpt }}</p>
                        </div>
                      </div>
                      <div class="col-category">
                        <span class="category-badge" :style="{ backgroundColor: post.category_color }">
                          {{ post.category_name }}
                        </span>
                      </div>
                      <div class="col-status">
                        <span :class="['status-badge', post.status]">
                          {{ post.status }}
                        </span>
                      </div>
                      <div class="col-stats">
                        <span class="views">{{ post.view_count }}</span>
                      </div>
                      <div class="col-date">
                        {{ formatDate(post.created_at) }}
                      </div>
                      <div class="col-actions">
                        <div class="action-buttons">
                          <button @click="viewPost(post.slug)" class="btn-icon" :title="t('view')">
                            <i class="fas fa-eye"></i>
                          </button>
                          <button @click="editPost(post.slug)" class="btn-icon" :title="t('edit')">
                            <i class="fas fa-edit"></i>
                          </button>
                          <button @click="deletePost(post)" class="btn-icon danger" :title="t('delete')">
                            <i class="fas fa-trash"></i>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Empty State -->
                  <div v-else class="empty-state">
                    <i class="fas fa-newspaper"></i>
                    <h3>{{ t('noPostsFound') }}</h3>
                    <p>{{ t('noBlogPostsAvailable') }}</p>
                    <button @click="createNewPost" class="btn btn-primary">
                      {{ t('createNewPost') }}
                    </button>
                  </div>
                </div>
              </div>

              <!-- Categories Tab -->
              <div v-if="activeTab === 'categories'" class="tab-content">
                <div class="categories-header">
                  <h2>{{ t('categories') }}</h2>
                </div>

                <!-- Categories Grid -->
                <div class="categories-grid">
                  <div 
                    v-for="category in categories" 
                    :key="category.id"
                    class="category-card"
                  >
                    <div class="category-header">
                      <div class="category-color" :style="{ backgroundColor: category.color }"></div>
                      <h3>{{ category.name }}</h3>
                      <div class="category-actions">
                        <button @click="editCategory(category)" class="btn-icon" :title="t('edit')">
                          <i class="fas fa-edit"></i>
                        </button>
                        <button @click="deleteCategory(category)" class="btn-icon danger" :title="t('delete')">
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </div>
                    <p class="category-description">{{ category.description || t('noDescription') }}</p>
                    <div class="category-stats">
                      <span class="post-count">{{ category.post_count }} {{ t('posts') }}</span>
                      <span v-if="category.linked_product_category" class="linked-category">
                        {{ t('linkedToProductCategory') }}: {{ category.linked_product_category.name }}
                      </span>
                    </div>
                  </div>

                  <!-- Empty State -->
                  <div v-if="categories.length === 0" class="empty-state">
                    <i class="fas fa-tag"></i>
                    <h3>{{ t('noCategoriesFound') }}</h3>
                    <p>{{ t('createNewCategory') }}</p>
                    <button @click="showCreateCategory = true" class="btn btn-primary">
                      {{ t('createCategory') }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </v-container>
    </div>

    <v-bottom-navigation
      v-if="isMobile"
      :model-value="mobileNav"
      @update:model-value="handleMobileNav"
      color="primary"
      class="mobile-bottom-nav"
    >
      <v-btn value="blog">
        <v-icon>mdi-newspaper</v-icon>
        <span>پست‌ها</span>
      </v-btn>
      <v-btn value="categories">
        <v-icon>mdi-tag</v-icon>
        <span>دسته‌بندی‌ها</span>
      </v-btn>
      <v-btn value="create">
        <v-icon>mdi-plus-circle</v-icon>
        <span>افزودن</span>
      </v-btn>
    </v-bottom-navigation>

    <!-- Create/Edit Category Modal -->
    <div v-if="showCreateCategory || showEditCategory" class="modal-overlay" @click="closeModals">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ showEditCategory ? t('editCategory') : t('createNewCategory') }}</h2>
          <button @click="closeModals" class="close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <form @submit.prevent="submitCategory" class="modal-body">
          <div class="form-group">
            <label>{{ t('categoryName') }} *</label>
            <input 
              v-model="categoryForm.name" 
              type="text" 
              required 
              :placeholder="t('enterCategoryName')"
            />
          </div>

          <div class="form-group">
            <label>{{ t('categoryDescription') }}</label>
            <textarea 
              v-model="categoryForm.description" 
              :placeholder="t('categoryDescriptionPlaceholder')"
              rows="3"
            ></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>{{ t('categoryColor') }}</label>
              <input 
                v-model="categoryForm.color" 
                type="color" 
                class="color-input"
              />
            </div>
            <div class="form-group">
              <label>{{ t('linkedToProductCategory') }}</label>
              <select v-model="categoryForm.linked_product_category_id">
                <option value="">{{ t('none') }}</option>
                <option v-for="productCategory in productCategories" :key="productCategory.id" :value="productCategory.id">
                  {{ productCategory.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>
              <input v-model="categoryForm.is_active" type="checkbox" />
              {{ t('active') }}
            </label>
          </div>

          <div class="modal-footer">
            <button type="button" @click="closeModals" class="btn btn-secondary">
              {{ t('cancel') }}
            </button>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              <i v-if="submitting" class="fas fa-spinner fa-spin"></i>
              {{ showEditCategory ? t('updateCategory') : t('createCategory') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useDisplay } from 'vuetify'
import { useAuthStore } from '@/stores/auth'
import { useBlogStore } from '@/stores/blog'
import { useCategoryStore } from '@/stores/modules/categoryStore'
import AdminSidebar from '@/components/admin/AdminSidebar.vue'

export default {
  name: 'BlogDashboard',
  components: {
    AdminSidebar
  },
  setup() {
    const router = useRouter()
    const blogStore = useBlogStore()
    const categoryStore = useCategoryStore()
    const authStore = useAuthStore()
    const { mdAndDown } = useDisplay()
    
    // State
    const drawer = ref(!mdAndDown.value)
    const rail = ref(false)
    const isMobile = computed(() => mdAndDown.value)
    const activeTab = ref('posts')
    const sidebarActiveView = ref('blog')
    const mobileNav = ref('blog')
    const showCreatePost = ref(false)
    const showEditPost = ref(false)
    const showCreateCategory = ref(false)
    const showEditCategory = ref(false)
    const postFilter = ref('all')
    const searchQuery = ref('')
    const submitting = ref(false)
    
    watch(isMobile, (newVal) => {
      drawer.value = !newVal
    })
    
    // Forms
    const postForm = ref({
      title: '',
      excerpt: '',
      content: '',
      category: '',
      status: 'draft',
      is_featured: false,
      meta_title: '',
      meta_description: '',
      featured_image: null
    })
    
    const categoryForm = ref({
      name: '',
      description: '',
      color: '#007bff',
      linked_product_category_id: '',
      is_active: true
    })
    
    // Computed
    const myPosts = computed(() => blogStore.posts)
    const categories = computed(() => blogStore.categories)
    const productCategories = computed(() => categoryStore.categories)
    const loading = computed(() => blogStore.loading)
    const t = computed(() => blogStore.t)
    
    const totalViews = computed(() => {
      return myPosts.value.reduce((sum, post) => sum + post.view_count, 0)
    })
    
    const totalComments = computed(() => {
      return myPosts.value.reduce((sum, post) => sum + post.comment_count, 0)
    })
    
    const filteredPosts = computed(() => {
      let posts = myPosts.value
      
      // Filter by status
      if (postFilter.value !== 'all') {
        posts = posts.filter(post => post.status === postFilter.value)
      }
      
      // Search filter
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        posts = posts.filter(post => 
          post.title.toLowerCase().includes(query) ||
          post.excerpt.toLowerCase().includes(query)
        )
      }
      
      return posts
    })
    
    const mainContentStyle = computed(() => ({
      paddingRight: !isMobile.value && drawer.value ? (rail.value ? '64px' : '271px') : '0',
      paddingBottom: isMobile.value ? '80px' : '0'
    }))
    
    const adminViewMap = {
      dashboard: 'dashboard',
      users: 'users',
      products: 'products',
      departments: 'departments',
      categories: 'categories',
      subcategories: 'subcategories',
      activities: 'activities',
      rfqs: 'rfqs'
    }
    
    watch(activeTab, (tab) => {
      if (tab === 'posts') {
        sidebarActiveView.value = 'blog'
        if (mobileNav.value !== 'blog') {
          mobileNav.value = 'blog'
        }
      } else if (tab === 'categories') {
        sidebarActiveView.value = 'blog-categories'
        if (mobileNav.value !== 'categories') {
          mobileNav.value = 'categories'
        }
      }
    }, { immediate: true })
    
    // Methods
    const scrollToTop = () => {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    const closeDrawerOnMobile = () => {
      if (isMobile.value) {
        drawer.value = false
      }
    }

    const handleSidebarAction = (action) => {
      if (adminViewMap[action]) {
        const targetView = adminViewMap[action]
        sidebarActiveView.value = targetView
        const query = targetView && targetView !== 'dashboard' ? { view: targetView } : {}
        router.push({ path: '/admin/dashboard', query }).catch(() => {})
        scrollToTop()
        closeDrawerOnMobile()
        return
      }

      if (action === 'products-create') {
        sidebarActiveView.value = 'products'
        router.push('/admin/dashboard/products/new').catch(() => {})
        closeDrawerOnMobile()
        return
      }

      if (action === 'blog' || action === 'blog-posts') {
        activeTab.value = 'posts'
        sidebarActiveView.value = 'blog'
        mobileNav.value = 'blog'
        scrollToTop()
        closeDrawerOnMobile()
        return
      }

      if (action === 'blog-create') {
        sidebarActiveView.value = 'blog'
        createNewPost()
        closeDrawerOnMobile()
        return
      }

      if (action === 'blog-categories') {
        activeTab.value = 'categories'
        sidebarActiveView.value = 'blog-categories'
        mobileNav.value = 'categories'
        scrollToTop()
        closeDrawerOnMobile()
      }
    }

    const handleMobileNav = (value) => {
      if (value === 'blog') {
        activeTab.value = 'posts'
        sidebarActiveView.value = 'blog'
        mobileNav.value = 'blog'
        scrollToTop()
      } else if (value === 'categories') {
        activeTab.value = 'categories'
        sidebarActiveView.value = 'blog-categories'
        mobileNav.value = 'categories'
        scrollToTop()
      } else if (value === 'create') {
        sidebarActiveView.value = 'blog'
        createNewPost()
        mobileNav.value = 'blog'
      }
    }
    
    const fetchData = async () => {
      await Promise.all([
        blogStore.fetchMyPosts(),
        blogStore.fetchCategories(),
        categoryStore.fetchCategories()
      ])
    }
    
    const filterPosts = () => {
      // Filter is handled by computed property
    }
    
    const searchPosts = () => {
      // Search is handled by computed property
    }
    
    const viewPost = (slug) => {
      router.push({ name: 'BlogDetail', params: { slug } })
    }
    
    const createNewPost = () => {
      router.push({ name: 'CreateBlogPost' })
    }
    
    const editPost = (slug) => {
      router.push({ name: 'EditBlogPost', params: { slug } })
    }
    
    const deletePost = async (post) => {
      if (confirm(t.value('confirmDelete') + ` "${post.title}"?`)) {
        try {
          await blogStore.deletePost(post.slug)
          await fetchData()
        } catch (error) {
          console.error('Error deleting post:', error)
        }
      }
    }
    
    const editCategory = (category) => {
      categoryForm.value = {
        name: category.name,
        description: category.description || '',
        color: category.color,
        linked_product_category_id: category.linked_product_category?.id || '',
        is_active: category.is_active
      }
      showEditCategory.value = true
    }
    
    const deleteCategory = async (category) => {
      if (confirm(t.value('confirmDelete') + ` "${category.name}"?`)) {
        try {
          await blogStore.deleteCategory(category.slug)
          await fetchData()
        } catch (error) {
          console.error('Error deleting category:', error)
        }
      }
    }
    
    const handleImageUpload = (event) => {
      const file = event.target.files[0]
      if (file) {
        postForm.value.featured_image = file
      }
    }
    
    const submitPost = async () => {
      submitting.value = true
      try {
        const formData = new FormData()
        Object.keys(postForm.value).forEach(key => {
          if (postForm.value[key] !== null && postForm.value[key] !== '') {
            formData.append(key, postForm.value[key])
          }
        })
        
        if (showEditPost.value) {
          // Update existing post
          const post = myPosts.value.find(p => p.slug === post.slug)
          await blogStore.updatePost(post.slug, formData)
        } else {
          // Create new post
          await blogStore.createPost(formData)
        }
        
        closeModals()
        await fetchData()
      } catch (error) {
        console.error('Error submitting post:', error)
      } finally {
        submitting.value = false
      }
    }
    
    const submitCategory = async () => {
      submitting.value = true
      try {
        const data = { ...categoryForm.value }
        if (!data.linked_product_category_id) {
          delete data.linked_product_category_id
        }
        
        if (showEditCategory.value) {
          // Update existing category
          const category = categories.value.find(c => c.slug === category.slug)
          await blogStore.updateCategory(category.slug, data)
        } else {
          // Create new category
          await blogStore.createCategory(data)
        }
        
        closeModals()
        await fetchData()
      } catch (error) {
        console.error('Error submitting category:', error)
      } finally {
        submitting.value = false
      }
    }
    
    const closeModals = () => {
      showCreatePost.value = false
      showEditPost.value = false
      showCreateCategory.value = false
      showEditCategory.value = false
      
      // Reset forms
      postForm.value = {
        title: '',
        excerpt: '',
        content: '',
        category: '',
        status: 'draft',
        is_featured: false,
        meta_title: '',
        meta_description: '',
        featured_image: null
      }
      
      categoryForm.value = {
        name: '',
        description: '',
        color: '#007bff',
        linked_product_category_id: '',
        is_active: true
      }
    }
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
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
      fetchData()
    })
    
    return {
      authStore,
      drawer,
      rail,
      isMobile,
      activeTab,
      sidebarActiveView,
      mobileNav,
      showCreatePost,
      showEditPost,
      showCreateCategory,
      showEditCategory,
      postFilter,
      searchQuery,
      submitting,
      mainContentStyle,
      postForm,
      categoryForm,
      myPosts,
      categories,
      productCategories,
      loading,
      totalViews,
      totalComments,
      filteredPosts,
      t,
      handleSidebarAction,
      handleMobileNav,
      filterPosts,
      searchPosts,
      viewPost,
      editPost,
      deletePost,
      editCategory,
      deleteCategory,
      handleImageUpload,
      submitPost,
      submitCategory,
      closeModals,
      formatDate,
      handleLogout
    }
  }
}
</script>

<style scoped>
.blog-admin-dashboard-wrapper {
  min-height: 100vh;
  background-color: #f8f9fa;
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

.blog-admin-main {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding-top: 64px;
  transition: padding-right 0.3s ease;
}

.blog-dashboard-content {
  min-height: calc(100vh - 64px);
}

.mobile-bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  direction: rtl;
}

.blog-dashboard {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding: 2rem 0;
  direction: rtl;
  text-align: right;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-direction: row-reverse;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
}

.header-actions {
  display: flex;
  gap: 1rem;
  flex-direction: row-reverse;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  flex-direction: row-reverse;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #545b62;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-direction: row-reverse;
}

.stat-icon {
  width: 50px;
  height: 50px;
  background-color: #007bff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.stat-content h3 {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.stat-content p {
  color: #6c757d;
  margin: 0;
}

.dashboard-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #dee2e6;
  flex-direction: row-reverse;
}

.tab-btn {
  background: none;
  border: none;
  padding: 1rem 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6c757d;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
  flex-direction: row-reverse;
}

.tab-btn:hover {
  color: #007bff;
}

.tab-btn.active {
  color: #007bff;
  border-bottom-color: #007bff;
}

.tab-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.posts-header, .categories-header {
  padding: 1.5rem;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: row-reverse;
}

.posts-filters {
  display: flex;
  gap: 1rem;
  flex-direction: row-reverse;
}

.search-input {
  padding: 0.5rem;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  width: 200px;
}

.posts-table {
  overflow-x: auto;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background-color: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #dee2e6;
  align-items: center;
}

.post-title h4 {
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
}

.post-excerpt {
  margin: 0;
  color: #6c757d;
  font-size: 0.9rem;
}

.category-badge {
  display: inline-block;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: capitalize;
}

.status-badge.published {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.draft {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.archived {
  background-color: #f8d7da;
  color: #721c24;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  flex-direction: row-reverse;
}

.btn-icon {
  background: none;
  border: 1px solid #dee2e6;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  color: #6c757d;
  transition: all 0.3s ease;
}

.btn-icon:hover {
  background-color: #f8f9fa;
}

.btn-icon.danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-icon.danger:hover {
  background-color: #dc3545;
  color: white;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  padding: 1.5rem;
}

.category-card {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1.5rem;
  transition: box-shadow 0.3s ease;
}

.category-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.category-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-direction: row-reverse;
}

.category-color {
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.category-header h3 {
  flex: 1;
  margin: 0;
  color: #2c3e50;
}

.category-actions {
  display: flex;
  gap: 0.5rem;
  flex-direction: row-reverse;
}

.category-description {
  color: #6c757d;
  margin-bottom: 1rem;
}

.category-stats {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #6c757d;
  flex-direction: row-reverse;
}

.linked-category {
  font-style: italic;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #dee2e6;
  flex-direction: row-reverse;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
}

.modal-body {
  padding: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  font-family: inherit;
}

.color-input {
  height: 40px;
  padding: 0;
  border: none;
  border-radius: 4px;
}

.modal-footer {
  display: flex;
  justify-content: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #dee2e6;
  flex-direction: row-reverse;
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .header-actions {
    flex-direction: column;
  }
  
  .dashboard-stats {
    grid-template-columns: 1fr;
  }
  
  .table-header,
  .table-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .posts-filters {
    flex-direction: column;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .search-input {
    width: 100%;
  }
}
</style>
