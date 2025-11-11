/**
 * Orders API composable
 * Handles order management for buyers and sellers
 */

export interface Order {
  id: number
  order_number: string
  buyer_username?: string
  seller_username?: string
  status: string
  total_amount: string | number
  is_paid: boolean
  payment_method?: string
  payment_date?: string
  created_at: string
  updated_at: string
  items?: OrderItem[]
}

export interface OrderItem {
  id: number
  product: any
  quantity: number
  price: string | number
  subtotal: string | number
}

export const useOrderApi = () => {
  return {
    // Create Order
    async createOrder(data: {
      items: Array<{ product_id: number; quantity: number }>
      shipping_address?: string
      notes?: string
    }) {
      return useApiFetch<Order>('orders/', {
        method: 'POST',
        body: data
      })
    },

    // Get Orders
    async getOrders(params: Record<string, any> = {}) {
      return useApiFetch<{ results: Order[]; count: number }>('orders/', {
        params
      })
    },

    async getOrder(id: number) {
      return useApiFetch<Order>(`orders/${id}/`)
    },

    // Update Order Status
    async updateOrderStatus(id: number, status: string) {
      return useApiFetch(`orders/${id}/status/`, {
        method: 'PATCH',
        body: { status }
      })
    },

    // Cancel Order
    async cancelOrder(id: number, reason?: string) {
      return useApiFetch(`orders/${id}/cancel/`, {
        method: 'POST',
        body: { reason }
      })
    },

    // Payment
    async initiatePayment(orderId: number, paymentMethod: string) {
      return useApiFetch(`orders/${orderId}/payment/`, {
        method: 'POST',
        body: { payment_method: paymentMethod }
      })
    },

    async verifyPayment(orderId: number, transactionId: string) {
      return useApiFetch(`orders/${orderId}/payment/verify/`, {
        method: 'POST',
        body: { transaction_id: transactionId }
      })
    }
  }
}

