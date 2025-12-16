import { useApiFetch } from './useApiFetch'

export interface SellerDashboardData {
  total_products: number
  active_products: number
  total_sales: string
  total_orders: number
  product_views: number
  total_reviews: number
  recent_orders?: SellerOrder[]
}

export interface SellerOrder {
  id: number
  order_number: string
  buyer_username?: string
  status: string
  total_amount: string
  created_at: string
}

export interface SellerReview {
  id: number
  product?: { name: string }
  author?: { username: string }
  rating: number
  comment: string
  created_at: string
}

export interface SellerAd {
  id: number
  title: string
  description: string
  contact_info: string
  is_active: boolean
  created_at: string
}

export const useSellerApi = () => {
  const getSellerDashboard = async (): Promise<SellerDashboardData> => {
    return await useApiFetch<SellerDashboardData>('auth/seller/dashboard/', {
      skip404Redirect: true
    })
  }

  const getSellerOrders = async (): Promise<SellerOrder[]> => {
    const response = await useApiFetch<{ results?: SellerOrder[] } | SellerOrder[]>(
      'auth/seller/orders/'
    )
    return Array.isArray(response) ? response : response.results || []
  }

  const getSellerReviews = async (): Promise<SellerReview[]> => {
    const response = await useApiFetch<{ results?: SellerReview[] } | SellerReview[]>(
      'auth/seller/reviews/'
    )
    return Array.isArray(response) ? response : response.results || []
  }

  const getSellerAds = async (): Promise<SellerAd[]> => {
    const response = await useApiFetch<{ results?: SellerAd[] } | SellerAd[]>(
      'auth/ads/'
    )
    return Array.isArray(response) ? response : response.results || []
  }

  const createSellerAd = async (data: Partial<SellerAd>): Promise<SellerAd> => {
    return await useApiFetch<SellerAd>('auth/ads/', {
      method: 'POST',
      body: data
    })
  }

  const updateSellerAd = async (id: number, data: Partial<SellerAd>): Promise<SellerAd> => {
    return await useApiFetch<SellerAd>(`auth/ads/${id}/`, {
      method: 'PUT',
      body: data
    })
  }

  const deleteSellerAd = async (id: number): Promise<void> => {
    await useApiFetch(`auth/ads/${id}/`, {
      method: 'DELETE'
    })
  }

  return {
    getSellerDashboard,
    getSellerOrders,
    getSellerReviews,
    getSellerAds,
    createSellerAd,
    updateSellerAd,
    deleteSellerAd
  }
}

