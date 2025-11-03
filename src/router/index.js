// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import pinia from '@/stores'
import config from '@/config'
import ProductList from '../views/ProductList.vue'
import ProductDetail from '../views/ProductDetail.vue'
import ProductForm from '../views/ProductForm.vue'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import SiteMap from '../views/SiteMap.vue'
import ApiTest from '../views/ApiTest.vue'
import BlogList from '../views/BlogList.vue'
import BlogDetail from '../views/BlogDetail.vue'
import BlogDashboard from '../views/BlogDashboard.vue'
import BlogForm from '../views/BlogForm.vue'
import DepartmentList from '../views/DepartmentList.vue'
import DepartmentDetail from '../views/DepartmentDetail.vue'
import CategoryDetail from '../views/CategoryDetail.vue'
import SubcategoryDetail from '../views/SubcategoryDetail.vue'
import SupplierList from '../views/SupplierList.vue'
import SupplierDetail from '../views/SupplierDetail.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import BuyerDashboard from '../views/BuyerDashboard.vue'
import SellerDashboard from '../views/SellerDashboard.vue'
import AdminDashboard from '../views/AdminDashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/sitemap',
      name: 'SiteMap',
      component: SiteMap
    },
    {
      path: '/api-test',
      name: 'ApiTest',
      component: ApiTest
    },
    // Authentication Routes
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
      meta: { guestOnly: true }
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterView,
      meta: { guestOnly: true }
    },
    // Dashboard Routes
    {
      path: '/buyer/dashboard',
      name: 'BuyerDashboard',
      component: BuyerDashboard,
      meta: { requiresAuth: true, requiresBuyer: true }
    },
    {
      path: '/seller/dashboard',
      name: 'SellerDashboard',
      component: SellerDashboard,
      meta: { requiresAuth: true, requiresSeller: true }
    },
    {
      path: '/admin/dashboard',
      name: 'AdminDashboard',
      component: AdminDashboard,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    // Department Routes
    {
      path: '/departments',
      name: 'DepartmentList',
      component: DepartmentList
    },
    {
      path: '/departments/:slug',
      name: 'DepartmentDetail',
      component: DepartmentDetail,
      props: true
    },
    // Category Routes
    {
      path: '/categories/:slug',
      name: 'CategoryDetail',
      component: CategoryDetail,
      props: true
    },
    // Subcategory Routes
    {
      path: '/subcategories/:slug',
      name: 'SubcategoryDetail',
      component: SubcategoryDetail,
      props: true
    },
    // Supplier Routes
    {
      path: '/suppliers',
      name: 'SupplierList',
      component: SupplierList
    },
    {
      path: '/suppliers/:id',
      name: 'SupplierDetail',
      component: SupplierDetail,
      props: true
    },
    // Product Routes
    {
      path: '/products',
      name: 'ProductList',
      component: ProductList
    },
    {
      path: '/my-products',
      name: 'MyProducts',
      component: ProductList,
      meta: { requiresAuth: true, showOnlyMyProducts: true }
    },
    {
      path: '/products/new',
      name: 'CreateProduct',
      component: ProductForm,
      meta: { requiresAuth: true }
    },
    {
      path: '/products/:id',
      name: 'ProductDetail',
      component: ProductDetail,
      props: true
    },
    {
      path: '/products/:id/edit',
      name: 'EditProduct',
      component: ProductForm,
      props: true,
      meta: { requiresAuth: true }
    },
    // Blog Routes
    {
      path: '/blog',
      name: 'BlogList',
      component: BlogList
    },
    {
      path: '/blog/:slug',
      name: 'BlogDetail',
      component: BlogDetail,
      props: true
    },
    {
      path: '/blog/dashboard',
      name: 'BlogDashboard',
      component: BlogDashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/blog/new',
      name: 'CreateBlogPost',
      component: BlogForm,
      meta: { requiresAuth: true }
    },
    {
      path: '/blog/:slug/edit',
      name: 'EditBlogPost',
      component: BlogForm,
      props: true,
      meta: { requiresAuth: true }
    }
  ]
})

// Navigation guard to check authentication and roles
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore(pinia)

  // Redirect authenticated users away from guest-only pages
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    if (authStore.isAdmin) {
      // Redirect admins to Django admin panel
      window.location.href = config.djangoAdminUrl
      return
    } else if (authStore.isSeller) {
      next('/seller/dashboard')
    } else if (authStore.isBuyer) {
      next('/buyer/dashboard')
    } else {
      next('/')
    }
    return
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  // Check role-based access
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/')
    return
  }

  if (to.meta.requiresSeller && !authStore.isSeller) {
    next('/')
    return
  }

  if (to.meta.requiresBuyer && !authStore.isBuyer) {
    next('/')
    return
  }

  next()
})

export default router
