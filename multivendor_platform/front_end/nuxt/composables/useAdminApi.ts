export const useAdminApi = () => {
  return {
    // Dashboard
    async getDashboard() {
      return useApiFetch<{
        users: { total: number; buyers: number; sellers: number }
        products: { total: number; active: number }
        orders: { total: number; pending: number }
        rfqs: { total: number; pending: number }
      }>('auth/admin/dashboard/')
    },

    // Users
    async getUsers(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[]; count: number }>('auth/admin/users/', {
        params
      })
    },

    async updateUser(id: number, data: Record<string, any>) {
      return useApiFetch(`auth/admin/users/${id}/`, {
        method: 'PATCH',
        body: data
      })
    },

    async changeUserPassword(id: number, password: string) {
      return useApiFetch(`auth/admin/users/${id}/change_password/`, {
        method: 'POST',
        body: { password }
      })
    },

    async blockUser(id: number, blocked: boolean) {
      return useApiFetch(`auth/admin/users/${id}/block/`, {
        method: 'POST',
        body: { is_blocked: blocked }
      })
    },

    // Products
    async getAdminProducts(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[]; count: number }>('auth/admin/products/', {
        params
      })
    },

    async getAdminProductDetail(id: number) {
      return useApiFetch<any>(`auth/admin/products/${id}/`)
    },

    async updateProductStatus(id: number, isActive: boolean) {
      // Use bulk action endpoint for single product status update
      return useApiFetch('auth/admin/products/bulk-action/', {
        method: 'POST',
        body: {
          action: isActive ? 'activate' : 'deactivate',
          product_ids: [id]
        }
      })
    },

    async deleteProduct(id: number) {
      return useApiFetch(`auth/admin/products/${id}/delete/`, {
        method: 'DELETE'
      })
    },

    // Activities
    async getActivities(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[]; count: number }>('auth/admin/activities/', {
        params
      })
    },

    // Gamification anti-abuse
    async getGamificationFlags() {
      return useApiFetch<{
        flagged_supplier_comments: any[]
        flagged_product_reviews: any[]
        invitation_blocks: any[]
      }>('gamification/admin/flags/')
    },

    async clearGamificationFlag(data: { object_type: string; id: number }) {
      return useApiFetch('gamification/admin/flags/clear/', {
        method: 'POST',
        body: data
      })
    },

    // RFQs
    async getRFQs(params: Record<string, any> = {}) {
      return useApiFetch<any[]>('orders/admin/rfq/', {
        params
      })
    },

    async getRFQDetail(id: number) {
      return useApiFetch<any>(`orders/admin/rfq/${id}/`)
    },

    async updateRFQStatus(id: number, status: string) {
      return useApiFetch(`orders/admin/rfq/${id}/status/`, {
        method: 'PATCH',
        body: { status }
      })
    },

    async createRFQ(data: FormData | Record<string, any>) {
      return useApiFetch('orders/admin/rfq/create/', {
        method: 'POST',
        body: data
      })
    },

    // Blog
    async getAdminBlogPosts(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[]; count: number }>('auth/admin/blog/posts/', {
        params
      })
    },

    async deleteBlogPost(slug: string) {
      return useApiFetch(`auth/admin/blog/posts/${slug}/`, {
        method: 'DELETE'
      })
    },

    async getBlogCategories() {
      return useApiFetch<any[]>('auth/admin/blog/categories/')
    },

    async createBlogCategory(data: Record<string, any>) {
      return useApiFetch('auth/admin/blog/categories/', {
        method: 'POST',
        body: data
      })
    },

    async updateBlogCategory(slug: string, data: Record<string, any>) {
      return useApiFetch(`auth/admin/blog/categories/${slug}/`, {
        method: 'PATCH',
        body: data
      })
    },

    async deleteBlogCategory(slug: string) {
      return useApiFetch(`auth/admin/blog/categories/${slug}/`, {
        method: 'DELETE'
      })
    },

    // Departments
    async getDepartments(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[]; count: number }>('auth/admin/departments/', {
        params
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
      return useApiFetch<{ results: any[]; count: number }>('auth/admin/categories/', {
        params
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
      return useApiFetch<{ results: any[]; count: number }>('auth/admin/subcategories/', {
        params
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
    },

    // Bulk Actions
    async productBulkAction(action: string, productIds: number[]) {
      return useApiFetch('auth/admin/products/bulk-action/', {
        method: 'POST',
        body: { action, product_ids: productIds }
      })
    },

    async blogPostBulkAction(action: string, postSlugs: string[]) {
      return useApiFetch('auth/admin/blog/posts/bulk-action/', {
        method: 'POST',
        body: { action, post_slugs: postSlugs }
      })
    },

    // Orders Management
    async getOrders(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[]; count: number }>('auth/admin/orders/', {
        params
      })
    },

    async updateOrderStatus(orderId: number, status: string) {
      return useApiFetch(`auth/admin/orders/${orderId}/status/`, {
        method: 'PUT',
        body: { status }
      })
    }
  }
}

