/**
 * Comments API composable
 * Handles product and blog comments/reviews
 */

export interface Comment {
  id: number
  author: string
  author_username?: string
  content: string
  comment?: string
  rating?: number
  created_at: string
  updated_at: string
}

export const useCommentApi = () => {
  return {
    // Product Comments/Reviews
    async getProductComments(productId: string | number) {
      return useApiFetch<Comment[]>(`products/${productId}/comments/`)
    },

    async createProductComment(productId: string | number, data: {
      comment: string
      rating?: number
    }) {
      return useApiFetch(`products/${productId}/comment/`, {
        method: 'POST',
        body: data
      })
    },

    // Blog Comments
    async getBlogPostComments(postSlug: string) {
      return useApiFetch<Comment[]>(`blog/posts/${postSlug}/comments/`)
    },

    async createBlogComment(postSlug: string, data: {
      content: string
    }) {
      return useApiFetch(`blog/posts/${postSlug}/comment/`, {
        method: 'POST',
        body: data
      })
    }
  }
}











