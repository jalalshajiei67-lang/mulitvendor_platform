import { defineStore, acceptHMRUpdate } from 'pinia'
import { ref, reactive, computed } from 'vue'

type BlogPost = Record<string, any>
type BlogCategory = Record<string, any>
type BlogComment = Record<string, any>

type Paginated<T> = {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

const translations: Record<string, string> = {
  loading: 'در حال بارگذاری...',
  error: 'خطا',
  save: 'ذخیره',
  cancel: 'لغو',
  delete: 'حذف',
  edit: 'ویرایش',
  view: 'مشاهده',
  create: 'ایجاد',
  update: 'بروزرسانی',
  search: 'جستجو',
  filter: 'فیلتر',
  all: 'همه',
  published: 'منتشر شده',
  draft: 'پیش‌نویس',
  archived: 'آرشیو شده',
  featured: 'ویژه',
  active: 'فعال',
  actions: 'عملیات',
  blog: 'وبلاگ',
  dashboard: 'داشبورد',
  posts: 'پست‌ها',
  post: 'پست',
  categories: 'دسته‌بندی‌ها',
  category: 'دسته‌بندی',
  comments: 'نظرات',
  comment: 'نظر',
  author: 'نویسنده',
  date: 'تاریخ',
  views: 'بازدید',
  readingTime: 'دقیقه مطالعه',
  totalPosts: 'کل پست‌ها',
  totalViews: 'کل بازدیدها',
  totalComments: 'کل نظرات',
  myPosts: 'پست‌های من',
  newPost: 'پست جدید',
  newCategory: 'دسته‌بندی جدید',
  createNewPost: 'ایجاد پست جدید',
  createNewCategory: 'ایجاد دسته‌بندی جدید',
  editPost: 'ویرایش پست',
  editCategory: 'ویرایش دسته‌بندی',
  deletePost: 'حذف پست',
  deleteCategory: 'حذف دسته‌بندی',
  postTitle: 'عنوان پست',
  postContent: 'محتوای پست',
  postExcerpt: 'خلاصه پست',
  featuredImage: 'تصویر شاخص',
  metaTitle: 'عنوان متا',
  metaDescription: 'توضیحات متا',
  status: 'وضعیت',
  isFeatured: 'پست ویژه',
  categoryName: 'نام دسته‌بندی',
  categoryDescription: 'توضیحات دسته‌بندی',
  categoryColor: 'رنگ دسته‌بندی',
  noPostsFound: 'هیچ پستی یافت نشد',
  noCategoriesFound: 'هیچ دسته‌بندی یافت نشد',
  noCommentsFound: 'هیچ نظری یافت نشد',
  leaveComment: 'نظر بگذارید',
  postComment: 'ارسال نظر',
  reply: 'پاسخ',
  share: 'اشتراک‌گذاری',
  relatedPosts: 'پست‌های مرتبط',
  popularPosts: 'پست‌های محبوب',
  recentPosts: 'پست‌های اخیر',
  backToBlog: 'بازگشت به وبلاگ',
  back: 'بازگشت',
  next: 'بعدی',
  previous: 'قبلی',
  page: 'صفحه',
  of: 'از',
  minRead: 'دقیقه مطالعه',
  clickToUpload: 'برای آپلود کلیک کنید',
  recommendedSize: 'اندازه پیشنهادی',
  enterTitle: 'عنوان جذاب برای پست خود وارد کنید',
  writeExcerpt: 'توضیح کوتاهی از پست خود بنویسید',
  writeContent: 'محتوای پست خود را اینجا بنویسید...',
  enterCategoryName: 'نام دسته‌بندی را وارد کنید',
  categoryDescriptionPlaceholder: 'توضیحات دسته‌بندی',
  writeComment: 'نظر خود را اینجا بنویسید...',
  loginToComment: 'لطفاً برای نظر دادن وارد شوید',
  beFirstToComment: 'هنوز نظری وجود ندارد. اولین نفری باشید که نظر می‌دهد!',
  postNotFound: 'پست یافت نشد',
  failedToFetch: 'خطا در دریافت اطلاعات',
  failedToCreate: 'خطا در ایجاد',
  failedToUpdate: 'خطا در بروزرسانی',
  failedToDelete: 'خطا در حذف',
  confirmDelete: 'آیا مطمئن هستید که می‌خواهید حذف کنید؟',
  linkCopied: 'لینک کپی شد!',
  loadingPosts: 'در حال بارگذاری پست‌ها...',
  loadingPost: 'در حال بارگذاری پست...',
  postingComment: 'در حال ارسال نظر...',
  creatingCategory: 'در حال ایجاد دسته‌بندی...',
  updatingCategory: 'در حال بروزرسانی دسته‌بندی...',
  savingDraft: 'ذخیره پیش‌نویس',
  publishPost: 'انتشار پست',
  updatePost: 'بروزرسانی پست',
  createCategory: 'ایجاد دسته‌بندی',
  updateCategory: 'بروزرسانی دسته‌بندی',
  selectCategory: 'دسته‌بندی را انتخاب کنید',
  none: 'هیچکدام',
  linkedToProductCategory: 'مرتبط با دسته‌بندی محصول',
  postCount: 'پست',
  thisWillBeShown: 'این در لیست وبلاگ و پیش‌نمایش شبکه‌های اجتماعی نمایش داده می‌شود',
  useLineBreaks: 'از خطوط جدید برای جدا کردن پاراگراف‌ها استفاده کنید',
  leaveEmptyToUse: 'خالی بگذارید تا از عنوان پست استفاده شود',
  leaveEmptyToUseExcerpt: 'خالی بگذارید تا از خلاصه پست استفاده شود',
  featuredPostsAppear: 'پست‌های ویژه به طور برجسته در صفحه اصلی وبلاگ نمایش داده می‌شوند',
  noDescription: 'بدون توضیحات',
  noPostsInCategory: 'هنوز پستی در این دسته‌بندی وجود ندارد',
  noBlogPostsAvailable: 'هنوز پست وبلاگی موجود نیست',
  discoverInsights: 'بینش‌ها، نکات و داستان‌ها را از جامعه ما کشف کنید',
  allPosts: 'همه پست‌ها',
  gridView: 'نمایش شبکه‌ای',
  listView: 'نمایش لیستی',
  tryAgain: 'دوباره تلاش کنید',
  basicInformation: 'اطلاعات پایه',
  publishSettings: 'تنظیمات انتشار',
  seoSettings: 'تنظیمات SEO',
  preview: 'پیش‌نمایش',
  seoTitleOptional: 'عنوان SEO (اختیاری)',
  seoDescriptionOptional: 'توضیحات SEO (اختیاری)',
  yourPostTitleWillAppearHere: 'عنوان پست شما اینجا نمایش داده می‌شود',
  yourExcerptWillAppearHere: 'خلاصه شما اینجا نمایش داده می‌شود',
  tags: 'برچسب‌ها'
}

const setCollection = <T>(source: Paginated<T> | T[]) => {
  if (Array.isArray(source)) {
    return {
      items: source,
      pagination: { count: 0, next: null, previous: null }
    }
  }

  return {
    items: source.results ?? [],
    pagination: {
      count: source.count ?? 0,
      next: source.next ?? null,
      previous: source.previous ?? null
    }
  }
}

export const useBlogStore = defineStore('blog', () => {
  const posts = ref<BlogPost[]>([])
  const currentPost = ref<BlogPost | null>(null)
  const featuredPosts = ref<BlogPost[]>([])
  const recentPosts = ref<BlogPost[]>([])
  const popularPosts = ref<BlogPost[]>([])
  const relatedPosts = ref<BlogPost[]>([])

  const categories = ref<BlogCategory[]>([])
  const currentCategory = ref<BlogCategory | null>(null)

  const comments = ref<BlogComment[]>([])

  const loading = ref(false)
  const error = ref<string | null>(null)
  const pagination = reactive({
    count: 0,
    next: null as string | null,
    previous: null as string | null
  })

  const applyPagination = (payload: { count: number; next: string | null; previous: string | null }) => {
    pagination.count = payload.count
    pagination.next = payload.next
    pagination.previous = payload.previous
  }

  const fetchPosts = async (params: Record<string, any> = {}) => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<Paginated<BlogPost> | BlogPost[]>('blog/posts/', {
        query: params
      })
      const { items, pagination: meta } = setCollection(response)
      posts.value = items
      applyPagination(meta)
    } catch (err: any) {
      error.value = `${translations.failedToFetch}: ${err?.message ?? ''}`
      console.error('Error fetching blog posts:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchPost = async (slug: string) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<BlogPost>(`blog/posts/${slug}/`)
      currentPost.value = data

      const index = posts.value.findIndex((post) => post.slug === slug)
      if (index !== -1) {
        posts.value.splice(index, 1, data)
      }

      return data
    } catch (err: any) {
      error.value = translations.failedToFetch
      console.error('Error fetching blog post:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createPost = async (payload: FormData | Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<BlogPost>('blog/posts/', {
        method: 'POST',
        body: payload as any
      })
      posts.value = [data, ...posts.value]
      return data
    } catch (err: any) {
      error.value = translations.failedToCreate
      console.error('Error creating blog post:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updatePost = async (slug: string, payload: FormData | Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<BlogPost>(`blog/posts/${slug}/`, {
        method: 'PUT',
        body: payload as any
      })

      const index = posts.value.findIndex((post) => post.slug === slug)
      if (index !== -1) {
        posts.value.splice(index, 1, data)
      }

      if (currentPost.value?.slug === slug) {
        currentPost.value = data
      }

      return data
    } catch (err: any) {
      error.value = translations.failedToUpdate
      console.error('Error updating blog post:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deletePost = async (slug: string) => {
    loading.value = true
    error.value = null

    try {
      await useApiFetch<void>(`blog/posts/${slug}/`, { method: 'DELETE' })
      posts.value = posts.value.filter((post) => post.slug !== slug)
      if (currentPost.value?.slug === slug) {
        currentPost.value = null
      }
    } catch (err: any) {
      error.value = translations.failedToDelete
      console.error('Error deleting blog post:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchFeaturedPosts = async () => {
    try {
      featuredPosts.value = await useApiFetch<BlogPost[]>('blog/posts/featured/')
    } catch (err) {
      console.error('Error fetching featured posts:', err)
    }
  }

  const fetchRecentPosts = async () => {
    try {
      recentPosts.value = await useApiFetch<BlogPost[]>('blog/posts/recent/')
    } catch (err) {
      console.error('Error fetching recent posts:', err)
    }
  }

  const fetchPopularPosts = async () => {
    try {
      popularPosts.value = await useApiFetch<BlogPost[]>('blog/posts/popular/')
    } catch (err) {
      console.error('Error fetching popular posts:', err)
    }
  }

  const fetchRelatedPosts = async (slug: string) => {
    try {
      relatedPosts.value = await useApiFetch<BlogPost[]>(`blog/posts/${slug}/related/`)
    } catch (err) {
      console.error('Error fetching related posts:', err)
      relatedPosts.value = []
    }
  }

  const fetchMyPosts = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<Paginated<BlogPost> | BlogPost[]>('blog/my-posts/')
      const { items, pagination: meta } = setCollection(response)
      posts.value = items
      applyPagination(meta)
    } catch (err: any) {
      error.value = translations.failedToFetch
      console.error('Error fetching my blog posts:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchCategories = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<Paginated<BlogCategory> | BlogCategory[]>('blog/categories/')
      const { items } = setCollection(response)
      categories.value = items
    } catch (err: any) {
      error.value = translations.failedToFetch
      console.error('Error fetching blog categories:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchCategory = async (slug: string) => {
    loading.value = true
    error.value = null

    try {
      currentCategory.value = await useApiFetch<BlogCategory>(`blog/categories/${slug}/`)
    } catch (err: any) {
      error.value = translations.failedToFetch
      console.error('Error fetching blog category:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createCategory = async (payload: Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<BlogCategory>('blog/categories/', {
        method: 'POST',
        body: payload
      })
      categories.value = [...categories.value, data]
      return data
    } catch (err: any) {
      error.value = translations.failedToCreate
      console.error('Error creating blog category:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateCategory = async (slug: string, payload: Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<BlogCategory>(`blog/categories/${slug}/`, {
        method: 'PUT',
        body: payload
      })

      const index = categories.value.findIndex((category) => category.slug === slug)
      if (index !== -1) {
        categories.value.splice(index, 1, data)
      }

      if (currentCategory.value?.slug === slug) {
        currentCategory.value = data
      }

      return data
    } catch (err: any) {
      error.value = translations.failedToUpdate
      console.error('Error updating blog category:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteCategory = async (slug: string) => {
    loading.value = true
    error.value = null

    try {
      await useApiFetch<void>(`blog/categories/${slug}/`, { method: 'DELETE' })
      categories.value = categories.value.filter((category) => category.slug !== slug)
      if (currentCategory.value?.slug === slug) {
        currentCategory.value = null
      }
    } catch (err: any) {
      error.value = translations.failedToDelete
      console.error('Error deleting blog category:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchCategoryPosts = async (slug: string) => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<Paginated<BlogPost> | BlogPost[]>(`blog/categories/${slug}/posts/`)
      const { items, pagination: meta } = setCollection(response)
      posts.value = items
      applyPagination(meta)
    } catch (err: any) {
      error.value = translations.failedToFetch
      console.error('Error fetching category posts:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchComments = async (slug: string) => {
    try {
      comments.value = await useApiFetch<BlogComment[]>(`blog/posts/${slug}/comments/`)
    } catch (err) {
      console.error('Error fetching comments:', err)
    }
  }

  const createComment = async (slug: string, payload: Record<string, any>) => {
    try {
      const data = await useApiFetch<BlogComment>(`blog/posts/${slug}/comment/`, {
        method: 'POST',
        body: payload
      })
      comments.value = [...comments.value, data]
      return data
    } catch (err: any) {
      error.value = translations.failedToCreate
      console.error('Error creating comment:', err)
      throw err
    }
  }

  const clearCurrentPost = () => {
    currentPost.value = null
  }

  const clearCurrentCategory = () => {
    currentCategory.value = null
  }

  const clearError = () => {
    error.value = null
  }

  const postsByCategory = computed(
    () => (categoryId: number | string) => posts.value.filter((post) => post.category === categoryId)
  )
  const publishedPosts = computed(() => posts.value.filter((post) => post.status === 'published'))
  const draftPosts = computed(() => posts.value.filter((post) => post.status === 'draft'))
  const approvedComments = computed(() => comments.value.filter((comment) => comment.is_approved))

  const t = (key: string) => translations[key] ?? key

  return {
    posts,
    currentPost,
    featuredPosts,
    recentPosts,
    popularPosts,
    relatedPosts,
    categories,
    currentCategory,
    comments,
    loading,
    error,
    pagination,
    fetchPosts,
    fetchPost,
    createPost,
    updatePost,
    deletePost,
    fetchFeaturedPosts,
    fetchRecentPosts,
    fetchPopularPosts,
    fetchRelatedPosts,
    fetchMyPosts,
    fetchCategories,
    fetchCategory,
    createCategory,
    updateCategory,
    deleteCategory,
    fetchCategoryPosts,
    fetchComments,
    createComment,
    clearCurrentPost,
    clearCurrentCategory,
    clearError,
    postsByCategory,
    publishedPosts,
    draftPosts,
    approvedComments,
    t
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useBlogStore, import.meta.hot))
}

