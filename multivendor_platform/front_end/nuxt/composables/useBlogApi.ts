export const useBlogApi = () => {
  return {
    // Blog Posts
    async getPosts(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[]; count: number }>('blog/posts/', {
        params
      })
    },

    async getPost(slug: string) {
      return useApiFetch(`blog/posts/${slug}/`)
    },

    async createPost(data: FormData | Record<string, any>) {
      return useApiFetch('blog/posts/', {
        method: 'POST',
        body: data
      })
    },

    async updatePost(slug: string, data: FormData | Record<string, any>) {
      return useApiFetch(`blog/posts/${slug}/`, {
        method: 'PUT',
        body: data
      })
    },

    async deletePost(slug: string) {
      return useApiFetch(`blog/posts/${slug}/`, {
        method: 'DELETE'
      })
    },

    // My Posts (for authors)
    async getMyPosts(params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[]; count: number }>('blog/my-posts/', {
        params
      })
    },

    // Featured/Recent/Popular Posts
    async getFeaturedPosts() {
      return useApiFetch<any[]>('blog/posts/featured/')
    },

    async getRecentPosts(limit: number = 5) {
      return useApiFetch<any[]>('blog/posts/recent/', {
        params: { limit }
      })
    },

    async getPopularPosts(limit: number = 5) {
      return useApiFetch<any[]>('blog/posts/popular/', {
        params: { limit }
      })
    },

    async getRelatedPosts(slug: string) {
      return useApiFetch<any[]>(`blog/posts/${slug}/related/`)
    },

    // Blog Categories
    async getCategories() {
      return useApiFetch<any[]>('blog/categories/')
    },

    async getCategory(slug: string) {
      return useApiFetch(`blog/categories/${slug}/`)
    },

    async createCategory(data: Record<string, any>) {
      return useApiFetch('blog/categories/', {
        method: 'POST',
        body: data
      })
    },

    async updateCategory(slug: string, data: Record<string, any>) {
      return useApiFetch(`blog/categories/${slug}/`, {
        method: 'PUT',
        body: data
      })
    },

    async deleteCategory(slug: string) {
      return useApiFetch(`blog/categories/${slug}/`, {
        method: 'DELETE'
      })
    },

    async getCategoryPosts(slug: string, params: Record<string, any> = {}) {
      return useApiFetch<{ results: any[]; count: number }>(`blog/categories/${slug}/posts/`, {
        params
      })
    }
  }
}

