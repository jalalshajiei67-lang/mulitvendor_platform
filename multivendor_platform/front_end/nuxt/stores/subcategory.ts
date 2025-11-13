type Subcategory = Record<string, any>

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
  subcategories: 'زیردسته‌ها',
  subcategory: 'زیردسته',
  products: 'محصولات',
  home: 'خانه',
  tryDifferentFilters: 'فیلترهای متفاوت را امتحان کنید.'
}

const defaultDescription = 'برای این زیردسته هنوز توضیحاتی ثبت نشده است.'

const decodeHtmlEntities = (input: string): string =>
  input
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'")
    .replace(/&zwnj;/gi, '\u200C')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')

const sanitizeHtml = (input: string): string =>
  input
    .replace(/<script[\s\S]*?>[\s\S]*?<\/script>/gi, '')
    .replace(/\son\w+="[^"]*"/gi, '')
    .replace(/\son\w+='[^']*'/gi, '')
    .replace(/javascript:/gi, '')

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

const enhanceSubcategory = <T extends Subcategory | null>(entity: T): T => {
  if (!entity) {
    return entity
  }

  return {
    ...entity,
    description_html: buildRichText(entity.description, defaultDescription)
  }
}

const normaliseCollection = <T extends Subcategory>(payload: Paginated<T> | T[]) => {
  if (Array.isArray(payload)) {
    return {
      items: payload.map((item) => enhanceSubcategory(item)),
      meta: { count: payload.length, next: null, previous: null }
    }
  }

  return {
    items: (payload.results ?? []).map((item) => enhanceSubcategory(item)),
    meta: {
      count: payload.count ?? 0,
      next: payload.next ?? null,
      previous: payload.previous ?? null
    }
  }
}

export const useSubcategoryStore = defineStore('subcategories', () => {
  const subcategories = ref<Subcategory[]>([])
  const currentSubcategory = ref<Subcategory | null>(null)
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

  const fetchSubcategories = async (params: Record<string, any> = {}) => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<Paginated<Subcategory> | Subcategory[]>('subcategories/', {
        query: params
      })
      const { items, meta } = normaliseCollection(response)
      subcategories.value = items
      applyPagination(meta)
    } catch (err: any) {
      error.value = `${t('failedToFetch')}: ${err?.message ?? ''}`
      console.error('Error fetching subcategories:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchAdminSubcategories = async (params: Record<string, any> = {}) => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<Paginated<Subcategory> | Subcategory[]>(
        'auth/admin/subcategories/',
        {
          query: params
        }
      )
      const { items, meta } = normaliseCollection(response)
      subcategories.value = items
      applyPagination(meta)
      return response
    } catch (err: any) {
      error.value = `${t('failedToFetch')}: ${err?.message ?? ''}`
      console.error('Error fetching admin subcategories:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchSubcategory = async (id: number | string) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Subcategory>(`subcategories/${id}/`)
      const enhanced = enhanceSubcategory(data)
      currentSubcategory.value = enhanced
      return enhanced
    } catch (err: any) {
      error.value = t('failedToFetch')
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchAdminSubcategoryDetail = async (id: number | string) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Subcategory>(`auth/admin/subcategories/${id}/`)
      currentSubcategory.value = data
      return data
    } catch (err: any) {
      error.value = t('failedToFetch')
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchSubcategoryBySlug = async (slug: string) => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<Paginated<Subcategory> | Subcategory[]>('subcategories/', {
        query: { slug }
      })
      const { items } = normaliseCollection(response)
      if (items.length) {
        const [first] = items
        currentSubcategory.value = first
        return first
      }
      throw new Error('Subcategory not found')
    } catch (err: any) {
      error.value = t('failedToFetch')
      throw err
    } finally {
      loading.value = false
    }
  }

  const createSubcategory = async (payload: FormData | Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Subcategory>('auth/admin/subcategories/create/', {
        method: 'POST',
        body: payload as any
      })
      const enhanced = enhanceSubcategory(data)
      subcategories.value = [...subcategories.value, enhanced]
      return enhanced
    } catch (err: any) {
      error.value = t('failedToCreate')
      console.error('Error creating subcategory:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateSubcategory = async (id: number | string, payload: FormData | Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Subcategory>(`auth/admin/subcategories/${id}/update/`, {
        method: 'PUT',
        body: payload as any
      })
      const enhanced = enhanceSubcategory(data)
      const index = subcategories.value.findIndex((subcategory) => subcategory.id === id)
      if (index !== -1) {
        subcategories.value.splice(index, 1, enhanced)
      }
      if (currentSubcategory.value?.id === id) {
        currentSubcategory.value = enhanced
      }
      return enhanced
    } catch (err: any) {
      error.value = t('failedToUpdate')
      console.error('Error updating subcategory:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteSubcategory = async (id: number | string) => {
    loading.value = true
    error.value = null

    try {
      await useApiFetch<void>(`auth/admin/subcategories/${id}/delete/`, {
        method: 'DELETE'
      })
      subcategories.value = subcategories.value.filter((subcategory) => subcategory.id !== id)
      if (currentSubcategory.value?.id === id) {
        currentSubcategory.value = null
      }
    } catch (err: any) {
      error.value = t('failedToDelete')
      console.error('Error deleting subcategory:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearSubcategories = () => {
    subcategories.value = []
    currentSubcategory.value = null
    applyPagination({ count: 0, next: null, previous: null })
  }

  const isLoading = computed(() => loading.value)
  const hasError = computed(() => Boolean(error.value))
  const getSubcategoryById = computed(
    () => (id: number | string) => subcategories.value.find((subcategory) => subcategory.id === id)
  )
  const getSubcategoryBySlug = computed(
    () => (slug: string) => subcategories.value.find((subcategory) => subcategory.slug === slug)
  )
  const getSubcategoriesByCategory = computed(
    () => (categoryId: number | string) =>
      subcategories.value.filter((subcategory) => subcategory.category === categoryId)
  )
  const getSubcategoriesByDepartment = computed(
    () => (departmentId: number | string) =>
      subcategories.value.filter((subcategory) => subcategory.department === departmentId)
  )
  const activeSubcategories = computed(() =>
    subcategories.value.filter((subcategory) => subcategory.is_active)
  )
  const getNewProductsBySubcategory = computed(
    () => (subcategoryId: number | string) =>
      subcategories.value.find((subcategory) => subcategory.id === subcategoryId)?.new_products ?? []
  )

  return {
    subcategories,
    currentSubcategory,
    loading,
    error,
    pagination,
    fetchSubcategories,
    fetchAdminSubcategories,
    fetchSubcategory,
    fetchAdminSubcategoryDetail,
    fetchSubcategoryBySlug,
    createSubcategory,
    updateSubcategory,
    deleteSubcategory,
    clearSubcategories,
    isLoading,
    hasError,
    getSubcategoryById,
    getSubcategoryBySlug,
    getSubcategoriesByCategory,
    getSubcategoriesByDepartment,
    activeSubcategories,
    getNewProductsBySubcategory,
    t
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useSubcategoryStore, import.meta.hot))
}

