/**
 * Payment API Composable
 * Handles all payment-related API calls
 */

export interface PaymentRequest {
  billing_period: 'monthly' | 'quarterly' | 'semiannual' | 'yearly'
}

export interface PaymentResponse {
  success: boolean
  track_id?: string
  payment_url?: string
  amount?: number
  amount_toman?: number
  order_id?: string
  error?: string
}

export interface Payment {
  id: number
  user: number
  user_username: string
  billing_period: string
  billing_period_display: string
  amount: number
  amount_toman: number
  track_id: string
  order_id: string
  ref_number?: string
  card_number?: string
  status: string
  status_display: string
  payment_method: string
  created_at: string
  paid_at?: string
  verified_at?: string
  description?: string
}

export interface Invoice {
  id: number
  payment: Payment
  invoice_number: string
  issue_date: string
  due_date: string
  subtotal: number
  tax_amount: number
  total_amount: number
  invoice_pdf_url?: string
  notes?: string
  created_at: string
}

export interface PaymentHistoryResponse {
  count: number
  next?: string
  previous?: string
  results: Payment[]
}

export const usePaymentApi = () => {
  return {
    /**
     * Request premium payment
     */
    async requestPremiumPayment(
      billingPeriod: 'monthly' | 'quarterly' | 'semiannual' | 'yearly' = 'monthly'
    ): Promise<PaymentResponse> {
      try {
        const response = await useApiFetch<PaymentResponse>('payments/premium/request/', {
          method: 'POST',
          body: { billing_period: billingPeriod }
        })
        return response
      } catch (error: any) {
        console.error('Payment request error:', error)
        return {
          success: false,
          error: error?.data?.error || 'خطا در درخواست پرداخت'
        }
      }
    },

    /**
     * Verify payment manually
     */
    async verifyPayment(trackId: string) {
      try {
        return await useApiFetch(`payments/premium/verify/${trackId}/`, {
          method: 'POST'
        })
      } catch (error: any) {
        console.error('Payment verification error:', error)
        throw error
      }
    },

    /**
     * Get payment history
     */
    async getPaymentHistory(params?: {
      status?: string
      page?: number
      page_size?: number
    }): Promise<PaymentHistoryResponse> {
      try {
        return await useApiFetch<PaymentHistoryResponse>('payments/history/', {
          query: params
        })
      } catch (error: any) {
        console.error('Payment history error:', error)
        throw error
      }
    },

    /**
     * Download invoice PDF
     */
    downloadInvoice(invoiceId: number) {
      const config = useRuntimeConfig()
      const apiBase = config.public.apiBase
      const url = `${apiBase}/payments/invoice/${invoiceId}/download/`
      
      // Open in new tab
      window.open(url, '_blank')
    },

    /**
     * Get invoice download URL
     */
    getInvoiceDownloadUrl(invoiceId: number): string {
      const config = useRuntimeConfig()
      const apiBase = config.public.apiBase
      return `${apiBase}/payments/invoice/${invoiceId}/download/`
    }
  }
}

