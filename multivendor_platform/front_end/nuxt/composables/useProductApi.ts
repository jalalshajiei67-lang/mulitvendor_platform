export const useProductApi = () => {
  return {
    // Product CRUD
    async getProducts(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[]; count: number }>('products/', {
        params
      })
    },

    async getProduct(id: string | number) {
      return useApiFetch(`products/${id}/`)
    },

    async getProductBySlug(slug: string) {
      return useApiFetch(`products/slug/${slug}/`)
    },

    async createProduct(data: FormData | Record<string, any>) {
      return useApiFetch('products/', {
        method: 'POST',
        body: data
      })
    },

    async updateProduct(id: string | number, data: FormData | Record<string, any>) {
      return useApiFetch(`products/${id}/`, {
        method: 'PUT',
        body: data
      })
    },

    async deleteProduct(id: string | number) {
      return useApiFetch(`products/${id}/`, {
        method: 'DELETE'
      })
    },

    // My Products (for sellers)
    async getMyProducts(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[]; count: number }>('products/my_products/', {
        params
      })
    },

    // Product Images
    async uploadProductImage(productId: string | number, formData: FormData) {
      return useApiFetch(`products/${productId}/images/`, {
        method: 'POST',
        body: formData
      })
    },

    async deleteProductImage(productId: string | number, imageId: number) {
      return useApiFetch(`products/${productId}/images/${imageId}/`, {
        method: 'DELETE'
      })
    },

    // Taxonomy (kept for backward compatibility, use useCategoryApi instead)
    async getDepartments(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[] }>('departments/', {
        params
      })
    },

    async getCategories(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[] }>('categories/', {
        params
      })
    },

    async getSubcategories(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[] }>('subcategories/', {
        params
      })
    }
  }
}

