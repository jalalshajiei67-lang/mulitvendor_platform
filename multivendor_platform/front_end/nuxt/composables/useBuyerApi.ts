import { useApiFetch } from './useApiFetch'

export interface BuyerDashboardData {
  total_orders: number
  pending_orders: number
  completed_orders: number
  total_reviews: number
}

export interface BuyerOrder {
  id: number
  order_number: string
  status: string
  total_amount: string
  is_paid: boolean
  created_at: string
}

export interface BuyerReview {
  id: number
  product?: { name: string }
  rating: number
  comment: string
  created_at: string
}

export const useBuyerApi = () => {
  const getBuyerDashboard = async (): Promise<BuyerDashboardData> => {
    return await useApiFetch<BuyerDashboardData>('auth/buyer/dashboard/')
  }

  const getBuyerOrders = async (): Promise<BuyerOrder[]> => {
    const response = await useApiFetch<{ results?: BuyerOrder[] } | BuyerOrder[]>(
      'auth/buyer/orders/'
    )
    return Array.isArray(response) ? response : response.results || []
  }

  const getBuyerReviews = async (): Promise<BuyerReview[]> => {
    const response = await useApiFetch<{ results?: BuyerReview[] } | BuyerReview[]>(
      'auth/buyer/reviews/'
    )
    return Array.isArray(response) ? response : response.results || []
  }

  return {
    getBuyerDashboard,
    getBuyerOrders,
    getBuyerReviews
  }
}

