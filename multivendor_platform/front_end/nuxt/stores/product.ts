type Product = Record<string, any>

type PaginatedResponse<T> = {
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
  failedToSubmitComment: 'خطا در ثبت نظر',
  products: 'محصولات',
  product: 'محصول',
  myProducts: 'محصولات من',
  discoverMarketplace: 'بازار چندفروشنده ایندکسو را کشف کنید و بهترین پیشنهادها را انتخاب نمایید.',
  searchProducts: 'جستجوی محصولات',
  selectCategory: 'انتخاب دسته‌بندی',
  sortBy: 'مرتب‌سازی',
  newest: 'جدیدترین',
  priceLowToHigh: 'قیمت از کم به زیاد',
  priceHighToLow: 'قیمت از زیاد به کم',
  noProductsFound: 'هیچ محصولی یافت نشد',
  tryDifferentFilters: 'فیلترهای خود را تغییر دهید یا دوباره تلاش کنید.',
  resetFilters: 'بازنشانی فیلترها',
  contactForPrice: 'تماس برای قیمت',
  price: 'قیمت',
  view: 'مشاهده',
  requestQuote: 'درخواست استعلام',
  keySpecifications: 'مشخصات کلیدی',
  sku: 'کد محصول',
  stockStatus: 'وضعیت موجودی',
  minimumOrder: 'حداقل سفارش',
  originCountry: 'کشور سازنده',
  productDescription: 'توضیحات محصول',
  relatedProducts: 'محصولات مرتبط',
  home: 'خانه'
}

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

const enhanceProduct = <T extends Product | null>(entity: T): T => {
  if (!entity) {
    return entity
  }

  // Decode description if it exists
  if (entity.description) {
    const decoded = decodeHtmlEntities(entity.description)
    const sanitized = sanitizeHtml(decoded)
    return {
      ...entity,
      description: sanitized
    }
  }

  return entity
}

export const useProductStore = defineStore('products', () => {
  const products = ref<Product[]>([])
  const currentProduct = ref<Product | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const pagination = reactive({
    count: 0,
    next: null as string | null,
    previous: null as string | null
  })

  const t = (key: string) => translations[key] ?? key

  const setPagination = (payload?: Partial<typeof pagination>) => {
    pagination.count = payload?.count ?? 0
    pagination.next = payload?.next ?? null
    pagination.previous = payload?.previous ?? null
  }

  const fetchProducts = async (params: Record<string, any> = {}) => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<PaginatedResponse<Product> | Product[]>('products/', {
        query: params
      })

      if (Array.isArray(response)) {
        products.value = response.map((item) => enhanceProduct(item))
        setPagination()
      } else {
        products.value = (response.results ?? []).map((item) => enhanceProduct(item))
        setPagination(response)
      }
    } catch (err: any) {
      const message = err?.data?.detail ?? err?.message ?? t('failedToFetch')
      error.value = `${t('failedToFetch')}: ${message}`
      console.error('Error fetching products:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchProduct = async (id: string | number) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Product>(`products/${id}/`)
      const enhanced = enhanceProduct(data)
      currentProduct.value = enhanced
      return enhanced
    } catch (err: any) {
      error.value = t('failedToFetch')
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchProductBySlug = async (slug: string) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Product>(`products/slug/${slug}/`)
      const enhanced = enhanceProduct(data)
      currentProduct.value = enhanced
      return enhanced
    } catch (err: any) {
      error.value = t('failedToFetch')
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchMyProducts = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<PaginatedResponse<Product> | Product[]>('products/my_products/')
      if (Array.isArray(response)) {
        products.value = response.map((item) => enhanceProduct(item))
        setPagination()
      } else {
        products.value = (response.results ?? []).map((item) => enhanceProduct(item))
        setPagination(response)
      }
    } catch (err: any) {
      const message = err?.data?.detail ?? err?.message ?? t('failedToFetch')
      error.value = `${t('failedToFetch')}: ${message}`
      console.error('Error fetching my products:', err)
    } finally {
      loading.value = false
    }
  }

  const createProduct = async (payload: FormData | Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Product>('products/', {
        method: 'POST',
        body: payload as any
      })
      const enhanced = enhanceProduct(data)
      products.value = [enhanced, ...products.value]
      return enhanced
    } catch (err: any) {
      // Import error formatting utility dynamically
      const { formatErrorMessage } = await import('~/utils/apiErrors')
      const formattedError = formatErrorMessage(err)
      error.value = formattedError
      console.error('Error creating product:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateProduct = async (id: string | number, payload: FormData | Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Product>(`products/${id}/`, {
        method: 'PUT',
        body: payload as any
      })

      const enhanced = enhanceProduct(data)
      const index = products.value.findIndex((product) => product.id === id)
      if (index !== -1) {
        products.value.splice(index, 1, enhanced)
      }

      if (currentProduct.value?.id === id) {
        currentProduct.value = enhanced
      }

      return enhanced
    } catch (err: any) {
      // Import error formatting utility dynamically
      const { formatErrorMessage } = await import('~/utils/apiErrors')
      const formattedError = formatErrorMessage(err)
      error.value = formattedError
      console.error('Error updating product:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteProduct = async (id: string | number) => {
    loading.value = true
    error.value = null

    try {
      await useApiFetch<null>(`products/${id}/`, {
        method: 'DELETE'
      })
      products.value = products.value.filter((product) => product.id !== id)
      if (currentProduct.value?.id === id) {
        currentProduct.value = null
      }
    } catch (err: any) {
      error.value = t('failedToDelete')
      console.error('Error deleting product:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteProductImage = async (productId: string | number, imageId: string | number) => {
    loading.value = true
    error.value = null

    try {
      await useApiFetch<null>(`products/${productId}/images/${imageId}/`, {
        method: 'DELETE'
      })

      if (currentProduct.value?.id === productId) {
        currentProduct.value.images = currentProduct.value.images?.filter(
          (image: any) => image.id !== imageId
        )
      }

      const index = products.value.findIndex((product) => product.id === productId)
      if (index !== -1) {
        const product = products.value[index]
        product.images = product.images?.filter((image: any) => image.id !== imageId)
        products.value.splice(index, 1, product)
      }
    } catch (err: any) {
      error.value = t('failedToDelete')
      console.error('Error deleting product image:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createProductComment = async (productId: string | number, payload: Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Product>(`products/${productId}/comments/`, {
        method: 'POST',
        body: payload
      })
      await fetchProduct(productId)
      return data
    } catch (err: any) {
      error.value = t('failedToSubmitComment')
      console.error('Error creating product comment:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchProductComments = async (productId: string | number) => {
    loading.value = true
    error.value = null

    try {
      return await useApiFetch<any>(`products/${productId}/comments/`)
    } catch (err: any) {
      error.value = t('failedToFetch')
      console.error('Error fetching product comments:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearProducts = () => {
    products.value = []
    currentProduct.value = null
    setPagination()
  }

  const isLoading = computed(() => loading.value)
  const hasError = computed(() => Boolean(error.value))

  const getProductsByCategory = computed(
    () => (categoryId: string | number) =>
      products.value.filter((product) => product.category === categoryId)
  )

  const getProductsBySubcategory = computed(
    () => (subcategoryId: string | number) =>
      products.value.filter((product) => product.subcategory === subcategoryId)
  )

  const getProductsByVendor = computed(
    () => (vendorId: string | number) =>
      products.value.filter((product) => product.vendor === vendorId)
  )

  const activeProducts = computed(() => products.value.filter((product) => product.is_active))
  const inStockProducts = computed(() => products.value.filter((product) => product.stock > 0))
  const newestProducts = computed(() =>
    [...products.value].sort(
      (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    )
  )
  const cheapestProducts = computed(() =>
    [...products.value].sort((a, b) => Number(a.price) - Number(b.price))
  )
  const mostExpensiveProducts = computed(() =>
    [...products.value].sort((a, b) => Number(b.price) - Number(a.price))
  )

  return {
    products,
    currentProduct,
    loading,
    error,
    pagination,
    t,
    fetchProducts,
    fetchProduct,
    fetchProductBySlug,
    fetchMyProducts,
    createProduct,
    updateProduct,
    deleteProduct,
    deleteProductImage,
    createProductComment,
    fetchProductComments,
    clearProducts,
    isLoading,
    hasError,
    getProductsByCategory,
    getProductsBySubcategory,
    getProductsByVendor,
    activeProducts,
    inStockProducts,
    newestProducts,
    cheapestProducts,
    mostExpensiveProducts
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useProductStore, import.meta.hot))
}

