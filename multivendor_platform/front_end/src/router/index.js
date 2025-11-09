// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import head from '@/plugins/head'
//import config from '@/config'
import ProductList from '../views/ProductList.vue'
import ProductDetail from '../views/ProductDetail.vue'
import ProductForm from '../views/ProductForm.vue'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import ContactUs from '../views/ContactUs.vue'
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
      component: HomeView,
      meta: {
        pageTitle: 'صفحه اصلی',
        pageDescription: 'ایندکسو برای اتصال تامین‌کنندگان و خریداران ماشین‌آلات صنعتی با تجربه کاربری فارسی و راست‌چین.'
      }
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
      meta: {
        pageTitle: 'درباره ما',
        pageDescription: 'آشنایی با ماموریت و چشم‌انداز ایندکسو در تحول خرید و فروش تجهیزات صنعتی.'
      }
    },
    {
      path: '/contact-us',
      name: 'ContactUs',
      component: ContactUs,
      meta: {
        pageTitle: 'تماس با ما',
        pageDescription: 'از طریق فرم، تلفن یا شبکه‌های اجتماعی با تیم پشتیبانی ایندکسو در ارتباط باشید.'
      }
    },
    {
      path: '/sitemap',
      name: 'SiteMap',
      component: SiteMap,
      meta: {
        pageTitle: 'نقشه سایت',
        pageDescription: 'دسترسی سریع به صفحات کلیدی ایندکسو برای خریداران و تامین‌کنندگان.'
      }
    },
    {
      path: '/api-test',
      name: 'ApiTest',
      component: ApiTest,
      meta: {
        pageTitle: 'آزمایش رابط برنامه‌نویسی',
        pageDescription: 'ابزار تست API برای توسعه‌دهندگان و همکاران فنی ایندکسو.'
      }
    },
    // Authentication Routes
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
      meta: {
        guestOnly: true,
        pageTitle: 'ورود به حساب کاربری',
        pageDescription: 'برای مدیریت سفارش‌ها و محصولات خود در ایندکسو وارد شوید.'
      }
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterView,
      meta: {
        guestOnly: true,
        pageTitle: 'ثبت‌نام در ایندکسو',
        pageDescription: 'در چند دقیقه حساب فروشنده یا خریدار خود را ایجاد کنید و به تامین‌کنندگان معتبر در ایندکسو دسترسی پیدا کنید.'
      }
    },
    // Dashboard Routes
    {
      path: '/buyer/dashboard',
      name: 'BuyerDashboard',
      component: BuyerDashboard,
      meta: {
        requiresAuth: true,
        requiresBuyer: true,
        pageTitle: 'داشبورد خریداران',
        pageDescription: 'پیگیری سفارش‌ها، مدیریت درخواست‌ها و برقراری ارتباط با تامین‌کنندگان در داشبورد خریدار.'
      }
    },
    {
      path: '/seller/dashboard',
      name: 'SellerDashboard',
      component: SellerDashboard,
      meta: {
        requiresAuth: true,
        requiresSeller: true,
        pageTitle: 'داشبورد فروشندگان',
        pageDescription: 'مدیریت محصولات، سفارش‌ها و ارتباط با خریداران از طریق داشبورد فروشنده.'
      }
    },
    {
      path: '/admin/dashboard',
      name: 'AdminDashboard',
      component: AdminDashboard,
      meta: {
        requiresAuth: true,
        requiresAdmin: true,
        pageTitle: 'پنل مدیریت',
        pageDescription: 'کنترل کامل بر کاربران، محصولات و محتوای ایندکسو در پنل مدیریت.'
      },
      children: [
        {
          path: 'products/new',
          name: 'AdminCreateProduct',
          component: ProductForm,
          meta: {
            requiresAuth: true,
            requiresAdmin: true,
            pageTitle: 'ایجاد محصول جدید',
            pageDescription: 'افزودن محصول تازه به ایندکسو همراه با جزئیات کامل و تصاویر.'
          }
        },
        {
          path: 'products/:id/edit',
          name: 'AdminEditProduct',
          component: ProductForm,
          props: true,
          meta: {
            requiresAuth: true,
            requiresAdmin: true,
            pageTitle: 'ویرایش محصول',
            pageDescription: 'به‌روزرسانی مشخصات محصول برای حفظ اطلاعات دقیق و جذاب برای خریداران.'
          }
        },
        {
          path: 'blog/new',
          name: 'AdminCreateBlogPost',
          component: BlogForm,
          meta: {
            requiresAuth: true,
            requiresAdmin: true,
            pageTitle: 'ایجاد مقاله جدید',
            pageDescription: 'تولید محتوای ارزشمند برای وبلاگ ایندکسو جهت آموزش و اطلاع‌رسانی.'
          }
        },
        {
          path: 'blog/:slug/edit',
          name: 'AdminEditBlogPost',
          component: BlogForm,
          props: true,
          meta: {
            requiresAuth: true,
            requiresAdmin: true,
            pageTitle: 'ویرایش مقاله وبلاگ',
            pageDescription: 'به‌روزرسانی محتوای مقالات وبلاگ برای حفظ دقت و جذابیت مطالب.'
          }
        }
      ]
    },
    // Department Routes
    {
      path: '/departments',
      name: 'DepartmentList',
      component: DepartmentList,
      meta: {
        pageTitle: 'دسته‌بندی‌های اصلی',
        pageDescription: 'مروری بر بخش‌های اصلی ایندکسو و کشف تامین‌کنندگان تخصصی.'
      }
    },
    {
      path: '/departments/:slug',
      name: 'DepartmentDetail',
      component: DepartmentDetail,
      props: true,
      meta: {
        pageTitle: 'جزئیات بخش',
        pageDescription: 'مشاهده تامین‌کنندگان و محصولات مرتبط با بخش انتخابی در ایندکسو.'
      }
    },
    // Category Routes
    {
      path: '/categories/:slug',
      name: 'CategoryDetail',
      component: CategoryDetail,
      props: true,
      meta: {
        pageTitle: 'دسته‌بندی محصولات',
        pageDescription: 'کشف محصولات تخصصی در دسته‌بندی انتخابی با فیلترهای متنوع و محتوای فارسی.'
      }
    },
    // Subcategory Routes
    {
      path: '/subcategories/:slug',
      name: 'SubcategoryDetail',
      component: SubcategoryDetail,
      props: true,
      meta: {
        pageTitle: 'زیرشاخه محصولات',
        pageDescription: 'لیست کامل محصولات در زیرشاخه تخصصی با تجربه کاربری راست‌چین و فارسی.'
      }
    },
    // Supplier Routes
    {
      path: '/suppliers',
      name: 'SupplierList',
      component: SupplierList,
      meta: {
        pageTitle: 'تامین‌کنندگان',
        pageDescription: 'لیست تامین‌کنندگان تاییدشده در ایندکسو برای همکاری مستقیم و بدون واسطه.'
      }
    },
    {
      path: '/suppliers/:id',
      name: 'SupplierDetail',
      component: SupplierDetail,
      props: true,
      meta: {
        pageTitle: 'پروفایل تامین‌کننده',
        pageDescription: 'جزئیات تخصص، محصولات و سوابق همکاری تامین‌کننده منتخب.'
      }
    },
    // Product Routes
    {
      path: '/products',
      name: 'ProductList',
      component: ProductList,
      meta: {
        pageTitle: 'محصولات صنعتی',
        pageDescription: 'جستجو و مقایسه ماشین‌آلات صنعتی ارائه‌شده توسط تامین‌کنندگان معتبر ایرانی.'
      }
    },
    {
      path: '/my-products',
      name: 'MyProducts',
      component: ProductList,
      meta: {
        requiresAuth: true,
        showOnlyMyProducts: true,
        pageTitle: 'محصولات من',
        pageDescription: 'مدیریت و به‌روزرسانی فهرست محصولات شخصی در ایندکسو.'
      }
    },
    {
      path: '/products/new',
      name: 'CreateProduct',
      component: ProductForm,
      meta: {
        requiresAuth: true,
        pageTitle: 'افزودن محصول جدید',
        pageDescription: 'ثبت محصول تازه به همراه ویژگی‌ها، تصاویر و قیمت در چند مرحله ساده.'
      }
    },
    {
      path: '/products/:slug',
      name: 'ProductDetail',
      component: ProductDetail,
      props: true,
      meta: {
        pageTitle: 'جزئیات محصول',
        pageDescription: 'مشاهده مشخصات، تصاویر و شرایط همکاری برای محصول انتخابی.'
      }
    },
    {
      path: '/products/:id/edit',
      name: 'EditProduct',
      component: ProductForm,
      props: true,
      meta: {
        requiresAuth: true,
        pageTitle: 'ویرایش محصول',
        pageDescription: 'اصلاح اطلاعات محصول برای نمایش دقیق به خریداران تخصصی.'
      }
    },
    // Blog Routes
    {
      path: '/blog',
      name: 'BlogList',
      component: BlogList,
      meta: {
        pageTitle: 'وبلاگ ایندکسو',
        pageDescription: 'مطالب آموزشی و تحلیلی درباره صنعت، خرید تجهیزات و توسعه کسب‌وکار در ایندکسو.'
      }
    },
    {
      path: '/blog/:slug',
      name: 'BlogDetail',
      component: BlogDetail,
      props: true,
      meta: {
        pageTitle: 'جزئیات مقاله',
        pageDescription: 'مطالعه مقاله تخصصی درباره روندهای صنعت و راهکارهای خرید تجهیزات.'
      }
    },
    {
      path: '/blog/dashboard',
      name: 'BlogDashboard',
      component: BlogDashboard,
      meta: {
        requiresAuth: true,
        pageTitle: 'داشبورد وبلاگ',
        pageDescription: 'مدیریت مقالات، انتشار مطالب جدید و تحلیل عملکرد محتوا.'
      }
    },
    {
      path: '/blog/new',
      name: 'CreateBlogPost',
      component: BlogForm,
      meta: {
        requiresAuth: true,
        pageTitle: 'نوشتن مقاله جدید',
        pageDescription: 'ایجاد مقاله جدید برای آموزش و اطلاع‌رسانی به کاربران ایندکسو.'
      }
    },
    {
      path: '/blog/:slug/edit',
      name: 'EditBlogPost',
      component: BlogForm,
      props: true,
      meta: {
        requiresAuth: true,
        pageTitle: 'ویرایش مقاله',
        pageDescription: 'بازبینی و اصلاح مقاله منتشر شده برای بهبود کیفیت محتوا.'
      }
    }
  ]
})

let removeRouteHeadEntry

// Navigation guard to check authentication and roles
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Redirect authenticated users away from guest-only pages
  if ((to.meta.guestOnly && authStore.isAuthenticated)) {
    if (authStore.isAdmin) {
      // Redirect admins to Vue.js admin dashboard
      next('/admin/dashboard')
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

router.afterEach((to) => {
  if (removeRouteHeadEntry && typeof removeRouteHeadEntry === 'function') {
    removeRouteHeadEntry()
    removeRouteHeadEntry = undefined
  }

  const matchedMeta = to.matched.map((record) => record.meta || {})
  const resolveValue = (key) => {
    for (let i = matchedMeta.length - 1; i >= 0; i -= 1) {
      if (matchedMeta[i][key]) {
        return matchedMeta[i][key]
      }
    }
    return undefined
  }

  const customHead = resolveValue('head') || {}
  const pageTitle = resolveValue('pageTitle')
  const pageDescription = resolveValue('pageDescription')

  const headPayload = { ...customHead }

  if (!headPayload.title && pageTitle) {
    headPayload.title = pageTitle
  }

  const metaTags = Array.isArray(headPayload.meta) ? [...headPayload.meta] : []

  if (pageTitle) {
    metaTags.push(
      {
        key: 'og:title',
        property: 'og:title',
        content: pageTitle
      },
      {
        key: 'twitter:title',
        name: 'twitter:title',
        content: pageTitle
      }
    )
  }

  if (pageDescription) {
    metaTags.push(
      {
        key: 'description',
        name: 'description',
        content: pageDescription
      },
      {
        key: 'og:description',
        property: 'og:description',
        content: pageDescription
      },
      {
        key: 'twitter:description',
        name: 'twitter:description',
        content: pageDescription
      }
    )
  }

  if (metaTags.length) {
    const seenKeys = new Set()
    headPayload.meta = metaTags.filter((tag) => {
      if (!tag) {
        return false
      }
      if (tag.key) {
        if (seenKeys.has(tag.key)) {
          return false
        }
        seenKeys.add(tag.key)
      }
      return true
    })
  }

  if (!headPayload.title && !(headPayload.meta && headPayload.meta.length) && !(headPayload.link && headPayload.link.length)) {
    return
  }

  removeRouteHeadEntry = head.push(headPayload)
})

export default router