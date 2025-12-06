/**
 * Category, Department, and Subcategory API composable
 * Handles all taxonomy-related API calls
 */

export const useCategoryApi = () => {
  return {
    // Departments
    async getDepartments(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[]; count: number }>('departments/', {
        params
      })
    },

    async getDepartment(id: string | number) {
      return useApiFetch(`departments/${id}/`)
    },

    async getDepartmentBySlug(slug: string) {
      return useApiFetch('departments/', {
        params: { slug }
      })
    },

    async createDepartment(data: FormData | Record<string, any>) {
      return useApiFetch('auth/admin/departments/create/', {
        method: 'POST',
        body: data
      })
    },

    async updateDepartment(id: number, data: FormData | Record<string, any>) {
      return useApiFetch(`auth/admin/departments/${id}/update/`, {
        method: 'PUT',
        body: data
      })
    },

    async deleteDepartment(id: number) {
      return useApiFetch(`auth/admin/departments/${id}/delete/`, {
        method: 'DELETE'
      })
    },

    // Categories
    async getCategories(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[]; count: number }>('categories/', {
        params
      })
    },

    async getCategory(id: string | number) {
      return useApiFetch(`categories/${id}/`)
    },

    async getCategoryBySlug(slug: string) {
      return useApiFetch('categories/', {
        params: { slug }
      })
    },

    async createCategory(data: FormData | Record<string, any>) {
      return useApiFetch('auth/admin/categories/create/', {
        method: 'POST',
        body: data
      })
    },

    async updateCategory(id: number, data: FormData | Record<string, any>) {
      return useApiFetch(`auth/admin/categories/${id}/update/`, {
        method: 'PUT',
        body: data
      })
    },

    async deleteCategory(id: number) {
      return useApiFetch(`auth/admin/categories/${id}/delete/`, {
        method: 'DELETE'
      })
    },

    // Subcategories
    async getSubcategories(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[]; count: number }>('subcategories/', {
        params
      })
    },

    async getSubcategory(id: string | number) {
      return useApiFetch(`subcategories/${id}/`)
    },

    async getSubcategoryBySlug(slug: string) {
      return useApiFetch('subcategories/', {
        params: { slug }
      })
    },

    async createSubcategory(data: FormData | Record<string, any>) {
      return useApiFetch('auth/admin/subcategories/create/', {
        method: 'POST',
        body: data
      })
    },

    async updateSubcategory(id: number, data: FormData | Record<string, any>) {
      return useApiFetch(`auth/admin/subcategories/${id}/update/`, {
        method: 'PUT',
        body: data
      })
    },

    async deleteSubcategory(id: number) {
      return useApiFetch(`auth/admin/subcategories/${id}/delete/`, {
        method: 'DELETE'
      })
    }
  }
}






















