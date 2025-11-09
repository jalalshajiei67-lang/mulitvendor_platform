type Department = Record<string, any>

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
  departments: 'دپارتمان‌ها',
  department: 'دپارتمان',
  home: 'خانه'
}

const normaliseCollection = <T>(payload: Paginated<T> | T[]) => {
  if (Array.isArray(payload)) {
    return {
      items: payload,
      meta: { count: payload.length, next: null, previous: null }
    }
  }

  return {
    items: payload.results ?? [],
    meta: {
      count: payload.count ?? 0,
      next: payload.next ?? null,
      previous: payload.previous ?? null
    }
  }
}

export const useDepartmentStore = defineStore('departments', () => {
  const departments = ref<Department[]>([])
  const currentDepartment = ref<Department | null>(null)
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

  const fetchDepartments = async (params: Record<string, any> = {}) => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<Paginated<Department> | Department[]>('departments/', {
        query: params
      })
      const { items, meta } = normaliseCollection(response)
      departments.value = items
      applyPagination(meta)
    } catch (err: any) {
      error.value = `${t('failedToFetch')}: ${err?.message ?? ''}`
      console.error('Error fetching departments:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchAdminDepartments = async (params: Record<string, any> = {}) => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<Paginated<Department> | Department[]>('auth/admin/departments/', {
        query: params
      })
      const { items, meta } = normaliseCollection(response)
      departments.value = items
      applyPagination(meta)
      return response
    } catch (err: any) {
      error.value = `${t('failedToFetch')}: ${err?.message ?? ''}`
      console.error('Error fetching admin departments:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchDepartment = async (id: number | string) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Department>(`departments/${id}/`)
      currentDepartment.value = data
      return data
    } catch (err: any) {
      error.value = t('failedToFetch')
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchDepartmentBySlug = async (slug: string) => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<Paginated<Department> | Department[]>('departments/', {
        query: { slug }
      })
      const { items } = normaliseCollection(response)
      if (items.length) {
        currentDepartment.value = items[0]
        return items[0]
      }
      throw new Error('Department not found')
    } catch (err: any) {
      error.value = t('failedToFetch')
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchAdminDepartmentDetail = async (id: number | string) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Department>(`auth/admin/departments/${id}/`)
      currentDepartment.value = data
      return data
    } catch (err: any) {
      error.value = t('failedToFetch')
      throw err
    } finally {
      loading.value = false
    }
  }

  const createDepartment = async (payload: FormData | Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Department>('auth/admin/departments/create/', {
        method: 'POST',
        body: payload as any
      })
      departments.value = [...departments.value, data]
      return data
    } catch (err: any) {
      error.value = t('failedToCreate')
      console.error('Error creating department:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateDepartment = async (id: number | string, payload: FormData | Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<Department>(`auth/admin/departments/${id}/update/`, {
        method: 'PUT',
        body: payload as any
      })
      const index = departments.value.findIndex((department) => department.id === id)
      if (index !== -1) {
        departments.value.splice(index, 1, data)
      }
      if (currentDepartment.value?.id === id) {
        currentDepartment.value = data
      }
      return data
    } catch (err: any) {
      error.value = t('failedToUpdate')
      console.error('Error updating department:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteDepartment = async (id: number | string) => {
    loading.value = true
    error.value = null

    try {
      await useApiFetch<void>(`auth/admin/departments/${id}/delete/`, {
        method: 'DELETE'
      })
      departments.value = departments.value.filter((department) => department.id !== id)
      if (currentDepartment.value?.id === id) {
        currentDepartment.value = null
      }
    } catch (err: any) {
      error.value = t('failedToDelete')
      console.error('Error deleting department:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearDepartments = () => {
    departments.value = []
    currentDepartment.value = null
    applyPagination({ count: 0, next: null, previous: null })
  }

  const isLoading = computed(() => loading.value)
  const hasError = computed(() => Boolean(error.value))
  const getDepartmentById = computed(
    () => (id: number | string) => departments.value.find((department) => department.id === id)
  )
  const getDepartmentBySlug = computed(
    () => (slug: string) => departments.value.find((department) => department.slug === slug)
  )
  const activeDepartments = computed(() =>
    departments.value.filter((department) => department.is_active)
  )

  return {
    departments,
    currentDepartment,
    loading,
    error,
    pagination,
    fetchDepartments,
    fetchAdminDepartments,
    fetchDepartment,
    fetchAdminDepartmentDetail,
    fetchDepartmentBySlug,
    createDepartment,
    updateDepartment,
    deleteDepartment,
    clearDepartments,
    isLoading,
    hasError,
    getDepartmentById,
    getDepartmentBySlug,
    activeDepartments,
    t
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useDepartmentStore, import.meta.hot))
}

