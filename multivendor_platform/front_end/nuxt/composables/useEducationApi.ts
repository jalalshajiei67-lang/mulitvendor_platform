export interface EducationPost {
  id: number
  title: string
  slug: string
  excerpt: string
  author: number
  author_name: string
  category: number
  category_name: string
  category_color: string
  status: string
  view_count: number
  comment_count: number
  reading_time: number
  created_at: string
  updated_at: string
  published_at: string | null
}

export interface EducationPostDetail extends EducationPost {
  content: string
  comments: any[]
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export const useEducationApi = () => {
  return {
    /**
     * Get seller education posts with pagination
     */
    async getSellerEducationPosts(page: number = 1, pageSize: number = 10) {
      return useApiFetch<PaginatedResponse<EducationPost>>('blog/posts/seller_education/', {
        params: {
          page,
          page_size: pageSize
        }
      })
    },

    /**
     * Get buyer education posts with pagination
     */
    async getBuyerEducationPosts(page: number = 1, pageSize: number = 10) {
      return useApiFetch<PaginatedResponse<EducationPost>>('blog/posts/buyer_education/', {
        params: {
          page,
          page_size: pageSize
        }
      })
    },

    /**
     * Get a single education post by slug
     */
    async getEducationPost(slug: string) {
      return useApiFetch<EducationPostDetail>(`blog/posts/${slug}/`)
    }
  }
}

