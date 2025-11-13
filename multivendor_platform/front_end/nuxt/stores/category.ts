type Category = Record<string, any>

type Paginated<T> = {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

const translations: Record<string, string> = {
  loading: 'در حال بارگذاری...',
  error: 'خطا',
  failedToFetch: 'خطا در دریافت اطلاعات',
  failedToCreate: 'خطا در ایجاد',
  failedToUpdate: 'خطا در بروزرسانی',
  failedToDelete: 'خطا در حذف',
  categories: 'دسته‌بندی‌ها',
  category: 'دسته‌بندی',
  tryDifferentFilters: 'فیلترهای متفاوت را امتحان کنید.',
  home: 'خانه'
}

const defaultDescription = 'برای این دسته هنوز توضیحاتی ثبت نشده است.'

const decodeHtmlEntities = (input: string): string => {
  if (!input) return input
  // Handle double-encoding by decoding multiple times if needed
  let decoded = input
  let previousDecoded = ''
  
  // Decode until no more changes occur (handles double/triple encoding)
  while (decoded !== previousDecoded) {
    previousDecoded = decoded
    decoded = decoded
      .replace(/&lt;/gi, '<')
      .replace(/&gt;/gi, '>')
      .replace(/&quot;/gi, '"')
      .replace(/&#39;/gi, "'")
      .replace(/&#x27;/gi, "'")
      .replace(/&zwnj;/gi, '\u200C')
      .replace(/&nbsp;/gi, ' ')
      .replace(/&amp;/gi, '&')
      .replace(/&#160;/gi, ' ')
      .replace(/&apos;/gi, "'")
  }
  
  return decoded
}

const sanitizeHtml = (input: string): string =>
  input
    .replace(/<script[\s\S]*?>[\s\S]*?<\/script>/gi, '')
    .replace(/\son\w+="[^"]*"/gi, '')
    .replace(/\son\w+='[^']*'/gi, '')
    .replace(/javascript:/gi, '')

const stripHtmlTags = (html: string): string => {
  if (!html) return html
  // Create a temporary DOM element to parse HTML and extract text
  if (typeof document !== 'undefined') {
    const tmp = document.createElement('div')
    tmp.innerHTML = html
    return tmp.textContent || tmp.innerText || ''
  }
  // Fallback for SSR: use regex to strip tags
  return html.replace(/<[^>]*>/g, '').trim()
}

const buildRichText = (raw: string | null | undefined, fallback = defaultDescription): string => {
  if (!raw) {
    return `<p>${fallback}</p>`
  }

  const decoded = decodeHtmlEntities(raw).trim()
  if (!decoded) {
    return `<p>${fallback}</p>`
  }

  const sanitized = sanitizeHtml(decoded).trim()
  if (!sanitized) {
    return `<p>${fallback}</p>`
  }

  const hasHtmlTags = /<\/?[a-z][\w-]*\b[^>]*>/i.test(sanitized)
  return hasHtmlTags ? sanitized : `<p>${sanitized}</p>`
}

const buildPlainText = (raw: string | null | undefined, fallback = defaultDescription): string => {
  if (!raw) {
    return fallback
  }

  const decoded = decodeHtmlEntities(raw).trim()
  if (!decoded) {
    return fallback
  }

  const plainText = stripHtmlTags(decoded).trim()
  return plainText || fallback
}

const enhanceCategory = <T extends Category | null>(entity: T): T => {
  if (!entity) {
    return entity
  }

  return {
    ...entity,
    description_html: buildRichText(entity.description, defaultDescription),
    description_plain: buildPlainText(entity.description, defaultDescription)
  }
}

const normaliseCollection = <T extends Category>(payload: Paginated<T> | T[]) => {
  if (Array.isArray(payload)) {
    return {
      items: payload.map((item) => enhanceCategory(item)),
      meta: { count: payload.length, next: null, previous: null }
    }
  }

  return {
    items: (payload.results ?? []).map((item) => enhanceCategory(item)),
    meta: {
      count: payload.count ?? 0,
      next: payload.next ?? null,
      previous: payload.previous ?? null
    }
  }
}

export const useCategoryStore = defineStore('categories', () => {
  const categories = ref<Category[]>([])
  const currentCategory = ref<Category | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const pagination = reactive({
    count: 0,
    next: null as string | null,
    previous: null as string | null
  })

  const t = (key: string) => translations[key] ?? key

  const applyPagination = (meta: { count: number; next: string | null; previous: string | null }) => {
    pagination.count = meta.count
    pagination.next = meta.next
    pagination.previous = meta.previous
  }

  const fetchCategories = async (params: Record<string, any> = {}) => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<Paginated<Category> | Category[]>('categories/', {
        query: params
      })
      const { items, meta } = normaliseCollection(response)
      categories.value = items
      applyPagination(meta)
    } catch (err: any) {
      error.value = `${t('failedToFetch')}: ${err?.message ?? ''}`
      console.error('Error fetching categories:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchAdminCategories = async (params: Record<string, any> = {}) => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<Paginated<Category> | Category[]>('auth/admin/categories/', {
        query: params
      })
      const { items, meta } = normaliseCollection(response)
      categories.value = items
      applyPagination(meta)
      return response
    } catch (err: any) {
      error.value = `${t('failedToFetch')}: ${err?.message ?? ''}`
      console.error('Error fetching admin categories:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchCategory = async (id: number | string) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Category>(`categories/${id}/`)
      const enhanced = enhanceCategory(data)
      currentCategory.value = enhanced
      return enhanced
    } catch (err: any) {
      error.value = t('failedToFetch')
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchAdminCategoryDetail = async (id: number | string) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Category>(`auth/admin/categories/${id}/`)
      currentCategory.value = data
      return data
    } catch (err: any) {
      error.value = t('failedToFetch')
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchCategoryBySlug = async (slug: string) => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<Paginated<Category> | Category[]>(`categories/`, {
        query: { slug }
      })
      const { items } = normaliseCollection(response)
      if (items.length) {
        const [first] = items
        currentCategory.value = first
        return first
      }
      throw new Error('Category not found')
    } catch (err: any) {
      error.value = t('failedToFetch')
      throw err
    } finally {
      loading.value = false
    }
  }

  const createCategory = async (payload: FormData | Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Category>('auth/admin/categories/create/', {
        method: 'POST',
        body: payload as any
      })
      const enhanced = enhanceCategory(data)
      categories.value = [...categories.value, enhanced]
      return enhanced
    } catch (err: any) {
      error.value = t('failedToCreate')
      console.error('Error creating category:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateCategory = async (id: number | string, payload: FormData | Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Category>(`auth/admin/categories/${id}/update/`, {
        method: 'PUT',
        body: payload as any
      })
      const enhanced = enhanceCategory(data)
      const index = categories.value.findIndex((category) => category.id === id)
      if (index !== -1) {
        categories.value.splice(index, 1, enhanced)
      }
      if (currentCategory.value?.id === id) {
        currentCategory.value = enhanced
      }
      return enhanced
    } catch (err: any) {
      error.value = t('failedToUpdate')
      console.error('Error updating category:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteCategory = async (id: number | string) => {
    loading.value = true
    error.value = null

    try {
      await useApiFetch<void>(`auth/admin/categories/${id}/delete/`, {
        method: 'DELETE'
      })
      categories.value = categories.value.filter((category) => category.id !== id)
      if (currentCategory.value?.id === id) {
        currentCategory.value = null
      }
    } catch (err: any) {
      error.value = t('failedToDelete')
      console.error('Error deleting category:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearCategories = () => {
    categories.value = []
    currentCategory.value = null
    applyPagination({ count: 0, next: null, previous: null })
  }

  const isLoading = computed(() => loading.value)
  const hasError = computed(() => Boolean(error.value))
  const getCategoryById = computed(
    () => (id: number | string) => categories.value.find((category) => category.id === id)
  )
  const getCategoryBySlug = computed(
    () => (slug: string) => categories.value.find((category) => category.slug === slug)
  )
  const getCategoriesByDepartment = computed(
    () => (departmentId: number | string) =>
      categories.value.filter((category) => category.department === departmentId)
  )
  const activeCategories = computed(() => categories.value.filter((category) => category.is_active))

  return {
    categories,
    currentCategory,
    loading,
    error,
    pagination,
    fetchCategories,
    fetchAdminCategories,
    fetchCategory,
    fetchAdminCategoryDetail,
    fetchCategoryBySlug,
    createCategory,
    updateCategory,
    deleteCategory,
    clearCategories,
    isLoading,
    hasError,
    getCategoryById,
    getCategoryBySlug,
    getCategoriesByDepartment,
    activeCategories,
    t
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useCategoryStore, import.meta.hot))
}

